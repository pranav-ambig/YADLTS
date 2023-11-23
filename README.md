# Distributed Load Testing System

## Overview

Welcome to the Distributed Load Testing System! This project aims to provide a scalable, high-throughput, and concurrent load testing solution for web servers WITH POKEMONS!. The system is designed to coordinate multiple driver nodes using Kafka as a communication service. It supports two types of load tests: Tsunami testing with configurable delays between requests and Avalanche testing with immediate request dispatch.

## Table of Contents

- [Architecture](#architecture)
- [Getting Started](#getting-started)
- [Installation](#Installation)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)

## Architecture

The system consists of an Orchestrator Node, Driver Nodes, a Kafka broker for communication, and a Target HTTP Server for testing. The communication between nodes is facilitated through Kafka topics. The Orchestrator Node exposes a REST API for test control, metrics reporting, and monitoring.

![Architecture Diagram](https://github.com/Cloud-Computing-Big-Data/RR-Team-11-Distributed-Load-Testing-System/blob/main/Architecture.png)

## Getting Started

### Built With

* [![Kafka][Kafka]][[Kafka](https://kafka.apache.org/)]
* [![React][React.js]][[React-url](https://react.dev/)]

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/pranav-ambig/YADLTS.git

2. Navigatew:

   ```bash
   cd distributed-load-testing


3. Install requirements:

   ```bash
   pip install -r requirements.txt

4. RUN:

   ```bash
   cd Frontend
   npm install
   npm run dev
   ```
   ```bash
   cd Distributed_Load_Testing_System
   sudo systemctl start kafka
   python3 orchestrator.py localhost:9092
   
## Features
### Driver IDs:
* Charizard
* Blastoise
* Venusaur
* Pikachu
* Snivy
* Mewtwo
* Tentacruel
* Zapdos

### Kafka Topics:
* register
```bash
{
  "node_id": "<POKEMON NAME>",
  "node_IP": "<NODE IP ADDRESS (with port) HERE>",
  "message_type": "DRIVER_NODE_REGISTER",
}
```
* test_config
```bash
    {
        "test_id": test_id,
        "test_type": test_type,
        "test_message_delay": test_message_delay,
        "message_count_per_driver": message_count_per_driver
    }
```
* trigger
```bash
    {
        "test_id": test_id,
        "trigger": "YES"
    }
```
* metrics
```bash
    {
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
```
* heartbeat
```bash
  {
        "node_id": self.node_id,
        "heartbeat": yesno
  }
```

## Contributing
We welcome contributions! Feel free to open issues for bug reports or feature requests. Pull requests are encouraged

## License
This project is licensed under the MIT License - see the LICENSE file for details.

