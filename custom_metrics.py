#!/usr/bin/env python
"""
Copyright (c) 2020 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
               https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""
import requests
from netmiko import ConnectHandler
from pprint import pprint
import json
import time
import yaml
from yaml.loader import SafeLoader

# get credentials of the switch and AppDynamics
with open('credentials.yml') as f:
    creds = yaml.load(f, Loader=SafeLoader)

switch_ip = creds['switchIp']
switch_user = creds['switchUser']
switch_password = creds['switchPassword']

appd_events_ip = creds['appDIp']

# set the headers for the API call - it includes the global account name and API key
headers = {
    'X-Events-API-AccountName': creds['eventsAccountName'],
    'X-Events-API-Key': creds['eventsAPIKey'],
    'Accept': 'application/vnd.appd.events+json;v=2'
}

events_publish_endpoint = "/events/publish/" + creds['schemaName']

# retrieve the hardware statistics from the Catalyst switch and then send the data to AppDynamics - this loop will repeat indefinitely
try:
    while True:
        #make SSH connection to switch
        with ConnectHandler(ip=switch_ip,
            port=22,
            username=switch_user,
            password=switch_password,
            device_type="cisco_xe") as ch:

            # retrieve the hardware statistics
            output = ch.send_command("show interfaces transceiver")

            # parse the output from the hardware statistics
            output_lines = output.strip().splitlines()
            for line in output_lines:
                if "---" in line:
                    start_index = output_lines.index(line) + 1
                    break

            output_data = output_lines[start_index:]
            interface_stats = []

            # format the data in the schema that was provided to AppDynamics
            for data in output_data:
                data_list = data.split()
                stat = {
                    "port": data_list[0],
                    "temperature": float(data_list[1]),
                    "voltage": float(data_list[2]),
                    "current": float(data_list[3]),
                    "optical_tx_power": float(data_list[4]),
                    "optical_rx_power": float(data_list[5])
                }
                interface_stats.append(stat)

        pprint(interface_stats)

        # make API call to add data to AppDynamics
        publish_response = requests.post(appd_events_ip+events_publish_endpoint, headers=headers, data=json.dumps(interface_stats))

        pprint(publish_response.status_code)

        #pause for 5 seconds
        time.sleep(5)

except KeyboardInterrupt:
    print("Interrupted!")
