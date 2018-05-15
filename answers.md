<h1>Warren Mui Solutions Engineer Technical Challenge</h1>
<h2>Prerequisites </h2>

1) To test out Datadog's software, go to Datadog's website at www.datadoghq.com and click the "GET STARTED FOR FREE" button. That will bring up the Modal below:
![Imgur](https://i.imgur.com/O8PHdgj.png)

2) Upon submission, select the tab for the Operating System. This will open up a tab where Datadog's Agent can be installed.

![Imgur](https://i.imgur.com/b06skhL.png)
![Imgur](https://i.imgur.com/qv1ZNvN.png)
*API Key hidden

The installation process may look something like this at the end.
![Imgur](https://i.imgur.com/cPOhQ17.png)

Upon completion, head back to the Home Page and there will be a notification that the Datadog agent is now collecting metrics!
![Imgur](https://i.imgur.com/QK2V2GO.png)

Click on the logo icon in the upper left hand corner to go to the dashboard. Click on System Overview dashboard to get a sneak peak of some of the default metrics that the agent tracks. Example below:

![Imgur](https://i.imgur.com/5OlCexV.png)

<h2> Collecting Metrics </h2>

1) Hover over the Infrastructure tab that has an icon of 3 hexagons with 2 filled in and click on the Infrastructure tab.

2) Hover over your machine's hostname and click on the inspect button that appears. This will open up a separate screen that looks something like this:

![Imgur](https://i.imgur.com/l77Zl4b.png)

3) Open the Agent configuration file: `datadog.yaml` to add tags. The configuration file for the Agent can be found here: https://docs.datadoghq.com/agent/basic_agent_usage/#configuration-file

Once in the correct directory, open `datadog.yaml` with a text editor.

4) Scroll down to "# Set the host's tags (optional)" and add the tags. In this example, `tags: test:test_value` was used:

![Imgur](https://i.imgur.com/3rcfwdh.png)

To get started with tags and why they are useful go here: https://docs.datadoghq.com/getting_started/tagging/

5) To see the tags, go back to the Host Map page at: https://app.datadoghq.com/infrastructure/map?fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=availability-zone&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=true&palette=green_to_orange&paletteflip=false&node_type=host Screenshot below:
![Imgur](https://i.imgur.com/H1P2lsX.png)


6) Install PostgreSQL on your local machine. Instructions can be found here: https://wiki.postgresql.org/wiki/Detailed_installation_guides.

Once completed, install integration for PostgreSQL. To do this, head over to the Integrations Tab (puzzle piece) on the navigation bar and search for postgreSQL. Click on it and follow instructions provided. Here is an example of what the configuration panel would look like:

![Imgur](https://i.imgur.com/AYHxTnT.png)

** Inside your `conf.d` folder, there may not be a `postgres.yaml` file. Create a copy from the example file inside naming it `postgres.yaml` and edit as needed. Below is what my code looked like:

![Imgur](https://i.imgur.com/bbrkOKX.png)

7) To create a custom Agent check, here is documentation for reference: https://docs.datadoghq.com/agent/agent_checks/. To get started, go to your agent directory at `/etc/datadog-agent`. Enter `conf.d` and create a YAML file with your custom metric name, in this case `my_metric.yaml`. Create your configuration file as needed. My example is provided below:

![Imgur](https://i.imgur.com/1fxU0rC.png)

8) To create the check itself, create a separate file in `/etc/datadog-agent/checks.d` where the check file name must match the configuration file name. Here it is `my_metric.py`. My code is as seen below. Once saved, restart the agent. Below is what the `my_metric` graph looks like, at this link: https://app.datadoghq.com/dash/integration/custom?live=true&tpl_var_scope=host%3Awarren-740U3L&page=0&is_auto=false&from_ts=1526341720378&to_ts=1526345320378&tile_size=m

![Imgur](https://i.imgur.com/mLfjAAo.png)

<h4>Bonus Question: </h4> Can you change the collection interval without modifying the Python Check file you created?

I've looked through the documentation. I can't seem to find anything that allows for changing the collection interval without changing the check file. If I'm correct, adding that feature to the integrations page or to a TimeBoard or ScreenBoard would be pretty useful and intuitive.

<h2> Visualizing Data</h2>

1) In order to get familiar with the Datadog API refer to this link: https://docs.datadoghq.com/api/?lang=bash#create-a-timeboard.

2) I used Postman in order to create the TimeBoard. This link was referenced: https://help.datadoghq.com/hc/en-us/articles/115002182863-Using-Postman-With-Datadog-APIs. I followed the steps to generate an application key, imported the datadog collection, and made a POST request at https://api.datadoghq.com/api/v1/dash with specified api and application key. Once in Postman, select the Datadog collection and the Create a Timeboard tab in the Timeboards file. The request object below was used to create the TimeBoard with all neccssary graphs. See image below:

![Imgur](https://i.imgur.com/xsfSNKN.png)
*API and Application Keys Hidden

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
                     {"q": "avg:my_metric{host:warren-740U3L}"}]
          },
          "viz": "timeseries"
      },
      {
          "title": "Integration - Average PostgreSQL Commits with Anomaly function",
          "definition": {
              "requests": [
                      {"q": "anomalies(avg:postgresql.commits{*}, 'basic', 2)"}]
          },
          "viz": "timeseries"
      },
      {
          "title": "Custom Metric with Rollup function over Sum of 1 Hour Buckets",
          "definition": {
              "requests": [{"q": "avg:my_metric{*}.rollup(sum, 3600)"}]
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
3) Once the timeboard is created, head over to https://app.datadoghq.com/dashboard/lists and select the new TimeBoard. Zoom into one of the graphs to get a 5 minute timeframe. Click on each graph and I commented my email address in each one. Below are snapshots:

![Imgur](https://i.imgur.com/vgWhCEb.png)
**Note: Since the rollup graph is summed over 1 hour buckets, there is no visual data because the graph is zoomed into a 5 minute timeframe.

Below are the three graph comments I made, shown in my event stream:
![Imgur](https://i.imgur.com/ulsGUlU.png)

<h4>BONUS QUESTION: </h4> What is the Anomaly graph displaying?

The anomaly graph for the postgreSQL integration commits helps identity when the data is behaving differently from past trends. This particular graph uses the basic detection algorithm, meaning it uses recent values in the graph to determine the range of expected values. It is best for metrics that don't have a repeating seasonal pattern. Its bounds are set to 2. This value visually corresponds to the gray bands in the graph. In this case, the graph shows bound parameters with a range set to 2 standard deviations from the expected value.

<h2>Monitoring Data</h2>

1) Hover over the monitor tab (exclamation point) in the navigation bar and click on New Monitor. Click on metric and fill out the form as needed. Examples are below:

![Imgur](https://i.imgur.com/xcDuDCv.png)

![Imgur](https://i.imgur.com/VPyHOK1.png)

Here are emails for an Alert, Warning, and No Data state:

Alert Email

![Imgur](https://i.imgur.com/hzopakM.png)

Warning Email

![Imgur](https://i.imgur.com/hzopakM.png)

No Data Email

![Imgur](https://i.imgur.com/1FD4WUm.png)

<h4>Bonus Question: </h4>
Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

One that silences it from 7pm to 9am daily on M-F,
And one that silences it all day on Sat-Sun.
Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

<h4>Answer: </h4>
1) Hover over the monitor tab (exclamation point) in the navigation bar and click on Manage Downtime. Click the yellow Schedule Downtime tab and fill out the fields for when notifications should be turned off. Link for reference: https://docs.datadoghq.com/monitors/downtimes/

Screenshot of example of weekday evening downtime below:
![Imgur](https://i.imgur.com/oxmCxGS.png)

When writing a custom message with a message template, here is a link for reference:
https://docs.datadoghq.com/monitors/notifications/#message-template-variables

Here are the screenshots of the emails detailing downtime for weekday evenings and weekends:

![Imgur](https://i.imgur.com/RMEWQ2h.png)

<h2>Collecting APM Data </h2>

General documentation for reference: https://docs.datadoghq.com/tracing/setup/

1) Install Flask using this link: http://flask.pocoo.org/docs/0.12/installation/#installation

2) Using this link as reference: http://flask.pocoo.org/docs/0.12/quickstart/, copy the provided code and create a file. In this example, the file is named `app.py` with the following code.

![Imgur](https://i.imgur.com/B0zLnNS.png)

**In line 28: `app.run(host='0.0.0.0', port=8080)`, the server is set to be publicly available using port 8080 since port 80 is currently occupied.

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

3) Open `datadog.yaml` and set `apm config: enabled true` as seen below:

![Imgur](https://i.imgur.com/xCgBdEJ.png)

4) Once this is completed, go to the APM tab in the navigation bar and select Getting Started. Click python and install ddtrace.

5) In the directory where your Flask file is located, run `ddtrace-run python my_app.py` with `my_app.py` as the name of your file.

Here is an example of what the Flask code looks like running in browser:
![Imgur](https://i.imgur.com/jE7Tc3y.png)

6) Head back to the APM tag and your service's metrics will soon be visible. Click on the Services sub-tab wthin APM tag to select flask. On each graph click on the down-facing arrow with the circle around it and save them to your TimeBoard. Once completed, head to this link to view:
https://app.datadoghq.com/dash/809900/warren-mui-timeboard-creation?live=true&page=0&is_auto=false&from_ts=1526266174817&to_ts=1526352574817&tile_size=m

![Imgur](https://i.imgur.com/73AOF59.png)

<h4>Bonus Question: </h4>
What's the difference between a Service and a Resource?

A Service is a group of procedures or processes that when used work together provide a set of features. It's a software implementation that focuses on providing functionality to fulfill some kind of business goal. A Resource is a particular query to a service. For example, a service for a bank would be something like "validate a customer's credit score." This service would be comprised of various processes like confirming customer identity, collecting customer information, security checks, and determining if its a soft or hard inquiry. The resource could be a simple GET request (with specified parameters for the data you want) to a credit score database.

-----
<h4>Final Question:</h4>

Is there anything creative you would use Datadog for?

I think monitoring of self-driving cars would be useful. Being able to monitor the vehicles' software could help find errors to assist with quality assurance, especially considering that a single error could result in death or injury for the passenger(s). On a similar note, Datadog could be used for traffic light control centers in urban areas. Being able to monitor and analyze these processes could potentially have immediate societal benefits. For example, the morning and evening commute in New York City could be less of a time sink if it was optimized better.