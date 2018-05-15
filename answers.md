Your answers to the questions go here.
------------------------------------------------------------
Prerequisites - Steps

**I ran into issues installing a Virtual Machine on my machine. Since these issues are likely machine specific, I decided to not include the trouble shooting steps I ran into.

1) To test out Datadog's software, go to Datadog's website at www.datadoghq.com and click the "GET STARTED FOR FREE" button. That will bring up the Modal below:

Modal.png

fill out the form, and type “Datadog Recruiting Candidate” in the “Company” field.

2) Upon submission, select the tab for your Operating System. This will open up a tab where you can install Datadog's Agent.

Installation.png

Ubuntu Install Window.png

You will be prompted for your machine's password. The installation process may look something like this at the end. 

Datadog Agent Console Install.png

Upon completion, head back to the Home Page and you should see a notification that your Datadog agent is now collecting metrics on your machine! 

Home Page.png

If you click on the logo icon in the upper left hand corner, that will take you to your dashboard. Click on "System Overview dashboard" to get a sneak peak of some of the default metrics that the agent tracks.

Sneak Peat ay System Overview.png

------------------------------------------------------------
Collecting Metrics:
Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

Change your check's collection interval so that it only submits the metric once every 45 seconds.

Bonus Question Can you change the collection interval without modifying the Python check file you created?

-------------------------------------------------------------
Collecting Metrics - Steps
1) CLick on the navigation bar item "Infrastructure" that has an icon of 3 hexagons with 2 filled in.

2) Hover over your machine's hostname and click on the "inspect" button that appears. This will open up a separate screen that looks something like this. 

inspect.png

3) Open your Agent configuration file:datadog.yaml to add tags. Your configuration file for the Agent can be found here: https://docs.datadoghq.com/agent/basic_agent_usage/#configuration-file
Once you're in the correct directory, open the file with your favorite text editor.

4) Scroll down to "# Set the host's tags (optional)" and add the tags. In this example, `tags: test:test_value` was used: 

tag Post.png

To get started with tags and why they are useful go here: https://docs.datadoghq.com/getting_started/tagging/

5) Go back to the Host Map page at: https://app.datadoghq.com/infrastructure/map?fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=availability-zone&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=true&palette=green_to_orange&paletteflip=false&node_type=host
to see your tags.

Tag Screen.png

6) Install PostgreSQL on youre local machine. Instructions can be found here: https://wiki.postgresql.org/wiki/Detailed_installation_guides.
Once completed, install integration for PostgreSQL. To do this, head over to the Integrations Tab (puzzle piece) on the navigation bar and search for postgreSQL. Click on it and follow instructions provided. Here is an example of what the configuation panel would look like 

Install postgres.png 

** Inside your `conf.d` folder, there may not be a `postgres.yaml` file. Create a copy from the example file inside naming it `postgres.yaml` and edit as needed. Below is what my code looked like: 

Postgres Code.png

7) To create a custom Agent check, here is documentation to get oriented: https://docs.datadoghq.com/agent/agent_checks/. To get started, go to your agent directory at `/etc/datadog-agent`. Enter conf.d and create a YAML file with your custom metric name, in this case `my_metric.yaml`. Create your configuration file as needed. My example is provided below.

myMetricYaml.png

8) To create the check itself, create a separate file in `/etc/datadog-agent/checks.d` where the check file name must match the configuration file name. Here it is `my_metric.py`. My code is as seen below. Once saved, restart the agent. Below is what the `my_metric` graph looks like, at this link: https://app.datadoghq.com/dash/integration/custom?live=true&tpl_var_scope=host%3Awarren-740U3L&page=0&is_auto=false&from_ts=1526341720378&to_ts=1526345320378&tile_size=m

myMetricPy.png

BONUS QUESTION: Can you change the collection interval without modifying the Python Check file you created?
I've looked through the documentation. I can't seem to find anything that allows for changing the collection interval without changing the check file. If I'm correct, adding that feature to the integrations page or to a TimeBoard or ScreenBoard would be pretty useful and intuitive.
---------------------------------------------------
Utilize the Datadog API to create a Timeboard that contains:

Your custom metric scoped over your host.
Any metric from the Integration on your Database with the anomaly function applied.
Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timemboard.

Once this is created, access the Dashboard from your Dashboard List in the UI:

Set the Timeboard's timeframe to the past 5 minutes
Take a snapshot of this graph and use the @ notation to send it to yourself.
Bonus Question: What is the Anomaly graph displaying?
---------------------------------------------------
1) In order to get familiar with the Datadog API refer to this link: https://docs.datadoghq.com/api/?lang=bash#create-a-timeboard.

2) I used Postman in order to create the TimeBoard. This link was referenced: https://help.datadoghq.com/hc/en-us/articles/115002182863-Using-Postman-With-Datadog-APIs. I followed the steps to generate an application key, imported the datadog collection, and made a POST request at https://api.datadoghq.com/api/v1/dash with specified api and application key. The request object below was used to create the TimeBoard with all neccssary graphs. See image below: 

Postman Create TimeBoard.png

These links were used to understand and create the anomaly and rollup function, respectively:
 https://docs.datadoghq.com/monitors/monitor_types/anomaly/#anomaly-detection-algorithms
 https://docs.datadoghq.com/graphing/#rollup-to-aggregate-over-time

