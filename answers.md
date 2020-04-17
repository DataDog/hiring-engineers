## The Exercise

Don’t forget to read the [References](https://github.com/DataDog/hiring-engineers/blob/solutions-engineer/README.md#references)


## Prerequisites - Setup the environment

You can utilize any OS/host that you would like to complete this exercise. However, we recommend one of the following approaches:

* You can spin up a fresh linux VM via Vagrant or other tools so that you don’t run into any OS or dependency issues. [Here are instructions](https://github.com/DataDog/hiring-engineers/blob/solutions-engineer/README.md#vagrant) for setting up a Vagrant Ubuntu VM. We strongly recommend using minimum `v. 16.04` to avoid dependency issues.
* You can utilize a Containerized approach with Docker for Linux and our dockerized Datadog Agent image.

Then, sign up for Datadog (use “Datadog Recruiting Candidate” in the “Company” field), get the Agent reporting metrics from your local machine.


*****Answer: After signging up for my free trial, I leveraged the documentation to appropriately install the agent for mac: https://docs.datadoghq.com/agent/basic_agent_usage/osx/?tab=agentv6v7
API: https://app.datadoghq.com/account/settings#agent/mac

DD_AGENT_MAJOR_VERSION=7 DD_API_KEY=37474ab2e85b7514a8a41d131ce2b351 bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_mac_os.sh)"

To be sure I launched GUI in terminal:
    datadog-agent start
    datadog-agent launch-gui
    
 ![GUI metrics](/images/gui_metrics.png)
 
 
## Collecting Metrics:

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

*****Answer: In line with the documentation, I added some simple tags: name:tim, env:production, role:database in the datadog-agent config file accessed through VS Code. I had a little trouble here (the youtube demonstration helped) because I didn't realize I needed to restart the agent altogether. Once I did that, the new tags were there.

 ![Tags](/images/tags_config.png)
 ![Host with Tags](/images/tags_host.png)
 
 Hostmap url: https://app.datadoghq.com/infrastructure/map?fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=availability-zone&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=true&palette=green_to_orange&paletteflip=false&node_type=host


Tagging documentation used: https://docs.datadoghq.com/tagging/
Also watched an instructional youtube video: https://www.youtube.com/watch?v=xKIO1aWTWrk&t=240s

* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
*****Answer: Fortunately, I already had PostgreSQL downloaded on my machine. I read the documentation and ran the integration for the database. 

*****I ran into a number of permission issues trying to download the integration. Firstly, I couldn't access the psql shell in terminal, which I needed in order to enter the integration commands. I fixed this after reading a few stack overflow questions about the psql binary location and editing the bash_profile path. 

****I also made the mistake of not restarting the agent once I executed the integration. Once corrected, I could move on to the next steps

****Next, I faced a permissions issue, which turned out to be a mistake of where my code lived within the agent directory (Error: no valid check found). I played around with this path error for a bit until I figured out where the scripts needed to live.  

* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
****I created a my_metric.py file in the checks.d folder in the agent directory and wrote a script to create a random value.

![my_metric.py](/images/my_metric.png)

* Change your check's collection interval so that it only submits the metric once every 45 seconds.
****To do this the my_metric.yaml file needs to be the same name as the python script file. So in my_metric.yaml I changed the collection interval to submit a metric once every 45 seconds


![Collection Interval](/images/collection_interval.png)
![Collection Interval Dashboard](/images/postgres_metrics.png)


* **Bonus Question** Can you change the collection interval without modifying the Python check file you created?
****I changed the min_collection_interval to 45 in the conf.yaml file to achieve this

Documentation: https://docs.datadoghq.com/integrations/postgres/
https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7
https://docs.datadoghq.com/agent/troubleshooting/agent_check_status/?tab=agentv6v7
https://docs.datadoghq.com/agent/guide/agent-commands/?tab=agentv6v7
https://docs.datadoghq.com/developers/metrics/agent_metrics_submission/?tab=count
https://www.datadoghq.com/blog/collect-postgresql-data-with-datadog/#datadogs-postgresql-integration
Stack Overflow: https://dba.stackexchange.com/questions/3005/how-to-run-psql-on-mac-os-x


## Visualizing Data:

Utilize the Datadog API to create a Timeboard that contains:

* Your custom metric scoped over your host.
* Any metric from the Integration on your Database with the anomaly function applied.
* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.

Once this is created, access the Dashboard from your Dashboard List in the UI:

****Timeboard Script:

import os
from datadog import initialize, api

options = {
#    'api_key': os.getenv("37474ab2e85b7514a8a41d131ce2b351"),
#    'app_key': os.getenv("5705503ca76be6ce1100251f93ed6bc86acc9848")
    'api_key': os.getenv("API_KEY"),
     'app_key': os.getenv("APP_KEY")
}

initialize(**options)

custom_metrics_graph = {
    "title": "Example Graph",
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:example.graph{*}"}
        ],
        "viz": "timeseries"
    }
}
anomaly_graph = {
    "title": "Anomaly Graph",
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:postgresql.bgwriter.write_time{*}.as_count(), 'basic', 2)"}
        ],
        "viz": "timeseries"
    }
}
custom_rollup_graph = {
    "title": "Rollup of Example for past hour",
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:example{*}.rollup(sum, 3600)"}
        ],
        "viz": "timeseries"
    }
}
title       = "DataDog SE"
description = "A dashboard for DataDog SE"
graphs      = []

graphs.append(custom_metrics_graph)
graphs.append(anomaly_graph)
graphs.append(custom_rollup_graph)

template_variables = [{
    "name": "Tim",
    "prefix": "host",
    "default": "host:tim-cronin"
}]


read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)
                     
