[![MIT License][license-shield]][license-url]
[![Contributors][contributors-shield]][contributors-url]
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

* [![React][React.js]][React-url]
* [![Apache Kafka][Apache Kafka.js]][kafka-url]

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
1. <span style="color: #FF0000;">**Charizard**</span> | 2. <span style="color: #0000FF;">**Blastoise**</span> | 3. <span style="color: #00FF00;">**Venusaur**</span> | 4. <span style="color: #FFD700;">**Pikachu**</span> | 5. <span style="color: #008000;">**Snivy**</span> | 6. <span style="color: #800080;">**Mewtwo**</span> | 7. <span style="color: #4682B4;">**Tentacruel**</span> | 8. <span style="color: #FFA500;">**Zapdos**</span>

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


<!-- MARKDOWN LINKS & IMAGES -->

[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/pranav-ambig/YADLTS/graphs/contributors
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/pranav-ambig/YADLTS

[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/

[Apache Kafka.js]: https://img.shields.io/badge/Apache%20Kafka-000?style=for-the-badge&logo=apachekafka
[kafka-url]: https://kafka.apache.org/
