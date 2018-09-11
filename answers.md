# Solution Engineer Take Home Test Answers

## Environment setup

For this exercice, I chose to setup a Ubuntu 16.04 VM. In order to setup the agent on the VM, I used the datadog instructions to install the following script :
```
DD_API_KEY=7a949afa3aecc29828c96b90e0fa440f bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```
## Collecting Metrics

1. To add tags to the agent, we can add them as follows in the `datadog.yaml` configuration file found in the ``/etc/datadog-agent/`` folder :

```yaml
tags: owner:homere, region:fr, role:database
```


Adding the tags to the config file will reflect on the Hostmap below (In the Datadog dashboard, navigate to **Infrastructure>Hostmap**):

![enter image description here](https://lh3.googleusercontent.com/MtKMwzmq77LkxWpyKlyhgWvyYbFRY6q08zqV1Nw9ZZIL5OhyFVfjctLMi_l7FLK65yIYaa-wiapb "Hostmap")

2. I chose to install the latest version of MongoDB on my host, and then configuring its corresponding integration with Datadog. This is a two part process:
* Creating a new datadog user in the admin table in MongoDB as follows : 
```
use admin
db.auth("admin", "admin-password") 
db.createUser({"user":"datadog", "pwd": "password", "roles" : [ {role: 'read', db: 'admin' }, {role: 'clusterMonitor', db: 'admin'}, {role: 'read', db: 'local' }]})
 ```
 
* Adding my MongoDB instance in the ``conf.d/mongo.yaml`` configuration file as follows: 
```yaml 
init_config: 
instances: - server: mongodb://datadog:password:27017 
```
I also had to make sure, in order for the communication between the Datadog agent and MongoDB to work that the MongoDB application would be reachable from a remote server, by binding the the database server to the necessary IP interfaces, and opening the 27017 port on my VM.

Once the integration was configured successfully, the ``datadog-agent status`` command return the following status for mongo:
![enter image description here](https://lh3.googleusercontent.com/hkEO6c8R7Msj9eHNMKHdSUOmcRYO66xIuH6D8eMNEv9AnH_BtekM3MS4pBu-UTZfv-4r9zmjxi9N "MongoDB integration successful")

The integration on the Saas platform also showed as successful :
![enter image description here](https://lh3.googleusercontent.com/KLaAhPY2i83XBfbqe8IjJQmpQO5j4OEoyBLTLwHItKKFUN9-Y243VTzPHpFs286pwmDQ_Hyai8eP "Integration successful")
3. To create a custom agent check, it is necessary to create two files : 
- A Python check file, to be placed in the  ``/etc/datadog-agent/checks.d/`` folder
-  A corresponding configuration file in the  ``/etc/datadog-agent/conf.d/``
These two files must have matching names.

The configuration file, ``/etc/datadog-agent/conf.d/my_metric.yaml``, is as follows:
```yaml
init_config:
		
instances:
	    [{}]

```

The code for the custom python Agent check that submits a metric named my_metric with a random value between 0 and 1000 , which goes in ``/etc/datadog-agent/checks.d/my_metric.py`` is as follows: 

```python
from checks import AgentCheck
import random
class MyCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', random.randint(0,1000))
```
The new metric graph should now appear in the hostmap dashboard when clicking on the (no-namespace) metric in the host hexagon:
![enter image description here](https://lh3.googleusercontent.com/Gc3TNDWRfdP8xbr69f6OQDjz_o06XLIvYRKz9E1M1o5T8PYe3FlK1ZllZbbz25W9uXSuZn5lRkrX "My_metric appearing in metrics")


4. According to the Datadog documentation, the default collection interval is set to 15-20 seconds. To change to collection interval to 45 seconds, we can change the ``my_metric.yaml`` file, by adding a ``min_collection_interval`` key set to 45:
```yaml
init_config:
		min_collection_interval: 45
instances:
	    [{}]

```
### Bonus:
It's possible the change the collection interval without changing the Python check file by simply changing the check configuration file like shown above.

## Vizualising Data

1. Creating the Timeboard

In order to create a Timeboard through the Datadog API, I read the following [documentation](https://docs.datadoghq.com/api/?lang=python#timeboards) . I decided to write a Python script that executes a POST request  to the API to create the Timeboard. 

The first step in this script is to define the **API key** and the **App key** used to access Datadog's API for this specific scripts. These keys can be found in the **Integrations>APIs** page. It is necessary to create a new application key for our script. I called mine "timeboard".

![enter image description here](https://lh3.googleusercontent.com/zSJSSiSJl_lX0B8yzA0jL-slWS6zS-gSxluDFSTMWXvCx3an_sNoEgX-h1KubX_qWrbU_fqCOGa0 "Application key")

For each required graph, I defined the following graph definitions :
*    *My custom metric scoped over your host (my_metric):*
```python
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "my_metric{host:homy.roamy}"}
        ],
        "viz": "timeseries"
    },
    "title": "Homere's custom metric"
}
```
*    *Any metric from the Integration on your Database with the anomaly function applied. I chose the number of current connections to MongoDB :*
```python
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:mongodb.connections.current{host:homy.roamy}, 'basic', 2)"}
        ],
        "viz": "timeseries"
    },
    "title": "Anomalies in current number of connections to MongoDB"
}
```
*  *My custom metric with the rollup function applied to sum up all the points for the past hour into one bucket :* 
````python
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "my_metric{host:homy.roamy}.rollup(sum,3600)"}
        ],
        "viz": "query_value"
    },
    "title": "Homere's custom metric summed over an hour"
}
````

The final python script to create the desired Timeboard script looks as follows :
````python
from datadog import initialize, api

options = {
    'api_key': '7a949afa3aecc29828c96b90e0fa440f',
    'app_key': '8ff749621824a4346f8186a3d2c4d12a65e60564'
}

initialize(**options)

title = "Solutions Engineer Test : My API Timeboard"
description = "Playing around with the Datadog API to generate a Timeboard."
graphs = [
    {
    "definition": {
        "events": [],
        "requests": [
            {"q": "my_metric{host:homy.roamy}"}
        ],
        "viz": "timeseries"
    },
    "title": "Homere's custom metric"
    },
    {
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:mongodb.connections.current{host:homy.roamy}, 'basic', 2)"}
        ],
        "viz": "timeseries"
    },
    "title": "Anomalies in current number of connections to MongoDB"
    },
    {
    "definition": {
        "events": [],
        "requests": [
            {"q": "my_metric{host:homy.roamy}.rollup(sum,3600)"}
        ],
        "viz": "query_value"
    },
    "title": "Homere's custom metric summed over an hour"
    }
]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:my-host"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)
````