The script is here: 
```
{
      "graphs" : [{
          "title": "Average Custom Metric over Host",
          "definition": {
              "requests": [
                     {
      "q": "avg:my_metric{host:warren-740U3L}"
    }]
          },
          "viz": "timeseries"
      },
      {
          "title": "Integration - Average PostgreSQL Commits with Anomaly function",
          "definition": {
              "requests": [
                      {
      "q": "anomalies(avg:postgresql.commits{*}, 'basic', 2)"
    }]
          },
          "viz": "timeseries"
      },
      {
          "title": "Custom Metric with Rollup function over Sum of 1 Hour Buckets",
          "definition": {
              "requests": [
                      {
      "q": "avg:my_metric{*}.rollup(sum, 3600)"
      }]
          },
          "viz": "timeseries"
      }], 
      "title" : "Warren Mui TimeBoard Creation",
      "description" : "Visualizing Data Portion of Hiring Challenge",
      "template_variables": [{
          "name": "host1",
          "prefix": "host",
          "default": "host:my-host"
      }],
      "read_only": "True"
}
```

3) Once the timeboard is created, head over to https://app.datadoghq.com/dashboard/lists and selct the new TimeBoard. Zoom into one of the graphs to get a 5 minute timeframe. Click on each graph and comment email address in each one. Below are snapshots:

5m Timeframe TimeBoard.png
3 5m graphs

**Note: Since the rollup graph is summed over 1 hour buckets, there is no visual data because the graph is zoomed into a 5 minute timeframe.

BONUS QUESTION: What is the Anomaly graph displaying?

The anomaly graph for the postgreSQL integration commits helps identity when the data is behaving differently from past trends. This particular graph uses the basic detection algorithm, meaning it uses recent values in the graph to determine the range of expected values. It is best for metrics that don't have a repeating seasonal pattern. Its bounds are set to 2. This value visually corresponds to the gray bands in the graph. In this case, the graph shows bound parameters with a range set to 2 standard deviations from the expected value.

---------------------------------------------------
Monitoring Data
Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

Warning threshold of 500
Alerting threshold of 800
And also ensure that it will notify you if there is No Data for this query over the past 10m.
Please configure the monitor’s message so that it will:

Send you an email whenever the monitor triggers.

Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.

Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.

When this monitor sends you an email notification, take a screenshot of the email that it sends you.

Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

One that silences it from 7pm to 9am daily on M-F,
And one that silences it all day on Sat-Sun.
Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

-------------------------------------------------------
Monitoring Data - 
1) Hover over the monitor tab (exclamation point) in the navigation bar and click on New Monitor. Click on metric and fill out the form as needed. Examples are below:

Monitor Metric.png
MonitorMetric2.png

Here are emails for an Alert, Warning, and No Data state:

Alert Message.png
Warning Email.png
No Data state.png

Bonus Question:
1) Hover over the monitor tab (exclamation point) in the navigation bar and click on Manage Downtime. Click the yellow Schedule Downtime tab and fill out the fields for when notifications should be turned off. Link for reference: https://docs.datadoghq.com/monitors/downtimes/ 
Screenshot of example modal below: 

Scheduling Downtime.png

When writing a custom message, refer to the following link:
https://docs.datadoghq.com/monitors/notifications/#message-template-variables

Here are the screenshots of the emails detailing downtime for weekday evenings and weekends:

WeekendAndWeekdayDowntime.png
-------------------------------------------------------
Collecting APM Data - 
General documentation for reference: https://docs.datadoghq.com/tracing/setup/

1) Install Flask using this link: http://flask.pocoo.org/docs/0.12/installation/#installation
2) Using this link as reference: http://flask.pocoo.org/docs/0.12/quickstart/, copy the provided code and create a file. In this example the file is named `app.py` with the following code.

apppy.png

**In line 28: `app.run(host='0.0.0.0', port=8080)`, the server is set to be publicly available using port 8080 since the default 80 port is currently occupied. 

Code: 
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
    app.run(host='0.0.0.0', port=8080)
```

3) Open datadog.yaml and set `apm config: enabled true` as seen below:

Trace Agent Configurations.png

4) Once this is completed, go to the APM tab in the navigation bar and select Getting Started. Click python and install ddtrace.

5) In the directory where your Flask file is located, run `ddtrace-run python my_app.py` with `my_app.py` as the name of your file. 

Here is an example of what the Flask code looks like running in browser:

6) Head back to the APM tag and your service's metrics will soon be visible. Click on the Services sub-tab wthin APM tag to select flask. On each graph click on the down-facing arrow with the circle around it and save them to your TimeBoard. Once completed, head to this link:
https://app.datadoghq.com/dash/809900/warren-mui-timeboard-creation?live=true&page=0&is_auto=false&from_ts=1526266174817&to_ts=1526352574817&tile_size=m

APM Metrics.png

BONUS QUESTION: What's the difference between a Service and a Resource?
A Service is a group of procedures or processes that when used work together provide a set of features. It's more of a software implementation that focuses on a specific (usually business-focused) functionality. A Resource is a particular query to a service. For example, a service for a bank would be something like "validate a customer's credit score." The resource would be a simple GET request (with specificed parameters for the data you want) to a credit score database.
------------------------------------------------------
Final Question:
Is there anything creative you would use Datadog for?

I think monitoring of self-driving cars would be useful. Being able to monitor the vehicles' software could help find errors to provide quality assurance, especially considering that a single error could result in death or injury for the passenger(s). On the same note, Datadog could be used for traffic light control centers in urban areas. Being able to monitor and analyze these processes would have immediate societal benefits. For example, the morning and evening commute in New York City could be less of a time sink.


