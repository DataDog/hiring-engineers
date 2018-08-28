# Eric Kollegger Solutions Engineer Exercise

## Collecting Metrics

Added unique tags and aliased my host name by opening the `datadog.yaml` config file located in `/opt/datadog-agent/etc/`:
![agent config](screenshots/host_tags_01.png "Config Tags and Host Alias")

Then checked to confirm the changes had taken effect in the Host Map:
![dashboard tags](screenshots/host_tags_02.png "Tags on Host Map")

Due to being previously installed on my machine and my familiarity with it, I decided on PostgreSQL as my database of choice. I followed the configuration steps found [here](https://app.datadoghq.com/account/settings#integrations/postgres)

I edited the `postgres.yaml` file found in `/opt/datadog-agent/etc/conf.d`:
![posgres yaml](screenshots/postgres_yaml.png "Posgres Config")

Restarted the agent and ran `datadog-agent status` in terminal to confirm my integration was successful:
![posgres confirmation](screenshots/postgres_integration_confirmed.png "Postgres Integration Confirmed")

And on the Dashboard:
![postgres integration](screenshots/postgres_integration.png "Postgres Success Screen")

Created custom check file `checkvalue.py` and it's corresponding config file `checkvalue.yaml` in `/opt/datadog-agent/etc/checks.d` and `/opt/datadog-agent/etc/conf.d`, respectively:
![check file](screenshots/check_file.png "Check File")
![check config](screenshots/check_config.png "Check Config")

**Bonus Question:** Can you change the collection interval without modifying the Python check file you created?

**Answer:** Yes, the collection interval for a check can be changed in it's accompanying config file.

## Visualizing Data

I followed this [guide](https://help.datadoghq.com/hc/en-us/articles/115002182863-Using-Postman-With-Datadog-APIs) to setup a DataDog environment in Postman. Then submitted the three requested graphs for my timeboard with the following:
```{
      "graphs" : [{
          "title": "Metric average over durandal.minimalghost",
          "definition": {
              "events": [],
              "requests": [
                  {"q": "avg:my_metric{host:durandal.minimalghost}"}
              ]
          },
          "viz": "timeseries"
      },
      {
          "title": "Postgres transactions committed",
          "definition": {
              "events": [],
              "requests": [
                  {"q": "anomalies(avg:postgresql.commits{*}, 'basic', 2)"}
              ]
          },
          "viz": "timeseries"
      },
      {
          "title": "One hour rollup visualization",
          "definition": {
              "events": [],
              "requests": [
                  {"q": "avg:my_metric{*}.rollup(sum, 3600)"}
              ]
          },
          "viz": "timeseries"
      }],
      "title" : "Eric's Custom Timeboard",
      "description" : "Solutions Engineer Task",
      "template_variables": [{
          "name": "host1",
          "prefix": "host",
          "default": "host:my-host"
      }],
      "read_only": "True"
    }
```

I found my newly created timeboard by navigating to the dashboard list. This can be seen below scoped to 4 hours in order to see some manner of graphing in action for the rollup frame, which only has a single point of data when set to the default scope:
![timeboard 4h](screenshots/timeboard_4h.png "Timeboard 4 Hour")

I then set it to the requested 5 minute scope by using the keyboard shortcut `alt + ]`:
![timeboard 5m](screenshots/timeboard_scoped_5m.png "Timeboard 5 Minutes")

Next I took a snapshot of my metric average graph by clicking the camera icon that appears when you mouse over any individual frame and sent it to myself using the @ symbol:
![snapshot graph](screenshots/dashboard_snapshot.png "Dashboard Snapshot")

This results in the targeted user receiving an email notification with the snapshot:
![snapshot email](screenshots/snapshot_email_notification.png "Snapshot Email")

**Bonus Question:** What is the Anomaly graph displaying?

**Answer:** The grey area on the graph represents DataDog's assessment of the normalized thresholds for that metric based on previous data. Anything falling above or below this range is considered anomalous or abnormal behavior and is flagged in red.

## Monitoring Data

To create a new monitor go to **Monitors > New Monitor** on the dashboard.

1. Choose the detection method: Leave the default **Threshold Alert**.
2. Define the metric: Select `my_metric` from the metric dropdown list and set from to `host:durandal.minimalghost`, the rest of the options can be left to default.
3. Set alert conditions: Set **Alert threshold** to **800** and **Warning threshold** to **500**. Select `Notify` if data is missing from the dropdown. Everything else can be left as default.

The final product should look something like this:
![create monitor](screenshots/monitor_creation.png "Create Monitor")

My custom alert, warning and no data message snippet:
```{{#is_alert}}
my_metric at host ip {{host.ip}} has surpassed {{threshold}} and is currently at {{value}}!
{{/is_alert}}

{{#is_warning}}
my_metric has surpassed {{warn_threshold}} and is currently at {{value}}!
{{/is_warning}}

{{#is_no_data}}
my_metric has not received data for the past 10 minutes!
{{/is_no_data}}

@eric.kollegger@gmail.com
```

When the warning threshold condition was met I received this email:
![monitor warning](screenshots/monitor_email_warn.png "Monitor Warning")

**Bonus Question:** Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:
  * One that silences it from 7pm to 9am daily on M-F
  * And one that silences it all day on Sat-Sun
  * Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification

By navigating to **Monitors > Manage Downtime** and clicking the **Schedule Downtime** button, I was able to configure these two downtime requests.

* Weeknights downtime:
![weeknight downtime](screenshots/weeknight_downtime.png "Weeknight Downtime")

* Weekend downtime:
![weekend downtime](screenshots/weekend_downtime.png "Weekend Downtime")

* Email notification for weeknight downtime:
![weeknight email notification](screenshots/weeknight_email_downtime.png "Weeknight Email Notification")

## Collecting APM Data

I manually downloaded the trace agent from GitHub by running `go get github.com/DataDog/datadog-trace-agent/cmd/trace-agent` then `cd go/src/github.com/DataDog/datadog-trace-agent` and ran `make install`.
I checked to confirm my trace agent had properly installed by looking for it in `/opt/datadog-agent/embedded/bin`.

Then I made sure to uncomment the agent APM settings in `datadog.yaml` so my app could be properly traced by the agent. I installed dd_trace and blinker via `pip install`. Then following the Flask trace docs [here](http://pypi.datadoghq.com/trace/docs/#) I added the necessary imports and pointed the tracer at my Flask app:

```from flask import Flask
import blinker as _
import logging
import sys
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
traced_app = TraceMiddleware(app, tracer, service="dd-flask-app", distributed_tracing=False)

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

First I enabled the trace-agent with `go/bin/trace-agent`, then in a separate terminal window I navigated to my Flask app and started it with `python dd_flask_app.py`.

* I saw the following outputs from the trace-app:
![trace app output](screenshots/tracer_output.png "Trace App Output")

* And my Flask app:
![flask app output](screenshots/flask_app_output.png "Flask App Output")

Which indicated to me that the tracer had successfully connected to my service and was listening for activity. I assumed once I wired up the trace agent to my service I would see new analytics appear on the APM docs page as it mentioned checking back there after completing setup, but I saw no change. I generated some traces by hitting the
`http://localhost:5050/` and `http://localhost:5050/api/trace` endpoints a couple times to generate traffic and checked back on the dashboard. Sure enough, there was a **Trace Search & Analytics** tab listing my Flask app. I then continued onto documenting the requested analytics ahead.

* Created a [screenboard](https://p.datadoghq.com/sb/6417246f3-6ec7b41faf9c7dac9fc3c825176756a6) with both APM and infrastructure metrics:
![apm screenboard](screenshots/APM_Infrastructure_Screenboard.png "APM Screenboard")

**Bonus Question:** What is the difference between a Service and a Resource?

**Answer:** A service can be thought of as a self-contained software implementation that *serves* a specific functionality and is generally built to easily integrate with other services. They are the component pieces that make up larger platforms. Examples of a service could be Rails, ReactJS, PostgreSQL or MongoDB. A resource is any data query made to a service, for example a CRUD action made directly to a database, through a URL or via a route in an MVC framework.

## Final Question
I'm always interested in harnessing technology for social good. I think with everything going on right now regarding our democratic process being tampered with by foreign and domestic powers alike *(see: voter roll purging, gerrymandering, polling site closures around targeted demographics, hacking, etc)*, comparing metrics like voter registration versus turnout during elections in different states/districts could generate fascinating data trends to study. Even though it's a less useful implementation in terms of real-time analytics, this could be used to potentially pinpoint concentrated areas where these nefarious practices take place to help combat them. I'd have to look into how much of this kind of information is available publicly, the Census Bureau has an API but I haven't done enough research on what kind of data it exposes.
