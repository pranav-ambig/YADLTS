#!/usr/bin/env python3

# IMPORTS
from flask import Flask, request, jsonify
from flask_cors import CORS
from kafka import KafkaProducer, KafkaConsumer
from flask_socketio import SocketIO
import json
import uuid
import threading
import statistics
from setup_drivers import setup_drivers
from time import sleep
import sys

bootstrapServers = sys.argv[1]  # taking bootstrap server url from command line

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

#log
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# FLASK
# SOCKETIO
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "supports_credentials": True}})
sio = SocketIO(app, cors_allowed_origins="*")

# FUNCTIONALITY

# Let's define a function to push the message according to the topics
def to_consumer(producer, topic, message):
    producer.flush()
    producer.send(topic, value=json.dumps(message).encode('utf-8'))


# Topics as producer --- trigger, test_config


def trigger_push(test_id):

    heartbeat_thread = threading.Thread(target=driver_heartbeat)
    metrics_thread = threading.Thread(target=driver_metrics, args=(test_id,))

    heartbeat_thread.start()
    metrics_thread.start()

    # while (not metrics_thread.is_alive()) and (not heartbeat_thread.is_alive()):
    #     pass

    sleep(2)
    trigger_msg = {
        "test_id": test_id,
        "trigger": "YES"
    }

    to_consumer(producer, "trigger", trigger_msg)

    print(f"\nPokemons Triggered!\n")

    heartbeat_thread.join()
    metrics_thread.join()

    

    print(f"FINAL METRICS of test ID ({test_id}):\n"
          f"Mean Latency --> {metrics[test_id]['Mean']} s\n"
          f"Median Latency --> {metrics[test_id]['Median']} s\n"
          f"Mode Latency --> {metrics[test_id]['Mode']} s\n"
          f"Minimum Latency --> {metrics[test_id]['Min']} s\n"
          f"Maximum Latency --> {metrics[test_id]['Max']} s\n"
          f"Number of requests sent --> {metrics[test_id]['Requests']}")

    return


def test_config_push(test_type, test_message_delay, test_id, message_count_per_driver):
    config_msg = {
        "test_id": test_id,
        "test_type": test_type,
        "test_message_delay": test_message_delay,
        "message_count_per_driver": message_count_per_driver
    }
    to_consumer(producer, "test_config", config_msg)


# Topics as consumer --- register, metrics, heartbeat
def driver_register():
    reg_msg = "DRIVER_NODE_REGISTER"
    for message in driver_reg_consumer:
        data = message.value
        if data["message_type"] == reg_msg and data["node_id"] not in drivers.keys():
            drivers[data["node_id"]] = data["node_IP"]
            print(f'{data["node_id"]} Registered')


def driver_metrics(test_id):
    latencies = []
    min_latency = float('inf')
    max_latency = float('-inf')
    mean = 0
    count = 0

    for message in drivers_metrics:
        data = message.value

        if 'kill' in data:
            print("Metrics thread was cancelled.")
            return
        try:
            metric_key = str(data["node_id"] + test_id)
            value = data["metrics"]
            metrics[metric_key] = value

            metric = {}

            latency = value["latency"]
            latencies.append(latency)
            min_latency = min(min_latency, latency)
            max_latency = max(max_latency, latency)

            count += 1
            mean = mean + (latency - mean) / count

            median = statistics.median(latencies)
            mode = statistics.mode(latencies)

            metric['Mean'] = mean
            metric['Median'] = median
            metric['Min'] = min_latency
            metric['Max'] = max_latency
            metric['Mode'] = mode
            metric['Requests'] = count  # number of requests sent

            metrics[test_id] = metric
            # Push the metrics through flask for live metrics data
            sio.emit(data["node_id"], {'key': metric_key, 'metrics': metrics[metric_key]})
            sio.emit('test_metrics', {'key': test_id, 'metrics': metrics[test_id]})

        except json.JSONDecodeError:
            print('Decoder Error')

    # This function terminates when heartbeat terminates 💀. handled while calling on different threads.


def driver_heartbeat():
    for message in drivers_heartbeat:
        data = message.value
        heartbeats[data["node_id"]] = data["heartbeat"]
        knockout_check = all(value == "NO" for value in heartbeats.values())
        if knockout_check:
            print("All Pokemons are knocked out!")

            to_consumer(producer, 'metrics', {'kill': 0})
            drivers.clear()
            heartbeats.clear()
            return


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

    driver_procs = setup_drivers(num_drivers, server_url, bootstrap_servers=bootstrapServers)

    while len(driver_procs) > len(drivers):  # make sure thy are synced up
        sleep(1)

    if test_type in ["AVALANCHE", "TSUNAMI"] and test_message_delay >= 0:  # as per project requirement

        test_id = str(uuid.uuid4())  # Generate a unique test_id
        tests.append(test_id)
        test_config_push(test_type, test_message_delay, test_id, message_count_per_driver)

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

        trigger_thread = threading.Thread(target=trigger_push, args=(test_id,))
        trigger_thread.start()
        # print('starting')

        while len(drivers) > 0:  # make sure the test is ended
            pass

        for driver_processes in driver_procs:
            driver_processes.terminate()  # killing all the drivers after test end

        return jsonify({"status": "success", "message": f"Test finished successfully!: {test_id}"})
    else:
        return jsonify({"status": "error", "message": "Invalid request parameters"}), 200


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
    register_thread = threading.Thread(target=driver_register)
    register_thread.start()
    # Running the driver register function indefinitely to service all the registers with an isolated thread

    # Start Flask-SocketIO app
    sio.run(app, debug=True, port=5000)
