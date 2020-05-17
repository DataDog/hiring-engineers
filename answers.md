Dashboard link: https://app.datadoghq.com/
Account: mqbui1@gmail.com
Datadog agent installed to host running on Vagrant VM
MySQL DB installed to same host

Collecting Metrics:
Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
- The following tags were added to the /etc/datadog-agent/datadog.yaml file 
![tags](https://github.com/mqbui1/hiring-engineers/blob/master/tags.PNG)

![tags_dashboard](https://github.com/mqbui1/hiring-engineers/blob/master/Datadog_Dashboard.PNG)

Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
- MySQL database is installed on the same host as where the Datadog Agent is installed
- Datadog integration with the MySQL was done by following the documentation: https://docs.datadoghq.com/integrations/mysql/
![mysql_image](https://github.com/mqbui1/hiring-engineers/blob/master/mysqldb_hostmap.PNG)

Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
- custom_my_metric.py was created at /etc/datadog-agent/checks.d

[custom_my_metric.py](https://github.com/mqbui1/hiring-engineers/blob/master/custom_my_metric.py)

- custom_my_metric.yaml was created at /etc/datadog-agent/conf.d

[custom_my_metric.yaml](https://github.com/mqbui1/hiring-engineers/blob/master/custom_my_metric.yaml)

Change your check's collection interval so that it only submits the metric once every 45 seconds.
- The custom_my_metric.yaml was updated so the collection interval would be 45 seconds:
init_config:
instances:
        - min_collection_interval: 45

![metric_dashboard](https://github.com/mqbui1/hiring-engineers/blob/master/custom_my_metric.PNG)
        
     
Utilize the Datadog API to create a Timeboard that contains:
![timeboard1_image](https://github.com/mqbui1/hiring-engineers/blob/master/maintimeboard.PNG)

Your custom metric scoped over your host.
![timeboard2_image](https://github.com/mqbui1/hiring-engineers/blob/master/timeboard2.PNG)

Any metric from the Integration on your Database with the anomaly function applied.
![timeboard4_image](https://github.com/mqbui1/hiring-engineers/blob/master/timeboard4.PNG)

Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
![timeboard3_image](https://github.com/mqbui1/hiring-engineers/blob/master/rollup.PNG)

Script executed: [timeboard.py](https://github.com/mqbui1/hiring-engineers/blob/master/timeboard.py)

Execution command: /opt/datadog-agent/embedded/bin$ python3 timeboard.py

Set the Timeboard's timeframe to the past 5 minutes
![5min_image](https://github.com/mqbui1/hiring-engineers/blob/master/5min.PNG)

Take a snapshot of this graph and use the @ notation to send it to yourself.
![snapshot_image](https://github.com/mqbui1/hiring-engineers/blob/master/snapshot.PNG)

Bonus Question: What is the Anomaly graph displaying?
- Anomaly detection checks to see when a metric is behaving differently than it has in the past through consideration of trends, seasonal day-of-week, and time-of-day patterns.

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:
Warning threshold of 500
Alerting threshold of 800
And also ensure that it will notify you if there is No Data for this query over the past 10m.
Please configure the monitor’s message so that it will:
Send you an email whenever the monitor triggers.
Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
When this monitor sends you an email notification, take a screenshot of the email that it sends you.
![monitor1](https://github.com/mqbui1/hiring-engineers/blob/master/monitor1.PNG)
![monitor2](https://github.com/mqbui1/hiring-engineers/blob/master/monitor2.PNG)
![monitor3](https://github.com/mqbui1/hiring-engineers/blob/master/monitor3.PNG)
![monitor4](https://github.com/mqbui1/hiring-engineers/blob/master/monitor4.PNG)

Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:
One that silences it from 7pm to 9am daily on M-F,
And one that silences it all day on Sat-Sun.
Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.
![monitor5](https://github.com/mqbui1/hiring-engineers/blob/master/monitor5.PNG)
![monitor6](https://github.com/mqbui1/hiring-engineers/blob/master/monitor6.PNG)
![monitor7](https://github.com/mqbui1/hiring-engineers/blob/master/monitor7.PNG)

Collecting APM Data:
Bonus Question: What is the difference between a Service and a Resource?
- Resource: a particular action for a given service (typically an individual endpoints or query)
- Service: building blocks of modern microservice architecutres-- a service groups together endpoints, queries, or jobs for the purposes of scaling instances

Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.
https://app.datadoghq.com/apm/service/flask/flask.request?end=1589738974858&env=flask_test&paused=false&start=1589735374858
![flaskapp image](https://github.com/mqbui1/hiring-engineers/blob/master/flaskapp2.PNG)
![flaskapp image2](https://github.com/mqbui1/hiring-engineers/blob/master/flaskapp3.PNG)

Command used to start tracing on flask app: FLASK_APP=flaskapp.py DATADOG_ENV=flask_test ddtrace-run flask run --port=4999
In order for the monitor status to show on the dashboard, curl command needed to be ran to trigger the application: curl -v http://127.0.0.1:4999

Final Question:
Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?
- I worked in corporate real estate for many years so the initial thought would to use Datadog for space utilization.  Sensors that detect seat occupancy could be placed at every seat in a building.  These sensors would update a central server that has a Datadog agent installed.  The agent would use a custom agent check to query the occupancy data stored on the server that gets stored to custom metrics.  Monitors would then be set up to alert when capacity thresholds are met for proper capacity planning. Additionally, dashboard graphics could be use to analyze trends, anomalies, and much more.
