Your answers to the questions go here.

I found this challenge very interesting. It did take me a good amount of time to finished it as I was trying to familiarize myself with DataDog. I felt that this is as much as takehome challenge as training for DataDog Solution Engineer as you learn so much of what dataDog is. 

##  Prerequisites - Setup the environment

Following instructions from Hiring exercise I set up  virtual environment with Vagrant on my computer. It was my first experience with vagrant so I use my time to learn about Vagrant from their introduction page on vagrantup.com. After that I opened Datadog account using “Datadog Recruiting Candidate” . After signing up, I used plenty of time to familiarize myself with product before continuing with challenge.

## Collecting Metrics:


First task was to add  tags in the Agent config file. I used couple of tags for the purposes of the training such as app:frontend; app:intake; role:database; role:webserver. Screenshot was taken by accessing on Datadog website Infrastructure-HostMap and clicking on agents. Following the instructions I took a screenshot :

<img width="1263" alt="screen shot 2018-08-05 at 1 16 08 pm" src="https://user-images.githubusercontent.com/33996832/43689587-c9043c80-98b1-11e8-8625-209863340c3a.png">

## Database Integration

After initially struggling with Mongo; I decided to install MySQL in the VE. Also I follow the examples how to integrate MySQL on Datadog. Also Configuration file needed to be updated as well. Screenshot was taken by accessing DataDog website Dashboards-Dasboard List and clicking on MySQL-Overview:

<img width="1291" alt="screen shot 2018-08-05 at 1 20 05 pm" src="https://user-images.githubusercontent.com/33996832/43689630-5f5eea0e-98b2-11e8-8038-4f909da36c3f.png">


## Creating a custom Agent check

Last part of collecting metrics was to submits a metric named my_metric with a random value between 0 and 1000 and also change your check's collection interval so that it only submits the metric once every 45 seconds. After I creating a new file in Python I capture of process and code in following screenshots:

<img width="711" alt="screen shot 2018-08-02 at 11 18 09 am" src="https://user-images.githubusercontent.com/33996832/43683234-7ce8802e-983c-11e8-8307-9ae8eb2407fc.png">

<img width="492" alt="screen shot 2018-08-02 at 11 29 10 am" src="https://user-images.githubusercontent.com/33996832/43683248-909bf452-983c-11e8-8aa4-1a9d59d39a72.png">

<img width="518" alt="screen shot 2018-08-02 at 11 28 26 am" src="https://user-images.githubusercontent.com/33996832/43683256-a60e8fa2-983c-11e8-9041-845d1c17f2b7.png">

## Bonus Question

Bonus question was "Can you change the collection interval without modifying the Python check file you created"? , and answer is yes simply by using the User Interface from dataDog website. In order for you to do that click simply on Metrics -Summary and find file you want to modify. Cliuck on that file and click on a pennext to Metadata. After yopu modify changes you want, simply save changes. Screenshot of the process :

<img width="1395" alt="screen shot 2018-08-04 at 11 22 44 pm" src="https://user-images.githubusercontent.com/33996832/43683320-d90ff7f0-983d-11e8-882f-103bdb1b44fc.png">

## Visualizing Data: Timeboard

Part of this challenge was to utilize the Datadog API to create a Timeboard that contains: Your custom metric scoped over your host; any metric from the Integration on your Database with the anomaly function applied and your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket. Timeboard with a name "Zoran-DataDog-TimeBoard" was created and anomaly fucntion was applied as well as rollup function to sum up all points. Code is listed bellow:

```
from datadog import initialize, api
options = {
    'api_key': '8b96bea313315d381580e77971b614a4',
    'app_key': '44ac1d10b45af60e309aa2ddadc507cc6a4bcfd2'
}
initialize(**options)
title = "Zoran-DataDog-TimerBoard"
description = "Timeboard."
graphs = [
     {
        "definition": {
            "events": [],
            "requests": [
                {   "q": "avg:my_metric{host:ubuntu-xenial}",
                }
            ],
        },
        "title": "my_metric"
    },
     {
        "definition": {
            "events": [],
            "requests": [
                {
                    "q": "anomalies(avg:mysql.net.connections{host:ubuntu-xenial}, 'basic', 2)"
                }
            ],
        },
        "title": "mysql connections  anomalies"
    },
     {
        "definition": {
            "events": [],
            "requests": [
                {
                    "q": "avg:my_metric{host:ubuntu-xenial}.rollup(sum,3600)"
                }
            ],
        },
        "title": "my_metric rollup"
    },
]
read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     read_only=read_only)

                                                   
```

Screenshot of the timeBoard is provided here:

