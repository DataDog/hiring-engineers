# Solutions Engineer Responses

After reading through the references, I decided to complete the updated Readme since it included an opportunity to play around with the APM features as well as the Flask micro framework. (I was also particularly interested in the last question.) I also answered a few of the bonus questions from the original assignment. My steps, answers and associated screenshots are presented in this Markdown sheet.


##### In your own words, what is the Datadog Agent?

The Datadog agent acts as a messenger, relaying any updates on events and performance metrics from a host (either a local computer or an online host) to Datadog's platform. The agent can fetch these metrics from the any software connected to the host that is configured to integrate with the platform.


## Installation Notes

I installed the Datadog Agent following the installation instructions for OSX featured here:
https://app.datadoghq.com/account/settings#agent/mac

I also edited the Datadog Configuration file datadog.conf to assign my local machine (Frederics-MacBook-Pro.local) as the host.

The agent immediately began collecting local runtime data to be featured on the dashboard. [Screenshot_1](screenshots/Screenshot_1_installation.png) shows the installation running in the terminal.


## Collecting Metrics

### 1. Tags

In the datadog.conf file, I added these three tags: region:east, env:prod, role:test and restarted the agent.

As seen on [Screenshot_2](screenshots/Screenshot_2_tags.png), the tags are viewable on the user interface via the Host Map. Upon hovering over each respective tag, Datadog informs us that the tags were submitted by the Agent.

### 2. MongoDB

With MongoDB already installed on my machine, I decided to integrate this database with my account. After initializing the database and toggling the administrator privileges to allow the authentication process, I successfully integrated MongoDB by following the directions featured here: https://app.datadoghq.com/account/settings#integrations/mongodb.

[Screenshot_3](screenshots/Screenshot_3_mongo.png) & [Screenshot_4](screenshots/Screenshot_4_mongo.png) feature the respective windows showing that I ran the commands in the terminal shell, created and configured the mongo.yaml file, restarted the Agent, and verified if the integration check was successful.

Here is a copy of the code in mongo.yaml

```yaml
init_config:

instances:
    -   server: 		mongodb://datadog:RhJuBT87QH08QK47XtSXxXMt@localhost:27017
          tags:
              - mytag1
              - mytag2
```

### 3. Custom Agent Check

I followed the Agent Checks guide in the documentation to complete this task. Printing a random integer (randint) with python required a method stored in python's (random) library.

I also searched Datadog support and Github in order to find the proper syntax to send the number via the Agent. Two new files were created in the datadog-agent directory--a python script to be placed in the checks.d directory and a yaml (configuration file) to be placed in the conf.d. Here is a copy of each, respectively

randomvalue.py

```python
import random
from checks import AgentCheck
class RandomCheck(AgentCheck):
	def check(self, instance):
		self.gauge('my_metric', random.randint(0,1000))

```

randomvalue.yaml

```yaml
init_config:
  min_collection_interval: 45

instances:
  [{}]
```

#### Can you change the collection interval without modifying the Python check file you created?

From my search, I learned that I could change the interval by providing the following key : value pair in the yaml file:  

min_collection_interval : (the number of seconds) as a key

I set the interval to 45 seconds.

Important: The Agent doesn't directly run the collection exactly at each interval, rather it, checks to see if the script submitted a metric once within the interval's timeframe.


## Visualizing Data

[Screenshot 5](screenshots/Screenshot_5_metrics.png) & [Screenshot 6](screenshots/Screenshot_6_anomaly.png) were taken to capture the Timeboard and the associated metrics requested in the Readme. The two custom metrics are featured on Screenshot_5, and the integration metric with the anomaly function is featured on Screenshot_6. You can also see the snapshots taken using the @ notation.

#### Bonus question: What is the difference between a timeboard and a screenboard?

Since Timeboard capture metrics in a time synchronized fashion and presents their graphs in a more established, grid-like layout, they're perfect for troubleshooting and noticing relationships between related metrics. The widget-like and customizable nature of Screenboards is better suited for presentations and more dynamic analysis of data, as they provide a change to look at a bigger picture. Additionally, the widgets and board featured on a Screenboard can be shared collectively, where as each Timeboard much be shared individually.


#### Bonus Question: What is the Anomaly graph displaying?

Anomaly graphs highlight any new behavior in a metric that is inconsistent from normal patterns. For instance, it can be used to highlight unusually high traffic volumes on a website or unusually high cpu usage on a given host. It works best with metrics that display consistent trends over time.


## Monitoring Data

I created a metric monitor that was configured to trigger warnings and alerts on the status of my custom metric. I successfully configured the three messages to be sent, with the alert state containing a message with the value and host.name also referenced. Screenshot_7 features the proper configuration for the host ip in the message, but getting the Host IP to render is still a work in progress.

[Screenshot_7](screenshots/Screenshot_7_Monitor.png) displays the status tab of the Monitor, featuring the data history and the associated messages for each alert condition. [Screenshot_8](screenshots/Screenshot_8_Email.png) shows the email received when the alert threshold is reached.


#### Bonus Question: Send screenshot of downtime email (Coming shortly!)

## Collecting APM Data

After downloading the Trace Agent, I followed the instructions for Flask, and downloaded the Blinker library. Next, I imported the libraries into the flask application on the ReadMe, exported the file (flaskapp.py) and ran the code using a virtualenv. Here is the final code:

```python
from flask import Flask
import blinker as _

from ddtrace import tracer
from ddtrace.contrib.flask import TraceMiddleware

app = Flask(__name__)
traced_app = TraceMiddleware(app, tracer, service="my-flask-app")

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

To begin collecting application monitoring data, I ran the Trace Agent using the Data Agent configuration:

```
./trace-agent-osx-X.Y.Z -ddconfig /opt/datadog-agent/etc/datadog.conf
```

[Screenshot_9](screenshots/Screenshot_9_APM-Infrastructure.png) shows a Dashboard that I created featuring APM and Integration Data.


Link to the Dashboard: https://app.datadoghq.com/dash/371903/apm--infrastructure-metrics


#### Bonus Question: What is the difference between a Service and a Resource?

A resource refers to a piece of code, usually either a query in a database or a route in an application, that can be experienced within a service. The service is the set of processes usually containing different resources.

In this case for instance, the service is a web application labeled "my-flask-app." Three designated resources in this application would be the three routes present in the script, in addition to any error routes (404) that may be traced.

## Final Question

#### Is there anything creative you would use Datadog for?

I think the efficiency of Datadog's monitoring software would work really well with a restaurant application. I'd imagine you could use the tool to create a restaurant management assistant that keeps track of typical restaurant upkeep, including the amount of customers in the restaurant at a given time, the order quantity for an item on the menu, the items on the menu that are still available, and the stage each customer is at in the meal (starter, entree, dessert).

Additionally, the application would provide useful data for monitoring when the restaurant performs best and when each item is most likely to be chosen by a customer, allowing you to detect any anomalies, improve overall processes and alert the restaurant team if there are any emergencies. 
