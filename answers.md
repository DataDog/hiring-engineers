# Solutions Engineer Solutions by Rafaeli Arroyo

## Collecting Metrics:

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

* _For carrying out this step, I ran the browser-based Datadog Agent Manager and added tags (hedgehogs, sloths, whales, sharks) under the "tags" field of "Settings". Initially, I had a bit of trouble in accessing the Datadog Agent Manager until I learned from Datadog docs that the most recent version of the Agent (v6) can be accessed only by running the manager as an administrator. For Agent version 5, it was accessible via a pop-out window._

#### Agent Config File

![Agent Config File](images/agentconfig.png)

_I found my changes reflected on my Datadog agent by viewing it in "Infrastructure" > "Host Map" after restarting the agent._

#### Host Map Visualization

![Host Map Visualization](images/hostmap.png)

* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

_I installed version 3.6.5 of MongoDB for this step, and ran the following commands on the mongo shell for installing its Datadog integration:_

```
use admin
db.auth("admin", "admin-password")
db.createUser({"user":"datadog", "pwd": "NMexkkPoWYv7p4hy86kRyaOG", "roles" : [ {role: 'read', db: 'admin' }, {role: 'clusterMonitor', db: 'admin'}, {role: 'read', db: 'local' }]})
```

_Through these commands, I'm using the MongoDB instance called "admin" and authenticating a read-only administrator for it called "datadog". These steps are necessary for later collecting the instance's metric data. The next step was to produce checks for my MongoDB instance in the form of a configuration file with a .yaml extension. I went to "Checks" > "Manage Checks" section of the Datadog Agent Manager, and attempted to add a check for MongoDB. However, I found that there was no option to add a mongo check on the manager, so instead, I decided to add the configuration file through my local machine which my agent was in sync with. Having the Datadog agent installed on it, it was a viable alternative. Initially, I didn't know what directory to insert the file in, so I had to do a bit of research on what it was. I learned that the location for the agent's checks on an agent's machine is dependent on OS, and since I was using Windows, mine can be found at the directory C:\ProgramData\Datadog\conf.d. There, I found a directory called mongo.d/ in which I produced the following file called conf.yaml, then restarted the agent:_

```
init_config:
instances:
  - server: mongodb://datadog:NMexkkPoWYv7p4hy86kRyaOG@localhost:27017/admin
    additional_metrics:
      - collection       # collect metrics for each collection
      - metrics.commands
      - tcmalloc
      - top
```

_"init_config" represents configurations that are present for every run of the check. "instances" list the individual instances on which the check is run against. In my case, my check would run against my MongoDB instance, my db called "admin". I have additional metrics that I would like to measure, specifically collection data focused on that instance. In order to actually generate collection data, I created 2-3 collections for my admin db and inserted random data into them. I used the following link as reference, which walks through how to start collecting metrics using the MongoDB integration:_

https://docs.datadoghq.com/integrations/mongo/#metrics

#### MongoDB Integration

![MongoDB Integration](images/mongodbintegration.png)

* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

_The following script creates a metric called 'my_metric' for the app 'first'. Its check generates a random value between 0 and 1000. I used https://docs.datadoghq.com/developers/agent_checks/#your-first-check as a reference, which details how to write a check. Specifically, it contains a script that sends a value of 1 for a sample metric. I slightly modified that script for providing the appropriate metric name and also producing the random values:_

**my_metric.py:**

```python
from checks import AgentCheck
from random import randint
class MetricCheck(AgentCheck):
	def check(self, instance):
		self.gauge('first.my_metric', randint(0, 1000))
```

* Change your check's collection interval so that it only submits the metric once every 45 seconds.

_Referring to the same link, defining a numerical value for min_collection_interval in the metric's respective .yaml file (check) got the job done. I was able to verify that the collection interval was set to 45 seconds by viewing my_metric's graph of the app "first" within my host through "Infrastructure" > "Host Map". There, I noticed all corners within the graph, representing point values between 0 and 1000, were separated by 45 units (i.e. 45 seconds), and these values kept being generated as time went by._

**my_metric.yaml:**

```
init_config:

instances:
  - min_collection_interval: 45
```

* **Bonus Question** Can you change the collection interval without modifying the Python check file you created?

