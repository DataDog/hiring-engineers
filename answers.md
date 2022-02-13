# Solutions-Engineer exercise - Nahuel Porzio

0. [Setting up environments](https://github.com/DataDog/hiring-engineers/edit/solutions-engineer/answers.md#0-setting-up-environments)
1. [Adding host tags](https://github.com/DataDog/hiring-engineers/edit/solutions-engineer/answers.md#1-adding-host-tags)
2. [Installing database](https://github.com/DataDog/hiring-engineers/edit/solutions-engineer/answers.md#2-installing-database)
3. [Custom agent check](https://github.com/DataDog/hiring-engineers/edit/solutions-engineer/answers.md#3-custom-agent-check)
4. [Creating Timeboard via API](https://github.com/DataDog/hiring-engineers/edit/solutions-engineer/answers.md#4-creating-timeboard-via-api)
5. [Sharing a graph](https://github.com/DataDog/hiring-engineers/edit/solutions-engineer/answers.md#5-sharing-snapshot)
6. [Creating a monitor](https://github.com/DataDog/hiring-engineers/edit/solutions-engineer/answers.md#6-creating-alert-monitor)
7. [Collecting APM data](https://github.com/DataDog/hiring-engineers/edit/solutions-engineer/answers.md#7-collecting-apm-data)

<br/>

## 0) Setting up environments


I've opted for the vagrant-option and initiated a standard Ubuntu 18.04 distribution. In my case I'm using a MacBook Pro, which is easily deployed via Brew:


```
# Install
brew install vagrant
# Create directory
mkdir ~/vagrant
cd ~/vagrant
# Build image
vagrant init hashicorp/bionic64
# Add project-conf to ~/vagrant/VagrantFile
Vagrant.configure("2") do |config|
  config.vm.box = "hashicorp/bionic64"
end
# Start vm
vagrant up
# Connect to box
vagrant ssh
```


<img width="623" alt="Screenshot 2022-02-07 at 13 46 51" src="https://user-images.githubusercontent.com/30311249/152790849-109f92a0-e275-4a1d-9a88-371b295fc730.png">

_____
<br/>


## 1) Adding host tags


After successfully installing and running the datadog-agent as per https://app.datadoghq.eu/account/settings#agent/ubuntu

![image](https://user-images.githubusercontent.com/30311249/152792775-093a849b-e436-4c23-a873-579805b2fa60.png)

and making sure that there's activity in the web-dashboard, I proceeded to configure some tags as per https://docs.datadoghq.com/getting_started/tagging.

```
# Add tags
sudo nano /etc/datadog-agent/datadog.yaml
# Content added
tags:
 - "<machine>:<nahuel's ubuntu vm>"
 - "<location>:<amsterdam-noord>"
 - "<hardware>:<macbook-pro>"
```

which after some propagation-time they showed in the Host Map section for my account:

![image](https://user-images.githubusercontent.com/30311249/152795464-183223b5-e47f-4b35-9390-cc434f313cff.png)

____
<br/>

## 2) Installing database

Here I've installed a standard mysql-service and created a test-database to make sure it works (steps followed very similar to the ones described in this external article https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-20-04).

![image](https://user-images.githubusercontent.com/30311249/152797386-c5a177e4-d173-4e89-868d-028bb837041d.png)
<br/>

Then I've configured the integration and deployed the datadog mysql-user along its pertinent permissions as per https://docs.datadoghq.com/integrations/mysql.

![image](https://user-images.githubusercontent.com/30311249/152799363-97ef7092-6399-4196-9e94-02177eb7f33b.png)
<br/>

Which enabled the agent to report some metrics visible in the dashboard almost immediately

![image](https://user-images.githubusercontent.com/30311249/152801703-7d0c2b9a-0482-470a-9d3a-107a0e0ca20c.png)

____
<br/>

## 3) Custom agent check

I referred to https://docs.datadoghq.com/developers/custom_checks/write_agent_check/ and configured a custom-check:

````
# Add file for the check
sudo nano /etc/datadog-agent/conf.d/custom_check.yaml
 
# Add correspondent script
sudo nano /etc/datadog-agent/checks.d/custom_check.py
  
# Verify that the check works
sudo -u dd-agent -- datadog-agent check custom_metric
# Restart service
sudo service datadog-agent restart
````

![image](https://user-images.githubusercontent.com/30311249/152807152-ce7a4d1d-3fc3-4bad-bf92-dbef12b8cbf9.png)


**custom_metric.yaml**
```
init_config:
instances:
 [{}]
 ````
**custom_metric.py**
````
from checks import AgentCheck
import random
class custom_metric(AgentCheck):
 def check(self, instance):
  self.gauge('custom.metric', self.generate_random_number())
 def generate_random_number(self):
  random_int = random.randint(1,1000)
  return random_int
````
<br/>

**Changing interval for the check** --the answer to the bonus question is yes, (as per https://docs.datadoghq.com/developers/custom_checks/write_agent_check/#updating-the-collection-interval) although it may be possible, there's no need to do do this via the python-script itself, since it can admittedly be modified directly on the .yaml.

```
# Update interval
sudo nano /etc/datadog-agent/conf.d/custom_check.yaml
````

**new custom_metric.yaml**
````
init_config:
instances:
  - min_collection_interval: 45
````
<br/>

snapshot of the metric itself on the dashboard
![image](https://user-images.githubusercontent.com/30311249/152814061-c83cf508-21cc-4276-a8b5-3808922e4b9b.png)

___
<br/>

## 4) Creating Timeboard via API

After reading the pertinent articles <br/>
    https://docs.datadoghq.com/api/latest <br/>
    https://docs.datadoghq.com/api/latest/authentication/ <br/>
    https://docs.datadoghq.com/api/latest/dashboards/ <br/>
    https://docs.datadoghq.com/dashboards/querying/ <br/><br/>
    
--I've made sure that I'm able to connect to the system by querying ```https://api.datadoghq.eu/api/v1/validate``` (200) via Postman.

![image](https://user-images.githubusercontent.com/30311249/153011521-4d714489-0465-4b6e-aedf-8b3dbd9d8542.png)

____

<br/>
Then I started testing and interacting with the /dashboards API to get a sense of the mechanics --I must say that since there's many depth levels of information and stated ways of creating dashboards/widgets, I was a little confused over which json-structure is the simplest and ideal model to be used for this instance. For which I went through some trial-and-error cycles with cURL and Postman until figuring out what works for this assignment.
<br/>
<br/>

Ultimately what helped me defining the right format for the requests was combining the DD Postman Collection available in the docs (https://docs.datadoghq.com/getting_started/api/#import-the-datadog-collection-into-postman) together with the JSON-definition available in the UX for the widgets that I created manually, and some basic grasp of functions (https://docs.datadoghq.com/dashboards/functions).

<br/> Once these elements were as clear as possible, I proceeded to write a simple python-script which creates the desired timeboard with the pertinent widgets:

```
import os
import json
import requests
# Auth keys (stored in local variables)
api_key = os.environ['API_KEY']
app_key = os.environ['APP_KEY']
# URL
url = 'https://api.datadoghq.eu/api/v1/dashboard'
# Headers
headers = {
  'DD-API-KEY': api_key,
  'DD-APPLICATION-KEY': app_key
  }
# JSON body
data = {
    "layout_type": "ordered",
    "title": "Timeboard created via API",
    "widgets": [{
            "definition": {
                "type": "timeseries",
                "title": "custom_metric_api",
                "requests": [{
                    "q": "custom.metric{host:vagrant}"
                }]
            }
        }, {
            "definition": {
                "type": "timeseries",
                "title": "mysql_cpu_api",
                "requests": [{
                    "q": "anomalies(mysql.performance.cpu_time{host:vagrant}, 'basic', 3)"
                }]
            }
        },
        {
            "definition": {
                "type": "timeseries",
                "title": "mysql_cpu_last_hour",
                "requests": [{
                    "q": "custom.metric{host:vagrant}.rollup(sum,3600)"
                }]
            }
        }
    ]
}
# Execute call
response = requests.post(url, headers=headers, data=json.dumps(data))
# Print result
print(response.json())
```

<br/>

URL to the dashboard - https://app.datadoghq.eu/dashboard/qgd-6r3-seb/timeboard-created-via-api?from_ts=1644583120454&to_ts=1644586720454&live=true

![image](https://user-images.githubusercontent.com/30311249/153601459-e28658de-0b6e-4eda-9902-f0f14989c791.png)

<br/>

## 5) Sharing snapshot

Here based on the wording of the exercise I wasn't sure that it was possible to share a snapshot of the whole timeboard, or only a specific graph.

After reading trough https://docs.datadoghq.com/metrics/explorer/#snapshot I deduced that it needs to be a graph, and shared it with myself:<br/>

![image](https://user-images.githubusercontent.com/30311249/153604306-fc39666f-dc6d-49ec-8fc1-955cc46acc52.png)

* NOTE - @ notation didn't work here for me, could it be that some setting is off? or perhaps it just doesn't work like that any longer?

<br/>

* > Bonus Question: What is the Anomaly graph displaying? <br/>
*  Bonus Answer: It overlaps the metric with the expected trayectory (I assume based on previous behaviour) in gray, together with the unexpected spikes in red (as in, anything deviating off the gray normal-behaviour reference). 

<br/>

## 6) Creating alert-monitor

Based on the given specs, I created the following monitor https://app.datadoghq.eu/monitors/4399442 with the configuration shown below.

![image](https://user-images.githubusercontent.com/30311249/153611080-e04a66c4-fcc8-4a66-926a-e73054adf306.png)

![image](https://user-images.githubusercontent.com/30311249/153615213-c6eb5ba8-ac9c-4d41-82af-d323cbd2ff35.png)

-Email screenshot
![image](https://user-images.githubusercontent.com/30311249/153624763-5f22d8d5-8924-4c73-8085-c515ee99b91d.png)

<br/>


* Scheduling downtime

I added the following downtime items: 
<br/>

-https://app.datadoghq.eu/monitors/downtimes?id=94331716
![image](https://user-images.githubusercontent.com/30311249/153618084-09daa217-5a34-4dad-ae6a-61c1884e59f9.png) <br/>

-https://app.datadoghq.eu/monitors/downtimes?id=94333243
![image](https://user-images.githubusercontent.com/30311249/153618916-29538669-ccad-4322-968a-36cd80338995.png) <br/>

-Email screenshot
![image](https://user-images.githubusercontent.com/30311249/153619673-0ca9ffbf-50a6-4232-aa27-61520003253f.png) <br/>


_____
<br/>


## 7) Collecting APM data

<br/>

As per https://docs.datadoghq.com/tracing/setup_overview/setup/python I enabled APM-tracing in the vagrant vm
```
# Edit config
sudo nano /etc/datadog-agent/datadog.yaml
# Content
set apm_config: true
# Restart service
sudo service datadog-agent restart
```

<br/>

After resolving some dependencies with python/pip I was able to install ddtrace.
<br/>
Then I stored the flask-app under ```/etc/flask/flask_app.py``` and ran it as advised in the docs. <br/>

```DD_SERVICE="flask_app" DD_ENV="test" DD_LOGS_INJECTION=true ddtrace-run python flask_app.py```
![image](https://user-images.githubusercontent.com/30311249/153751051-dd70e415-f787-4c0e-b781-4751a0c86523.png)
<br/>
In order to create some visible activity in the service I executed this simple unix-script a couple of times to generate some _visits_:
```
#!/bin/bash

for i in {1..500}
do
    curl -X get http://0.0.0.0:5050/
done
```
<br/>
and proceeded as requested to create the following dashboard with some specific APM stats and standard cpu-metrics https://app.datadoghq.eu/dashboard/gx9-nzj-3zr/apm-metrics.
![image](https://user-images.githubusercontent.com/30311249/153751697-cb52d404-c111-4dfa-9327-7c6068ae87dc.png)

<br/><br/>

* > Bonus Question: What is the difference between a Service and Resource? <br/>
*  Bonus Answer: Based on my reading through the documentation, in my own words, a service is a process, or a bundle of processes with a specific function in your architecture --while resources are normally the different domains which can be consumed and monitored within or in relation to the service itself.

 <br/>
 
 ________
 
 ## What's something creative I would do with Datadog?
 
Given my environmentalist nature, provided the resources I would use it to trace and map the actual fuel consumption-metrics from every vehicle in a country (or any larger scale for that matter) running on petrol in order to have tangible data to later properly argument regulations and measures accordingly.

<br/>

The idea's premise is that we currently don't have an accurate way of knowing exactly how much a car actually pollutes in a live nor accumulative fashion except for what car-producers claim or governments sample-test.
<br/>
Having _true_ metrics on this would in my view help in realising footprint and take another step forward towards a more sustainable system.
<br/><br/>
_______
<br/>

End

<br/>
Thanks for taking your time to read my assignment!

<br/>

Nahuel Porzio

