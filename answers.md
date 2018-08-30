# Eric Kollegger Solutions Engineer Exercise

## Setup the Environment

* This exercise will explain how to get up and running with the DataDog Mac OS X Agent. I'll be using macOS High Sierra 10.13.6. First go to `https://www.datadoghq.com/` and click on the **Get Started Free** button in the upper right corner. After filling out and submitting the form, you'll receive an email confirming that your free trial has begun.

* I logged in with my credentials at `https://app.datadoghq.com` and clicked on **Integrations > Agent > Mac OS X**. Rather than downloading the DMG package, I opted to download via terminal by running `DD_API_KEY=<YOUR_API_KEY> bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_mac_os.sh)"` so my API key would come integrated with the Agent out-of-the-box.

* The DataDog Agent is located in **Finder > Applications**, after opening it you should see a small dog bone icon appear in the top right tray which signals that it's active. We now have our very own DataDog Agent installed and ready for configuration!

## Collecting Metrics

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

Using terminal, navigate to the Agent configuration file by typing `cd /opt/datadog-agent/etc/` and opening the `datadog.yaml` config file. From there, add some custom tags to help identify your host. I decided to alias my hostname, but it's perfectly fine to leave the hostname commented out. This will result in it defaulting to your machine name, e.g. `Erics-Macbook-Pro`. For more on tagging best practices check out the docs [here](https://docs.datadoghq.com/tagging/). Below is the `datadog.yaml` file with my edits:
![agent config](screenshots/host_tags_01.png "Config Tags and Host Alias")