_The collection interval can be changed by configuring min_collection_interval of each check instance to a positive numerical value in the metric's .yaml file. After sifting through documentation for Python check files, I was unable to find a method or function that could be used in Python for completing the task, so doing so through the .yaml file is the only way I know of thus far._

## Visualizing Data:

Utilize the Datadog API to create a Timeboard that contains:

* Your custom metric scoped over your host.
* Any metric from the Integration on your Database with the anomaly function applied.
* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

_Referring to https://docs.datadoghq.com/api/?lang=python#timeboards, I utilized its sample template script for completing the above tasks. Before that, I also created the required graph on a timeboard through the Datadog interface directly for fleshing out what data to place within the script's dictionaries according to the API docs. On that interface, when editing a graph of a timeboard, I found a "JSON" tab within its "Edit" section. In the graph's JSON, I found that there is a "requests" field, which is also present in the object defined in "definition" of the API template script. After learning the relationship between the interface's timeboards and API docs, in preparing my script, I went to "APIs" under "Integrations" of the Datadog interface to generate API and app keys for being able to submit metrics to Datadog as well as access Datadog's API. Then, I transferred the JSON request data from the Datadog interface to the script so that the script is now being able to visualize the metrics when run._

**timeboard.py:**

```python
from datadog import initialize, api

options = {
    'api_key': '5077ea49d30f7c6e2b1e47a2eb9e701d',
    'app_key': '07d17cb9388be688455f1e13b8f3067e7a659ca0'
}

initialize(**options)

title = "My Metric Data + MongoDB Collections"
description = "Values generated every 45 sec + MongoDB collections."
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:first.my_metric{*}"},
            {"q": "anomalies(avg:mongodb.stats.collections{*}, 'basic', 2)"},
            {"q": "avg:first.my_metric{*}.rollup(sum, 3600)"}
        ],
        "viz": "timeseries"
    },
    "title": "Random Values Over Time"
}]

template_variables = [{
    "name": "timeboard",
    "prefix": "my_metric",
    "default": "host:Ralph-PC"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)


```

Once the Timeboard is created, access the Dashboard from your Dashboard List in the UI:

* Set the Timeboard's timeframe to the past 5 minutes

_I did this by manually highlighting a fraction of the graph's window until a 5 minute interval was created, displaying the data for that time frame._

#### Generated Timeboard (last 5 minutes)

![Generated Timeboard](images/last5min.png)

Timeboard link: https://app.datadoghq.com/dash/834868/

* Take a snapshot of this graph and use the @ notation to send it to yourself.

_This is done by clicking the camera icon at the top-right corner of the graph and @'ing the user you would like to send the graph to._

#### Timeboard Emailed to Self

![Emailed Timeboard](images/senttimeboard.png)

* **Bonus Question**: What is the Anomaly graph displaying?

The anomaly graph displays the metric visualization plus any areas that deviate from the expected flow of data (in the case of my graph, deviations are colored red). Since my timeboard was visualizing Mongo collection data for my admin db, an anomaly occurred as I was generating more collections for that db since initially, there were little to none within the time frame.

## Monitoring Data

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

* Warning threshold of 500
* Alerting threshold of 800
* And also ensure that it will notify you if there is No Data for this query over the past 10m. (shown in 2nd screenshot in this section)

_I created a monitor by selecting "New Monitor" under "Monitors" of the Datadog interface and making the following configurations:_

![Monitor Config](images/monitorconfig.png)

Please configure the monitor’s message so that it will:

* Send you an email whenever the monitor triggers.
* Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
* Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.

_By expanding "Use message template variables" above the message window, the user is able to view examples for configuring messages depending on the monitor state. Through this, I learned that the host's IP and name can be obtained through {host.ip} and {host.name} respectively for the host defined in earlier field of the monitor's interface. I initially struggled with obtaining the host IP for the notifications, but I was able to solve that problem by learning that I mistakenly forgot to define a host (my host) in the very first section of the monitor config. Encapsulating messages between starting and ending labels enclosed by "{{ }}" allows for different kinds of messages. Also, in typing "{{#", a drop-down menu appears displaying what labels are available to choose from. Using that menu as guidance, I was able to configure different messages depending on if the monitor triggered on an Alert, Warning, or No Data state._

