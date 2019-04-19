Your answers to the questions go here.

## Collecting Metrics:

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

> I added the following lines to `/etc/datadog-agent/datadog.yaml`:
> ```
> # Set the host's tags (optional)
> tags:
>   - os:ubuntu
>   - env:dev
>   - role:database
> ```
> Which is visible in the screenshot below:
> <img src='Screenshot 2019-04-12 23.00.32.png'>

* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

> I added the following lines to `/etc/datadog-agent/conf.d/mongo.d/conf.yaml`:
> ```
> init_config:
>
>instances:
>  # Specify the MongoDB URI, with database to use for reporting (defaults to "admin")
>  # E.g. mongodb://datadog:LnCbkX4uhpuLHSUrcayEoAZA@localhost:27016/my-db
>  - server: mongodb://datadog:qsKfBnD1CAsCt9Wz613T912Q@localhost:27017
>    # tags:
>    #   - optional_tag1
>    #   - optional_tag2
>    replica_check: true
> ```
> <img src='Screenshot 2019-04-13 20.02.06.png'>

* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

> I created the following script in `/etc/datadog-agent/checks.d/my_metric.py`:
> ```
> # the following try/except block will make the custom check compatible with any Agent version
> try:
>     # first, try to import the base class from old versions of the Agent...
>     from checks import AgentCheck
> except ImportError:
>     # ...if the above failed, the check is running in Agent version 6 or later
>     from datadog_checks.checks import AgentCheck
>
> import random
>
> # content of the special variable __version__ will be > shown in the Agent status page
> __version__ = "1.0.0"
>
>
> class MyMetricCheck(AgentCheck):
>     def check(self, instance):
>         self.gauge('my_metric', random.randint(1,1000))
> ```
> I also created a `/etc/datadog-agent/conf.d/my_metric.yaml` containing:
> ```
> instances: [{}]
> ```
> <img src="Screenshot 2019-04-13 20.37.58.png">

* Change your check's collection interval so that it only submits the metric once every 45 seconds.

> I modified my `/etc/datadog-agent/conf.d/my_metric.yaml` to contain the following:
> ```
> init_config:
>
> instances:
>  - min_collection_interval: 45
> ```

* **Bonus Question** Can you change the collection interval without modifying the Python check file you created?

> I believe that the solution outlined above accomplishes this task.


## Visualizing Data:

Utilize the Datadog API to create a Timeboard that contains:

* Your custom metric scoped over your host.
* Any metric from the Integration on your Database with the anomaly function applied.
* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.

> Solution script contents can be found in <a href="new-dashboard.py">new-dashboard.py</a>
>

Once this is created, access the Dashboard from your Dashboard List in the UI:

* Set the Timeboard's timeframe to the past 5 minutes

> The newly created doashboard can be located at: <a href="https://app.datadoghq.com/dashboard/sq4-qu4-a2x/my-new-dashboard?tile_size=m&page=0&is_auto=false&from_ts=1555555815000&to_ts=1555556715000&live=true">https://app.datadoghq.com/dashboard/sq4-qu4-a2x/my-new-dashboard?tile_size=m&page=0&is_auto=false&from_ts=1555555815000&to_ts=1555556715000&live=true
>
> I set the timeframe to display the last 15 minutes
> <img src="Screenshot 2019-04-14 15.39.45.png">
> I can select a time interval of 5 minutes by highlighting a 5 minute section of the timeseries graph; however, that only shows that exact timeframe, not a running graph of the last 5 minutes.
> <img src="Screenshot 2019-04-17 22.08.39.png">

* Take a snapshot of this graph and use the @ notation to send it to yourself.

> <img src="Screenshot 2019-04-14 15.39.59.png">
> <img src="Screenshot 2019-04-14 15.43.40.png">

* **Bonus Question**: What is the Anomaly graph displaying?

> In my dashboard, I am showing MongoDB queries per second. Since my database is not used for anything, its baseline is 0 queries per second. If I make a bunch of queries to the database, I can demonstrate an anomalous spike in the metric and therefore the graph shows a red spike in queries per second representing a anomaly/deviation from the baseline.
> <img src="Screenshot 2019-04-14 15.54.22.png">


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

