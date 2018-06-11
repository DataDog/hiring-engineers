# Answers
To complete this excercise, I used Mac OS X with agent 6. All instructions and issues are related to this specific set up.
## Collecting Metrics

- Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog:

  I added tags to the config file at `~/.datadog-agent/datadog.yaml`, here is a code snippet from the file:
  ```yaml
  tags: env:dev, role:database, region:east
  ```
  Here is a screenshot of what it looks like on the host map:
  ![tags screenshot](/screenshots/datadog_host_tags.png)

- Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

  I used PostgreSQL for this step. Following the instructions on integrations with Postgres. I edited the tags in the config file for postgres at `~/.datadog-agent/conf.d/postgres.d/conf.yaml`. It looks something like this:
  ```yaml
  init_config:

  instances:
  - host: localhost
    port: 5432
    username: datadog
    password: "{{ generated_password }}"
    tags:
      - local
      - test
  ```

  A screenshot of its successful installation:
  ![postgres installation screenshot](/screenshots/postgres_install.png)

- Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

  I created a config file called `mycheck.yaml` located at `~/.datadog-agent/conf.d` that looks like this:
  ```yaml
  init_config:

  instances:
      [{}]
  ```
  Then, I created a check file `mycheck.py` at `~/.datadog-agent/checks.d` that looks like this:

  ``` python
  # mycheck.py
  import random
  from checks import AgentCheck

  class MyCheck(AgentCheck):
      def check(self, instance):
          # sends a random value between 0 to 1000 to the agent
          self.gauge('my_metric', random.randint(0, 1000))
  ```
  I encountered an issue here when trying to test the check with the command in the documentation. The specific command I tried is `sudo -u dd-agent -- datadog-agent check mycheck`. However I was able to run the check without `sudo`, using `datadog-agent check mycheck`. Here is the relevant portion of the report I got back after running the check:
  ```
    === Series ===
  {
    "series": [
      {
        "metric": "my_metric",
        "points": [
          [
            1528508654,
            664
          ]
        ],
        "tags": null,
        "host": "Dannis-Air",
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
      mycheck
      -------
        Total Runs: 1
        Metrics: 1, Total Metrics: 1
        Events: 0, Total Events: 0
        Service Checks: 0, Total Service Checks: 0
        Average Execution Time : 0ms
  ```

- Change your check's collection interval so that it only submits the metric once every 45 seconds. **Bonus Question** Can you change the collection interval without modifying the Python check file you created?

  Since the agent defaults to collecting metrics every 15 seconds, changing the `min_collection_interval` on the instance prevents it from collecting metric from that instance if time since last collection has been less than the `min_collection_interval`. So I changed `mycheck.yaml` to look like this:
  ``` yaml
  init_config:

  instances:
      - min_collection_interval: 45
  ```

  Here is a screenshot of the graph for `my_metric`:
  ![metric screenshot](/screenshots/my_metric.png)

## Visualizing Data

I created the timeboard using the script at `timeboard.py`

When selecting the best visualization for the `my_metric_rollup` graph, I initially selected "line", which made the display invisible since it's displaying data rolled up to an hour. So I changed it to "bar" visualization.

Here is a screenshot of the finished timeboard:
![timebaord screenshot](/screenshots/my_metric_timeboard.png)

