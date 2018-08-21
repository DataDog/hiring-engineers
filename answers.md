
# My solution to the Solutions Engineer questions
## - Hetansh Madhani

### Prerequisites - Setup the environment:
I used Ubunut 18.04 as my operating system which I started in VM VirtualBox

I used the command given on the Datadog Installation Docs:
```
DD_API_KEY=YOUR_API_KEY bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```
Where I used the API key I found after creating the account and replaced it in the command above at *YOUR_API_KEY*
- - - -
### Collecting Metrics:
#### Question: Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
#### Adding tags in the agent config file.

I needed to edit the _datadog.yaml_ file to add the tags. Here is the snapshot of the file after editing.
![Tags Configured File](https://s3.amazonaws.com/solutions-engineer-photos/tag_file.png)

Here is the screenshot of my host and its tags on the Host Map page in Datadog Agent reflecting the tags I added in the config file.
![Tags Reflected in Agent](https://s3.amazonaws.com/solutions-engineer-photos/tags_agent.png)
- - - -
#### Question: Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

For this task I decided to go with PostgreSQL. I installed PostgreSQL on my ubuntu machine using the following command:
```
sudo apt install postgresql postgresql-contrib
```
I followed the integration steps found in the agent as well the Datadog Support Documents on the official Website
https://docs.datadoghq.com/integrations/postgres/

I had to create and edit the *__postgres.yaml__*  file in *__conf.d/postgres.d/__* to make the agent collect PostgreSQL metrics and logs
![PostgreSQL Configured File](https://s3.amazonaws.com/solutions-engineer-photos/postgres_yaml.png)

I could see the integration was successful in the agent. 
![PostgreSQL Success in Intergrations](https://s3.amazonaws.com/solutions-engineer-photos/post_success.png)
![PostgreSQL Showed in Host](https://s3.amazonaws.com/solutions-engineer-photos/postgres_agent.png)
- - - -
#### Question: Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
To write and create a custom Agent check I referred the following guide on the Official Docs:
https://docs.datadoghq.com/developers/agent_checks/

I had to create 2 files:
   - *__my_metric.yaml__* in *___conf.d/__* for configuring the agent check 
   - *__my_metric.py__* in *___checks.d/__* for writing the what the agent check is suppose to do

*__my_metric.py__* is as shown:

![Custom Agent Check Metric File](https://s3.amazonaws.com/solutions-engineer-photos/new_agent.png)

*__my_metric.yaml__* is as shown to include the 45 sec time interval:

We do that by adding ``` -min_collection_interval: 45 ```

![Custom Agent Check Configuration File](https://s3.amazonaws.com/solutions-engineer-photos/check_yaml.png)

We can check that the agent is posting once every 45 seconds from referring the logs:

![Custom Agent Check Logs](https://s3.amazonaws.com/solutions-engineer-photos/custom_agent.png)
- - - -
#### Bonus Question Can you change the collection interval without modifying the Python check file you created?

I dont think so. I think one way would be to change the main check interval. But I am not sure about it.

### Visualizing Data: 
#### Question: Utilize the Datadog API to create a Timeboard
Here is my code to create the timeboard as asked
```
from datadog import initialize, api

options = {
    'api_key': '412d911e8166a2a1488c6fc8206b51cc',
    'app_key': 'aff723d2f7496c25a98ef3ca13d0cf342533e462'
}

initialize(**options)

title = "My Solutions Engineer Timeboard"
description = "Timeboard for solutions engineer task"
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{host:Hetansh-Ubuntu-VirtualBox}"}
        ],
        "viz": "timeseries"
    },
    "title": "My Metric average over host: Hetansh-Ubuntu-VirtualBox"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:postgresql.commits{*}, 'basic',2)"}
        ],
        "viz": "timeseries"
    },
    "title": "PostgreSQL Commits"
},{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{*}.rollup(sum,3600)"}
        ],
        "viz": "timeseries"
    },
    "title": "My Metric rollup visualization with time 1hr"
}]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:my-host"
}]

read_only = True
resp = api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)
```

This created the timeboard with timeframe as 5 mins as shown in the image: 

![The Timeboard](https://s3.amazonaws.com/solutions-engineer-photos/timeboard.png)

To see the roll up function of 1hr applied to my_metric I changed the timeframe to past 4 hrs to see 4 values of each hour as:

![The Timeboard](https://s3.amazonaws.com/solutions-engineer-photos/roll_up.png)

#### Question: Take a snapshot of this graph and use the @ notation to send it to yourself.

Sending the graph to myself and also getting notified on email: 

![The Timeboard](https://s3.amazonaws.com/solutions-engineer-photos/atonation.png)
![The Timeboard](https://s3.amazonaws.com/solutions-engineer-photos/events.png)
![The Timeboard](https://s3.amazonaws.com/solutions-engineer-photos/email_anot.png)

#### Bonus Question: What is the Anomaly graph displaying?
The metrics are variable and it keeps on changing everytime. Figuring out what change, or what value of a metrics is abormal
or should trigger a alert is a tough task. Anomaly graph shows us the expected behavior of that particular value based on the historic
values of that metrics. It takes into account the past data corresponding to that day, time of day, etc. to give a gray band which covers
the range of the metric value expected to be normal. Anything outside the grey band is considered not normal.

### Monitoring Data:

I created a new Metric Monitor that watches the average of my custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:
- Warning threshold of 500
- Alerting threshold of 800
- And also ensure that it will notify you if there is No Data for this query over the past 10m.
The settings are as shown in the image below:
![The Metric Monitor Settings](https://s3.amazonaws.com/solutions-engineer-photos/monitor.png)

Here is the Monitor's custom message:
```
{{#is_warning}}
Your metric my_metric has gone above  {{warn_threshold}}! Your metric is {{value}}.
{{/is_warning}} 

 {{#is_alert}}
Your metric my_metric has gone above  {{alert_threshold}}! Your metric is {{value}} on host IP: {{host.ip}}
{{/is_alert}} 

 {{#is_no_data}}
Your metric has stopped sending data for 10 Minutes. 
{{/is_no_data}} 
Notify @thenormalengineer@gmail.com
```
Here is the image of an alert email to me:
![The Alert Email](https://s3.amazonaws.com/solutions-engineer-photos/monitor_email.png)

Two scheduled downtimes for monitor:
1. Weekday 7:00pm to 9:00am
![The Alert Email](https://s3.amazonaws.com/solutions-engineer-photos/downtime_4.png)
2. No alerts from Friday 7:00pm to Monday 9:00am (Weekend)
![The Alert Email](https://s3.amazonaws.com/solutions-engineer-photos/downtime_3.png)

The downtime email sent to me:

![The Alert Email](https://s3.amazonaws.com/solutions-engineer-photos/downtime_email.png)


----
#### Collecting APM Data:
First I needed to install ddtrace to trace the flask app for which I used pip install
```
pip install ddtrace
```
Next to integrate APM tracing for flask app I refered the flask documentation given on:
http://pypi.datadoghq.com/trace/docs/#module-ddtrace.contrib.flask

The code for my final flask app is as:
```
from flask import Flask
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

Next I needed to edit the config file to enable APM

![The Apm](https://s3.amazonaws.com/solutions-engineer-photos/aom_config.png)

Then run the flask app using the code:
```
ddtrace-run python apm_trail.py
```
I could find the service and the trace in the APM section:
![The Apm](https://s3.amazonaws.com/solutions-engineer-photos/apm_trace.png)
![The Apm](https://s3.amazonaws.com/solutions-engineer-photos/apm_service.png)

Here is a screenshot of a dashboard with APM metrics and Infrastructure Metrics:
![The Apm](https://s3.amazonaws.com/solutions-engineer-photos/apm_dashboard.png)

The public url : https://p.datadoghq.com/sb/8cfa517e3-ac04059d152f1e940e1394d187e198ce

#### Bonus Question: 
#### What is the difference between a Service and a Resource?
A Service is the name of a set of processes that work together to provide a whole feature like a web application. 
It may contain different things like database connection, admin section and different processing 

A resource is defined by its URL and definition of inputs/outputs for every operation supported by a resource.
Unlike a service, where methods are completely independent and can be deployed as independent endpoints, methods on a resource
have to exist on the same URL

----

##Final Question
#### Datadog has been used in a lot of creative ways in the past. 
We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!
Is there anything creative you would use Datadog for?

I think use of datadog to monitor traffic would be a really cood idea. Not just vehicle traffic but also pedestrain traffic. 
It would be cool to see the traffic to my way home from a datadog dashboard, or for the surrounding areas.
We can have sensors to calculate foot traffic, who's data can be monitored by datadog and can be used in many interesting ways,
for example, a advertising company can look at the number of people walking and control the digital ads dynamically based on the foot traffic.


