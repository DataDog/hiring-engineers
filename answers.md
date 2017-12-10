<h1>Table of Content</h1>
1. Intalling Datadog Agent
1. Create Tags on Agent
1. Configuring Database
1. Creating Custom Metric
1. Create Timeboard with Datadog API
1. Monitoring Data
1. Collecting APM Data
1. Final Thoughts About the Task
  
<h2>Installing Datadog Agent</h2>
  
<h2>Create Tags on Agent</h2>
To show that your machine is currently being monitored, it has to tagged to be shown on the Host Map. 

In your command prompt with in `vagrant ssh`

Type in `sudoedit /etc/dd-agent/datadog.conf`

Press `CRTL + V` until you see the line below.

#tags: country:au, state:nsw, role:database

Remove the "#" and add the tag of your choice, in my case it looks like above.

![screenshot](https://raw.githubusercontent.com/FantasyStarr/hiring-engineers/master/sudoeditagent.PNG)

Press CTRL + X , Press Y then Enter to save the changes.
 
[Go to your Host Map by clicking here](https://app.datadoghq.com/infrastructure/map)

<h2>Configuring Database</h2>

Install my SQL with the commands below

`sudo apt-get update`<br>
`sudo apt-get install mysql-server`<br>
`/usr/bin/mysql_secure_installation`<br>

Access MySQL by using `/usr/bin/mysql -u root -p`

Following the configuration steps in the link below. This will be for MYSQL integation.

https://app.datadoghq.com/account/settings#integrations/mysql 

This didn't work for me, so I followed the steps in the knowledge base.

https://docs.datadoghq.com/integrations/mysql/

![screenshot](https://raw.githubusercontent.com/FantasyStarr/hiring-engineers/master/mysqlsuccess.PNG)
![screenshot](https://raw.githubusercontent.com/FantasyStarr/hiring-engineers/master/mysqlverification.PNG)

<h2>Creating Custom Metric</h2>
 
 The basic creation of a random number generator being returned as a metric on Datadog dashboard is made by following this link
 
 https://docs.datadoghq.com/guides/agent_checks/
 
Create two files using the commands below<br>

`sudo touch /etc/dd-agent/conf.d/my_metric.yaml`<br>
`sudo touch /etc/dd-agent/checks.d/my_metric.py`

Edit the my_metric.py with the code below
```python
import random
from checks import AgentCheck

class randomCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', random.randint(0,1000))
```
Edit the configuration my_metric.yaml file with the code below
```yaml
init_config:
 min_collection_interval: 45
instances:
    [{}]
```

Reset the agent and view the custom metric in your host map or the metric summary page
![screenshot](https://raw.githubusercontent.com/FantasyStarr/hiring-engineers/master/customMetric.PNG)
![screenshot](https://raw.githubusercontent.com/FantasyStarr/hiring-engineers/master/customMetricCollect.PNG)

<h2>5. Create Timeboard with Datadog API</h2>

https://docs.datadoghq.com/api/#timeboards Used as an reference to create a basic timeboard and editted 

Used https://docs.datadoghq.com/guides/anomalies/ to run anomalies function

Following the reference in the link below will make a timeboard with our custom metric, any MySQL Metric with the anomaly function, and a sum of of custom metrics within the last hour.

Ran into a problem with Python, but updating it fixed the issue. I've received SNIMissingWarning & InsecurePlatformWarning while running the script, but it appeared to have not affected the overall script as the dashboard was generated.

The script below was ran using the `python ./[filename]` command

```python
from datadog import initialize, api

options = {
    'api_key': '[api]',
    'app_key': '[app]'
}

initialize(**options)

title = "Custom Metric and MYSQL"
description = "An informative timeboard."
graphs = [
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{*} by {precise64}"}
	
        ],
    "viz": "timeseries"
    },
    "title": "My Custom Metric for Host"
},
{
    "definition": {
        "events": [],
        "requests": [
	    {"q": "anomalies(avg:mysql.performance.cpu_time{*}, 'basic', 2)"}
        ],
    "viz": "timeseries"
    },
    "title": "MySQL CPU Perfomance with Anomaly Detection"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "my_metric{*} by {precise64}.rollup(sum, 3600)"}
        ],
    "viz": "timeseries"
    },
    "title": "Sum of Custom Metric within past hour"
}
]


template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:my-host"
}]

read_only = False

api.Timeboard.create(title=title, description=description, graphs=graphs, template_variables=template_variables, read_only=read_only)

```

If this script ran correctly, it should look something like the image below [or click here](https://app.datadoghq.com/dash/417964/custom-metric-and-mysql?live=true&page=0&is_auto=false&from_ts=1512863051946&to_ts=1512866651946&tile_size=m&tpl_var_host1=*)

![screenshot](https://raw.githubusercontent.com/FantasyStarr/hiring-engineers/master/customTimeboard.PNG)

Using the UI in the Timeframe, we're going to set the timeline to 5 minutes and add notation on the graph.

Setting the timeline to 5 minutes using the keyboard hotkeys `alt + [ / alt + ] : zoom out/in timeframe`

![screenshot](https://raw.githubusercontent.com/FantasyStarr/hiring-engineers/master/5minute.PNG)

Notation can be added by holding shift and clicking on a point of the graph.

![screenboard](https://raw.githubusercontent.com/FantasyStarr/hiring-engineers/master/notation.PNG)

<h3>Bonus Question: What is the Anomaly graph displaying?</h3>

Anomaly graph displays the unusual changes in metric taking in account to all past trends, time of day, time of week etc. This allows monitoring and alerts to be set up. I would use this to find out if somebody is using more network capacity then usual on their machine.

<h2>Monitoring Data</h2>

Following the solution below, we're going to create a monitoring that sends a warning at 500 value and an alert at 800 value.

[Guide to Monitoring](https://docs.datadoghq.com/guides/monitors/) 

Go to the link below to create a monitor for your custom metric

[Link to create monitor for metric](https://app.datadoghq.com/monitors#create/metric)

We're going to select our custom my_metric ,set Alert threshold: 800 & Warning threshold: 500, and send a notification if no data has been generated in the last 10 minutes

![screenshot](https://raw.githubusercontent.com/FantasyStarr/hiring-engineers/master/monitor1.PNG)

To create multiple responses markdown is supported so we could send a different response depending what was breached.
The example of the email is below.

```html
Hi User,

Please note that you are receiving this email for the following:

{{#is_warning}} my_metric has reached above 500. The value of the breach was: {{value}} on the IP address: {{host.ip}}. {{/is_warning}}

{{#is_alert}} my_metric has reached above 800. The value of the breach was: {{value}} on the IP address: {{host.ip}}. {{/is_alert}}

{{#is_no_data}} my_metric has not received any data in 10 minutes {{/is_no_data}} 

Please review your data in the link below.

https://app.datadoghq.com/dash/host/382070538?live=true&page=0&from_ts=1512863554339&to_ts=1512877954339&is_auto=false&tile_size=m

Kind Regards,

Thai Nguyen 
```
[Click on the link to view monitor settings](https://app.datadoghq.com/monitors#3537821?group=all&live=4h)

The email has been sent to my email with the alert, the value and the ip address (Removed my email address for obvious reasons)

![screenshot](https://raw.githubusercontent.com/FantasyStarr/hiring-engineers/master/monitoremailnew.PNG)

Problem I encountered here was I received an email after the value has reached below 500 as a resolution email. Could not find the setting to remove this.

<h3>Bonus Question</h3>
Click the link below to manage downtime. Downtime is needed as you will frequently receive alerts on your monitored metrics.

[Set up Downtime](https://app.datadoghq.com/monitors#downtime)

This is the setting for the weekday downtime and the message.
![screenshot](https://raw.githubusercontent.com/FantasyStarr/hiring-engineers/master/weekday.PNG)
![screenshot](https://raw.githubusercontent.com/FantasyStarr/hiring-engineers/master/weekmessage.PNG)

This is  the setting for the weekend downtime and the message.
![screenshot](https://raw.githubusercontent.com/FantasyStarr/hiring-engineers/master/weekend.PNG)
![screenshot](https://raw.githubusercontent.com/FantasyStarr/hiring-engineers/master/weekendmessage.PNG)

<h2>Collecting APM Data</h2>

Following the solution and guide in the link below, will work with Flask to collect APM Data
[Guide for Flask](http://flask.pocoo.org/docs/0.12/quickstart/)

We used the python code below:

```python
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

Following [this link](https://app.datadoghq.com/apm/docs), we used python to run the script

Run the following commands in the terminal

Run `pip install ddtrace`

Run`ddtrace-run python apmdata.py`

In another terminal we've installed Lynx (text based brower) to connect to our local host 127.0.0.1:5000

Install Lynx `sudo apt-get install lynx`

Connect to localhost `lynx http://127.0.0.1:5000/`

![screenshot](https://raw.githubusercontent.com/FantasyStarr/hiring-engineers/master/apmTerminal.PNG)

I was only able to generate more data by exiting lynx and re-entering it.

If all was completed, you should see this in your APM page

![screenshot](https://raw.githubusercontent.com/FantasyStarr/hiring-engineers/master/APMMetric.PNG)

Link to APM & Infrastructure Dashboard - [Click Here](https://app.datadoghq.com/dash/418005/apm--infrastructure-metrics?live=true&page=0&is_auto=false&from_ts=1512896666359&to_ts=1512900266359&tile_size=l)

<h3>Bonus Question: What is the difference between a Service and a Resource?</h3>
A service is a set of processes that are used to overall provide a feature for an application.
A resource is query within a service.

<h3>Final Thoughts About the Task</h3>