Then we'll need to restart the Agent for the changes to get picked up. To do this you can click the Agent icon in the tray and select **Restart**, or if you want to achieve the same thing in terminal you'll run `launchctl stop com.datadoghq.agent` and then `launchctl start com.datadoghq.agent`. For more on basic Agent usage for Mac OS X, check out the docs [here](https://docs.datadoghq.com/agent/basic_agent_usage/osx/?tab=agentv6).

Now back on our DataDog dashboard, go to **Infrastructure > Host Map**. There should be a single hexagonal shape representing our host, go ahead and click it. Please note that if you recently aliased your hostname, you may see **two** hexagons in the Host Map, side-by-side. Don't panic, you haven't created a second host! This is just DataDog differentiating two instances of your single host; the default named state and the newly aliased state. The old instance of your host will not continue to be displayed after a short time. Once you've clicked on your host, under the **Tags** section you should see your custom tags are now being displayed. Mine looks like this:
![dashboard tags](screenshots/host_tags_02.png "Tags on Host Map")

* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

Due to being previously installed on my machine and my familiarity with it, I decided on [PostgreSQL](https://www.postgresql.org/download/macosx/) as my database of choice. On the dashboard go to **Integrations > Integrations** and find **PostgreSQL**. Click on it and follow the configuration steps outlined [here](https://app.datadoghq.com/account/settings#integrations/postgres).

Once you've completed **Step 1** under **Configuration**, you'll need to edit the `postgres.yaml` file to reflect your generated password. This file can be found in `/opt/datadog-agent/etc/conf.d`. After making the necessary changes mine looks like this:
![posgres yaml](screenshots/postgres_yaml.png "Posgres Config")

Restart the Agent and run `datadog-agent status` in terminal to confirm that your integration was successful. This will output a list of information, for our needs we'll be looking specifically for a bit of output confirming the PostgreSQL integration was successful:
![posgres confirmation](screenshots/postgres_integration_confirmed.png "Postgres Integration Confirmed")

Then if we check back again on the Dashboard under **Integrations > Integrations** we should see our database is showing up under **Installed**:
![postgres integration](screenshots/postgres_integration.png "Postgres Success Screen")

* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

For our custom Agent check we'll need to create two files; a `.py` check file in `/opt/datadog-agent/etc/checks.d` and it's corresponding `.yaml` configuration file to be placed in `/opt/datadog-agent/etc/conf.d`. You can call it whatever you'd like but both file names must match. I named mine `checkvalue.py` and `checkvalue.yaml`, respectively.

As stated in the [documentation](https://docs.datadoghq.com/developers/agent_checks/), all custom Agent checks inherit from the `AgentCheck` class and require a `check()` method. We're going to import our `AgentCheck` dependency and `randInt` to generate our randomized metric for collection. Then in our `check()` method, we name and sample our metric with `self.gauge()`.
![init check files](screenshots/initial_check_files.png "Init Check Files")

* Change your check's collection interval so that it only submits the metric once every 45 seconds.

The collector runs every 15-20 seconds by default, but we can change this by adding a `min-collection-interval` to our check's config file globally or at the instance level. For the purposes of this exercise we'll add it under `init_config` to set it globally. When you're done it should look like this:
![check config](screenshots/check_config.png "Check Config")

We'll need to restart the Agent to in order to see the changes on the dashboard, this is true whenever changes are made to the check file or the accompanying config file. On the dashboard, navigate back to **Infrastructure > Host Map** and click on your host hexagon. On the left side of the panel there are several blue buttons representing our metrics being recorded thus far. If you named your random metric simply `my_metric` as I did it'll display as `(no-namespace)`. Click on it and you should see something like this:
![my metric graph](screenshots/my_metric_graph.png "My Metric Graph")

**Bonus Question:** Can you change the collection interval without modifying the Python check file you created?

**Answer:** Yes, the collection interval for a check can be changed in it's accompanying config file.

## Visualizing Data

Utilize the Datadog API to create a Timeboard that contains:

* Your custom metric scoped over your host.
* Any metric from the Integration on your Database with the anomaly function applied.
* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

I highly recommend installing [Postman for Mac OS X](https://www.getpostman.com/apps) and following this [guide](https://help.datadoghq.com/hc/en-us/articles/115002182863-Using-Postman-With-Datadog-APIs) which walks through incorporating the [DataDog API Collection](https://help.datadoghq.com/hc/en-us/article_attachments/360002499303/datadog_collection.json) for setting up a DataDog-specific environment in Postman. This empowers you with organized API calls for easy editing and re-use. It also offers a birds-eye view of the wide range of requests that can be made to DataDog. Check [here](https://docs.datadoghq.com/graphing/functions/#apply-functions-optional) for all available functions that can be applied to your metrics. Below is a request I put together for a Timeboard that graphs the average of `my_metric`, transaction `anomalies()` on my database and a `rollup()` average of `my_metric` over the course of one hour:

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

After making a successful submission (indicated by a `200` status code response) return to the DataDog Web UI and navigate to **Dashboards > Dashboard List**. At the top of the list should be a new Dashboard with the name you assigned to `title` in the above request. Clicking on it will bring up your newly created Timeboard taking in real-time data! Below is my own Timeboard scoped to 4 hours in order to display some manner of graphing for the rollup frame, which looks empty when set to the default scope of 1 hour since it only has a single point of data:
![timeboard 4h](screenshots/timeboard_4h.png "Timeboard 4 Hour")

* Set the Timeboard's timeframe to the past 5 minutes

You can manipulate the timeframe you want your graph scoped for by using the keyboard shortcuts `alt + [` to increase and `alt + ]` to decrease it. I've set mine to the requested 5 minute scope by using this method:
![timeboard 5m](screenshots/timeboard_scoped_5m.png "Timeboard 5 Minutes")

* Take a snapshot of this graph and use the @ notation to send it to yourself.

You can take a snapshot of a graph on the Timeboard by clicking the camera icon that appears when you mouse over any individual frame. You can then send it to yourself or a co-worker by using the @ symbol followed by the appropriate user name. Below is an example of me sending the `my_metric` average graph to myself:
![snapshot graph](screenshots/dashboard_snapshot.png "Dashboard Snapshot")

This will send the snapshot with any notes you include to the email associated with that user. Here is the resulting email notification I received:
![snapshot email](screenshots/snapshot_email_notification.png "Snapshot Email")

**Bonus Question:** What is the Anomaly graph displaying?

**Answer:** The grey area on the graph represents DataDog's assessment of the normalized thresholds for that metric based on previous data. Anything falling above or below this range is considered anomalous or abnormal behavior and is flagged in red.

## Monitoring Data

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

* Warning threshold of 500
* Alerting threshold of 800
* And also ensure that it will notify you if there is No Data for this query over the past 10m.

To create a new Metric Monitor navigate to **Monitors > New Monitor > Metric** on the dashboard.

1. **Choose the detection method:** Determines the type of detection method we want to use. Since the default is set to *Threshold Alert* we don't have to change anything.
2. **Define the metric:** Selects which of our metrics we will be monitoring. I've selected `my_metric` from the metric dropdown list and set the *from* dropdown to my aliased host `host:durandal.minimalghost`, the rest of the options can be left to default.
3. **Set alert conditions:** This is where we decide what threshold value being hit should issue a warning and a threshold value we consider critical to issue an alert. I've set *Alert threshold* to 800 and *Warning threshold* to 500 for this exercise. We can also get notifications when no data is received for a period of time by selecting `Notify` from the dropdown. The default is 10 minutes which is what we're after right now, the rest of this section can be left as default.

The final product should look something like this:
![create monitor](screenshots/monitor_creation.png "Create Monitor")

Please configure the monitor’s message so that it will:

* Send you an email whenever the monitor triggers.

* Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.

* Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.

4. **Say what's happening:** This is where you can custom tailor the notifications to be sent out for each condition, including any specific data as you need it. Documentation for custom notifications can be found [here](https://docs.datadoghq.com/monitors/notifications/). Below is a snippet of my custom alert, warning and no data messages:
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

* When this monitor sends you an email notification, take a screenshot of the email that it sends you.

If you've been following along with the random `my_metric` example you should receive an email notification shortly after creating the monitor when one of the specified conditions is met. When the warning threshold was breached I received this email:
![monitor warning](screenshots/monitor_email_warn.png "Monitor Warning")

**Bonus Question:** Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

To schedule downtime for our monitors, navigate to **Monitors > Manage Downtime** and click the **Schedule Downtime** button on the top right. In it's most basic usage, this allows us to specify recurring times throughout the week to silence our monitors.

1. **Choose what to silence:** Select which monitor we want to target for downtime. There's also optional scoping for individual hosts or groups.
2. **Schedule:** Choose whether it will be a one-time or recurring event, then specify date/time/duration/etc.
3. **Add a Message:** This is where you can add any custom message to give additional insight about the type of monitor, downtime event, etc. This is also where you would tag the users who should be notified about the event using the @ symbol. Below are screenshots of the two completed downtime requests.

* One that silences it from 7pm to 9am daily on M-F

Weeknights downtime:
![weeknight downtime](screenshots/weeknight_downtime.png "Weeknight Downtime")

* And one that silences it all day on Sat-Sun

Weekend downtime:
![weekend downtime](screenshots/weekend_downtime.png "Weekend Downtime")

* Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification

Email notification for weeknight downtime:
![weeknight email notification](screenshots/weeknight_email_downtime.png "Weeknight Email Notification")

## Collecting APM Data

* To get started with integrating APM I navigated to **APM > Docs** to familiarize myself with the implementation process using Python/Flask. The Python section under the **Getting Started** tab didn't yield a ton of front-loaded information so I clicked over to the **Docs** tab to dig deeper.

* I watched the 2 minute video which gave a great high-level overview of the what and why for the Application Performance Monitoring service, but wasn't very helpful for my installation journey. I scrolled down to the links at the bottom and clicked on **Set up your Application to send traces to DataDog**. From there I was able to glean a basic overview of the steps I needed to take, primarily:
1. Enable use of the Trace Agent and configure the environment in the `datadog.yaml` file
2. Get the appropriate Trace Agent based on OS
3. Instrument my chosen application

* I followed the link to the [macOS Trace Agent documentation](https://github.com/DataDog/datadog-trace-agent#run-on-osx). Because I was using macOS it explained I'd need to run the trace agent manually alongside the main DataDog Agent. I attempted to follow the steps outlined there:  
1. Download the latest OSX Trace Agent release `trace-agent-darwin-amd64-6.4.1`
2. Run the Trace agent using the Datadog Agent configuration `./trace-agent-darwin-amd64-X.Y.Z -config /opt/datadog-agent/etc/datadog.yaml`

* Downloading the Trace Agent was no problem, but when I ran the config command I got a `permission denied`. Appending `sudo` to it gave me a `command not found` message. Since this was the only part of the documentation I could find referencing installation for the macOS Trace Agent, I began googling around looking for similar issues. I came across [this thread](https://github.com/DataDog/datadog-trace-agent/issues/397). In particular one comment jumped out at me because it matched up verbatim with the documentation on the [official repo](https://github.com/DataDog/datadog-trace-agent#run-on-osx) under the **Development** section, and was generally a well regarded solution by the community:
![go installation](screenshots/thread_go_comment.png "Go Installation")

* I decided to give this method a *go* (ha) -- installed Go by following the steps in the provided [link](https://golang.org/dl/). Manually downloaded  and installed the trace agent from GitHub in terminal by running `go get github.com/DataDog/datadog-trace-agent/cmd/trace-agent`, then `cd go/src/github.com/DataDog/datadog-trace-agent` and `make install`.
I checked to confirm my trace agent had properly installed by finding it in `/opt/datadog-agent/embedded/bin` and in my go directory `go/bin/` as `trace-agent`.

* Then going back to the original steps I had laid out for myself, I made sure to uncomment the agent APM settings in `datadog.yaml` so my app could be properly traced by the agent.

* I setup a simple Flask app called `dd_flask_app.py` and pasted in the source code from the exercise as a starting point. Then referenced the advanced [Flask Trace docs]((http://pypi.datadoghq.com/trace/docs/#)) for installing dd_trace and blinker via `pip install`. Then adding the necessary `blinker/tracer/TracMiddleware` imports and pointed the tracer middleware at my Flask app with `traced_app = TraceMiddleware(app, tracer, service="dd-flask-app", distributed_tracing=False)`. Below is the code for my fully instrumented app:

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

Once I felt like I had made the required edits to my app, I started the trace-agent via terminal by running `go/bin/trace-agent`. Then in a separate terminal window I navigated to the top level directory of my Flask app and started it with `python dd_flask_app.py`.

* I saw the following outputs from the trace-app:
![trace app output](screenshots/tracer_output.png "Trace App Output")

* And my Flask app:
![flask app output](screenshots/flask_app_output.png "Flask App Output")

Which indicated to me that the tracer had successfully connected to my service and was listening for activity based on this readout from the Tracer Agent:

```
2018-08-27 10:08:15 INFO (service_mapper.go:59) - total number of tracked services: 1
```

As well as the debug log originating from my Flask app:

```DEBUG:ddtrace.api:reported 1 services
2018-08-27 09:5225,758 - ddtrace.api - DEBUG - reported 1 services
```

I assumed since I had successfully wired up the Trace Agent to my service I would see new analytics appear on the APM docs page as it mentions checking back there after completing setup, but I saw no changes. The `no data received` part of the logs had me concerned that I had somehow screwed up the setup in a meaningful way, so once again I hit the internet looking for answers.

I found a lot of issue tickets in the same vein of what I was trying to achieve but most dealt with running into errors or getting `0 services reported` along with the `no data received` logs. It felt like I was very close and was just missing something small, so I pinged Todd with the screens of my trace and app logs seeing if he had any insights. While he explained that giving assistance on the exercise wasn't allowed, at a glance it seemed like I had things setup properly and that I should ensure that the app was receiving traffic.

I had one of those all-too-common "Eureka! How could I be so dense?" moments, generated some traces by hitting the
`http://localhost:5050/` and `http://localhost:5050/api/trace` endpoints a couple times and checked back on the dashboard. Sure enough, when I navigated to the **Trace Search & Analytics** tab my Flask app was listed!. I then went to **APM > Serivce Map** where I found my named service `dd_flask_app` displayed:
![service map](screenshots/service_map.png "Service Map")

* I navigated to **Dashboards > New Dashboard** and selected **New Screenboard**. Then clicked and dragged down a **Graph** template and selected the `system.cpu.user` metric from the dropdown and clicked **Done** at the bottom to satisfy the infrastructure requirement. I then repeated the process but this time selected the `trace.flask.request.hits` from the dropdown for the APM metric requirement:
![apm screenboard](screenshots/APM_Infrastructure_Screenboard.png "APM Screenboard")

I saved it and returned to **Dashboards > Dashboard List** to find my newly created Screenboard at the top of the list. Once inside the Screenboard display, I clicked on the settings cog icon in the top right and selected **Generate Public URL** in order to share this [link](https://p.datadoghq.com/sb/6417246f3-6ec7b41faf9c7dac9fc3c825176756a6).

**Bonus Question:** What is the difference between a Service and a Resource?

**Answer:** A service can be thought of as a self-contained software implementation that *serves* a specific functionality and is generally built to easily integrate with other services. They are the component pieces that make up larger platforms. Examples of a service could be Rails, ReactJS, PostgreSQL or MongoDB. A resource is any data query made to a service, for example a CRUD action made directly to a database, through a URL or via a route in an MVC framework.

## Final Question
I'm always interested in harnessing technology for social good. I think with everything going on right now regarding our democratic process being tampered with by foreign and domestic powers alike *(see: voter roll purging, gerrymandering, polling site closures around targeted demographics, hacking, etc)*, comparing metrics like voter registration versus turnout during elections in different states/districts could generate fascinating data trends to study. Even though it's a less useful implementation in terms of real-time analytics, this could be used to potentially pinpoint concentrated areas where these nefarious practices take place to help combat them. I'd have to look into how much of this kind of information is available publicly, the Census Bureau has an API but I haven't done enough research on what kind of data it exposes.
