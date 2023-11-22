#!/usr/bin/env python3

import requests
from multiprocessing import Process
from random import choice
from driver import Driver

# 'http://localhost:5052'


def setup_drivers(num_drivers, server_url, bootstrap_servers):

    available_node_ids = {'Charizard', 'Blastoise', 'Venusaur', 'Pikachu', 'Snivy', 'Mewtwo', 'Tentacruel', 'Zapdos'}

    driver_procs = []

    for _ in range(num_drivers):
        # generate a new node_id
        node_id = choice(list(available_node_ids))
        available_node_ids.remove(node_id)

        # driver_inst = Driver(node_id, bootstrap_servers, server_url)

        driver_proc = Process(target=Driver, args=[node_id, 100, bootstrap_servers, server_url])
        driver_procs.append(driver_proc)
        driver_proc.start()

    return driver_procs
