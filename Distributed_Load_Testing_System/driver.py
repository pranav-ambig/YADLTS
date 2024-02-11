import requests
from threading import Thread
from kafka import KafkaConsumer, KafkaProducer
import json
from time import sleep, perf_counter
import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Event

class Driver():

    def __init__(self, node_id: str, throughput: int, bootstrap_servers: str, server_url: str):
        self.node_id = node_id
        self.throughput = throughput
        self.driver_threads = []
        self.current_test_config = {}
        self.bootstrap_servers = bootstrap_servers
        self.server_url = server_url + '/ping'
        self.info(self.server_url)
        self.test_active = Event()
        self.test_active.clear()
        self.producer = KafkaProducer(bootstrap_servers=bootstrap_servers)
        self.consumer_test_config = KafkaConsumer(
            'test_config',
            bootstrap_servers=self.bootstrap_servers,
            auto_offset_reset='latest'
        )
        self.consumer_trigger = KafkaConsumer(
            'trigger',
            bootstrap_servers=self.bootstrap_servers,
            auto_offset_reset='latest',
        )
        self.start() # Start driver immediately after instantiating

    def start(self):
        print(f'Starting Driver {self.node_id}')
        self.info('Attempting to start consumers')
        self.create_consumer_threads()
        self.start_consumers()
        sleep(1) # hard delay of 1s to wait for consumer threads to start, change later
        self.register()
        self.join_consumers()

    def info(self, message):
        print(f'{self.node_id}: {message}')

    def test_config(self):
        self.info('Starting test_config thread')
        for message in self.consumer_test_config:
            message = message.value.decode('utf-8')
            # if message == 'kill': return
            try:
                self.current_test_config = json.loads(message)
                self.test_active.set()
                self.info('recieved test config')
            except json.JSONDecodeError:
                print("Decode error")
                return

    def trigger(self):
        self.info('Starting trigger thread')
        bombardThread = None
        for message in self.consumer_trigger:
            message = message.value.decode('utf-8')
            try:
                data = json.loads(message)
            except json.JSONDecodeError:
                print("Decode error")
            if self.current_test_config == {}:
                self.info('Trigger with blank config')
                # return
            if data["trigger"] == "YES":
                # start bombarding
                self.test_active.set()
                bombardThread = Thread(target=self.bombard)
                bombardThread.start()
            elif data["trigger"] == "NO":
                self.stop_test()
                self.send_heartbeat("NO")
                print('heartbeat NO sent')
                #self.server_url = 'https://www.google.com/error'
                break
        if bombardThread:
            bombardThread.join()
    
    def bombard(self):
        
        delay = int(self.current_test_config["test_message_delay"])
        self.info(f'Starting bombardment  Type: {self.current_test_config["test_type"]}  Delay: {delay}')
        latency_values = []

        req_sent = 0

        min_latency = float('inf')
        max_latency = -1
        sum_latency = 0

        def send_req():
            nonlocal req_sent, min_latency, max_latency, sum_latency
            try:
                start_time = perf_counter()
                response = requests.get(self.server_url)
                end_time = perf_counter()
                req_sent += 1
                self.send_heartbeat("YES")
                # Calculate latency and store in the list
                latency = end_time - start_time
                latency *= 1000
                min_latency = min(min_latency, latency)
                max_latency = max(max_latency, latency)
                sum_latency += latency
                latency_values.append(latency)
                metrics_data = {
                    "node_id": self.node_id,
                    "test_id": self.current_test_config["test_id"],
                    "metrics": {
                        "Mean": sum_latency/req_sent,
                        "Median": statistics.median(latency_values),
                        "Mode": statistics.mode(latency_values),
                        "Min": min_latency,
                        "Max": max_latency,
                        "latency": latency,
                        "Requests": req_sent
                    }
                }
                self.producer.send("metrics", value=json.dumps(metrics_data).encode("utf-8"))

            except requests.exceptions.ConnectionError:
                self.stop_test(self)
                return
        
        if self.current_test_config["test_type"] == "TSUNAMI":
            while self.test_active.is_set():
                send_req()
                sleep(self.current_test_config["test_message_delay"])

            self.info("Server crashed")
            self.send_heartbeat("NO")
            return
        else:
            with ThreadPoolExecutor(max_workers=int(self.current_test_config["message_count_per_driver"])) as executor:
                while True:
                    for _ in range(int(self.current_test_config["message_count_per_driver"])):
                        executor.submit(send_req)
                    sleep(1)
                    if not self.test_active.is_set(): 
                        self.info("Server crashed")
                        self.send_heartbeat("NO")
                        return


    def send_heartbeat(self, yesno):
        heartbeat = {"node_id": self.node_id,
                     "heartbeat": yesno
                     }
        self.producer.send('heartbeat', json.dumps(heartbeat).encode("utf-8"))

    def create_consumer_threads(self):
        test_config_thread = Thread(target=self.test_config)
        trigger_thread = Thread(target=self.trigger)
        self.driver_threads.append(test_config_thread)
        self.driver_threads.append(trigger_thread)

    def start_consumers(self):
        for thread in self.driver_threads:
            thread.start()

    def join_consumers(self):
        for thread in self.driver_threads:
            thread.join()

    def register(self):
        register_dict = {
            "node_id": self.node_id,
            "node_IP": "0.0.0.0",
            "message_type": "DRIVER_NODE_REGISTER",
            }
        self.producer.send('register', json.dumps(register_dict).encode())

        self.info('Register message sent')
    
    def stop_test(self):
        self.test_active.clear()
    
