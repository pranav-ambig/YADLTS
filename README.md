[![MIT License][license-shield]][license-url]
[![Contributors][contributors-shield]][contributors-url]
# Distributed Load Testing System

## Overview

Welcome to the Distributed Load Testing System! This project aims to provide a scalable, high-throughput, and concurrent load testing solution for web servers WITH POKEMONS!. The system is designed to coordinate multiple driver nodes using Kafka as a communication service. It supports two types of load tests: Tsunami testing with configurable delays between requests and Avalanche testing with immediate request dispatch.

### Built With

[![Apache Kafka][Apache Kafka.js]][kafka-url]
[![React][React.js]][React-url]
[![JavaScript][Js.js]][Js-url]
[![Flask][Flask.js]][Flask-url]
[![Python][Python.js]][Python-url]
[![Ubuntu][Ubuntu.js]][Ubuntu-url]

## Table of Contents

- [Architecture](#architecture)
- [Installation](#Installation)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)

## Architecture

The system consists of an Orchestrator Node, Driver Nodes, a Kafka broker for communication, and a Target HTTP Server for testing. The communication between nodes is facilitated through Kafka topics. The Orchestrator Node exposes a REST API for test control, metrics reporting, and monitoring.

![Architecture Diagram](https://github.com/Cloud-Computing-Big-Data/RR-Team-11-Distributed-Load-Testing-System/blob/main/Architecture.png)

## Installation

> [!WARNING]
> This application involves high utilization of resources and is recommended to run on WSL (Windows Subsystem for Linux).

1. Clone the repository:

   ```bash
   git clone https://github.com/pranav-ambig/YADLTS.git
   ```
   
2. Navigate:

   ```bash
   cd distributed-load-testing
   ```
   
3. Install requirements:

   ```bash
   pip install -r requirements.txt
   ```
   
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
   ```
>[!NOTE]
>If you **donot** have Apache Kafka installed, follow [this](https://github.com/pranav-ambig/YADLTS/blob/main/Kafka/installation.md).

## Features
### Driver IDs:
**Charizard** &emsp;|  &emsp;**Blastoise**  &emsp;|  &emsp;**Venusaur**  &emsp;|  &emsp;**Pikachu**  &emsp;|  &emsp;**Snivy**  &emsp;|  &emsp;**Mewtwo**  &emsp;|  &emsp;**Tentacruel**  &emsp;|  &emsp;**Zapdos**


### Kafka Topics:
* register
```bash
{
  "node_id": '<POKEMON NAME>',
  "node_IP": '<NODE IP ADDRESS (with port) HERE>',
  "message_type": 'DRIVER_NODE_REGISTER',
}
```
* test_config
```bash
    {
        "test_id": '<RANDOMLY GENERATED UNQUE TEST ID>',
        "test_type": '<AVALANCHE|TSUNAMI>',
        "test_message_delay": '<0 | CUSTOM_DELAY (only applicable in place of Tsunami testing)>',
        "message_count_per_driver": '<A NUMBER>'
    }
```
* trigger
```bash
    {
        "test_id": '<RANDOMLY GENERATED UNQUE TEST ID>',
        "trigger": "YES"
    }
```
* metrics
```bash
    {
        "node_id": '<POKEMON NAME>',
        "test_id": '<RANDOMLY GENERATED UNQUE TEST ID>',
        "metrics": {
            "Mean": '<Mean of Latency>',
            "Median": '<Median of Latency>',
            "Mode": '<Mode of Latency>',
            "Min": '<Minimum Latency>',
            "Max": '<Maximum Latency>',
            "latency": '<Latency>',
            "Requests": '<Number of requests sent>'
        }
    }
```
* heartbeat
```bash
  {
        "node_id": '<POKEMON NAME>',
        "heartbeat": "<YES/NO>"
  }
```

## Contributing
We welcome contributions! Feel free to open issues for bug reports or feature requests. Pull requests are encouraged
***If you find this repository useful, kindly consider giving it a star ⭐️***

## License
This project is licensed under the [MIT License](https://github.com/pranav-ambig/YADLTS/blob/main/MIT-LICENSE.txt)


<!-- MARKDOWN LINKS & IMAGES -->

[contributors-shield]: https://img.shields.io/github/contributors/pranav-ambig/YADLTS.svg?style=for-the-badge
[contributors-url]: https://github.com/pranav-ambig/YADLTS/graphs/contributors
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/pranav-ambig/YADLTS/blob/main/MIT-LICENSE.txt

[Apache Kafka.js]: https://img.shields.io/badge/Apache%20Kafka-000?style=for-the-badge&logo=apachekafka
[kafka-url]: https://kafka.apache.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Js.js]: https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black
[Js-url]: https://www.javascript.com/
[Flask.js]: https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white
[Flask-url]: https://flask.palletsprojects.com/en/3.0.x/
[Python.js]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org
[Ubuntu.js]: https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white
[Ubuntu-url]: https://ubuntu.com/