<img width="1298" alt="screen shot 2018-08-05 at 2 26 56 am" src="https://user-images.githubusercontent.com/33996832/43684569-7e4fbb88-9857-11e8-91f6-524688d27a91.png">


After accessing Dashboard from your Dashboard List in the UI, Timeboard's timeframe was set to the past 5 minutes. Snapshot of this graph was took and use the @ notation to send it to ourself .

<img width="503" alt="screen shot 2018-08-05 at 12 14 48 am" src="https://user-images.githubusercontent.com/33996832/43683651-314c5a2e-9845-11e8-9cc3-c27c205a1898.png">

## Bonus Question:

Bonus question was What is the Anomaly graph displaying? Anomaly detection is an algorithmic feature that allows you to identify when a metric is behaving differently than it has in the past, taking into account trends, seasonal day-of-week and time-of-day patterns. You can find more in DataDog docs on https://docs.datadoghq.com/monitors/monitor_types/anomaly/

## Monitoring Data

This part of the challenge was manipulation with the monitor. It was asked to create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:Warning threshold of 500;alerting threshold of 800 and also ensure that it will notify you if there is No Data for this query over the past 10m.Monitor’s message was created on the website under Monitor with warning/alerts and No data Info. 

```
{{#is_no_data}}data is missing in last 10 minutes. {{/is_no_data}}

{{#is_alert}}Alerting threshold of {{value}}, host ip address is {{host.ip}} {{/is_alert}}

{{#is_warning}} Warning threshold of {{value}}, host ip address is {{host.ip}} {{/is_warning}}

@zoransavic@me.com

```
This a screenshot of an e-mail that I recieved:

<img width="476" alt="screen shot 2018-08-05 at 12 48 52 am" src="https://user-images.githubusercontent.com/33996832/43683842-713a349a-9849-11e8-9024-ed6855d97d45.png">

## Bonus Question

Bonus question was to set up two scheduled downtimes for this monitor: One that silences it from 7pm to 9am daily on M-F and one that silences it all day on Sat-Sun.Also to set up an  email that  will notified when you schedule the downtime and take a screenshot of that notification.To do this you simply navigate on website to Monitors and choose Manage Downtime.There I set up two different downtimes. One that will run from Saturday 12:01 am until Sunday 11:59 pm and second that will be go daily from 7 pm until 9 am next day. I realized that two of them will run concurently over the weekend but that was necessary so downtime can be recurring. I alsno noticed that weekend one ending at Sunday midnight , when in reality it could be extended by Monday morning but that was already covered by Daily downtime (6 pm-9am). In the screenshot that I am submitting there is a typo that I fixed by editing the message.

<img width="508" alt="screen shot 2018-08-05 at 1 03 16 am" src="https://user-images.githubusercontent.com/33996832/43683955-5d709362-984b-11e8-9125-b939bf2e839d.png">

## Collecting APM Data:

In collecting APM Data I used FLASK APP that was provided :

```
from flask import Flask
import logging
import sys

from ddtrace import tracer
from ddtrace.contrib.flask import TraceMiddleware
from ddtrace import patch_all
import blinker as _

# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

app = Flask(__name__)

traced_app = TraceMiddleware(app, tracer, service="flask_trace", distributed_tracing=False)

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
        app.run(host='0.0.0.0', port='8000')
	
```
	
Screenshot is provided here:

<img width="669" alt="screen shot 2018-08-05 at 1 22 51 am" src="https://user-images.githubusercontent.com/33996832/43684083-66853284-984e-11e8-974b-516506acef37.png">

After that on DataDog website under the dashboard I added some of  APM data and system metric data.

<img width="1238" alt="screen shot 2018-08-05 at 1 38 05 am" src="https://user-images.githubusercontent.com/33996832/43684199-779429a2-9850-11e8-86ad-07f5442da6ad.png">

Public URL of that Dashobard Data is provided here: https://p.datadoghq.com/sb/2c0cfd46c-fc640196d77616c9c7f57554e53a6ef1

## Bonus Question

Question is :'What is the difference between a Service and a Resource"? Service is a set of processes that do the same job.A resource is a particular action for a given service.

## Final Question:

One of the thing I was thinking is Supermarkets. By monitoring number of some items on the shelves you can send notifications when some item run low so instead of worker manualy checking if something needs to be stock.As soon as customer take the item fromn the shelves data is updated and simply setting aleerts when number of items is low, you will be able to know what need to be restock. Also fruit and vegetable area for example temperature  can be monitor and if is too high or too low, alert can be send. Same goes for coolers. Going even more insane, every line can provide number of people who are waiting in that particular line to pay so you can easily find a line with smaller number of customers to exit the store as fast as you can instead of visually trying to figure it out. 

