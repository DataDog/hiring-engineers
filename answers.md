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

> I set the timeframe to 15 minutes as I didn't see an option for 5 minute interval
> <img src="Screenshot 2019-04-14 15.39.45.png">

* Take a snapshot of this graph and use the @ notation to send it to yourself.

> <img src="Screenshot 2019-04-14 15.39.59.png">
> <img src="Screenshot 2019-04-14 15.43.40.png">

* **Bonus Question**: What is the Anomaly graph displaying?

> In my dashboard, I am showing MongoDB queries per second. Since my database is not used for anything, its baseline is 0 queries per second. If I make a bunch of queries to the database, I can demonstrate an anomalous spike in the metric and therefore the graph shows a red spike in queries per second representing a anomaly/deviation from the baseline.
> <img src="Screenshot 2019-04-14 15.54.22.png">
