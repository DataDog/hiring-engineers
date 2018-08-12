# Nick Bebel's Step by Step Guide to Installing and Setting Up Datadog

## Getting Started
1. Went to https://www.datadoghq.com/ and created an Account
2. Signed into AWS account and spun up a new Ubuntu 16.04 EC2 instance (Vagrant was having issues)

![dd1](https://user-images.githubusercontent.com/22799519/43994186-b5774ce8-9d66-11e8-9f32-056f7f68d8a9.PNG)

3. Time to SSH into the instance
  - ssh -i "nbebel_datadog.pem" ubuntu@ec2-18-222-230-242.us-east-2.compute.amazonaws.com
4. Then I ran the Datadog curl command to install the agent
5. Install AWS Integration
  - Create DD Role in AWS (https://docs.datadoghq.com/integrations/amazon_web_services/)
6. Verify Agent is working

![dd2](https://user-images.githubusercontent.com/22799519/44004211-e6e912cc-9e2c-11e8-8959-61073c87c033.PNG)

## Configuring the Agent to Collect Metrics
(datadog.yaml file can be found at the end of file)
1. Adding a custom tag in the datadog.yaml file
  - tags:
      role:datadog_test
2. Since I am using AWS for the instance, I also turned on the collect EC2 tags option in the file
``` 
collect_ec2_tags: true
```
3. Verify that the tags came in

![dd3](https://user-images.githubusercontent.com/22799519/44004602-ca6f5a7e-9e32-11e8-82ac-d3c4bc338c57.PNG)

4. Since I was most familiar with mySQL, so I installed that
  - sudo apt-get install mysql-server -y
5. Created datadog user in mySQL with full permissions to collect metrics
  - sudo mysql -e "CREATE USER 'datadog'@'localhost' IDENTIFIED BY 'password';"
  - sudo mysql -e "GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'localhost' WITH MAX_USER_CONNECTIONS 5;"
  - sudo mysql -e "GRANT PROCESS ON *.* TO 'datadog'@'localhost';"
  - sudo mysql -e "GRANT SELECT ON performance_schema.* TO 'datadog'@'localhost';"
6. Created mysql.yaml file to set up mySQL datadog integration (https://app.datadoghq.com/account/settings#integrations/mysql)
7. Verify that mySQL is collecting metrics

![dd4](https://user-images.githubusercontent.com/22799519/44004762-ec5b0702-9e35-11e8-9cc3-f85611352bb1.PNG)

8. Created funmetric.py to create a custom random number metric
``` 
import random

from checks import AgentCheck
class HelloCheck(AgentCheck):
    def check(self, instance):
        self.gauge('funmetric', random.randint(0,1000))
```
9. Create funmetric.yaml which will also set the minimum collection time to 45 seconds
```
init_config:

instances:
   -  min_collection_interval: 45
```
10. Restart Datadog Agent 
```
sudo service datadog-agent restart
```
11. Verify that funmetric is reporting in the console

![dd5](https://user-images.githubusercontent.com/22799519/44004941-35e8591c-9e39-11e8-8ca8-ab6d9eee3919.PNG)

## Time to Work with the Data
1. In order to use the Datadog API, I used the instructions found here (https://github.com/DataDog/datadogpy)
2. Install datadog python tools
``` 
pip install datadog
```
3. Create dashboard.py script that will create a timeboard that will include a normal graph for my custom metric, a rollup of the custom metric and an anomaly graph for mySQL CPU Performance and I found the information here (https://docs.datadoghq.com/api/?lang=python#timeboards) 
```
from datadog import initialize, api

options = {
    'api_key': '8675309',
    'app_key': 'Jenny'
}

initialize(**options)

title = "Datadog Assignment - API Dashboard"
description = "Please hire me :)"

graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:funmetric{*}"}
        ],
        "viz": "timeseries"
    },
    "title": "funmetric"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:mysql.performance.cpu_time{*}, 'basic', 1)"}
        ],
        "viz": "timeseries"
    },
    "title": "mySQL CPU Time"


},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:funmetric{*}.rollup(sum, 3600)"}
        ],
        "viz": "timeseries"
    },
    "title": "funmetric Rollup"


}
]
```
4. Run the python script
```
python dashboard.py
```
5. Verify that the Dashboard was created

![dd6](https://user-images.githubusercontent.com/22799519/44005447-9cfbaa84-9e41-11e8-8e56-caf14e6103ac.PNG)

6. I set the time board to 5 minutes by adjusting the to_ts in the URL to 5 minutes later than the from_ts 

![dd7](https://user-images.githubusercontent.com/22799519/44005482-49406384-9e42-11e8-9800-292445b7fb14.PNG)

7. Took a snapshot of one of the graphs and sent it to myself

![dd8](https://user-images.githubusercontent.com/22799519/44005544-092e1b32-9e43-11e8-9834-546212fae491.PNG)

### Surprise Question Time!
The anomaly graph is looking for outliers in patterns.  It is taking a look at the historic data and will change color when the metric goes outside of the range the system has learned as normal.  This would be seen if you had a graph for CPU utilization and the instance was almost always between 10% and 20%, but if it suddenly spiked to 50% or dropped to 3%, then the graph line would turn red during that time.

## Alerting!
1. Created the alert that can be seen below that has the 3 different states (Alert, Warning and No Data).  Host IP was not populating when it usuall auto-fills after the brackets and was not given the option (didn't have an option for anything i.e. host.name)

![dd9](https://user-images.githubusercontent.com/22799519/44005818-7278e258-9e47-11e8-9347-3a877fdd2ead.PNG)
![dd10](https://user-images.githubusercontent.com/22799519/44005819-72855a74-9e47-11e8-89ac-c445aea0cf3d.PNG)

2. Set up maintenance windows for the alarm for over night and the weekend.

![dd11](https://user-images.githubusercontent.com/22799519/44005975-2b9c7c84-9e4a-11e8-9119-8544f1504eaf.PNG)
![dd12](https://user-images.githubusercontent.com/22799519/44005976-2ba88042-9e4a-11e8-853e-92cf71089de3.PNG)

3. I then muted the alarm to get it to stop emailing me.

## APM
1. I first installed ddtrace for a python application
```
pip install ddtrace
```
2. Then I made the changes to the datadog.yaml file
```
# Trace Agent Specific Settings
#
apm_config:
#   Whether or not the APM Agent should run
enabled: true
#   The environment tag that Traces should be tagged with
#   Will inherit from "env" tag if none is applied here
env: none
#   The port that the Receiver should listen on
receiver_port: 8126
#   Whether the Trace Agent should listen for non local traffic
#   Only enable if Traces are being sent to this Agent from another host/container
apm_non_local_traffic: false
#   Extra global sample rate to apply on all the traces
#   This sample rate is combined to the sample rate from the sampler logic, still promoting interesting traces
#   From 1 (no extra rate) to 0 (don't sample at all)
extra_sample_rate: 1.0
#   Maximum number of traces per second to sample.
#   The limit is applied over an average over a few minutes ; much bigger spikes are possible.
#   Set to 0 to disable the limit.
max_traces_per_second: 10
#   A blacklist of regular expressions can be provided to disable certain traces based on their resource name
#   all entries must be surrounded by double quotes and separated by commas
#   Example: ["(GET|POST) /healthcheck", "GET /V1"]
ignore_resources: []
```
3. Then i configured the middleware in the script
```
from flask import Flask

import time
import logging
import sys
import blinker as _

from ddtrace import tracer
from ddtrace.contrib.flask import TraceMiddleware

# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)
app = Flask(__name__)
traced_app = TraceMiddleware(app, tracer, service="my-flask-app", distributed_tracing=False)

@app.route('/')
def api_entry():
    return 'Entrypoint to the Application'

@app.route('/api/apm')
def apm_endpoint():
    return 'Getting APM Started'

@app.route('/api/trace')
def trace_endpoint():
    return 'Posting Traces'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5050')
```
4. I then installed flask and blinker onto the instance (probably should have done that one step earlier)
5. I then started the script running on the instance
6. Then after being unable to make the requests work, I realized that my instance didn't have the proper security clearance so I updated that to allow someone to hit port 5050
7. Then I got the requests to work and saw the traces come in

![dd13](https://user-images.githubusercontent.com/22799519/44007582-5f3eaa64-9e66-11e8-954c-e18469052cba.PNG)

8. I made a small dashboard that had and APM metric (Flask Hits) and Infrastructure (CPU Utilization)

![dd14](https://user-images.githubusercontent.com/22799519/44007619-fe2192ea-9e66-11e8-9e22-4c44c0146305.PNG)

## Another Surprise Question!!
A service is a group of processes that are doing the same job and a resource is a specific action for a service. (Answer cribbed from the datadog document repo)

## Fun Times with Datadog
This was almost something we did with Datadog at Everquote for our Annual Hack-a-thon, but it was rejected for not being that relevant to the company (I think that means it was too fun).  But I wanted to put Datadog onto a raspberry pi device and the attach a trigger to the device.  I would then attach the trigger to a dog treat dispenser.  The goal of this was to put the dispenser just outside of our window and would notify our Slack channel that a dog was nearby so we could all go look at the dog.  We had had too many times missing seeing a dog.
