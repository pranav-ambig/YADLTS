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
import site_inspector

# Set logging level
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

load_dotenv() 

BOOTSTRAP_SERVER = os.environ['BOOTSTRAP_SERVER']  # taking bootstrap server url from .env
MAX_REQUESTS = os.environ['MAX_REQUESTS']
MAX_REQUESTS = int(MAX_REQUESTS)

# PRODUCER SETTINGS
producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVER)

# CONSUMER SETTINGS
consumer_settings = {
    'bootstrap_servers': BOOTSTRAP_SERVER,  # Address of the Kafka broker(s)
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
timer_thread_instance = None # Global variable to track the timer thread
stop_timer_event = threading.Event() # Event to signal the timer thread to stop
request_limit_event = threading.Event() # Send kill message when req limit reached
#test_active= threading.Event()


# FLASK
# SOCKETIO
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "supports_credentials": True}}) # replace * with frontend url
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
    num_drivers = data.get('num_drivers')
    server_url = data.get('server_url')

    if True or site_inspector.inspect(server_url): #check for robots.txt
        msg_count_per_driver = message_count_per_driver # for metrics calcualtions

        driver_procs = setup_drivers(num_drivers, server_url, bootstrap_servers=BOOTSTRAP_SERVER)

        while len(driver_procs) > len(drivers):  # make sure thy are synced up
            sleep(1)

        if test_type in ["AVALANCHE", "TSUNAMI"] and test_message_delay >= 0:  # as per project requirement

            test_id = str(uuid.uuid4())  # Generate a unique test_id
            tests.append(test_id)
            setup_orch.test_config_push(producer, test_type, test_message_delay, test_id, message_count_per_driver, num_drivers)

            response_data = {
                "status": "success",
                "message": "Test configuration pushed successfully",
                "test_id": test_id  # send back the generated test id
            }
            return jsonify(response_data)

        else:

            return jsonify({"status": "error", "message": "Invalid request parameters"}), 400
    
    else:
        return jsonify({"status": "error", "message": "This URL doesnot allow testing!"}), 400


@app.route('/timeout', methods=['post'])
def user_timeout():
    return jsonify({"status": "termination", "message": "Inavctivity detected!"})
    data = request.get_json()
    test_id = data.get('test_id')
    active = data.get('active')

    global timer_thread_instance

    if active == "NO" and test_active.is_set:

        if not timer_thread_instance or not timer_thread_instance.is_alive():
            timer_thread_instance = threading.Thread(target=setup_orch.timer_thread, args=(producer, stop_timer_event, test_id))
            timer_thread_instance.start()
            print("Timer started.")
        
    elif active == "YES":

        if timer_thread_instance and timer_thread_instance.is_alive():
            stop_timer_event.set()
            timer_thread_instance.join()
            stop_timer_event.clear()
            print("Timer stopped.")

    return jsonify({"status": "termination", "message": "Inavctivity detected!"})


@app.route('/trigger', methods=['POST'])
def trigger_endpoint():
    # request json should contain --> {"test_id"}
    data = request.get_json()
    test_id = data.get('test_id')

    if test_id:
        trigger_thread = threading.Thread(target=setup_orch.trigger_push, args=(producer, metrics, test_id, drivers_heartbeat, heartbeats, drivers, drivers_metrics, sio, msg_count_per_driver, request_limit_event, MAX_REQUESTS))
        trigger_thread.start()
#        test_active.set()

        while len(drivers) > 0:  # make sure the test is ended
            pass

        for driver_processes in driver_procs:
            driver_processes.terminate()  # killing all the drivers after test end
#        test_active.clear()
        return jsonify({"status": "success", "message": f"Test finished successfully!: {test_id}"})
    else:
        return jsonify({"status": "error", "message": "Invalid request parameters"}), 400


@app.route('/history', methods=['GET'])
def history_endpoint():
    # send metrics history to frontend
    history = {}
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

