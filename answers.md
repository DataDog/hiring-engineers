Your answers to the questions go here.

This is the Results for Greg Specht
**Prerequisites - Setup the environment**
You can utilize any OS/host that you would like to complete this exercise. However, we recommend one of the following approaches:



**My Environment**

For the exercise, I actually got a bit curious so I set up two Ubuntu instances, one via Vagrant, another in my AWS test environement. My Vagrant instance is Unbuntu 14.04.5 while my AWS instance is 18.04. Due to the following statement for the exercise I chose to leverage my AWS instance for installation of MySQL and will use it for most of the requirements for the exercise.
```
You can spin up a fresh linux VM via Vagrant or other tools so that you don’t run into any OS or dependency issues. Here are instructions for setting up a Vagrant Ubuntu VM. We strongly recommend using minimum v. 16.04 to avoid dependency issues
```
![](http://i.imgur.com/zlnhfv0.png)
*Figure 1 Vagrant Instance*

**Apache Installation**

I set up the Apache server and was successfully installed. I can browse to ther server.

![](http://i.imgur.com/fcNE8hm.png)
*Figure 2 Apache Server*


**Installing MySQL**
I chose to install MySQL for the database.



**Install Datadog Agent**
The Datadog agent was successfully installed via the following:
[//]: # (This syntax works like a comment, and won't appear in any output.)
```
vagrant@precise64:~$ DD_API_KEY=<!-- This is commented out. --> bash -c "$(curl -L https://raw.githubusercontent.com/D
ataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```
Returned the following message: Your Agent is running and functioning properly. It will continue to run in the
background and submit metrics to Datadog.

![](http://i.imgur.com/VVh8EyH.png)
*Figure 3 Datadog Agent Install*

MySQL integration was set up. for the Datadog Agent and the datadog user was created. using the following command.
```
create MYSQL USER
CREATE USER 'datadog'@'localhost' IDENTIFIED BY '<!-- This is commented out. -->'
```


**Collecting Metrics:**


Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

**Answer:**

Tags field was added in the datadog/yaml file. Code is as follows

Set the host's tags (optional)
I went ahead and updated the datadog.yaml file and added the following lines:
```
tags:
   - prodserverdb1
   - env:prod
   - role:database_servers
```


Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

I installed a MySQL server for this use case. Integration was setup according to MySQL instructions. On the attached hostmap, the system on the left is my MySQL server.

![](http://i.imgur.com/0WGoQO7.png)
*Figure 4 Host Map showing MySQL integration with other agents.*

This view shows the my custom tags are properly set up
![](http://i.imgur.com/hNJ6buU.png)
*Figure 5 Host Map showing tags from datadog.yaml*


Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
Change your check's collection interval so that it only submits the metric once every 45 seconds.

**Answer:**
I created a my_metric.py file in the /etc/datadog-agent/checks.d directory and added the following code.
```
import random
from checks import AgentCheck
class HelloCheck(AgentCheck):
  def check(self, instance):
     self.gauge('my_metric', random.randint(1,1001))
```

I then created a my_metric.yaml file in the /etc/datadog-agent/conf.d directory and added the following code.
```
init_config:
instances: [{}]
Instances:
    - min_collection_interval: 45
```
I then ran a sudo service datadog-agent restart to restart the agent.
I then ran the following command to ensure the custom metric was working. sudo -u dd-agent -- datadog-agent check my_metric

The following data was returned indicating that the custom metric was working properly.
```
=== Series ===
{
  "series": [
    {
      "metric": "my_metric",
      "points": [
        [
          1544564296,
          891
        ]
      ],
      "tags": null,
      "host": "precise64",
      "type": "gauge",
      "interval": 0,
      "source_type_name": "System"
    }
  ]
}
=========
Collector
=========

  Running Checks
  ==============

    my_metric (unversioned)
    -----------------------
        Instance ID: my_metric:d884b5186b651429 [OK]
        Total Runs: 1
        Metric Samples: 1, Total: 1
        Events: 0, Total: 0
        Service Checks: 0, Total: 0
        Average Execution Time : 0s
```

Check has run only once, if some metrics are missing you can try again with --check-rate to see any other metric if available.

Custom Metric is successfully reporting. I created a timeboard with my custom metric and it displays as follows:

![](http://i.imgur.com/OrhUuUU.png)
*Figure 6 TimeBoard showing custom metric*


Bonus Question Can you change the collection interval without modifying the Python check file you created?
**Answer:**
Yes, the interval exists within the yaml file so it can be easily changed there. I went ahead and set it to 45 seconds. under instances "-min_collection_interval"

**Visualizing Data:**
Utilize the Datadog API to create a Timeboard that contains:

Your custom metric scoped over your host.
Any metric from the Integration on your Database with the anomaly function applied.
Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.


* **Answer:** I first went to the API section and copied my API key and added a APP key to insert into my timeboard script. 
* I created a timeboard.py file with the following code:
```python
#!/opt/datadog-agent/embedded/bin/python
import datadog
from datadog import initialize, api
options = {
    'api_key': '<!-- This is commented out. -->',
    'app_key': '<!-- This is commented out. -->'
}
initialize(**options)
title = "Datadog Test Timeboard"
description = "Test Metric Timeboard."
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{*}"}
        ],
        "viz": "timeseries"
    },
    "title": "My_Metric"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:mysql.net.connections.current{*}, 'basic', 2)"}
        ],
        "viz": "timeseries"
    },
    "title": "MySQL Anomaly"
},
 {
 "definition": {
        "events": [],
        "requests": [
            {"q": "sum:my_metric{*}.rollup(sum,3600)"}
        ],
        "viz": "timeseries
```
A few other things needed to be done, which included proper python and datadog set up.
**First command to run:**
```
sudo apt-get install python-pip
```
**Once Pip was installed I could then run the next command for datadog:**
```
sudo pip install datadog
```
**Collecting datadog**

I was able to succesfully create the timeboard, I did make one minor change to the rollup section, I made it an area chart just so it looked better.

![](http://i.imgur.com/anvJTWo.png)
*Figure 7 TimeBoard create via API and python script*

Once this is created, access the Dashboard from your Dashboard List in the UI and the above screenshot shows the view.

Set the Timeboard's timeframe to the past 5 minutes

**Answer:** This is done by dragging the mouse over the set time period you want and all graphs on the timeboard will show that time frame. In this example the time is from 10:08 to 10:13.

![](http://i.imgur.com/ciU9WHL.png)
*Figure 8 TimeBoard changed to last 5 minutes*


Take a snapshot of this graph and use the @ notation to send it to yourself.

**Answer:** The notation allows you to quickly send specific data to a specific person or group of people for instant analysis of data. This is done by clicking on the camera icon. The screenshot below shows the example.

![](http://i.imgur.com/mklX2FP.png)
*Figure 9 Using the Snapshot Feature*

The email output shows in the next screenshot.
![](http://i.imgur.com/t57SAaQ.png)
*Figure 10 Using the Snapshot Feature Email Output*

**Bonus Question: What is the Anomaly graph displaying?**
**Answer:** The anomaly graph is designed to show any deviations in the data points from normal trends. If the data point is outside of what is predicted, it will be considered an anomaly.

**Monitoring Data**
Since you've already caught your test metric going above 800 once, you don't want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let's make life easier by creating a monitor.

- Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it's above the following values over the past 5 minutes:

- Warning threshold of 500
- Alerting threshold of 800
- And also ensure that it will notify you if there is No Data for this query over the past 10m.

Please configure the monitor's message so that it will:
- Send you an email whenever the monitor triggers.

**Answers:**
The first screenshot shows the setup of the monitor.

![](http://i.imgur.com/B6QW1TB.png)
*Figure 11 Metric Monitor set up of thresholds*

Additional Setup views
![](http://i.imgur.com/DcCKUxL.png)
*Figure 12 Metric Monitor set up of Notifications*

Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
This is an example of how to show different messages based on type of alert.

![](http://i.imgur.com/UbiWBGi.png)
*Figure 13 Monitor can be set up to show different messages*

Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
**Answer:**
I used the following text for my alert message:
```
{{value}}   sent to @g.specht@gmstechllc.com

{{#is_warning}} My_metric is in a warning state for  Host {{Host.Name}} with {{Host.ip}} {{/is_warning}} 
{{^is_warning}} My_metric is critical for Host {{Host.Name}} with {{Host.ip}} {{/is_warning}} 
```
I played around with the different parameters to see what output changes I would get.

![](http://i.imgur.com/8UxTqay.png)
*Figure 14 Email format from Alert Notification*
When this monitor sends you an email notification, take a screenshot of the email that it sends you.

**Bonus Question:** Since this monitor is going to alert pretty often, you don't want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

One that silences it from 7pm to 9am daily on M-F,
And one that silences it all day on Sat-Sun.

![](http://i.imgur.com/I1KcI64.png)
![](http://i.imgur.com/o8V3LRa.png)
*Figure 15 & 16 Scheduling Downtime*

Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.
![](http://i.imgur.com/0Ep1QtN.png)
*Figure 17 Email Notification of Downtime*

**Collecting APM Data:**

Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog's APM solution:

**Answer:**
I installed flask via **sudo -H install flask**
I then install ddtrace as follows **sudo -H pip install ddtrace**

I created a file called apm.py with the code below
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
    app.run(host='0.0.0.0', port='5050')
```
Note: Using both ddtrace-run and manually inserting the Middleware has been known to cause issues. Please only use one or the other. I used ddtrace

I ran sudo **ddtrace-run python apm.py** to bring up the app

I was able to see APM data in the APM Views
![](http://i.imgur.com/J9f18HU.png)
*Figure 18 APM Data Views*

Bonus Question: What is the difference between a Service and a Resource?

**Answer:** Every Service being monitored by your application will be associated with a "Type". This Type can be "Web", "DB", "HTTP etc.
A Service is the name of a set of processes that work together to provide a feature set. For instance, a simple web application may consist of two or more services.


**Final Question**

Datadog has been used in a lot of creative ways in the past. We've written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?

**Answer:**
I have worked in the Energy industry and Smart meter technology is becoming a standard. Getting the meter data can be very challenging as it is not a conventional approach. The Datadog API and custom integrations would allow for energy companies to monitor health and availability of smart meter technologies as well as the applications and infrastructures that support it. The ability to easily create timeboards would allow for a very intuitive view of the overall smart meter service from a business standpoint. Also, in traditional corporations, there is a increasing need to add business related metrics along with IT service metrics. This is another way the Datadog can add value to the line of business within an organization.

