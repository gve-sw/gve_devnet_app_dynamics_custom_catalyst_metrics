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
import json
import yaml
from yaml.loader import SafeLoader

# get credentials of AppDynamics
with open('credentials.yml') as f:
    creds = yaml.load(f, Loader=SafeLoader)

appd_events_ip = creds['appDIp']

# set the headers for the API call - it includes the global account name and API key
headers = {
    'X-Events-API-AccountName': creds['eventsAccountName'],
    'X-Events-API-Key': creds['eventsAPIKey'],
    'Accept': 'application/vnd.appd.events+json;v=2'
}

# define the schema the data will be formatted to send to AppDynamics
hw_stats_schema = {
    "schema":
    {
        "current": "float",
        "optical_rx_power": "float",
        "optical_tx_power": "float",
        "port": "string",
        "temperature": "float",
        "voltage": "float"
    }
}

events_schema_endpoint = "/events/schema/" + creds['schemaName']

# make API call to create schema in AppDynamics
response = requests.post(appd_events_ip+events_schema_endpoint, headers=headers, data=json.dumps(hw_stats_schema))
print(response.status_code)
