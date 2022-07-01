# AppDynamics Custom Catalyst Metrics
This prototype provides a method for integrating Catalyst switch hardware statistics with AppDynamics.

## Contacts
* Danielle Stacy

## Solution Components
* AppDynamics
* Catalyst switch

## Prerequisites

#### AppDynamics Events API
In order to use the AppDynamics Analytics Events API, you must create an API key. API keys are used only for Analytics Events REST APIs. 

> For detailed information on AppDynamics Analytics Events APIs, you may find them in the [AppDynamics Analytics Events API Documentation](https://docs.appdynamics.com/appd/21.x/21.7/en/extend-appdynamics/appdynamics-apis/analytics-events-api)

Unlike most AppDynamics REST APIs, you access the Events Analytics API by addressing the Events Service instance in the AppDynamics platform.

The URL for a SaaS instance of the Events Service will be one of the following:
|Region|URL|
|---|---|
|North America|https://analytics.api.appdynamics.com|
|Europe|https://fra-ana-api.saas.appdynamics.com|
|APAC|https://syd-ana-api.saas.appdynamics.com|

For an on-premises Events Service, address the Events Service instance host (or more likely, the virtual IP presented by a load balancer for the Events Service cluster). Use the primary default listening port for the Events Service, 9080. Make note of the URL of your Events Service instance because it will be used in the Installation/Configuration section.

Calls to the Analytics Events API need to specify the global account name for the Controller account being addressed. You may retrieve the global account name following these steps:
1. Click the settings icon in the right-hand corner of the AppDynamics dashboard (it is represented by a gear icon)
2. Select `License`.
3. Click on the `Account` tab.
4. The account name appears next to the **Name** label. Make note of this account name because it will be used in the Installation/Configuration section.

Lastly, API calls to the Analytics Events API need to be authenticated with an API key. To create an API key, follow these steps:
1. Navigate to `Analytics > Configuration > API Keys`
2. Click `+Add` to view the configuration panel
3. Add a **Name** and **Description**
4. Expand each permission section to select the permissions for this key. The only permissions that should be needed are located under the Custom Analytics Events Permissions section. Under this section, select all the permissions: Manage Schema, Query Custom Events, and Publish Custom Events
> Note: You cannot change the permissions of an API key once it has been created. If you forgot to include a permission or later need additional permissions, you will need to create a new API key.
5. Click **Create**
6. Copy and save the key. We will use this in the Installation/Configuration section.
> Note: Once you close this dialog box, you cannot retrieve the key again. You will have to create a new API key if you lose this one.
7. Select the checkbox indicating you have copied the key and click **Done**

> For more information on AppDynamics Analytics Events API keys, please click [here](https://docs.appdynamics.com/appd/21.x/21.7/en/analytics/deploy-analytics-with-the-analytics-agent/analytics-and-data-security/manage-api-keys)

#### Catalyst Switch
In order to retrieve the hardware statistics from the Catalyst switch, you will need to know the IP address that would be used to SSH into the switch, the username used to SSH into the switch, and the password to SSH into the switch with the username. Make note of these credentials because they will be used in the Installation/Configuration section.


## Installation/Configuration
1. Clone this repository with the command `git clone https://github.com/gve-sw/gve_devnet_app_dynamics_custom_catalyst`
2. Access the file `credentials.yml`. To this file, add the switch credentials and AppDynamics credentials that you found in the Prerequisites section. Additionally, there is a field for the schema name. For this field, provide a name that you would like to give to the metrics that you will be collecting with AppDynamics.
```
switchIp: 'ip address to ssh into switch'
switchUser: 'username to ssh into switch'
switchPassword: 'password to ssh into switch'
appDIp: 'IP address of the Events Services of AppD'
schemaName: 'Test'
eventsAccountName: 'Account name from the AppD dashboard'
eventsAPIKey: 'API key from the AppD dashboard'
```
3. Set up a Python virtual environment. Make sure Python 3 is installed in your environment, and if not, you may download Python [here](https://www.python.org/downloads/). Once Python 3 is installed in your environment, you can activate the virtual environment with the instructions found [here](https://docs.python.org/3/tutorial/venv.html).
4. Install the requirements with `pip3 install -r requirements.txt`

## Usage

To first create the schema that represents the format of the data sent to AppDynamics, run the command `python3 create_schema.py`

Once that program is complete, you may start adding the data to AppDynamics. To do this, run the command `python3 custom_metrics.py`

custom_metrics.py will poll the Catalyst switch every 5 seconds for its hardware stats. Then it sends these statistics to AppDynamics in the format specified by the schema created with create_schema.py. custom_metrics.py will run indefinitely until it is interrupted. To stop the program, press `Ctrl + C`.

# Screenshots

![/IMAGES/0image.png](/IMAGES/0image.png)

The schema for the Catalyst switch hardware statistics data:
![/IMAGES/schema.png](/IMAGES/schema.png)

The output of custom_metrics.py:
![/IMAGES/custom_metrics.png](/IMAGES/custom_metrics.png)

The data in the AppDynamics dashboard:
![/IMAGES/appd_data.png](/IMAGES/appd_data.png)

Data visuals that can be created with the data in AppDynamics:
![/IMAGES/appd_dashboard.png](/IMAGES/appd_dashboard.png)

### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.
