Your answers to the questions go here.

# Prerequisites - Setup the environment
In order to set up my environment I used [Oracle VM VirtualBox](https://www.virtualbox.org/), [Ubuntu Server 16.04.3](https://www.ubuntu.com/download/server), and [Docker](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-16-04) on my Lenovo laptop.  I actually ran into a complication, which was that my VM would not install a 64-bit Ubuntu server, which prevented me from obtaining Docker.  My laptop runs 64-bit Windows, so I figured there had to be some setting preventing me from installing the 64-bit Ubuntu server.  After some research, I figured out that the [Intel Virtualization Technology](http://www.fixedbyvonnie.com/2014/11/virtualbox-showing-32-bit-guest-versions-64-bit-host-os/#.WlEbyt-nGUk) was disabled.  After going into the bios and enabling the feature, I was able to install all the prerequisites needed for this challenge.


# Collecting Metrics:

### Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
I achieved this through the datadog portal.  I reviewed the [tagging](https://docs.datadoghq.com/agent/tagging/) documentation in DataDog and followed the instructions to add the tags in the UI. I attached the picture as hosttags.png:

![alt-text](https://raw.githubusercontent.com/DataDog/hiring-engineers/2f2b5fb699e83f58c390a6c1eaccd74d9347457c/hosttags.png "Host with 2 tags")

### Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
I installed [MongoDB](https://www.howtoforge.com/tutorial/install-mongodb-on-ubuntu-16.04/).  This part took me a while to complete.  While following the integrations guide in the UI, I was getting a connection failure to port 27016.  I decided to look at [Datadog Documentation](https://docs.datadoghq.com/integrations/mongo/) and noticed that only one port was used, 27017.  Once I updated my mongo.yaml file, I was getting an error that I was not using a replSet.  Below is the mongo.yaml file I created:
```python
init_config:

instances:
  - server: mongodb://datadog:{password}:27017/admin
```
I researched [replset on mongodb](https://docs.mongodb.com/v3.2/tutorial/deploy-replica-set/) and decided to run rs.initiate in mongo.  The first error code I got was 76.  Looking up this error in [stack overflow](https://stackoverflow.com/questions/32952653/replica-set-error-code-76), I realized I needed to set a replset name in my /etc/mongod.conf file.  I added the following code into my mongod.conf file:
```python
replication:
  replSetName:"greg1"
```
After creating the replSetName, I restarted MongoDB and tried rs.initiate() again.  However, I got another error code, 93.  I also looked up this error in [stack overflow](https://stackoverflow.com/questions/28843496/cant-initiate-replica-set-in-ubuntu) and found out that sometimes when MongoDB is installed, they have the wrong IP address for the host name.  I looked at /etc/hosts and noticed that the file had the ip 127.0.1.1 for my host (I commented it out with # below).  I changed the IP to 127.0.0.1, restarted mongo again, and rs.initiate ran as expected!  I restarted the DD agent and the check came out OK!  I installed the MongoDB integration and noticed metrics were coming in!

### Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
#### * Change your check's collection interval so that it only submits the metric once every 45 seconds.
#### * Bonus Question Can you change the collection interval without modifying the Python check file you created?
I researched https://docs.datadoghq.com/agent/agent_checks/ in order to complete this section.  I attached the code accordingly for the check and the python code.  I was not able to modify the collection interval without modifying the check file.  I tried to see how to write in python to submit the metric every 45 seconds, but I was unable to do so and added the interval time in the yaml file accordingly.  The code used is in checkvalue.py and checkvalue.yaml

checkvalue.py:
```python
import random
from checks import AgentCheck
class HelloCheck(AgentCheck):
  def check(self, instance):
    self.gauge('my_metric'), random.randint(1,1000))
```

checkvalue.yaml:
```
init_config:

instance:
  [{min_collection_interval: 45}]
```
# Visualizing Data:
Utilize the Datadog API to create a Timeboard that contains:

### Your custom metric scoped over your host.
I used postman in order to complete the CURL command to create the custom metric chart.  To see what was needed for the chart, I first looked up the documentation to look up [how to chart in the UI](https://docs.datadoghq.com/graphing/).  Seeing that a JSON is presented, I used the JSON template from the chart I created to create a [timeboard using the API](https://docs.datadoghq.com/api/?lang=python#timeboards):
```JSON
{"title": "Sum of My_Metric",
       "definition": {
       	"events": [],
       	"requests": [
     {
       "q": "sum:my_metric{*}.rollup(sum, 60)",
       "type": null,
       "style": {
         "palette": "dog_classic",
         "type": "solid",
         "width": "normal"
       },
       "conditional_formats": [],
       "aggregator": "sum"
     }
```

The request used was https://app.datadoghq.com/api/v1/dash?api_key={api_key}$application_key={app_key}.  The JSON is in the third part of this section as I put all charts on the same timeboard.  Below is a picture of the graph in the timeboard:
  
  ![alt-text](https://raw.githubusercontent.com/DataDog/hiring-engineers/f50388e55df917616b7095250863b9fcaa9bfd9e/Graph%201.png)


### Any metric from the Integration on your Database with the anomaly function applied.


### Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket. Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timemboard.
  Repeating the steps as in the first chart, I was able to use the JSON below to create the graph and the timeboard:
  ```JSON
 {
     "graphs" : [{
         "title": "My Metric Over Host",
         "definition": {
             "events": [],
             "requests": [
                 {"q": "avg:my_metric{host:dd}"}
             ]
         },
         "viz": "timeseries"
     },
          {"title": "Sum of My_Metric",
     "definition": {
     	"events": [],
     	"requests": [
   {
      "q": "sum:my_metric{host:dd}.rollup(sum, 3600)",
      "type": "line",
      "style": {
        "palette": "dog_classic",
        "type": "solid",
        "width": "normal"
      },
      "conditional_formats": [],
      "aggregator": "avg"
    }
  ],
  "viz": "timeseries",
  "autoscale": true
}
     },
     {"title": "MongoDB with anomaly function",
     	"definition": {
     		"events": [],
     		"requests": [
    {
      "q": "anomalies(sum:mongodb.uptime{*}, 'basic', 2)",
      "type": "line",
      "style": {
        "palette": "dog_classic",
        "type": "solid",
        "width": "normal"
      },
      "conditional_formats": [],
      "aggregator": "avg"
    }
  ],
  "viz": "timeseries",
  "autoscale": true
     	}
     }],
     "title" : "API Dashboard Visual Challenge Charts",
     "description" : "A dashboard made via API.",
     "read_only": "False"
   }
 ```
This was the dashboard after creation:
![alt-text](https://raw.githubusercontent.com/DataDog/hiring-engineers/f50388e55df917616b7095250863b9fcaa9bfd9e/Dashboard.png)
Once this is created, access the Dashboard from your Dashboard List in the UI:

### Set the Timeboard's timeframe to the past 5 minutes.  Take a snapshot of this graph and use the @ notation to send it to yourself.
 This is the graph that shows the value.  The number is small because I capture it within the 5 minute interval:
 ![alt-text](https://raw.githubusercontent.com/DataDog/hiring-engineers/f50388e55df917616b7095250863b9fcaa9bfd9e/Graph%202.png)

### Bonus Question: What is the Anomaly graph displaying?
 Since I was not able to display the anomaly graph, I was not able to attempt this bonus question.

# Monitoring Data

### Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

#### * Warning threshold of 500
#### * Alerting threshold of 800
#### * And also ensure that it will notify you if there is No Data for this query over the past 10m.
### Please configure the monitor’s message so that it will:

#### * Send you an email whenever the monitor triggers.

#### * Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.

### Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.

### When this monitor sends you an email notification, take a screenshot of the email that it sends you.
Being from Catchpoint, this was the easiest section for me to accomplish.  By playing around with the UI, I went directly to monitors in order to create the alert.  Below is the screenshot of the warning and alert thresholds:
![alt-text](https://raw.githubusercontent.com/DataDog/hiring-engineers/6a7e86e6dcf807039e9d0fef80b3128dfb3dfa95/monitorsetup.png)

In order to create different messages, I reviewed the [notifications](https://docs.datadoghq.com/monitors/notifications/) document.  I was able to create the following that provided my IP address of the VM and the value:
![alt-text](https://raw.githubusercontent.com/DataDog/hiring-engineers/6a7e86e6dcf807039e9d0fef80b3128dfb3dfa95/markdownscript.png)

It did not take long to get an email with the alert triggered:
![alt-text](https://raw.githubusercontent.com/DataDog/hiring-engineers/6a7e86e6dcf807039e9d0fef80b3128dfb3dfa95/email.png)

### Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

#### * One that silences it from 7pm to 9am daily on M-F,
#### * And one that silences it all day on Sat-Sun.
### Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.
When creating the monitor, I noticed a section for downtime.  I clicked on manage downtime, and started playing around in the area.  After creating the downtime schedules, I checked the following night and confirmed I received the email:

![alt-text](https://raw.githubusercontent.com/DataDog/hiring-engineers/6a7e86e6dcf807039e9d0fef80b3128dfb3dfa95/downtime.png)

# Collecting APM Data:
### Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution
#### Note: Using both ddtrace-run and manually inserting the Middleware has been known to cause issues. Please only use one or the other.
Being unfamiliar with python and class, I first took the class in [CodeAcademy](https://www.codecademy.com/learn/learn-python) in order to understand the basics of the language.  After that was done, I researched [how to run a flask app onto Ubuntu] Server(https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-16-04).  Using the code provided in the challenge, I applied the middleware using the method above to create the flask app.  Below is the code for the app:
```python
from flask import Flask
import logging
import sys
import blinker as _

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

traced_app = TraceMiddleware(app, tracer, service="my-flask-app", distributed_tracing=False)

@app.route('/')
def api_entry():
    return '<h1>Entrypoint to the Application</h1>'

@app.route('/api/apm')
def apm_endpoint():
    return 'Getting APM Started'

@app.route('/api/trace')
def trace_endpoint():
    return 'Posting Traces'

if __name__ == '__main__':
    app.run(host='0.0.0.0')
```
### Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.
Having experience with expressJS, I tested these routes accordingly in order to get data in the UI.  I had difficulty finding what is an APM metric vs what is an Infrastructure Metric.  I did see APM metrics and used the number of hits:

![alt-text](https://raw.githubusercontent.com/DataDog/hiring-engineers/ded04116e233f997413aa03306e40d93c6e6c760/APM%20and%20Infrastructure.png)

### Bonus Question: What is the difference between a Service and a Resource?
 I looked online to look for this answer.  Luckily, I found a [datadog document](https://help.datadoghq.com/hc/en-us/articles/115000702546-What-is-the-Difference-Between-Type-Service-Resource-and-Name-)! A "Service" is defined by the user when implementing an application.  These services are one or more processes that work together to provide a feature set.  Some examples of services are database and webapp.  These help distinguish what process each service provides.  A "Resource" is a query for a service. An example of a resource is a URL request to get a particular service.  In order to observe the resources, you must first visit the particular service.

# Final Question:
### Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability! Is there anything creative you would use Datadog for?
As mentioned, DataDog has beatend me to the blog post about Pokemon Go when it went down.  DataDog allows companies to measure performance of their applications.  Being a gamer myself, it would be interesting seeing how MOBA/online games use DataDog.  An interesting way would be with League of Legends and their matchmaking.  Not long ago, League of Legends updated their infrastructure to have all players go directly from their internet ISP to their services.  They were frustrated with ISP's they could not control, and wanted to make sure that if there was a problem, they could fix it.  With this change, I would also assume that a lot of their backend code has changed.  DataDog could measure the performance of the backend to see the improvement and if their servers are able to handle all the direct bandwidth.

A lot of companies are now concerned about Markdown and Spectre since this can decrease performance by 30%.  Datadog can help monitor and make sure apps are not effected by these bugs.
