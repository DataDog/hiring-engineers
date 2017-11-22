## Collecting Metrics:

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

I created 3 tags in the datadog.conf file in the .datadog-agent folder, as seen here:
<img src="./images/tags_code.png">

This created the tags that can now be viewed in the Host Map, shown here:
<img src="./images/tags_hostmap.png">

* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

I already had PostgreSQL installed on my machine, so it was just a matter of installing the Datadog integration.  I followed the instructions to add datadog as a User and give it the appropriate properties.  I then adjusted the code as instructed on the Postgres yaml file.  After doing a quick system check
<img src="./images/postgres_check.png">

I saw that it was properly installed on my Dashboard:
<img src="./images/postgres_installed.png">

* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

I created 2 files in the .datadog-agent folder: randmetric.py and randmetric.yaml.  The yaml file is a config file, to be placed in the conf.d subfolder.  The python file contains the actual check, and thus goes in the checks.d subfolder.  Here is what the code looked like:
<img src="./images/random_code.png">

The python file inherits from AgentCheck, and to get the random value, I've inherited from random as well.  In the yaml config file, for now I am just doing the bare minimum to get the check running.  Once it's running, here's what the metrics dashboard looks like:
<img src="./images/random_dashboard.png">

As a default, it collects data every 20 seconds.

* Change your check's collection interval so that it only submits the metric once every 45 seconds.

By changing the minimum collection interval to 45, data will now only be submitted no more than every 45 seconds.  It is still dependent upon when the agent collects, however.
<img src="./images/45sec.png">


* **Bonus Question** Can you change the collection interval without modifying the Python check file you created?

Yes - this can be done by changing the default collection interval for the entire agent.

## Visualizing Data:

Utilize the Datadog API to create a Timeboard that contains:

* Your custom metric scoped over your host.
* Any metric from the Integration on your Database with the anomaly function applied.
* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

I created this all as one Timeboard using 3 different graphs in a single API call.  The code for this is here:
<img src="./images/api_code.png">

The graph for my_metric is straight forward and has no constraints.  The metric from the PSQL integration is also ported in with little alteration.  I couldn't quite get the syntax for adding an anomaly at the point of Timeboard creation, so I added this manually on the Dashboard view in the UI.  Finally, I used the rollup function to create another graph of my_metric, for the period of one hour.  All 3 graphs can be seen on the Timeboard here:
<img src="./images/timeboard_graphs.png">

Once this is created, access the Dashboard from your Dashboard List in the UI:

* Set the Timeboard's timeframe to the past 5 minutes

To get to a 5 minute timeframe, I manually selected a 5 minute subsection on the graph itself.  This adjusted the whole timeboard to a 5 minute interval.

* Take a snapshot of this graph and use the @ notation to send it to yourself.

After adjusting this to 5 minutes, I sent myself a snapshot.  This now appears in my events, as seen here:
<img src="./images/snapshot.png">

* **Bonus Question**: What is the Anomaly graph displaying?

It is basically highlighting deviations from the norm.  Based on past behavior, the algorithm expect the data to behave a certain way, within some bounds.  If it deviates too much from this, the graph is marked in red to indicate these periods of anomalies.  This will not show much for a small data sample, but over time seems to be an effective of highlighting significant deviations in one's data.

## Monitoring Data

Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

* Warning threshold of 500
* Alerting threshold of 800
* And also ensure that it will notify you if there is No Data for this query over the past 10m.

To create this monitor, I clicked Monitors, and then New Monitor on the sidebar of my UI. From here I chose to create a Metric monitor.  I set this up as per the instructions above, with these results:
<img src="./images/thresholds.png">

Please configure the monitor’s message so that it will:

* Send you an email whenever the monitor triggers.
* Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
* Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
* When this monitor sends you an email notification, take a screenshot of the email that it sends you.

Using different variables in an if/else setup, I created messages that would be different depending on which alert was being recorded, as seen here:
<img src="./images/message.png">

And here is an email that was sent to me when the warning state was reached:
<img src="./images/email.png">

The IP does not appear to be displaying correctly, despite being templated exactly as stated in the templating dialogue box.

* **Bonus Question**: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

    * One that silences it from 7pm to 9am daily on M-F,
    * And one that silences it all day on Sat-Sun.
    * Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

These both can be setup by going to the Manage Downtime tab in the Monitors dashboard.  Here are what the monitors will look like in setup:
<img src="./images/downtime1.png">
<img src="./images/downtime2.png">


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

* **Note**: Using both ddtrace-run and manually inserting the Middleware has been known to cause issues. Please only use one or the other. 
    
* **Bonus Question**: What is the difference between a Service and a Resource?

Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.


## Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?