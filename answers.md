# 1. Collecting Metrics
## Add tags in the Agent config file:
Edited /etc/datadog-agent/datadog.yaml to add the metrics
```yaml
tags:
   - location:vagrant-local
   - env:dev
   - role:database
  ``` 
**Host Map Screenshot** 

<img src=images/01_host_map_tags.png width=600>


## Install a database and its respective Datadog integration

Installed MySQL 5.7 and created a user with required GRANTs as per instructions [here](https://docs.datadoghq.com/integrations/mysql/)

Now Host Map shows mysql on the host apps:
<img src=images/01_host_map_mysql_integration.png width=600>

And I can see the MySQL Dashboard on my Datadog account
<img src=images/01_mysql_dashboard.png width=600>

***Tip:*** `sudo datadog-agent status` was very useful to troubleshoot configuration file errors

    Config Errors
    ==============
       mysql
       -----
        Configuration file contains no valid instances

After fixing copy-paste indentation errors... (and disabling extra_performance_metrics) 

    Collector
    =========
    
    Running Checks
    ==============
    
    mysql (1.7.0)
    -------------
      Instance ID: mysql:741a51f77d94ba1c [OK]
      Total Runs: 1
      Metric Samples: Last Run: 163, Total: 163
      Events: Last Run: 0, Total: 0
      Service Checks: Last Run: 1, Total: 1
      Average Execution Time : 43ms

## Create a custom agent check that submits a metric named my_metric with a random value between 0 and 1000

* Followed instructions [here](https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6) to create a custom agent
* Created `custom_my_metric.py` under `/etc/datadog-agent/checks.d/custom_my_metric.py` (as per documentation, prefixing the check with custom_ in order to avoid conflict with the name of a preexisting Datadog Agent integrations).
  ```python
  # the following try/except block will make the custom check compatible with   any Agent version
  try:
      # first, try to import the base class from old versions of the Agent...
      from checks import AgentCheck
  except ImportError:
      # ...if the above failed, the check is running in Agent version 6 or later
      from datadog_checks.checks import AgentCheck
  
  import random
  
  # content of the special variable __version__ will be shown in the Agent   status page
  __version__ = "1.0.0"
  
  
  class MyMetricCheck(AgentCheck):
      def check(self, instance):
          self.gauge('my_metric', random.randint(1,1000))
  ```
* Created `/etc/datadog-agent/conf.d/custom_my_metric.yaml`
  ```yaml
  Instances: [{}]
  ```
* Restarted the datadog agent to pick up the custom metric. 
  ```
     custom_my_metric (1.0.0)
    ------------------------
      Instance ID: custom_my_metric:d884b5186b651429 [OK]
      Total Runs: 52
      Metric Samples: Last Run: 1, Total: 52
      Events: Last Run: 0, Total: 0
      Service Checks: Last Run: 0, Total: 0
      Average Execution Time : 0s
  ```

  Screenshots:
  <img src=images/01_custom_my_metric.png width=600>

* By default the collection interval is 15 seconds. We can change that to 45 seconds by editing the `/etc/datadog-agent/conf.d/custom_my_metric.yaml` and adding `min_collection_interval`
  ```
   init_config:
    
   instances:
     - min_collection_interval: 45
  ```
* Restart the datadog agent to pick up the new configuration and now the metric is published every 45 seconds. [Metric](https://app.datadoghq.com/graph/embed?token=8a064cd8a111549f3995714efc4f9e958218e050ef3c6b245ec5546e81932973&height=300&width=600&legend=true)

   <img src=images/01_custom_metric_45_sec.png width=600>

### Dashboard
Created a Screenboard with some of the metrics [here](https://p.datadoghq.com/sb/gc2f3rf7u99g8xc8-5e803f2fae4a35f18f360c81265f313c)

* **Bonus Question:** Can you change the collection interval without modifying the Python check file you created?
   Yes, using min_collection_interval on the conf.d YAML file for the metric

# 2. Visualizing data

Utilize the Datadog API to create a Timeboard that contains:
* Your custom metric scoped over your host.
* Any metric from the Integration on your Database with the anomaly function applied.
* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

Once this is created, access the Dashboard from your Dashboard List in the UI:

* Set the Timeboard's timeframe to the past 5 minutes
* Take a snapshot of this graph and use the @ notation to send it to yourself.

**Solution:**
Reviewed the API documentation [here](https://docs.datadoghq.com/api/?lang=python#overview)

Python code used to complete this exercise can be found under `code/create_timeboard.py`

**NOTE:** I had to manually install datadogpy from [source](https://github.com/DataDog/datadogpy) to be able to use the api.Dashboard module, as the version installed from pip doesn't seem to be the same even though both versions are shown as 0.26.0: ```AttributeError: module 'datadog.api' has no attribute 'Dashboard'```

***Note2: I didn't dive deeper on this issue*** 

**Graphs:**
* 1h-rollup function graph for my_metric:
   <img src=images/01_my_metric_rollup_function.png width=600>

* API-created dashboard 
   <img src=images/02_api_created_dashboard.png width=600>

* 5-min scoped dashboard 
   <img src=images/02_api_created_dashboard.png width=600>

* Graph snapshot sent over e-mail:
   <img src=images/02_email_snapshot.png width=600>

* **Bonus question:** What is the Anomaly graph displaying?
  It shows a range of values that are expected for the metric based on past behavior and trends and trends. Datadog provides three anomaly detection algorithms depending on the nature of the metric:
  ** Basic: for metrics that have no repeating seasonal pattern.
  ** Agile: for seasonal metrics when you want the algorithm to quickly adjust to level shifts in the metric
  ** Robust: for seasonal metrics where you expect the metric to be stable and want to consider slow level shifts as anomalies

  Further info can be found [here](https://docs.datadoghq.com/monitors/monitor_types/anomaly/)

# 3. Monitoring data

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

**Email Notification:**
<img src=images/03_my_metric_warning.png width=600>

* **Bonus Question**: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

  * One that silences it from 7pm to 9am daily on M-F,
  * And one that silences it all day on Sat-Sun.
  * Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

**Weekdays out of office downtime**
You need to add Sundays to the periodicity of the downtime, otherwise I'd be alerted on during Monday's AM before 9AM. There might be a better way to schedule this without overlapping downtimes... 

<img src=images/03_weekdays_downtime.png width=600>

**Weekends downtime**
I couldn't find a way to start a downtime from a previous day/time, which doesn't let you configure a recurrent downtime that would have already started during your current time... I had to start this downtime schedule to start next weekend. There might be another way to do this.

<img src=images/03_weekends_out_of_office_downtime.png width=600>

I created a one-time downtime for the rest of the weekend, and received the corresponding e-mail.

<img src=images/03_email_downtime_notification/png width=600>

# 4. Collecting APM Data:

Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution.

* **Note**: Using both ddtrace-run and manually inserting the Middleware has been known to cause issues. Please only use one or the other.

**Solution:**

First, I configured the datadog agent to enable trace collection. As per instructions [here](https://docs.datadoghq.com/agent/apm/?tab=agent630#agent-configuration), edited `/etc/datadog-agent/datadog.yaml` and uncommented the `apm_config` section:
      
```yaml
apm_config:
    enabled: true
``` 

Read blog post about Flask monitoring with datadog [here](https://www.datadoghq.com/blog/monitoring-flask-apps-with-datadog/)

Installed ddtrace with pip and tested automated instrumentation with ddtrace-run 
```bash
$ pip install ddtrace
$ FLASK_APP=flask_app.py DATADOG_ENV=test ddtrace-riun flask run --port 5050
```

I had a look at flask ddtrace integrations [here](http://pypi.datadoghq.com/trace/docs/web_integrations.html#flask) and defined a custom service name for my flask application as well as added error reporing for 404 responses.

```pyhthon
from ddtrace import config, patch_all,tracer
config.flask['service_name'] = "my_datadog_instrumented_flask_app"

# Report 404 responses as error
config.flask['extra_error_codes'] = [404]
patch_all()
```

After this, I added my service to analyzed_spans in the `/etc/datadog-agent/datadog.yaml` configuration file:

```yaml
apm_config:
   enabled: true
   analyzed_spans:
      my_datadog_instrumented_flask_app|flask.request: 1
```

Inspired by the sample code [here](https://gist.githubusercontent.com/davidmlentz/4538db971af0e1d69a7936f4f8046122/raw/4a238f1c74d0f5f5ee2dd40a92b81f4176493c8c/apm_test_flask_custom.py) provided on the blog post, I added an additional endpoint to the flask API that queries an external API to get random text as well as sleeps for 10 msec and added custom instrumentation. 

Using the tracer.wrap() function I instrumented the sleep function using 'sleep_function' as name and the `get_random_text()` function as a service and resource name 'get_random_text'

```python
# sleep for 10 msec
@tracer.wrap(name='sleep_function')
def sleep_function():
    time.sleep(0.01)
    return True

# get random text from randomtext.me
@tracer.wrap(name='get_random_text',service='randomtext.me')
def get_random_text():
    r = requests.get('http://www.randomtext.me/api/')
    j = json.loads(r.text)
    return j['text_out']
```

I also added the newly defined service and resource to the datadog configuration file to enable trace search

```yaml
apm_config:
   enabled: true
   analyzed_spans:
      my_datadog_instrumented_flask_app|flask.request: 1
      my_datadog_instrumented_flask_app|sleep_function: 1
      randomtext.me|get_random_text: 1
``` 

* **Bonus Question**: What is the difference between a Service and a Resource?
  A Service is a set of processeses providing a specific functionality, like a web application, or a database, while a resource is a particular action for a service: for a web application it could be a request, while for a database it could be a query. 

Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

**[Dashboad](https://p.datadoghq.com/sb/gc2f3rf7u99g8xc8-d720339b85cbfc7a1ca807907fd65377)**

**Screenshot**

<img src=images/04_dashboard_infra_and_apm.png width=600>

Please include your fully instrumented app in your submission, as well.

***The full instrumented app can be found under [`code/flask_app.py`](/code/flask_app.py)***

# 5. Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?

Similar to the bathroom availability example, meeting rooms in offices are an scarse resource and is often time consuming and frustrating to check if there are meeting rooms available, and if any of the booked meeting rooms is actually not in use. With sensors on the meeting rooms and programmatic access to the booking system (Exchange? Google Mail? put_here_your_service_name) it could be awesome to build a dashboard showing available meeting rooms per floor as well as booked meeting rooms not in use/empty.

In a general perspective, I believe any company using datadog should feed near-real-time business and/or functional metrics related to the applications and systems monitored to Datadog, so they can be looked at together with system and application metrics and detect issues/behaviors that won't show up on pure system/app metrics. 