Here is the link to my [Custom - Metrics Timeboard](https://app.datadoghq.com/dash/825841/custom---metrics?live=true&page=0&is_auto=false&from_ts=1528399035881&to_ts=1528402635881&tile_size=m).

To send a snapshot to myself, I selected a timeframe of 5 min and chose 'anotate graph' to add myself with the @ notation in the comment, like this:

![5min snapshot screenshot](/screenshots/5min_snapshot.png)

After doing this for all 3 graphs, these are the emails I got for each graph:

![my_metric_avg screenshot](/screenshots/my_metric_avg.png)

![my_metric_rollup screenshot](/screenshots/my_metric_rollup.png)

![postgres screenshot](/screenshots/postgres.png)

**Bonus Question**: What is the Anomaly graph displaying?

The anomaly graph includes normal results along with a grey band that shows the expected range of the metric based on historical context. In the case of `postgres_rows_fetched`, it uses the basic algorithm for anomaly detection and shows values that are 2 standard deviations apart. Metrics that go out of their expected ranges are anomalies, and should be monitored accordingly.

## Monitoring Data
Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:
  - Warning threshold of 500
  - Alerting threshold of 800
  - And also ensure that it will notify you if there is No Data for this query over the past 10m.

Using the Datadog dashboard UI, I created a new monitor and set its threshold like this:
![monitor config screenshot](/screenshots/monitor_config.png)

To have monitor send me an email whenever the monitor triggers, I added `@danni25liu@gmail.com` at the end of my message.

To create different messages based on whether the monitor is in an Alert, Warning, or No Data state, I used these conditionals:
```
{{#is_alert}} Alert: my_metric reached {{value}} on host {{host.name}} with IP {{host.ip}}! {{/is_alert}}
{{#is_warning}} Warning: my_metric reached {{warn_threshold}}! {{/is_warning}}
{{#is_no_data}} No data for my_metric in the last 10 min. {{/is_no_data}}
```
To include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state, I used `{{value}}` and `{{host.ip}}`.

Here is a screenshot of how I configured the monitor's message:

![monitor message screenshot](/screenshots/monitor_message.png)

Here are some screenshots of the emails sent to me when monitor triggers at differenet states:

Alert:
![alert screenshot](/screenshots/monitor_alert.png)

Warn:
![warn screenshot](/screenshots/monitor_warn.png)

No Data:
![no data screenshot](/screenshots/monitor_nodata.png)

**Bonus Question**: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

I scheduled downtimes using the datadog UI, by navigating to the monitors section and selecting "schedule downtime". Note that all of the email notifications are showing UTC, but the actual scheduled downtime is in EST:

![downtime_weekday screenshot](/screenshots/downtime_weekday.png)

One that silences it from 7pm to 9am daily on M-F:

![downtime_weekday screenshot](/screenshots/downtime_weekday.png)

And one that silences it all day on Sat-Sun:

![downtime_weekends screenshot](/screenshots/downtime_weekends.png)

## Collecting APM Data:
I enabled APM in datadog's agent config file like this:
```yaml
apm_config:
  enabled: true
  env: myapp
  receiver_port: 8126
```

Installing the trace agent was a roadblock for me. Specifically, after downloading the trace agent for mac, I could not activate the agent with the recommended command from the documentation: `./trace-agent-osx-X.Y.Z -config /opt/datadog-agent/etc/datadog.conf`. The commands I've tried include `./datadog-trace-agent-6.2.1 -config /opt/datadog-agent/etc/datadog.yaml` and `./datadog-trace-agent-6.2.1 -config ~/.datadog-agent/datadog.yaml`. Researching further led me to this [issue on github](https://github.com/DataDog/datadog-trace-agent/issues/397). To get around this issue, I installed the agent manually with the following steps:
  - install Go 1.10.3 for Mac OS X from their [official site](https://golang.org/dl/)
  - add Go to my path by adding the following lines to my shell script:
  ```
  export GOPATH=$HOME/go
  export GOBIN=$GOPATH/bin
  export PATH=$PATH:$GOBIN
  ```
  - download the agent by running:
  ```
  go get -u github.com/DataDog/datadog-trace-agent/...
  ```
  - install the trace agent:
  ```
  cd $GOPATH/src/github.com/DataDog/datadog-trace-agent
  make install
  ```
  - then, I was able to run the trace agent with the following command:
  ```
  trace-agent --config ~/.datadog-agent/datadog.yaml
  ```
  - Here are the logs after running the trace agent:
  ```
  2018-06-11 12:13:42 INFO (trace_writer.go:49) - Trace writer initializing with config: {MaxSpansPerPayload:1000 FlushPeriod:5s UpdateInfoPeriod:1m0s SenderConfig:{MaxAge:20m0s MaxQueuedBytes:67108864 MaxQueuedPayloads:-1 ExponentialBackoff:{MaxDuration:2m0s GrowthBase:2 Base:200ms}}}
  2018-06-11 12:13:42 INFO (stats_writer.go:31) - Stats writer initializing with config: {UpdateInfoPeriod:1m0s SenderConfig:{MaxAge:20m0s MaxQueuedBytes:67108864 MaxQueuedPayloads:-1 ExponentialBackoff:{MaxDuration:2m0s GrowthBase:2 Base:200ms}}}
  2018-06-11 12:13:42 INFO (service_writer.go:31) - Service writer initializing with config: {FlushPeriod:5s UpdateInfoPeriod:1m0s SenderConfig:{MaxAge:20m0s MaxQueuedBytes:67108864 MaxQueuedPayloads:-1 ExponentialBackoff:{MaxDuration:2m0s GrowthBase:2 Base:200ms}}}
  2018-06-11 12:13:42 INFO (main.go:211) - trace-agent running on host Dannis-MacBook-Air.local
  2018-06-11 12:13:42 INFO (receiver.go:142) - listening for traces at http://localhost:8126
  ```

After running the trace agent, I instrumented the test app at `myapp/myapp.py`, installing dependencies with a virtualenv. Here are the logs after running the app:

```
2018-06-11 12:20:15,178 - ddtrace.contrib.flask.middleware - DEBUG - flask: initializing trace middleware
2018-06-11 12:20:15,178 - ddtrace.tracer - DEBUG - set_service_info: service:myapp_service app:flask type:web
2018-06-11 12:20:15,179 - ddtrace.writer - DEBUG - resetting queues. pids(old:None new:68602)
2018-06-11 12:20:15,179 - ddtrace.writer - DEBUG - starting flush thread
 * Serving Flask app "myapp" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
2018-06-11 12:20:15,416 - werkzeug - INFO -  * Running on http://0.0.0.0:5050/ (Press CTRL+C to quit)
2018-06-11 12:20:16,239 - ddtrace.api - DEBUG - reported 1 services
```

After a couple minutes, I was able to view my traces on the datadog dashboard.

I created a new timeboard with Datadog's UI. Since I wanted to best immitate what DevOps engineers would want to monitor, I included the following metrics in my timeboard:
  - App metrics: total requests, errors per second, latancy (exported from service graphs)
  - Infrastructure metrics: system free memory, system cpu, user cpu.

Here is a screenshot of the completed timeboard:
![infrastructure screenshot](/screenshots/apm_infrastructure.png)

Here is the link to my [APM & infrastructure metrics for myapp_service Timeboard](https://app.datadoghq.com/dash/830201/apm--infrastructure-metrics-for-myappservice?live=true&page=0&is_auto=false&from_ts=1528398638091&to_ts=1528402238091&tile_size=m).

## Final Question:
Creative ways to use datadog:

Datadog can be used to monitor plant health by detecting their watering needs based on soil moisture and air humidity.  Since humidity varies seasonaly and geographically, it could be difficult to determine and keep track of how much to water a plant in a multi-plant household when they are purchased from out of state or when seasons change. Datadog can help establish a watering baseline and send alerts when a plant needs watering or has been watered too much.

## Links
- [Dashboard for local host](https://app.datadoghq.com/dash/host/491680408?live=true&page=0&from_ts=1528394732587&to_ts=1528409132587&is_auto=false&tile_size=m)
- [APM & infrastructure metrics for myapp_service Timeboard](https://app.datadoghq.com/dash/830201/apm--infrastructure-metrics-for-myappservice?live=true&page=0&is_auto=false&from_ts=1528398638091&to_ts=1528402238091&tile_size=m)
- [Custom - Metrics Timeboard](https://app.datadoghq.com/dash/825841/custom---metrics?live=true&page=0&is_auto=false&from_ts=1528399035881&to_ts=1528402635881&tile_size=m)

## References
Throughout this assignment, other than the datadog documentation, I also consulted [the SRE book](https://landing.google.com/sre/book/chapters/monitoring-distributed-systems.html) by Google to make sure I understand the needs of DevOps engineers.