This script can be run by executing command : 
````
python timeboard.py
````
Be sure to have Python and the datadog dependency installed before running this command.

You can then visualise the new Timeboard on the **Dashboards>Dashboard List** by clicking on the latest dashboard in the *All Dashboards* list. I happened to have called mine **Solutions Engineer Test : My API Timeboard**.

![enter image description here](https://lh3.googleusercontent.com/8vbf3wsdpcyMlTW0gQ89XB2rs1lmtJXCk0MSjg-oX3aPYN4WCSbpsfLmJavB6X42_BPmEVD09sIl "My timeboard")


2.  Setting the Timeboard's timeframe to the past 5 minutes:
To set the Timeboard's timeframe to the past 5 minutes, we can simply place our mouse on a graph at the current time, click and hold the mouse to drag it to the left to 5 minutes ago, which will give us the following result:
![enter image description here](https://lh3.googleusercontent.com/x_tAvxYqqZgxxdBgksVhvMKhe4Z96HzKtgPRtQZeo6bOGb0MHNSz266YjXK0295zOEBVMVZp4w-w "5 minute timeframe view")

3. Taking a snapshot of this graph and use the @ notation to send it to myself:
To take a snapshot of a specific graph, first click on the snapshot icon that appears when you mouseover the graph 
![
](https://lh3.googleusercontent.com/P-yzqTqyr4tweENKUuZVba1d7njb1B9bHwGD26XZi2QdnPWlKp5tnxAhWNdEmO1AnpMV1GE7vvel "snapshot icon")

Clicking on this icon will toggle the following form, where you can use the ***@*** notation to select an email to send the snapshot to.

![
](https://lh3.googleusercontent.com/IVDRHBP2uGkiiXVnzoB6s15Q5ir5POc6t2K9UYkzfhKYumQdBVnjNGMrlokuEPQFj27a0ySjBHsB "Sending the snapshot to an email")

An email is then automatically sent to the specified email address:
![
](https://lh3.googleusercontent.com/Qlq0ojVnnviP7qyCo18ozh3a2gkCz3-72KMmd-w2cBjFRSBQamslEej1X8OokmcRUCm_KWL-e5W- "Datadog sent email")

### Bonus : 
The grey area on the graph corresponds to ranges in which values are considered to be 'normal' when comparing with past metric values. Any values outside of this grey area are considered to be abnormal.

## Monitoring Data

1. Creating a Metric Monitor:

To create a Metric Monitor for ``my_metric``, navigate to **Monitors> New Monitor** from the sidebar menu.

In the **New Monitor** page, we first choose **Threshold Alert** has the detection method for our new monitor, as we want to be alerted when our custom metric exceeds a certain value:

![enter image description here](https://lh3.googleusercontent.com/rsVoPbUWLPZtOyPwGf50uw2tiZxvj_pXmXKUmgfO3s6mvtD_6gMK00QMqAFzG35HhhCCQm-Wy2mM "Threshold Alert")

We then choose the metric to be monitored, in this case ``my_metric``and choose the tags we want to reduce our dataset with:
![
](https://lh3.googleusercontent.com/IJYR2FVKjJeKjMXqeA_5anYpq4GDvwTUow9EmOvzK5Aiy5s9o2D67GkmIZlpKKXuRtt7jKlj9-Lo "Choosing a metric")

We can then define our alert as follows: 
![
](https://lh3.googleusercontent.com/meUdnsqFAAZ-y4b5ClrQtzCAI7nK7fBbdkcoqUkxBBAkXAdgbcklC0m1Xsbs35fV1JlgCWVSXCoG "Alert Conditions")

These conditions will :
-   Set a warning threshold of 500
-   Set an alerting threshold of 800
-   Ensure that it will notify you if there is No Data for this query over the past 10m.


2. Configuring the Monitor:

In order to configure the Monitor to :
* Send you an email whenever the monitor triggers, 
* Create different messages based on whether the monitor is in an Alert, Warning, or No Data state,
* Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state,
*  When this monitor sends you an email notification, take a screenshot of the email that it sends you,

We can use the following code in the **Say What's Happening** text  area : 
````
{{#is_alert}} 
ALERT: The Alert Threshold has been exceeded. Value of my_metric for {{host.name}}@{{host.ip}} was {{value}}.
{{/is_alert}}

{{#is_warning}} 
WARNING: The Warning Threshold has been exceeded. Value of my_metric for {{host.name}}@{{host.ip}} was {{value}}.
{{/is_warning}}

{{#is_no_data}} 
NO DATA: No Data for my_metric has been detected over the past ten minutes for {{host.name}}@{{host.ip}}.
{{/is_no_data}}

@Notify: @hfaivresaito@gmail.com 
````

Datadog sends the following email when a monitor is triggered:
![
](https://lh3.googleusercontent.com/88DcQ-XUDhB-fni_hCeMcExiQmulVS_sB4U3hJAwlK4qPGUwoB94A3BhymGWbUKIGPCNhZ94Ukwf "Monitor triggered")

### Bonus :

To setup two scheduled downtimes for this monitor, we can do can schedule a new downtime in the **Monitors>Manage Downtime page** as follows for each of the two required downtime:
-   One that silences it from 7pm to 9am daily on M-F :

![
](https://lh3.googleusercontent.com/tZztDAALzD2nqBtN8hxHKadp7lyOK4Q8JiJfLf0pbT8w7YnB2fnPf7XZbJIdqQ_y7--mjTdsyOL4 "Night downtime")

-   And one that silences it all day on Sat-Sun :

![
](https://lh3.googleusercontent.com/UU4WFcnxXdwNrL_d9n69gKX2-I-nblRRtzekD4pj6rbJFdEdE7j73u3HnZF1eLhtY_Bbza0NV4wc "Weekend dowtime")

The following notification email is sent when the downtime has been configured:

![
](https://lh3.googleusercontent.com/IQYcg_HQ7gJlNiwsmDxHk8A2UTGEwB1VitPaxUvBXUDJoeVGR51PuMwtTDTusnvQ1ye1eOzI4gCE "Downtime creation notification")

## Collecting APM Data


To instrument the given Python Flask application, I read the following [documentation](https://docs.datadoghq.com/tracing/setup/python/).

First it is necessary to configure the ``datadog.yaml``file in the ``/etc/datadog-agent``folder as follows :

```yaml
apm_config:
	enabled: true
```

Then we have to install the necessary libraries to run our Python Flask app, as well as ``ddtrace`` :

```
pip install flask
```
and
```
pip install ddtrace
```

Then we create a python file for our application, ``apm_test.py`` in the  ``/etc/datadog-agent``:

```python
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

# instrumenting DD APM for Flask
traced_app = TraceMiddleware(app, tracer, service="my-flask-app", distributed_tracing=False)

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
Once our file is created, we can start APM for our app :

```
ddtrace-run python apm_test.py
```

 We can then run some curl requests to our application and see the interaction with Datadog platform
 ````
 curl http://0.0.0.0:5050
 curl http://0.0.0.0:5050/api/apm
 curl http://0.0.0.0:5050/api/trace
````
 
 This will produce the following outcome on the  **APM>Traces** page:
![
](https://lh3.googleusercontent.com/Dia7Pwmehyquvt1ga89rBakBb9J894n8aM3qW_eZZOlw2FpJq2uSqi5KweLwu-3FIWpyWmKtv6p_ "Traces")

![enter image description here](https://lh3.googleusercontent.com/SZAuVMZo2H9oWWm-c8mKIvV1aeuFjJ1cdNaVXnQ4x4ApFiEqJNpFbeuzPViup5f8mAtHRdLsUAMb)

This interface can be seen [here](https://app.datadoghq.com/apm/service/my-flask-app/flask.request?env=none&start=1536683692603&end=1536687292603&paused=false).


### Bonus :
A "Service" is the name of a set of processes that work together to provide a feature set. For example a web application can be composed of two services, a web server service and a database service. A "Resource" is a particular query to a service, so for example a query in the database, to filter users of the web application, will be considered as a resource.


##  Final Question

One cool use case of datadog would be to conduct social studies in dating apps, such as Tinder, where discrimination has been known to thrive where stereotypical assumptions and racist remarks are often passed off as sexual preferences.
Even though I am not a user of Tinder ( although I admittedly was one long time ago), I find the social approach of Tinder very interesting : the game like interface, which only showcases the superficial aspects of one's personality/features might seems very shallow. Amazingly, a growing number of married couples meet on Tinder. I believe Tinder has a large role in  the dating habits/trends of today, even if I do not completely adhere to it.

Using Datadog could give the Tinder product team quantitative approach of what the main stereotypical assumptions are, and what qualifies the 'exceptions' that exists. I could maybe help them recalibrate the matching algorithms to lessen racial stereotypes.


