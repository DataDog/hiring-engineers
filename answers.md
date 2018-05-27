Questions

Please provide screenshots and code snippets for all steps.

Collecting Metrics:

1. Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

To add tags, I found "Assigning tags using the configuration files" in the Docs (https://docs.datadoghq.com/getting_started/tagging/assigning_tags/#assigning-tags-using-the-configuration-files) and configured datadog.yaml to add the region: nsw tag. Please refer to the two screenshots below.

Screenshot 1: datadog.yaml

![](https://github.com/su27k-2003/hiring-engineers/blob/master/image/Collecting_datadog_yaml.PNG)

Screenshot 2: Host Map (Added the "region:nsw" tag)

![](https://github.com/su27k-2003/hiring-engineers/blob/master/image/Collecting_HostMap.PNG)


2. Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

I've installed MySQL into my Ubuntu (16.04.4) and I followed the MySQL integration page (https://docs.datadoghq.com/integrations/mysql/) to configure the MySQL and the agent. After the configuration, confirmed the dashboard is receiving data from MySQL. Please refer to the two screenshots below.

Screenshot 1: Configured /etc/datadog-agent/conf.d/mysql.d/conf.yaml

![](https://github.com/su27k-2003/hiring-engineers/blob/master/image/Collecting_mysql_conf.PNG)

Screenshot 2: MySQL dashboard

![](https://github.com/su27k-2003/hiring-engineers/blob/master/image/Collecting_mysql.PNG)

3. Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

To create a custom Agent check, I followed the docs (https://docs.datadoghq.com/developers/agent_checks/) and created mycheck.yaml and mycheck.py then configured the two files accordingly. Please refer to the two screenshots below. 

Screenshot 1: Created and configured /etc/datadog-agent/conf.d/mycheck.yaml

![](https://github.com/su27k-2003/hiring-engineers/blob/master/image/Collecting_custom_check_1.PNG)

Screenshot 2: Created and configured /etc/datadog-agent/checks.d/mycheck.py

![](https://github.com/su27k-2003/hiring-engineers/blob/master/image/Collecting_custom_check_2.PNG)

4. Change your check's collection interval so that it only submits the metric once every 45 seconds.

I used time.sleep function in mycheck.py to making the 45 seconds time delay for changing the data collection interval. Please refer to the screenshot below.

Screenshot: Added time delay function into the /etc/datadog-agent/checks.d/mycheck.py

![](https://github.com/su27k-2003/hiring-engineers/blob/master/image/Collecting_custom_check_3.PNG)

5. Bonus Question Can you change the collection interval without modifying the Python check file you created?

We also could change the data collection interval by configuring min_collection_interval in the mycheck.yaml file. Please refer to the screenshot below.

Screenshot: Added min_collection_interval into the /etc/datadog-agent/conf.d/mycheck.yaml

![](https://github.com/su27k-2003/hiring-engineers/blob/master/image/Collecting_custom_check_4.PNG)


Visualizing Data:

Utilize the Datadog API to create a Timeboard that contains:
1. Your custom metric scoped over your host.

I created a timeboard which collects data of the custom metric: my_metric we just created in the previous step by submitted the Python code below and confirmed the timeboard works well in the UI as expected. Please refer to the two screenshots below. This page (https://docs.datadoghq.com/api/?lang=python#create-a-timeboard) gave me lots of useful information about how to use the Datadog API.

Screenshot 1: Python code

![](https://github.com/su27k-2003/hiring-engineers/blob/master/image/Visualizing_1.PNG)

Screenshot 2: My_metric in the timeboard just crated

![](https://github.com/su27k-2003/hiring-engineers/blob/master/image/Visualizing_2.PNG)

2. Any metric from the Integration on your Database with the anomaly function applied.

I randomly picked mysql.net.connections up as the metric we apply anomaly function (https://docs.datadoghq.com/monitors/monitor_types/anomaly/) to it.
Unfortunately, I could not find the way to add the mysql.net.connections metric into the timeboard I just created. It seems the anomaly function only could applies to the monitor so I created a monitor instead timeboard in this step. Please refer to the two screenshots below. 
If I missed something, please point me and let me know. Thank you.

Screenshot 1: Python code

![](https://github.com/su27k-2003/hiring-engineers/blob/master/image/Visualizing_3.PNG)

Screenshot 2: Anomaly function applied to the mysql.net.connections metric

![](https://github.com/su27k-2003/hiring-engineers/blob/master/image/Visualizing_4.PNG)

3. Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

This page (https://docs.datadoghq.com/graphing/miscellaneous/functions/#rollup-1)  guided me how to use .rollup function to sum up data and applied it to the custom metric (my_metric) from the host:deep-learning-virtual-machine. Please refer to the two screenshots below. 

Screenshot 1: Python code

![](https://github.com/su27k-2003/hiring-engineers/blob/master/image/Visualizing_5.PNG)

Screenshot 2: rollup function applied to the my_metric

![](https://github.com/su27k-2003/hiring-engineers/blob/master/image/Visualizing_6.PNG)

Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timemboard.
Once this is created, access the Dashboard from your Dashboard List in the UI:
Set the Timeboard's timeframe to the past 5 minutes

4. Take a snapshot of this graph and use the @ notation to send it to yourself.

Screenshot 1: Graph of the timeboard

![](https://github.com/su27k-2003/hiring-engineers/blob/master/image/Visualizing_7.PNG)

Screenshot 2: @ notation 

![](https://github.com/su27k-2003/hiring-engineers/blob/master/image/Visualizing_9.PNG)

5. Bonus Question: What is the Anomaly graph displaying?

We use Anomaly detection to identify when a metric is behaving differently than it has in the past, taking into account trends, seasonal day-of-week and time-of-day patterns. From the graph below we can see the algorithm is monitoring historical data to calculating the metric’s expected normal range of behaviour. 

Screenshot: Anomaly graph

![](https://github.com/su27k-2003/hiring-engineers/blob/master/image/Visualizing_8.PNG)
 
 
Monitoring Data

Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.
Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:
Warning threshold of 500
Alerting threshold of 800
And also ensure that it will notify you if there is No Data for this query over the past 10m.
Please configure the monitor’s message so that it will:
https://docs.datadoghq.com/monitors/notifications/
Send you an email whenever the monitor triggers.
Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
When this monitor sends you an email notification, take a screenshot of the email that it sends you.

Please refer to the screenshot below or my account (liuqi_jp@hotmail.com) to check the metric monitor I created.

Screenshot 1: Creating the monitor

![](https://github.com/su27k-2003/hiring-engineers/blob/master/image/Monitoring_2.PNG)

Screenshot 2: Email notification

![](https://github.com/su27k-2003/hiring-engineers/blob/master/image/Monitoring_1.PNG)

Bonus Question: 

Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:
https://docs.datadoghq.com/monitors/downtimes/
One that silences it from 7pm to 9am daily on M-F,
And one that silences it all day on Sat-Sun.
Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

Please refer to the two screenshots below.

Screenshot 1: Downtime from 7pm to 9am daily on M-F

![](https://github.com/su27k-2003/hiring-engineers/blob/master/image/Downtime_1.PNG)

Screenshot 2: Downtime all day on Sat-Sun

![](https://github.com/su27k-2003/hiring-engineers/blob/master/image/Downtime_2.PNG)


Collecting APM Data:

Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:

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


Note: Using both ddtrace-run and manually inserting the Middleware has been known to cause issues. Please only use one or the other.
Bonus Question: What is the difference between a Service and a Resource?

Service is a set of processes that do the same job. For instance, a simple web application may consist of two services: a single webapp service and a single database service.
Resource is a particular action for a service. For a web application: some examples might be a canonical URL, such as /user/home or a handler function like web.user.home. For a SQL database: a resource is the query itself, such as SELECT * FROM users WHERE id = ?.

Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

https://p.datadoghq.com/sb/1d199b067-1878f66f0cbee4b76c9a3de718a749bd?tv_mode=true

Please include your fully instrumented app in your submission, as well.

I only used the Python sample code (Flask app) above to create the APM.  
 
 
Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!
Is there anything creative you would use Datadog for?

I’m very interested in IoT and have developed a few Raspberry Pi based autonomous home projects such as smart garage door (Demo: https://youtu.be/OaJwVSyagKI) and home security camera. I’m aiming to build a smart home by myself and truly enjoying these projects as it could bring an easier life to my family and improve my technical skills.

During developing these projects, I found a few pain points and I think Datadog could help me to resolve it.

1. Analizy issues

For example, during the smart garage door project, sometimes I found the smart garage door system did not work properly for some reason. The issue could be a communication issue between my phone and the Raspberry Pi (HTTP sending/receiving) or some bugs in the script I developed and even the Raspberry Pi itself. Usually, it’s not easy to figure out the root cause so I've given lots of time on troubleshooting and debugging and found a way to determine and fix issues by sending out notification from each function in the system to trace which part caused the issue.
Now, I could create a dashboard in Datadog which include Infrastructure Metrics of Raspberry Pi and APM for the Flask application I developed, those data could help me to understand the current system state easily also allow me to quickly determine which part in the system does not function when some issue occurs. For example, if I still could receive those infrastructure metrics data from the Raspberry Pi but the APM doesn't show the proper data, I will check any potential communication issues such as the mobile data function has been turned off in my phone. If it’s not communication issue then I will look into the Flask as the next step to find the root cause.  
               
2. Integrate separate data into a single smart home system monitor

There are few smart home projects I’m running at home and different project generates their own data in different UI. For example, I have to check the room temperature by ssh to the Raspberry Pi remotely every time and use VNC to access the Raspberry Pi if I need to check the security camera video. 
I believe that I can send these data to Datadog and integrate them into a single smart home system dashboard which includes all data I need to improve system visibility and make my life even easier.
Unfortunately, I cannot provide a demo and show the possibility of Datadog could bring to me as the project need time to complete but I will find some time to achieve it and share it with you.
