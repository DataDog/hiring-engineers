Your answers to the questions go here.
# About Datadog
Datadog is a data monitoring service for cloud-scale applications, bringing together data from servers, databases, tools, and services to present a unified view of an entire stack. These capabilities are provided on a SaaS-based data analytics platform. [Wiki](https://en.wikipedia.org/wiki/Datadog)

### Features
* Observability - From infrastructure to apps, in any environment
* Dashboards - Use instant, real-time boards or build your own
* Infrastructure - From overview to deep details, fast
* Analytics - Custom app metrics or business KPIs
* Collaboration - Share data, discuss in context, solve issues quickly
* Alerts - Avoid alert fatigue with smart, actionable alerts
* API - Love infrastructure as code? You'll love Datadog's API
* Machine Learning - Automatically detect outliers and temporal anomalies
* APM - Monitor, optimize, and troubleshoot app performance

<a href="http://www.flickr.com/photos/alq666/10125225186/" title="The view from our roofdeck">
<img src="http://farm6.staticflickr.com/5497/10125225186_825bfdb929.jpg" width="500" height="332" alt="_DSC4652"></a>

# Here we go - Gerd Plewka, Germany...


# The Challenge

## Questions

### Level 0 (optional) - Setup an Ubuntu VM


### Level 1 - Collecting Metrics

Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

#### Answer: Find it at InitialHostmap.png

Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

#### Answer: I used MySQL

Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
Change your check's collection interval so that it only submits the metric once every 45 seconds.
Bonus Question Can you change the collection interval without modifying the Python check file you created?

#### ./checks.d/my_metric.py
``` Python

import random

from checks import AgentCheck
 
class my_metric(AgentCheck):
	def check(self, instance):
		self.gauge('my_metric', random.randint(1,1001))

```
     
#### ./conf.d/my_metric.yaml
``` YAML
init_config:
    min_collection_interval: 45

instances:
    [{}]
```

#### setting min_collecting_interval also is the answer to the bonus question...


### Level 2 - Visualizing your Data

#### challenge here, wasn't able to get this script to work properly... couldn't find a better syntax definition of the anomalies command...Nevertheless, the other commands worked...
#### anyway, the script to create this timeboard should look like this:

#### GerdsChallenge.sh
```Shell

api_key=22a62687a16651ff40ac350700bd1489
app_key=5f391773d79ec9ec871d5b1015ca2bd59f86a1de

curl  -X POST -H "Content-type: application/json" \
-d '{
        "title" : "Gerds API Timeboard",
        "description" : "API generated timeboard",
        "template_variables": [{
            "name": "host1",
            "prefix": "host",
            "default": "precise64"
            }],
        "graphs" : [{
            "title": "Gerds custom metric",
            "definition": {
                "events": [],
                "requests": [
                    {"q": "my_metric{host:precise64} "}
                ],
                "viz": "timeseries"
            }
        },
        {
            "title": "MYSQL anomalies"
            "definition": {
            "events": [],
            "requests": [
                {"q": "anomalies(avg:mysql.performance.user_time{host:precise64}, 'basic', 2)"}
                ],
            "viz": "timeseries"}
        },
        {
            "title": "Rollup",
            "definition": {
                "events": [],
                "requests": [
                    {"q": "avg:my_metric{host:precise64}.rollup(sum,3600)"}
                ],
                "viz": "query_value"
            }
        }
      ]
}' \
"https://api.datadoghq.com/api/v1/dash?api_key=${api_key}&application_key=${app_key}"
```



Set the Timeboard's timeframe to the past 5 minutes
Take a snapshot of this graph and use the @ notation to send it to yourself.
#### Find this at 5min graph.png

Bonus Question: What is the Anomaly graph displaying?
#### not sure, if this question is really meant this straight forward...
#### It is showing which data are outside the upper or lower bounds, that were calculated out of the past metric values.
#### From here, one can crreate trigger (monitors) to create actions... 


### Level 3 - Alerting on your Data

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

Warning threshold of 500
Alerting threshold of 800
And also ensure that it will notify you if there is No Data for this query over the past 10m.

#### See at metric monitor1.png and metric monitor2.png

Please configure the monitor’s message so that it will:

Send you an email whenever the monitor triggers.

Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.

Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.

When this monitor sends you an email notification, take a screenshot of the email that it sends you.

#### see at warningAlert.png

Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

One that silences it from 7pm to 9am daily on M-F,
And one that silences it all day on Sat-Sun.
Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification

#### see at Silenced MonitorUI1.png, Silenced Monitor Mail 1.png, resp the versions with the 2

### Level 4 - Collecting APM Data

#### see at Combined APM and Infrastructure.png
#### will link work?
#### https://app.datadoghq.com/dash/904666/gerds-api-timeboard?live=true&page=0&is_auto=false&from_ts=1535957036725&to_ts=1535971436725&tile_size=m

Bonus Question: What is the difference between a Service and a Resource?

### Level 5 - Final Question
Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?

#### 2 things immediately come to my mind:
#### Look into what can be done in terms of aggregating data for securitz personnel (I am holding a CISSP)
#### see, if I can get hold of a multisensor (GPS, GSM, acceleration, temp, humid...) to get more into the field of IoT


#### A "service" is a set of processes, whereas a "resource" is anz data that is returned, when querying a "service" 

## Instructions
If you have a question, create an issue in this repository.

To submit your answers:

1. Fork this repo.
2. Answer the questions in `answers.md`
3. Commit as much code as you need to support your answers.
4. Submit a pull request.
5. Don't forget to include links to your dashboard(s), even better links *and* screenshots.  We recommend that you include your screenshots inline with your answers.

## References

### How to get started with Datadog

* [Datadog overview](http://docs.datadoghq.com/overview/)
* [Guide to graphing in Datadog](http://docs.datadoghq.com/graphing/)
* [Guide to monitoring in Datadog](http://docs.datadoghq.com/guides/monitoring/)

### The Datadog Agent and Metrics

* [Guide to the Agent](http://docs.datadoghq.com/guides/basic_agent_usage/)
* [Writing an Agent check](http://docs.datadoghq.com/guides/agent_checks/)

### Other questions:
* [Datadog Help Center](https://help.datadoghq.com/hc/en-us)

### About Me
Mathematician, Computer Scientist, Barista, World Explorer

[My Linkedin](https://www.linkedin.com/in/mei-jin/)