> New Monitor creation:
> <img src="Screenshot 2019-04-14 16.08.46.png">
> <img src="Screenshot 2019-04-14 16.25.47.png">
> Email from Monitor:
> <img src="Screenshot 2019-04-14 16.24.55.png">

* **Bonus Question**: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

  * One that silences it from 7pm to 9am daily on M-F,
  * And one that silences it all day on Sat-Sun.
  * Make sure that your email is notified when you schedule the downtime and take a screenshot of that \
  'notification.

> Monitoring downtime entries:
> <img src="Screenshot 2019-04-14 16.34.24.png">
> <img src="Screenshot 2019-04-14 16.34.18.png">
> Email confirmation notifying of the upcoming downtime:
> <img src="Screenshot 2019-04-14 16.35.08.png">


## Collecting APM Data:

Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:

> Fully instrumented app can be found in <a href="flask-app.py">flask-app.py</a>

* **Note**: Using both ddtrace-run and manually inserting the Middleware has been known to cause issues. Please only use one or the other.

> For simplicity, I chose to use `ddtrace-run python3 /vagrant/hiring-engineers/flask-app.py`

* **Bonus Question**: What is the difference between a Service and a Resource?

> A Service is a set of processes that do the same job, for example the flask library in a python script is a service that creates web applications or APIs. A Resource is a specific action for a given service, for example a flask API can have different routes that perform different actions within the API.

Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

> A New dashboard that integrates APM tracing and Infrastructure monitoring can be found at <a href="https://app.datadoghq.com/dashboard/7vv-yip-g9k/apm-dashboard?tile_size=m&page=0&is_auto=false&from_ts=1555292820000&to_ts=1555296420000&live=true">https://app.datadoghq.com/dashboard/7vv-yip-g9k/apm-dashboard?tile_size=m&page=0&is_auto=false&from_ts=1555292820000&to_ts=1555296420000&live=true</a>
> In this dashboard, I am representing correlated and time-bound graphs showing hit counts on a flask API, MongoDB commands, and CPU on the host.
> <img src="Screenshot 2019-04-14 22.47.36.png">

Please include your fully instrumented app in your submission, as well.

> Fully instrumented <a href="flask-app.py">flask-app.py</a>
>
> While not instructed to do so, I wanted to learn a bit more about the platform, so I added some basic logging to pull into the Logs engine. To do so, I had to add the following lines to `/etc/datadog-agent/datadog.yaml`:
> ```
> logs_enabled: true
> ```
> and I had to create `/etc/datadog-agent/conf.d/python.d/conf.yml` with the contents:
> ```
> #Log section
> logs:
>
>     # - type : file (mandatory) type of log input source (tcp / udp / file)
>     #   port / path : (mandatory) Set port if type is tcp or udp. Set path if type is file
>     #   service : (mandatory) name of the service owning the log
>     #   source : (mandatory) attribute that defines which integration is sending the logs
>     #   sourcecategory : (optional) Multiple value attribute. Can be used to refine the source attribtue
>     #   tags: (optional) add tags to each logs collected
>
>   - type: file
>     path: /vagrant/hiring-engineers/flask-app.log
>     service: flask-app
>     source: python
>     sourcecategory: sourcecode
>     #For multiline logs, if they start with a timestamp with format yyyy-mm-dd uncomment the below processing rule
>     #log_processing_rules:
>     #   - type: multi_line
>     #     pattern: \d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])
>     #     name: new_log_start_with_date
> ```
> <img src="Screenshot 2019-04-14 23.22.29.png">

## Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?

> I have current customers complaining that some SAAS applications are a "black box" that they don't have visibility into health or performance. I think it would be great to implement the new Synthetics solution to monitor the health of SAAS applications or cloud-based APIs.
>
> I took the liberty to play around with this solution and add some basic SAAS monitoring with Datadog Synthetics. I created an API test to do a simple GET on a cloud-based API.
> <img src="Screenshot 2019-04-17 23.48.28.png">
> <img src="Screenshot 2019-04-17 23.56.25.png">
> In this case I knew it would fail because I used a temporary authorization token. When it timed out, I got the alert as expected.
> <img src="Screenshot 2019-04-18 21.35.10.png">
