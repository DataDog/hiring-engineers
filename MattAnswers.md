## Datadog Hiring Exercise **Matt Eastling** Questions and Answers

## Prerequisites - Setup the environment

Environments Utilized:
* MS Windows 8.1
* Ubuntu 12 / MySQL 
Vagrant Init

![Vagrant Init](https://github.com/MrEastling/hiring-engineers/blob/solutions-engineer/8_Test_Vagrant_VM_Init.PNG)

Vagrant up

![Vagrant up]( https://github.com/MrEastling/hiring-engineers/blob/solutions-engineer/15_Install_Vagrant_Download_and_Init_VirtualBoxVM_ERROR_4-GuestKey-cannot_reconcile.PNG),

## Collecting Metrics:

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

Tag Added

![Tag Added](https://github.com/MrEastling/hiring-engineers/blob/solutions-engineer/24_DD_Add_Tag.PNG)

* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database. 

Install MySQL

![Install MySql](https://github.com/MrEastling/hiring-engineers/blob/solutions-engineer/25_Install_my_sql.PNG)

SQL Installed Success

![SQL Installed Success](https://github.com/MrEastling/hiring-engineers/blob/solutions-engineer/29.1_Install_DD_mysql_integration_completed_and_checked.PNG)

Datadog MySQL Integration Installed

![Datadog MySQL Integration Installed](https://github.com/MrEastling/hiring-engineers/blob/solutions-engineer/29.2_Install_DD_mysql_integration_completed_and_checked_DD_UI.PNG)

* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

My_Metric.py

![My_Metric.py](https://github.com/MrEastling/hiring-engineers/blob/solutions-engineer/A.my_metric.py)

My Metric Added

![My Metric Added](https://github.com/MrEastling/hiring-engineers/blob/solutions-engineer/30.1_My_Metric_completed_and_checked_DD_Agent_Status.PNG)

My_Metric on DD Dashboard

![My_Metric on DD Dashboard](https://github.com/MrEastling/hiring-engineers/blob/solutions-engineer/30.2_My_metric_01_random%2B1to1000_timeboard_completed_and_checked_DD_UI.PNG)

* Change your check's collection interval so that it only submits the metric once every 45 seconds.

My_Metric.yaml

![My_Metric.yaml](https://github.com/MrEastling/hiring-engineers/blob/solutions-engineer/30.3_My_metric_yaml_45sec.PNG)

* **Bonus Question** Can you change the collection interval without modifying the Python check file you created?

Yes - this is acoomplished by updating the default collection interval in the yaml file, see previous screen capture

## Visualizing Data:

Utilize the Datadog API to create a Timeboard that contains:

* Your custom metric scoped over your host.

* Any metric from the Integration on your Database with the anomaly function applied.

MySQL_Anomaly

![MySQL_Anomaly](https://github.com/MrEastling/hiring-engineers/blob/solutions-engineer/31_Create_Anomaly_Monitor_MySQL_User_Perf.PNG)

MySQL_Anomaly Details
![MySQL_Anomaly Details](https://github.com/MrEastling/hiring-engineers/blob/solutions-engineer/32_Create_Anomaly_Monitor_MySQL_User_Perf_completed.PNG)

* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

My_Metric Rollup JSON

![My_Metric Rollup JSON](https://github.com/MrEastling/hiring-engineers/blob/solutions-engineer/33_Create_Rollup_My_Metric_completed-edit_JSON.PNG)

My_Metric Rollup Dash_Details
![My_Metric Rollup Dash_Details](https://github.com/MrEastling/hiring-engineers/blob/solutions-engineer/33.2_Create_Rollup_My_Metric_completed-edit_DD_Dash_Properties.PNG)

* Script used to create this Timemboard:

Create Timeboard via API Script

![Create Timeboard via API Script](https://github.com/MrEastling/hiring-engineers/blob/solutions-engineer/B.Matt_timeboard_api_7.py)

Once this is created, access the Dashboard from your Dashboard List in the UI:

* Set the Timeboard's timeframe to the past 5 minutes


* Take a snapshot of this graph and use the @ notation to send it to yourself.

My_Metric Sent via Comment
![My_Metric Sent via Comment](https://github.com/MrEastling/hiring-engineers/blob/solutions-engineer/34_Send_Snapshot_Via_Comment_My_Metric_Graph.PNG)

* **Bonus Question**: What is the Anomaly graph displaying?

Anomaly graphs show any tracked variable of a metric that is inconsistent from what are defined as 'normal' parameters. It can be used to highlight unusually high CPU usage, traffic volumes on a website, or other important activity that may cause performance issues. 

It works for metrics that display consistent trends over time and that the one who configures it having a sense of the metrics 'normal' patterns. 

I see this being particularly compelling when looking at a large pool resources/services providing metric data and applying the vetted Anomaly graphs configuration to the greater pool of resources to see which of them are not performing with prescribed parameters. This provided actional insights and valuable real time alerts for the managed resources.

## Monitoring Data

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

* Warning threshold of 500
* Alerting threshold of 800
* And also ensure that it will notify you if there is No Data for this query over the past 10m.

Please configure the monitor’s message so that it will:

* Send you an email whenever the monitor triggers.
* Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
* Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
* When this monitor sends you an email notification, take a screenshot of the email that it sends you.

* **Bonus Question**: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

    * One that silences it from 7pm to 9am daily on M-F,
    * And one that silences it all day on Sat-Sun.
    * Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.


## Collecting APM Data:

Using provided Flask app, instrument this using Datadog’s APM solution:

![Matt Flask App Python File Instrumented with DD](https://github.com/MrEastling/hiring-engineers/blob/solutions-engineer/C.Matt_Flask_1.py)

* **Bonus Question**: What is the difference between a Service and a Resource

A service in Datadog APM is defined as "A service is a set of processes that do the same job" in relation to one's managed applications such as a web server or a database. 

Datadog has the capability to monitor the performance of each service individually and provice metrics such as CPU usage, number of requests, average latency, and number of errors and their frequency.  .

A resource in Datadog APM is defined as "a particular action for a service.". The resources are the individual calls and traces that make up a service. 

For a web app service, resources will be web based entry points into the application such as specific URLs that users are hitting (ex. Endpoint: /home, /api). For a database, a resource will be an individual SQL call (ex. Query: select * from datadog). 

The metrics of said individual resources will make up the overall service's performance metrics and can be grouped together accordingly.


Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

Please include your fully instrumented app in your submission, as well. 

## Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?

## Instructions

If you have a question, create an issue in this repository.

To submit your answers:

* Fork this repo. ## DONE
* Answer the questions in answers.md ## IN PROGRESS
* Commit as much code as you need to support your answers. ## IN PROGRESS
* Submit a pull request. ## IN PROGRESS
* Don't forget to include links to your dashboard(s), even better links and screenshots. We recommend that you include your screenshots inline with your answers. ## IN PROGRESS

