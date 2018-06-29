# Tim's DataDog answers

Hi DataDoggers - my name is Tim.  I'm happy to share with you the results of the exercise.  It was a slight ordeal, but only because lightning took a toll on my home network and ISP and created many distractions and disconnections along the way!

## Pre-reqs
I played with a couple of environments for the agent, as I initially dove right into a cross-language APM use case on Docker.  However, after some incomplete results, I switched to a more traditional Ubuntu 16.04 VM to complete the exercise.

## Collecting metrics

> Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

* I've added a screenshot of the agent's configuration along with the tags in the Hostmap.
![Host View Screenshot with Tags](screenshots/tags.png?raw=true "Tags Screenshot")

> Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

* Added a MongoDB instance to the Ubuntu VM.
![MongoDB Host View Screenshot](screenshots/mongo.png?raw=true "Mongo DB In Host View Screenshot")
[MongoDB OOB Dashboard](https://app.datadoghq.com/screen/integration/13/mongodb?page=0&is_auto=false&from_ts=1530293880000&to_ts=1530297480000&live=true)

> Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

* I implemented the following check:

```python
from checks import AgentCheck

import random

class CustomCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', 
            random.randint(0,1000))
```

> Change your check's collection interval so that it only submits the metric once every 45 seconds.

> __Bonus Question:__ Can you change the collection interval without modifying the Python check file you created?

* I found the [agent check documentation](https://docs.datadoghq.com/developers/agent_checks/) indicates: 
* _For Agent 6, min_collection_interval must be added at an instance level, and can be configured individually for each instance._
* I went straight to this instead of modifying the collection interval in Python.  
```
init_config:

instances:
   - min_collection_interval: 45
```
* It appears this works, although the documentation also says:
* _If it is greater than the interval time for the Agent collector, a line is added to the log stating that collection for this script was skipped._ 
* I never saw anything logged, but the data points did appear to spread out - in most cases, seemingly closer to a minute, but that seemed to follow the 20 second collection interval documented.  

## Visualizing Data

>Utilize the Datadog API to create a Timeboard that contains:
>* Your custom metric scoped over your host.
>* Any metric from the Integration on your Database with the anomaly function applied.
>* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

* My [Timeboard API script](scripts/timeboard.py) successfully created the timeboard.
![Timeboard screenshot](screenshots/timeboard.png?raw=true "Timeboard Screenshot")
[Link to Timeboard](https://app.datadoghq.com/dash/843863/hiring-engineers?live=true&page=0&is_auto=false&from_ts=1530282956720&to_ts=1530297356720&tile_size=m)
>* Set the Timeboard's timeframe to the past 5 minutes
>* Take a snapshot of this graph and use the @ notation to send it to yourself.

* Snapshot with annotation and notification:
![Snapshot screenshot](screenshots/snapshot1.png?raw=true "Snapshot with notification")

>* __Bonus Question:__ What is the Anomaly graph displaying?

* The anomaly graph is showing whether the metric in question meets the "normal" defintion for the provided parameters.  In this example, that normal band is at 3 standard deviations.  The metric in my snapshot below had consistently been at a value of .02 and it's easy to see how the baseline started to adjust as the metric continued to report a value of .03.
![Snapshot screenshot of Anomaly](screenshots/snapshot2.png?raw=true "Snapshot with notification")

## Monitoring Data

>Create a new Metric Monitor...

* Metric monitor with the prescribed thresholds, messages, and notifications.
![Metric Monitor Configuration Screenshot](screenshots/monitordef.png?raw=true "Metric Monitor")

>* When this monitor sends you an email notification, take a screenshot of the email that it sends you.

* Warning email:
![Warning email screenshot](screenshots/alertemail.png?raw=true "Email Example")


>* __Bonus Question:__ Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor...

* Downtime definition for 7-9 PM:
![Weekday definition](screenshots/downtimedef1.png?raw=true "7-9 PM downtime definition")

* Downtime definition for Saturday & Sunday:
![Weekend definition](screenshots/downtimedef2.png?raw=true "Weekend definition")

## Collecting APM Data:

> Given the (..) Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution

* I opted to use the Flask app since the inital Java attempt on Docker didn't get me anywhere.  In retrospect, I think it was a misunderstanding about how the Docker agent related to the APM agent.

* First was some initial setup, cribbed from the Flask docs http://flask.pocoo.org/docs/0.12/installation/#installation : 
```bash
sudo apt install python-pip
sudo apt-get install python-virtualenv
mkdir myproject
$ cd myproject
$ virtualenv venv
. venv/bin/activate
pip install Flask
```
* Then, I brought over the sample app and amended it with APM instructions from http://pypi.datadoghq.com/trace/docs/#module-ddtrace.contrib.flask

* I executed the [modified sample app](scripts/sampleapp.py) and ran a few transactions before exiting and deactivating the virtual environment:
```bash
python sampleapp.py
^C
deactivate
```

* APM screen not loading with my plagued internet
![APM Setup](screenshots/apmsetup2.png?raw=true "APM Agent Traces")


* The screenboard constructed with Host, MongoDB, Metric Monitor, and App Service metrics:
![Screenboard](screenshots/screenboard.png?raw=true "Screenboard")
[Link to Screenboard](https://app.datadoghq.com/screen/369832/tims-screenboard-27-jun-2018-1302?page=0&is_auto=false&from_ts=1529949600000&to_ts=1530122400000&live=true)

* I was trying to do something a little more interesting with the callouts, like put some color behind the graph boxes, but I noticed the Z-order wouldn't stay preserved. 

>__Bonus Question:__ What is the difference between a Service and a Resource?

* Based on what I see in the UI, the service is the "named" version of what someone consumes.  As a developer, I may have named the application code [sampleapp.py](scripts/sampleapp.py), but within the organization we're much more likely to call it "tims-flask-app" or something more business friendly.  
![Trace Screen](screenshots/servicevresource.png?raw=true "Service with Resource")
From the screen capture, the resources are the entry points to the different tiers of this application/service.  They'd be referred to as FrontEnds in my usual APM tool.


## Final Question
> Is there anything creative you would use Datadog for?

IoT applications are always interesting.  As someone who once had a dryer in an outbuilding, I always wanted a way to know when the cycle had completed since the timing is usually not accurate and I could not hear the buzzer.  

Now that Rasberry Pis and Arduinos have filled a lot of instrumentation niches, it's easy to see that I was not the only one with this problem. [Many examples](https://www.google.com/search?q=arduino+dryer+cycle) used an Arduino to track the vibration of the machine.  I think it would be interesting to graph those oscillations. 
  * Does the frequency vary with the size of the load, assuming no overload?
  * What's the rate of power consumption vs. load size?
  
  Anomoly detection could possibly reveal other interesting pieces of data: 
  * Is the device overloaded?
  * Are there seasonal variations in the vibrations? (e.g. winter clothes!)

Instead of just measuring for the finished condition or the fault condition, DataDog would provide the opportunity to make more informed decisions.  What more could one ask from monitoring?

## Parting Thoughts

I definitely got a feel for what the DataDog tool is like, and would be interested to see how it comes together in a larger use case.