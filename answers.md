## Prerequisites - Setup the environment

> You can utilize any OS/host that you would like to complete this
> exercise. However, we recommend one of the following approaches:
> 
> * You can spin up a fresh linux VM via Vagrant or other tools so that you don’t run into any OS or dependency issues. [Here are
> instructions](https://github.com/DataDog/hiring-engineers/blob/solutions-engineer/README.md#vagrant)
> for setting up a Vagrant Ubuntu 12.04 VM.
> * You can utilize a Containerized approach with Docker for Linux and our dockerized Datadog Agent image.
> 
> Then, sign up for Datadog (use “Datadog Recruiting Candidate” in the
> “Company” field), get the Agent reporting metrics from your local
> machine.

**[Pejman]**: The chosen environnement is a Ubuntu 16.04 VM running on top of VMWare Fusion. Given some driver conflicts on my Mac between VirtualBox and VMWare, I couldn't actually use Vagrant. 
That said one can always use Vagrant with VMware, but in that case a specific provider needs to be used.  

***Agent installation steps:***

![](https://github.com/ptabasso2/hiring-engineers/blob/solutions-engineer/images/Agent%20Install%201.png)

![](https://github.com/ptabasso2/hiring-engineers/blob/solutions-engineer/images/Agent%20Install%202.png)

The agent is now up and running:

![](https://github.com/ptabasso2/hiring-engineers/blob/solutions-engineer/images/Agent%20running.png)

![](https://github.com/ptabasso2/hiring-engineers/blob/solutions-engineer/images/Datadog%20agent%20status.png)


## Collecting Metrics:

> * Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

**[Pejman]**: Adding tag can be done by updatding the agent config file datadog.yaml

![](https://github.com/ptabasso2/hiring-engineers/blob/solutions-engineer/images/Tag%20configuration.png)
 
![](https://github.com/ptabasso2/hiring-engineers/blob/solutions-engineer/images/Tags.png)


> * Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

**[Pejman]**: I actually chose to install a PostgreSQL database.  This DB is used along with a Web application based on a JEE implementation based on the following stack: Struts/Spring MVC on Tomcat, JPA/Hibernate, PostgreSQL. 

As per the PostgreSQL integration documentation:

![](https://github.com/ptabasso2/hiring-engineers/blob/solutions-engineer/images/Postgres%20Integration.png)

Here the PostgreSQL configuration file:

[postgres.yaml](https://github.com/ptabasso2/hiring-engineers/blob/solutions-engineer/config/postgres.yaml)

> * Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

**[Pejman]**: As per the documentation, let's create an agent check that will report the requested value: 

https://docs.datadoghq.com/agent/agent_checks/#your-first-check

I can create the custom agent check.

Here are the basic components used to create the agent check:

 1. ***Create*** a directory **pejcustomcheck.d** under `/etc/datadog-agent/conf.d`
 2. ***Create*** a configuration file named **pejcustomcheck.yaml** placed in the directory we've just created. This file contains the default structure below. We will not change anything for now.

```python
init_config:

instances:
    [{}]
```

 3. ***Create*** the following python script placed under `/etc/datadog-agent/checks.d` - [pejcustomcheck.py](https://github.com/ptabasso2/hiring-engineers/blob/solutions-engineer/scripts/pejcustomcheck.py)

***Remark***: Please note that these are different directories! `checks.d` vs  `conf.d`...

```python
import random
from checks import AgentCheck
class HelloCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', random.randint(0,1000))
```

All seems to be working as expected

![check status](https://github.com/ptabasso2/hiring-engineers/blob/solutions-engineer/images/Check%20status.png)

After a couple of minutes we can observe the metric with the expected behavior (variations between 0 and 1000).

![](https://github.com/ptabasso2/hiring-engineers/blob/solutions-engineer/images/my_metric%201.png)


> * Change your check's collection interval so that it only submits the metric once every 45 seconds.

The collection interval can be further changed by modifying the configuration file using the `min_collection_interval` property.

Now the custom agent check config looks like this

```python
init_config:

instances:
    - min_collection_interval: 45
```

***Resolution before config change***:

![](https://github.com/ptabasso2/hiring-engineers/blob/solutions-engineer/images/Before%20config%20change.png) 

Here the interval (time) between two datapoints is **15s**   

***Resolution after config change:***

![](https://github.com/ptabasso2/hiring-engineers/blob/solutions-engineer/images/After%20config%20change.png)

Now the interval is **45s** 

* **Bonus Question** Can you change the collection interval without modifying the Python check file you created?

**[Pejman]** Yes. As per the documentation ([Collection interval configuration](https://docs.datadoghq.com/agent/agent_checks/#configuration)), the collection interval can be controlled either globally (in the init_config section) or at the instance level (instances section). 
In my case it has been configured at the instance level without having to change the python script.   



## Visualizing Data:

> Utilize the Datadog API to create a Timeboard that contains:
> 
> * Your custom metric scoped over your host.
> * Any metric from the Integration on your Database with the anomaly function applied.
> * Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
> 
> Please be sure, when submitting your hiring challenge, to include the
> script that you've used to create this Timemboard.

**[Pejman]**: 
The workflow is as follows:

 1. ***First off***, we need to set the app key first in order to use the Datadog API.
This can be set at the following address:
[API & App keys](https://app.datadoghq.com/account/settings#api)
 2. ***Then*** we need to create a timeboard through the API. I started using the example given in the API ref guide showing how to produce a timeboard. [Create a timeboard through the DG API](https://docs.datadoghq.com/api/?lang=bash#timeboards)
 3. ***Now*** we need to add multiple graphs in the list:
we will use the **graphs** data structure that is a list of objects. Each individual object being a graph

```python
"graphs" : [{graph1},{graph2}, ...]
```

***Ex:***
```python
"graphs" : [{
          "title": "Network Bytes Sent",
          "definition": {
              "events": [],
              "requests": [
                  {"q": "avg:system.net.bytes_sent{*}"}
              ]
          },
          "viz": "timeseries"
      },{
          "title": "Average CPU User",
          "definition": {
              "events": [],
              "requests": [
                  {"q": "avg:system.cpu.user{*}"}
              ]
          },
          "viz": "timeseries"
      },
```

 4. I'm using curl along with Postman to perform these operations. But it can simply be written in Python, Java or any other language.
  
Below each of the widget definitions. The dashboard creation wizard has been used to generate the corresponding JSON.
  
***Custom metric scoped over my host***:
```json
{
          "title": "Custom metric scoped on pej",
          "definition": {
              "events": [],
              "requests": [
                  {"q": "avg:my_metric{host:pej}"}
              ]
          },
          "viz": "timeseries"
}
```
***Any metric from the Integration on your Database with the anomaly function applied***

```json
{
    "definition": {
        "events": [],
  "requests": [
    {
      "q": "anomalies(sum:postgresql.locks{host:pej}, 'basic', 2)",
      "type": "line",
      "style": {
        "palette": "dog_classic",
        "type": "solid",
        "width": "normal"
      },
      "conditional_formats": [],
      "aggregator": "avg"
    }
  ],
  "viz": "timeseries"
},
"title": "Anomalies for PostgreSQL locks"
}
```

***Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket***

```json
{
          "title": "Custom Metric rolled up",
          "definition": {
              "events": [],
              "requests": [
                  {
                   "q": "sum:my_metric{host:pej}.rollup(sum, 3600)",
                   "type": "bars",
                   "style": {
                       "palette": "dog_classic",
                       "type": "solid",
                       "width": "normal"
      },
      "conditional_formats": [],
      "aggregator": "avg"
    }
              ]
          },
          "viz": "timeseries"
}
```


I've also included additional graphs related to CPU & network utilization.

The result is as follows:

![](https://github.com/ptabasso2/hiring-engineers/blob/solutions-engineer/images/Timeboard%202.png)


The final curl command is available here:

[curl](https://github.com/ptabasso2/hiring-engineers/blob/solutions-engineer/scripts/curl)


Once this is created, access the Dashboard from your Dashboard List in the UI:

> * Set the Timeboard's timeframe to the past 5 minutes
> * Take a snapshot of this graph and use the @ notation to send it to yourself.

***Snapshot creation***
![](https://github.com/ptabasso2/hiring-engineers/blob/solutions-engineer/images/past%205%20min%20with%20annot.png)

***Email received***
![](https://github.com/ptabasso2/hiring-engineers/blob/solutions-engineer/images/email%20with%20anomaly%20within%205%20min.png)


> * **Bonus Question**: What is the Anomaly graph displaying?

**[Pejman]** The purpose of the anomaly function is to determine the normal range of values a given metric should be in. It helps understanding if there are deviations and if so it may be used to alert in case the values are out of the range.  
In the image below, we see that a little before 15h57 the avg number of locks is slightly higher (3) than what is expected under normal conditions (2,2).
For production systems, it is highly recommended to let the system collect information on a longer period (hours, days, weeks) to have more accurate data.


## Monitoring Data

> Since you’ve already caught your test metric going above 800 once, you
> don’t want to have to continually watch this dashboard to be alerted
> when it goes above 800 again. So let’s make life easier by creating a
> monitor.
> 
> Create a new Metric Monitor that watches the average of your custom
> metric (my_metric) and will alert if it’s above the following values
> over the past 5 minutes:
> 
> * Warning threshold of 500
> * Alerting threshold of 800
> * And also ensure that it will notify you if there is No Data for this query over the past 10m.

**[Pejman]**

In order to view the metric and compare it against the requested thresholds, we will create a new monitor as follows:

![](https://github.com/ptabasso2/hiring-engineers/blob/solutions-engineer/images/Monitor%201.png)

![](https://github.com/ptabasso2/hiring-engineers/blob/solutions-engineer/images/Monitor%202.png)

> Please configure the monitor’s message so that it will:
> 
> * Send you an email whenever the monitor triggers.
> * Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
> * Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
> * When this monitor sends you an email notification, take a screenshot of the email that it sends you.

**[Pejman]** Below example of email notification received upon the various states (Alert, Warning, No data)

***Alert state (800)*** 

my_metric > 800

![](https://github.com/ptabasso2/hiring-engineers/blob/solutions-engineer/images/Alert%20state.png)

***Warning state (500)***

my_metric ranging between 500 et 799 

![](https://github.com/ptabasso2/hiring-engineers/blob/solutions-engineer/images/Warning%20state.png)

***No data state***

![](https://github.com/ptabasso2/hiring-engineers/blob/solutions-engineer/images/No%20data%20state.png)


> * **Bonus Question**: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office.
> Set up two scheduled downtimes for this monitor:
> 
>     * One that silences it from 7pm to 9am daily on M-F,
>     * And one that silences it all day on Sat-Sun.
>     * Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

**[Pejman]** In order to exclude alerts over a specific time window, we will set up two scheduled downtimes for this monitor:

***One that silences it from 7pm to 9am daily on M-F***

![](https://github.com/ptabasso2/hiring-engineers/blob/solutions-engineer/images/Downtime%20on%20weekdays.png)

***And one that silences it all day on Sat-Sun.***

![](https://github.com/ptabasso2/hiring-engineers/blob/solutions-engineer/images/Downtime%20on%20sundays.png)

***Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification***

![](https://github.com/ptabasso2/hiring-engineers/blob/solutions-engineer/images/Downtime%20on%20weekdays%20notification.png)


## Collecting APM Data:

Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:

```
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
    app.run()
```    

> * **Note**: Using both ddtrace-run and manually inserting the Middleware has been known to cause issues. Please only use one or the
> other.
> 

**[Pejman]** 
The above application has been used to perform some basic tests using Datadog APM.  

The following steps have been taken:

1. Install flask: pip install flask ddtrace
2. save the above python code in `/opt/apps/my_flaskapp.py` 
3. `export FLASK_APP=/opt/apps/my_flaskapp.py`
4. `ddtrace-run python -m flask run --port=9090`
5. generating some load on `/`, `/api/trace`, `/api/apm*`

> * **Bonus Question**: What is the difference between a Service and a Resource?

**[Pejman]** 

***Service***
A  component or a process that perform a set of tasks which can be categorized by type of content. Ex Web server, App Server or DB server. This 3 services may be used to service user requests through a web application.

***Resource***
A resource is a particular action for a service
  ***For a web application***: some examples might be a canonical URL, such as  `/user/home`  or a handler function like  `web.user.home`  (often referred to as “routes” in MVC frameworks).
 ***For a SQL database***: a resource is the query itself, such as  `SELECT * FROM users WHERE id = ?`.
 

> Provide a link and a screenshot of a Dashboard with both APM and
> Infrastructure Metrics.

Link
[APM & Infra metrics](https://app.datadoghq.com/dash/810574/pejmans-timeboard-14-may-2018-1848?live=true&page=0&is_auto=false&from_ts=1526313868198&to_ts=1526317468198&tile_size=m)

Screenshot
![]()

Please include your fully instrumented app in your submission, as well. 

## Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?

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
* [Datadog overview](http://docs.datadoghq.com/overview/)
* [Guide to graphing in Datadog](http://docs.datadoghq.com/graphing/)
* [Guide to monitoring in Datadog](http://docs.datadoghq.com/guides/monitoring/)

### The Datadog Agent and Metrics

* [Guide to the Agent](http://docs.datadoghq.com/guides/basic_agent_usage/)
* [Datadog Docker-image repo](https://hub.docker.com/r/datadog/docker-dd-agent/)
* [Writing an Agent check](http://docs.datadoghq.com/guides/agent_checks/)
* [Datadog API](https://docs.datadoghq.com/api/)

### APM
* [Datadog Tracing Docs](https://docs.datadoghq.com/tracing)
* [Flask Introduction](http://flask.pocoo.org/docs/0.12/quickstart/)

### Vagrant
 * [Setting Up Vagrant](https://www.vagrantup.com/intro/getting-started/)

### Other questions:

* [Datadog Help Center](https://help.datadoghq.com/hc/en-us)





