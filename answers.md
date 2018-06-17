## Prerequisites - Setup the environment

You can utilize any OS/host that you would like to complete this exercise.
I decided to skip the Vagrant and Containerized approaches and decided to accept the challenge of getting the exercise done on macOS 10.13.14. Other than some minor compatibility issues, the installation was mostly straightforward.

* Then, sign up for Datadog (use “Datadog Recruiting Candidate” in the “Company” field), get the Agent reporting metrics from your local machine.

The initial installation steps for Mac were very straightforward: https://app.datadoghq.com/account/settings#agent/mac

![Agent](/1_agent_installation.png)

I was then taken to the [host page](https://app.datadoghq.com/infrastructure/map?host=498328944&fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=availability-zone&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=true&palette=green_to_orange&paletteflip=false&node_type=host).

The agent appeared to be in order when i ran a quick health check:

```
Joes-MacBook-Pro:~ joeplonsker$ datadog-agent health
Agent health: PASS
=== 10 healthy components ===
ad-autoconfig, ad-configresolver, aggregator, collector-queue, dogstatsd-main, forwarder, healthcheck, metadata-agent_checks, metadata-host, tagger
```


##Collecting Metrics:
===========================
* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

Typically, the yaml file is located in `~/.datadog-agent/datadog.yaml`. However my file was located in typically where things are located if you're working with the source code: `~/opt/datadog-agent/etc/datadog.yaml`. This was unexpected as I was certain that this yaml file would be generated automatically in directory noted [here](https://help.datadoghq.com/hc/en-us/articles/203037169-Where-is-the-configuration-file-for-the-Agent-). What mattered though at this point was seeing whether the tags added to the yaml would show up in the host page.

* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
* Change your check's collection interval so that it only submits the metric once every 45 seconds.
* **Bonus Question** Can you change the collection interval without modifying the Python check file you created?

I went ahead and made sure my API key was present and [enabled some tags](https://docs.datadoghq.com/getting_started/tagging/assigning_tags/#assigning-tags-using-the-configuration-files) that, if surfaced, would appear to have been clearly made by me.
```
tags:
  - mytag
  - env:prod
  - role:database
  - user:joe
  - animal:dog
  ```

And voila, these tags were surfaced on the hosts page as coming from my local machine.

![Live Hosts](/2_live_hosts.png)

* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

Here's where I encountered some issues with MySQL. First, my machine refused to grant universal permissions to the new 'datadog'@'localhost' user. I even tried specifying every unique MySQL action to the new user, but to no avail. It did not dawn on me what the issue was until I fired up a second terminal window with MySQL as `mysql -u root -p`. At root I was able to grant all permissions This felt like the MySQL troubleshooting equivalent of 'did you try turning it on and off again'.

With the new user created, I went to add the configuration block to the mysql.d/conf.yaml file.

```instances:
    # NOTE: Even if the server name is "localhost", the agent will connect to MySQL using TCP/IP, unless you also
    # provide a value for the sock key (below).
    - server: 127.0.0.1
      user: datadog
      pass: 'supersecurepassword'
      port: 3306
      options:
          replication: 0
          galera_cluster: 1
          extra_status_metrics: true
          extra_innodb_metrics: true
          extra_performance_metrics: true
          schema_size_metrics: false
          disable_innodb_metrics: false
```
* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

I then followed the instructions [in the Agent check documentation](https://docs.datadoghq.com/developers/agent_checks/) and made the custom metric at `opt/datadog-agent/etc/checks.d/my_metric.py` and a simple config file at `/opt/datadog-agent/etc/conf.d/my_metric.yaml`.

config:
```
init_config:

instances:
    [{}]
```


my_metric.py:

```
from checks import AgentCheck
import random

class HelloCheck(AgentCheck):
    def check(self, instance):
        metric_num = random.randint(0, 1000)
        self.gauge('my_metric', metric_num)

```

Running the agent check resulted in a successful response.


```
Joes-MacBook-Pro:checks.d joeplonsker$ datadog-agent check my_metric
=== Series ===
{
  "series": [
    {
      "metric": "my_metric",
      "points": [
        [
          1529094578,
          433
        ]
      ],
      "tags": null,
      "host": "Joes-MacBook-Pro.local",
      "type": "gauge",
      "interval": 0,
      "source_type_name": "System"
    }
  ]
}
=========
Collector
=========

  Running Checks
  ==============
    my_metric
    ---------
      Total Runs: 1
      Metrics: 1, Total Metrics: 1
      Events: 0, Total Events: 0
      Service Checks: 0, Total Service Checks: 0
      Average Execution Time : 0ms
```

* Change your check's collection interval so that it only submits the metric once every 45 seconds.
* **Bonus Question** Can you change the collection interval without modifying the Python check file you created?

I attempted to change the collection interval by using the Python time module in the file. I saw no specific change in the agent check, so decided to check if there was an alternative in the [Configuration documentation](https://docs.datadoghq.com/developers/agent_checks/#directory-structure). I found a min_collection_interval option in an example and updated my yaml file to reflect it, essentially addressing the bonus question of not changing the original Python file:

```
init_config:

instances:
    - username: 'datadog'
      password: 'supersecurepassword'
      min_collection_interval: 45
```

Output was unaffected:

```
Joes-MacBook-Pro:checks.d joeplonsker$ datadog-agent check my_metric
=== Series ===
{
  "series": [
    {
      "metric": "my_metric",
      "points": [
        [
          1529095297,
          201
        ]
      ],
      "tags": null,
      "host": "Joes-MacBook-Pro.local",
      "type": "gauge",
      "interval": 0,
      "source_type_name": "System"
    }
  ]
}
=========
Collector
=========

  Running Checks
  ==============
    my_metric
    ---------
      Total Runs: 1
      Metrics: 1, Total Metrics: 1
      Events: 0, Total Events: 0
      Service Checks: 0, Total Service Checks: 0
      Average Execution Time : 0ms
```

##Visualizing Data:
===============================

* Utilize the Datadog API to create a Timeboard that contains:
* Your custom metric scoped over your host.
* Any metric from the Integration on your Database with the anomaly function applied.
* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

This timeboard was created by making a POST request via Postman, as this was a platform I had used several times in the past to generate requests when using APIs. I followed the instructions listed [here](https://help.datadoghq.com/hc/en-us/articles/115002182863-Using-Postman-With-Datadog-APIs) for the most part, however I kept receiving errors that my API key was required, even after importing the Datadog Postman Collection and updating all required keys. Unfortunately it turned out that I needed to use a deprecated version (> version 6.0) to successfully make the calls. I headed over to the [Postman Changelog](https://www.getpostman.com/apps#changelog), copied the download link for the latest version, and then changed the version number in the URL to download a deprecated verison of Postman. I was then able to successfully make API calls and create a Timeboard:


```
{"graphs" : [{
	"title": "my_metric timeboard",
	"description": "created through the API",
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:system.mem.free{*}"},
            {"q": "my_metric{host:Joes-MacBook-Pro.local}"}
        ]
    },
    "viz": "timeseries"

		},
    {
    "title": "my_metric rollup",
      "definition": {
        "events":[],
        "requests": [
          {"q": "sum:my_metric{host:Joes-MacBook-Pro.local}.rollup(avg,3600)"}
        ]
    }
  },
    {
    "title": "DB Anomalies",
       "definition": {
         "events":[],
         "requests": [
          {"q": "anomalies(mysql.performance.open_files{host:Joes-MacBook-Pro.local}, 'basic', 3)"}
        ]
      },
      "viz": "timeseries"
    }
 ],
	"title" : "Joe Timeboards",
      "description" : "Tracking my_metric in the MySQL DB on my comp",
      "template_variables": [{
          "name": "host1",
          "prefix": "host",
          "default": "host:my-host"
      }],
      "read_only": "True"
}
```

This call broke several times before I realized I was including Python modules from examples listed in the documentation. I eventually dropped the code in JSHint to make this into a JSON-structured blob.

For the anomalies component, I went with the `mysql.performance.open_files` on my machine to check the number of open files.

I then used the rollup function to sum up all the point from the last hour:

`sum:my_metric{host:Joes-MacBook-Pro.local}.rollup(avg,3600)`

Originally I wrote the average as 60, but then realized it needs to be 3600 since this is in JavaScript.

Here is the final timeboard:

![Timeboard](timeboard.png)

* Once this is created, access the Dashboard from your Dashboard List in the UI:

* Set the Timeboard's timeframe to the past 5 minutes
* Take a snapshot of this graph and use the @ notation to send it to yourself.

While unable to break it change the timeframe to the past five minutes through the UI, I was able to use the snapshot tool to email myself a note.
![Joe Email Snapshot](/joe_email_snapshot.jpeg)>still on phone
![Joe Snapshot](/joe_snapshot.png)


* **Bonus Question**: What is the Anomaly graph displaying?

According to the Datadog blog, the anomaly graph is depicting the typical bounds of expected deviation versus the actual captured data over a series of time. The anomaly I put in was fairly benign, with a steady amount of four connections to my MySQL server. The following gif depicts a much more realistic capture of data:

![anomaly graph example](https://datadog-prod.imgix.net/img/blog/introducing-anomaly-detection-datadog/tolerance.gif?fit=max)

If data begins to deviate from that expected pattern

##Monitoring Data

* Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:
* Warning threshold of 500
* Alerting threshold of 800
* And also ensure that it will notify you if there is No Data for this query over the past 10m.

I found out the specifics of what a metric monitor was [here in the documentation](https://docs.datadoghq.com/monitors/monitor_types/metric/) and then set one up [here on the monitors page](https://app.datadoghq.com/monitors/manage). I went ahead and selected metric as my option and created monitors for a warning threshold of 500, an alerting threshold of 800, and an alert if there is no data for 10 minutes.

![metric monitors](/metric_monitor.png)


>Please configure the monitor’s message so that it will:

>Send you an email whenever the monitor triggers.

![Joe as incident commander](/joe_email_monitor.png)

>Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.

I used the message template variables provided to create specific and targeted messages based on the nature of the alert:

```
{{#is_warning}}Heads up, my_metric on {{host.name}} is hitting its warning threshold: {{value}} [~approx 5 mins ago].{{/is_warning}}

{{#is_alert}}Heads up, my_metric on {{host.name}} is hitting its alert threshold: {{value}} [~approx 5 mins ago].{{/is_alert}}

{{#is_no_data}} Heads up, data has been missing for my_metric on {{host.name}} for the last 10 minutes.{{/is_no_data}} @joe@plonsker.com
```

These messages were then emailed to me when triggered:

![Joe monitor messages](/joe_monitor_messages.png)
![Joe Email Monitor](/joe_email_monitor.png)
![Alert email 1](/alert_email_1.png)<
![Alert email 2](/alert_email_1.png)<



Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

Ah, the joys of going off-call. I set up the specified alerts via the [scheduled downtime page](https://app.datadoghq.com/monitors#/downtime).

>One that silences it from 7pm to 9am daily on M-F:

![downtime_1](/downtime_1.png)

>And one that silences it all day on Sat-Sun.

![downtime_2](/downtime_2.png)

>Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

![scheduled_downtime_1](/scheduled_downtime_1.png)
![scheduled_downtime_2](/scheduled_downtime_2.png)


##Collecting APM Data:

* Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:
Due to some updates in Java 8 where the apt endpoint was deprecated, I had trouble getting the Go command to be recognized on my machine. The commands specified in the [APM guide](https://docs.datadoghq.com/tracing/setup/) and [the trace agent repo](https://github.com/DataDog/datadog-trace-agent) would not work for me, and even a fresh installation of Go would not get the commands to be recognized. Eventually I edited my bash profile and set Go in my path according to [this question asked on superuser.com](https://superuser.com/questions/472018/bash-cant-find-go-exectuable-after-installing-go-package-for-os-x?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa).

Eventually the commands of `go get -u github.com/DataDog/datadog-trace-agent/...`, `cd $GOPATH/src/github.com/DataDog/datadog-trace-agent`, `make install`, and `trace-agent --config /etc/dd-agent/datadog.yaml` got it up and running.

```trace-agent --config ~/.datadog-agent/datadog.yaml
2018-06-14 22:23:08 INFO (trace_writer.go:49) - Trace writer initializing with config: {MaxSpansPerPayload:1000 FlushPeriod:5s UpdateInfoPeriod:1m0s SenderConfig:{MaxAge:20m0s MaxQueuedBytes:67108864 MaxQueuedPayloads:-1 ExponentialBackoff:{MaxDuration:2m0s GrowthBase:2 Base:200ms}}}
2018-06-14 22:23:08 INFO (stats_writer.go:42) - Stats writer initializing with config: {MaxEntriesPerPayload:12000 UpdateInfoPeriod:1m0s SenderConfig:{MaxAge:20m0s MaxQueuedBytes:67108864 MaxQueuedPayloads:-1 ExponentialBackoff:{MaxDuration:2m0s GrowthBase:2 Base:200ms}}}
2018-06-14 22:23:08 INFO (service_writer.go:31) - Service writer initializing with config: {FlushPeriod:5s UpdateInfoPeriod:1m0s SenderConfig:{MaxAge:20m0s MaxQueuedBytes:67108864 MaxQueuedPayloads:-1 ExponentialBackoff:{MaxDuration:2m0s GrowthBase:2 Base:200ms}}}
2018-06-14 22:23:08 INFO (main.go:216) - trace-agent running on host Joes-MacBook-Pro.local
2018-06-14 22:23:08 INFO (receiver.go:142) - listening for traces at http://localhost:8126
2018-06-14 22:23:18 INFO (receiver.go:325) - no data received
2018-06-14 22:24:08 INFO (service_mapper.go:59) - total number of tracked services: 0
....
```

![trace_agen_1.png](/trace_agent_1.png)
![trace_agen_2.png](/trace_agent_2.png)

Afterwards I got to tracing my Python app, running `pip install ddtrace` and then importing the tracer in the app.

```

from flask import Flask
import logging
import sys
from ddtrace import tracer

with tracer.trace("web.request", service="my_service") as span:
  span.set_tag("my_tag", "my_value")

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

My humble Python app was very responsive once I ran it:

```
Joes-MacBook-Pro:Documents joeplonsker$ python myapp.py
2018-06-14 23:13:55,795 - werkzeug - INFO -  * Running on http://0.0.0.0:5050/ (Press CTRL+C to quit)
2018-06-14 23:13:56,629 - ddtrace.api - DEBUG - reported 1 traces in 0.00295s
```

Bonus Question: What is the difference between a Service and a Resource?

A service is [a set of processes that work together to provide a feature set](https://help.datadoghq.com/hc/en-us/articles/115000702546-What-is-the-Difference-Between-Type-Service-Resource-and-Name). Essentially, a service is the overall skeleton of an app, containing the parts and basic framework of how it will operate. On the other hand, a resource on the is a particular query to a service. An example of this would be a canonical URL or endpoint that a user hits when trying to get data from a service.

Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

[Link to Dashboard](https://app.datadoghq.com/dash/836105/joes-timeboard-14-jun-2018-2312?live=true&page=0&is_auto=false&from_ts=1529104584269&to_ts=1529108184269&tile_size=m)
![APM monitor](/apm_monitor.png)
Your answers to the questions go here.