Timeboard dashboard: https://app.datadoghq.com/dashboard/wqm-fvz-k3t/datadog-se?from_ts=1587140772834&live=true&to_ts=1587141672834




* Set the Timeboard's timeframe to the past 5 minutes
* Take a snapshot of this graph and use the @ notation to send it to yourself.

Snapshot:
![5 Mins](/images/5_mins.png)

* **Bonus Question**: What is the Anomaly graph displaying?
It is analyzing new behavior as it compares to past behavior - thus providing an anomaly monitor alert when something changes from it's previous pattern

Timeboard Documentation: 
https://docs.datadoghq.com/dashboards/timeboards/
https://docs.datadoghq.com/dashboards/guide/timeboard-api-doc/?tab=python
https://docs.datadoghq.com/dashboards/
https://www.youtube.com/watch?v=bP1YH161GBM
https://www.youtube.com/watch?v=xMmWYyb5Z3o

## Monitoring Data

Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

* Warning threshold of 500
* Alerting threshold of 800
* And also ensure that it will notify you if there is No Data for this query over the past 10m.


Please configure the monitor’s message so that it will:

* Send you an email whenever the monitor triggers.
* Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
* Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
* When this monitor sends you an email notification, take a screenshot of the email that it sends you.


****I was able to perform these functions on the Datadog platform using the "monitors" feature. I created a new monitor and customized it accordingly to the thresholds provided.

Monitor link: https://app.datadoghq.com/monitors/17713330

Monitor Images

![Monitor Alert 1](/images/monitor_alert.png)
![Monitor Alert 2](/images/monitor_alert2.png)
![Alert Email](/images/alert_email.png)

* **Bonus Question**: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

  * One that silences it from 7pm to 9am daily on M-F,
  * And one that silences it all day on Sat-Sun.
  * Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

****Downtime weekday image:

![Alert Email](/images/downtime.png)

Monitoring & Alerting Documentation:
https://docs.datadoghq.com/monitors/notifications/?tab=is_alert
https://www.datadoghq.com/blog/monitoring-101-alerting/
https://docs.datadoghq.com/monitors/downtimes/

## Collecting APM Data:

Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:

```python
from flask import Flask
import logging
import sys

# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

app = Flask(__name__)

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

* **Note**: Using both ddtrace-run and manually inserting the Middleware has been known to cause issues. Please only use one or the other.

Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

Please include your fully instrumented app in your submission, as well.

****Answer:
First I installed ddtrace using pip install ddtrace. I used ddtrace-run and I leveraged the APM documentation and input the given script into a my_app.py file. ![My App](/images/my_app.png) I was able to run this and start collecting the APM data. Once again I originally had a path error reading the file, but sorted that issue out as I kept receiving a permissions error. 

Dashboard Images:
![Flask](/images/flask_apm.png)

****Admittedly I was only able to properly collect APM data when I ran it one time. I was unable to duplicate this process, thus the scarcity of the image provided.


* **Bonus Question**: What is the difference between a Service and a Resource?
Services work together to provide a feature set. Resources live within servcies. I.E. resources enable a platform, and services allow you to do things on that platform. 

Documentation: 
https://www.youtube.com/watch?v=faoR5M-BaSw
https://docs.datadoghq.com/tracing/
https://docs.datadoghq.com/tracing/setup/python/
https://docs.datadoghq.com/tracing/app_analytics/?tab=java
https://www.datadoghq.com/blog/monitoring-flask-apps-with-datadog/

## Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?


****Answer
I know it's an odd hobby to be passionate about, but I'm an adamant surfer (yes, even in the New York winters). I travel all over to surf when the conditions get good in the NY tristate area, as well as internationally on holidays. After having read a few blog posts, I think Datadog could have a unique impact on the surf community by monitoring time, energy, money, days, and months spent surfing or traveling to the surf. Being a NYC native, I was always envious of surfers in California or Hawaii, because I felt they had such easy access to the world class waves nearby. It would be interesting to see which days most surfers head to the water (in each location), as well as time spent in the water, and distanced traveled to get there. Something tells me the people who have access tend to surf less than those that get to sparingly. I'd love to see the juxtaposition of geographical location and expenses to surf as well. Over the course of time, proper monitoring would tell you how much time and money you're spending on such a hobby, and if it's paying off in the end!

Sources of inspiration: https://www.datadoghq.com/blog/datadog-in-the-wild-5-fun-projects/


## Instructions

If you have a question, create an issue in this repository.

To submit your answers:

* Fork this repo.
* Answer the questions in answers.md
* Commit as much code as you need to support your answers.
* Submit a pull request.
* Don't forget to include links to your dashboard(s), even better links and screenshots. We recommend that you include your screenshots inline with your answers.

## References

### How to get started with Datadog

* [Datadog overview](https://docs.datadoghq.com/)
* [Guide to graphing in Datadog](https://docs.datadoghq.com/graphing/)
* [Guide to monitoring in Datadog](https://docs.datadoghq.com/monitors/)

### The Datadog Agent and Metrics

* [Guide to the Agent](https://docs.datadoghq.com/agent/)
* [Datadog Docker-image repo](https://hub.docker.com/r/datadog/docker-dd-agent/)
* [Writing an Agent check](https://docs.datadoghq.com/developers/write_agent_check/)
* [Datadog API](https://docs.datadoghq.com/api/)

### APM

* [Datadog Tracing Docs](https://docs.datadoghq.com/tracing)
* [Flask Introduction](http://flask.pocoo.org/docs/0.12/quickstart/)

### Vagrant

* [Setting Up Vagrant](https://www.vagrantup.com/intro/getting-started/)

### Other questions:

* [Datadog Help Center](https://help.datadoghq.com/hc/en-us)
