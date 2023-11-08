#!/usr/bin/env python3
import sys
from kafka import KafkaProducer, KafkaConsumer
import json
import uuid
import flask
import threading
import concurrent.futures


# PRODUCER SETTINGS
producer = KafkaProducer(bootstrap_servers='localhost:9092')


# CONSUMER SETTINGS
consumer_settings = {
    'bootstrap_servers': 'localhost:9092',  # Address of the Kafka broker(s)
    #'group_id': 'popularity',  # Specify a unique group ID for the consumer
    'auto_offset_reset': 'latest',  # Start consuming from the earliest available offset
    #'enable_auto_commit': True,  # Automatically commit offsets
    #'key_deserializer': None,  # Deserializer for message keys
    'value_deserializer': lambda x: json.loads(x.decode('utf-8'))  # JSON deserializer for message values
}

# CONSUMERS
driver_reg_consumer = KafkaConsumer("register", **consumer_settings)
driver_metrics = KafkaConsumer("metrics", **consumer_settings)
driver_heartbeat = KafkaConsumer("heartbeat", **consumer_settings)


# STORAGE
drivers = {}
heartbeats = {}
metrics = {}

# FUNCTIONALITY 

# lets define a function to push the message according to the topics
def to_consumer(producer, topic, message):

    producer.flush()
    producer.send(topic, value=json.dumps(message).encode('utf-8'))
   
   
     
# topics as producer --- trigger, test_config
def trigger_push():

	trigger_msg = { 
		"test_id": str(uuid.uuid4()),
		"trigger": "YES"
		}
	
	to_consumer(producer, "trigger", trigger_msg)
	
	with concurrent.futures.ThreadPoolExecutor() as executor:
		heartbeat_thread = executor.submit(driver_heartbeat)
		metrics_thread = executor.submit(driver_metrics)
		# Wait for heartbeat_thread to complete
		concurrent.futures.wait([heartbeat_thread])
		# Cancel metrics_thread when heartbeat_thread ends
		metrics_thread.cancel()
	
	# aggregating the metrics and storing it with key as test_id
	for node_id in drivers.keys():
		key = node_id+trigger_msg["test_id"]
		metric = {
			#TODO
		}
		
			
def test_config_push(test_type, test_message_delay):
	
	config_msg = {
	"test_id": str(uuid.uuid4()),
	"test_type": test_type,
	"test_message_delay": test_message_delay,
	}
	
	to_consumer(producer, "test_config", config_msg)

# topics as consumer --- register, metrics, heartbeat
def driver_register():

	reg_msg = "DRIVER_NODE_REGISTER"
	for message in driver_reg_consumer:
    		data = message.value
    		if data["message_type"] == reg_msg and data["node_id"] not in drivers.keys():
    			drivers[data["node_id"]] = data["node_IP"]
    			 		 
def driver_metrics():

	# the metrics dict will contain 'node_idtest_id' as keys and the aggregated final metrics of the test will be stored in the key 'test_id'
	
	for message in driver_metrics:
		data = message.value
		key = data["node_id"]+data["test_id"]
		value = data["metrics"]
		metrics[key] = value

def driver_heartbeat():
	
	for message in driver_heartbeat:
		data = message.value
		heartbeats[data["node_id"]] = data["heartbeat"]
		knockout_check = all(value == "NO" for value in heartbeats.values())
		if knockout_check:
			break	
		
		
# FUNCTION CALLS

register_thread = threading.Thread(target = driver_register)
register_thread.start() # running the driver register function indefinitely to service all the registers with an isolated thread

test_config_push("AVALANCHE", 10)
trigger_push()