![Monitor Messages](images/monitormessages.png)

* When this monitor sends you an email notification, take a screenshot of the email that it sends you.

![Monitor Email](images/monitoremail.png)

* **Bonus Question**: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

  * One that silences it from 7pm to 9am daily on M-F,

  ![Downtime during Weekdays](images/downtimeweekdays.png)

  * And one that silences it all day on Sat-Sun.

  ![Downtime during Weekends](images/downtimeweekends.png)

  * Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

  ![Emailed Downtime](images/downtimeemail.png)

_In this section, I navigated to "Monitors" > "Manage Downtime" > "Schedule Downtime". From the intervals mentioned, I created two recurring downtimes. The first one silences the monitor from 7pm to 9am daily M-F, so I had this monitor occur every 1 week, and selected all days M-F. This downtime would start 7pm and last till 9am, so the duration would be 14 hours. The second downtime was a bit trickier to configure. Establishing a uniform downtime for several days seems straightforward after establishing the first downtime, however with just the first downtime alone, the monitor would become active on Saturday 9am onwards after being inactive 14 hours previously from the day before. Having a 24-hour downtime for Saturday and Sunday was my initial thought, however that would mean that the monitor would be active 12am onwards on Monday, which ideally is not what we would want. The true interval we'd want concerning weekend downtime is to have downtime from Friday 7pm till Monday 9am. It's an interval that I thought would be best represented in hours rather than days, since we still want downtime after Sunday is over. Therefore, I configured the second downtime to cover that interval (62 hours)._

## Collecting APM Data:

_Since I was using Windows, the Trace Agent was pre-packaged with my Datadog agent and no extra configuration was needed according to https://docs.datadoghq.com/tracing/setup/. The dashboard I generated for this section visualizes the number of request hits and their duration times for the provided Flask app. After running ddtrace-run on the following script, I accessed the app's apm and trace routes multiple times on my browser to collect trace data for my host, which I later rendered on a Timeboard:_

**my_app.py:**

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
    app.run(host='192.168.1.7', port='5050')

```

#### Dashboard containing APM and Infrastructure Metrics

_For comparing APM with infrastructure metrics, I first went to "Infrastructure" > "Infrastructure List" then selected my host. I selected the gear icon at the very top right of the displayed dashboard and selected "Clone Dashboard". Afterwards, by going to "APM" > "Traces", I was able to view the names and types of metrics (prefixed "trace.flask") collected from having accessed my Flask app's routes multiple times. Finally, I went to my cloned dashboard and created an additional graph with metrics collecting data pertaining to request hits and duration times for the app._

![dashboard](images/apm_infra_metrics.png)

Dashboard link: https://app.datadoghq.com/dash/834046

* **Bonus Question**: What is the difference between a Service and a Resource?

A service is a set of processes that drive an application or system, and a resource is a specific action that is carried out to fulfill that service. Let's take a restaurant as an example. There are often two primary services at restaurants: customer-engagement (hosts, servers) and kitchen workers (chefs, cleaners). The customer engagement team is in charge of greeting customers, seating them, and taking their orders, all of which are resources for that particular service. The resources of the kitchen workers consist of making food based off of customer orders and cleaning kitchen utensils for re-usability.

## Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?

I'd love to use Datadog to give me an idea of my app usage on my phone during my free time! I want to be fully aware of how I tend to use my phone on a day-to-day basis when I'm not working, since there are moments where I tend to open up apps like Facebook or Twitter without thinking about why I'm doing so. Because of that, I tend to lose track of how much time passes when I use my phone at times when I realize that I really don't need to. It's a habit that I'm sure a lot of people can relate to as well. If Datadog could provide information to people regarding how many times they open up certain apps on their phones AND how much time passes while they are actively navigating said apps, I think it would really help them understand how they are spending their free time and shape how they want to address their individual priorities in the future. Of course, this information should be accessible to the owner of the phone only and not anyone else, so the experience is personalized specifically for that individual. Since the information is personalized, maybe people would be inspired to develop or use notification systems, whether they are concrete or just apparent on the person's mind, to establish their own thresholds letting them know if they're using their phones more often than they think they should.