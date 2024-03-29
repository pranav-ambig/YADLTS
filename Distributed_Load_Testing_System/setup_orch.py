#!/usr/bin/env python3

# IMPORTS
import json
import threading
import statistics
from time import sleep

# FUNCTIONALITY

# Socket specific function, sends metrics to frontend
def transmit_metrics(sio, data, metrics, metric_key, test_id):
    sio.emit(data["node_id"], {'key': metric_key, 'metrics': metrics[metric_key]})
    sio.emit('test_metrics', {'key': test_id, 'metrics': metrics[test_id]})


# Orchestrator specific funcitons
# Let's define a function to push the message according to the topics
def to_consumer(producer, topic, message):
 #   producer.flush()
    producer.send(topic, value=json.dumps(message).encode('utf-8'))

# Topics as producer --- trigger, test_config

def trigger_push(producer, metrics, test_id, drivers_heartbeat, heartbeats, drivers, drivers_metrics, sio, msg_count_per_driver, request_limit_event, max_req):

    heartbeat_thread = threading.Thread(target=driver_heartbeat, args=(producer, drivers_heartbeat, heartbeats, drivers))
    metrics_thread = threading.Thread(target=driver_metrics, args=(drivers_metrics, metrics, sio, test_id, msg_count_per_driver, producer, request_limit_event, max_req))

    heartbeat_thread.start()
    metrics_thread.start()

    sleep(2)
    trigger_msg = {
        "test_id": test_id,
        "trigger": "YES"
    }

    to_consumer(producer, "trigger", trigger_msg)

    print(f"\nPokemons Triggered!\n")

    heartbeat_thread.join()
    metrics_thread.join()
    try:
        print(f"FINAL METRICS of test ID ({test_id}):\n"
            f"Mean Latency --> {metrics[test_id]['Mean']} s\n"
            f"Median Latency --> {metrics[test_id]['Median']} s\n"
            f"Mode Latency --> {metrics[test_id]['Mode']} s\n"
            f"Minimum Latency --> {metrics[test_id]['Min']} s\n"
            f"Maximum Latency --> {metrics[test_id]['Max']} s\n"
            f"Number of requests sent --> {metrics[test_id]['Requests']}")
    except KeyError:
        print(f"Error: Test ID {test_id} not found in metrics dictionary.")
    return


def test_config_push(producer, test_type, test_message_delay, test_id, message_count_per_driver, num_drivers):
    config_msg = {
        "test_id": test_id,
        "test_type": test_type,
        "test_message_delay": test_message_delay,
        "message_count_per_driver": message_count_per_driver,
        "num_drivers": num_drivers
    }
    to_consumer(producer, "test_config", config_msg)


# Topics as consumer --- register, metrics, heartbeat
def driver_register(driver_reg_consumer, drivers):
    reg_msg = "DRIVER_NODE_REGISTER"
    for message in driver_reg_consumer:
        data = message.value
        if data["message_type"] == reg_msg and data["node_id"] not in drivers.keys():
            drivers[data["node_id"]] = data["node_IP"]
            print(f'{data["node_id"]} Registered')


def driver_metrics(drivers_metrics, metrics, sio, test_id, msg_count_per_driver, producer, request_limit_event, max_req):
    latencies = []
    min_latency = float('inf')
    max_latency = float('-inf')
    mean = 0
    count = 0


    metric_count = 0
    metric_trigger_threshold = 0.01 * msg_count_per_driver**2 + 1.5 * msg_count_per_driver + 20 # number of requests after which metrics is sent to frontend
    last_metric_tuple = None

    exit = False

    for message in drivers_metrics:
        data = message.value

        if 'kill' in data:
            if last_metric_tuple:
                transmit_metrics(sio, *last_metric_tuple)
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
            metric_count += 1
            last_metric_tuple = (data, metrics, metric_key, test_id)

            if metric_count >= metric_trigger_threshold:
                # Push the metrics through flask for live metrics data
                transmit_metrics(sio, data, metrics, metric_key, test_id)
                metric_count = 0
            else:
                metric_count += 1
                
            if count >= max_req and not exit:
                request_limit_event.set()
                request_limit(producer, test_id, request_limit_event)
                request_limit_event.clear()
                exit = True
        except json.JSONDecodeError:
            print('Decoder Error')

    # This function terminates when heartbeat terminates 💀. handled while calling on different threads.


def driver_heartbeat(producer, drivers_heartbeat, heartbeats, drivers):
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


def kill_driver_processes(producer, test_id):
    trigger_msg = {
        'test_id': test_id,
        'trigger': 'NO'
    }
    to_consumer(producer, "trigger", trigger_msg)


def timer_thread(producer, stop_timer_event, test_id):
    max_wait_time = 20
    elapsed_time = 0

    while elapsed_time < max_wait_time and not stop_timer_event.is_set():
        sleep(1)
        elapsed_time += 1

    if not stop_timer_event.is_set():
        print(f'elapsed time: {elapsed_time}s')
        kill_driver_processes(producer, test_id)


def request_limit(producer,test_id, request_limit_event):
    if request_limit_event.is_set():
        print("REQUEST LIMIT REACHED!!")
        kill_driver_processes(producer, test_id)