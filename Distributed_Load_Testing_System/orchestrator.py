#!/usr/bin/env python3

# IMPORTS
import setup_orch
from flask import Flask, request, jsonify
from flask_cors import CORS
from kafka import KafkaProducer, KafkaConsumer
from flask_socketio import SocketIO
import json
import uuid
import threading
from setup_drivers import setup_drivers
from time import sleep
import sys
import logging
import os
from dotenv import load_dotenv

# Set logging level
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

load_dotenv() 

bootstrapServers = os.environ['BOOTSTRAP_SERVER']  # taking bootstrap server url from .env

# PRODUCER SETTINGS
producer = KafkaProducer(bootstrap_servers=bootstrapServers)

# CONSUMER SETTINGS
consumer_settings = {
    'bootstrap_servers': bootstrapServers,  # Address of the Kafka broker(s)
    'auto_offset_reset': 'latest',  # Start consuming from the earliest available offset
    'value_deserializer': lambda x: json.loads(x.decode('utf-8'))  # JSON deserializer for message values
}

# CONSUMERS
driver_reg_consumer = KafkaConsumer("register", **consumer_settings)
drivers_metrics = KafkaConsumer("metrics", **consumer_settings, )
drivers_heartbeat = KafkaConsumer("heartbeat", **consumer_settings)

# STORAGE
drivers = {}  # contains driver ids: 'ip address'
heartbeats = {}  # contains driver ids: 'YES/NO'
metrics = {}  # contains driver ids+test id : {metrics}
tests = []  # list containing all the test ids of tests conducted
driver_procs = []  # processes that are running the drivers
msg_count_per_driver = 0

# FLASK
# SOCKETIO
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "supports_credentials": True}})
sio = SocketIO(app, cors_allowed_origins="*")

# REST API Endpoints
@app.route('/driver_ids', methods=['GET'])
def driver_ids_endpoint():
    return jsonify({"driver_ids": list(drivers.keys())})  # send the registered driver ids to the frontend for configs


@app.route('/test_config', methods=['POST'])
def test_config_endpoint():
    # request json should contain --> {"test_type", "test_message_delay", }
    global driver_procs

    data = request.get_json()
    test_type = data.get('test_type')
    test_message_delay = data.get('test_message_delay')
    message_count_per_driver = data.get('message_count_per_driver')
    num_drivers = data.get('num_drivers')  # uncomment this while launching
    server_url = data.get('server_url')  # uncomment this while launching

    # num_drivers = 5                             # remove this after testing
    # server_url = 'http://localhost:5052'        # remove this after testing
    msg_count_per_driver = message_count_per_driver # for metrics calcualtions

    driver_procs = setup_drivers(num_drivers, server_url, bootstrap_servers=bootstrapServers)

    while len(driver_procs) > len(drivers):  # make sure thy are synced up
        sleep(1)

    if test_type in ["AVALANCHE", "TSUNAMI"] and test_message_delay >= 0:  # as per project requirement

        test_id = str(uuid.uuid4())  # Generate a unique test_id
        tests.append(test_id)
        setup_orch.test_config_push(producer, test_type, test_message_delay, test_id, message_count_per_driver)

        response_data = {
            "status": "success",
            "message": "Test configuration pushed successfully",
            "test_id": test_id  # send back the generated test id
        }
        return jsonify(response_data)

    else:

        return jsonify({"status": "error", "message": "Invalid request parameters"}), 400


@app.route('/trigger', methods=['POST'])
def trigger_endpoint():
    # request json should contain --> {"test_id"}
    data = request.get_json()
    test_id = data.get('test_id')

    if test_id:

        trigger_thread = threading.Thread(target=setup_orch.trigger_push, args=(producer, metrics, test_id, drivers_heartbeat, heartbeats, drivers, drivers_metrics, sio, msg_count_per_driver))
        trigger_thread.start()
        # print('starting')

        while len(drivers) > 0:  # make sure the test is ended
            pass

        for driver_processes in driver_procs:
            driver_processes.terminate()  # killing all the drivers after test end

        return jsonify({"status": "success", "message": f"Test finished successfully!: {test_id}"})
    else:
        return jsonify({"status": "error", "message": "Invalid request parameters"}), 400


@app.route('/history', methods=['GET'])
def history_endpoint():
    # send metrics history to frontend
    history = {}
    # print(metrics)
    # return jsonify({"history": {}})
    """
        history structure -->  
        { test_id:
            { 'mean': float, 
              'median': float, 
               ... , 
              'pokemon':
               { 'mean': float, 
                 'median': float,
                 ...
               }
            }
        }
    """
    for test_id in tests:
        history[test_id] = {}
        for metric_key in metrics.keys():
            if test_id == metric_key:
                history[test_id] = metrics[test_id]

            elif test_id != metric_key and test_id in metric_key:
                history_key = metric_key.replace(test_id, "")
                history[test_id][history_key] = metrics[metric_key]

    return jsonify({"history": history})


# SocketIO Event for Live Metrics
@sio.on('connect', namespace='/metrics')
def handle_connect():
    print('Client connected to metrics namespace')


@sio.on('disconnect', namespace='/metrics')
def handle_disconnect():
    print('Client disconnected from metrics namespace')


# LET THE FIGHT BEGIN!

if __name__ == "__main__":
    register_thread = threading.Thread(target=setup_orch.driver_register, args=(driver_reg_consumer, drivers,))
    register_thread.start()
    # Running the driver register function indefinitely to service all the registers with an isolated thread

    # Start Flask-SocketIO app
    sio.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True) #http://127.0.0.1:5000
    # make this port dynamic to accomodate multiple users and implement load balancer

