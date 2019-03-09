First and foremost, I had 2 datadog agents installed on the following 2 different operating systems, both were posting data to Datadog:
a) Windows 10 Home (laptop)
b) Ubuntu 16.04 LTS (using the Vagrant box 'ubuntu/xenial64' on Virtualbox)

I completed all of the exercises and was half way completed with the "Collecting APM Data" section when my Vagrant SSH private key authentication produced the following error: "ssh_exchange_identification: read: Connection reset"

The 'ubuntu/xenial64' machine stopped posting to datadog.
I attempted to resolve and then decided to submit what I have.

You should be able to see via my 'events' history and logs linked to my login ID that I created 'dashboards', 'monitors', 'downtime scheduled', custom metrics, installed a database and its Datadog integration, etc. on the 'ubuntu/xenial64' machine.

I have included links to my dashboards at the end of this exercise.
I will attempt to add the necessary screenshots. I can email the screenshots and forward the 'alert' emails that I received, if needed.

Collecting Metrics:
Complete - Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
Complete - Install a database on your machine (MySQL) and then install the respective Datadog integration for that database.
Complete - Create a custom Agent check that submits a metric named 'my_metric' with a random value between 0 and 1000.
Complete - Change your check's collection interval so that it only submits the metric once every 45 seconds.

Bonus Question Can you change the collection interval without modifying the Python check file you created?
Yes, edit 'datadog.yaml' (local_copy_refresh_rate, refresh_period, rollup)

Visualizing Data:
Utilize the Datadog API to create a Timeboard that contains:
  Complete - Your custom metric scoped over your host.
  Complete - Any metric from the Integration on your Database with the anomaly function applied. (MySQL Kernal performance time)
  Complete - Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.
Once this is created, access the Dashboard from your Dashboard List in the UI:
  Complete - Set the Timeboard's timeframe to the past 5 minutes
  Complete - Take a snapshot of this graph and use the @ notation to send it to yourself.
  
Bonus Question: What is the Anomaly graph displaying?
When a metric deviates from an expected pattern.  It is detecting anomolies 2 deviations from the predicted data.

Monitoring Data
Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.

Complete - Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:
  Complete - Warning threshold of 500
  Complete - Alerting threshold of 800
  Complete - And also ensure that it will notify you if there is No Data for this query over the past 10m.
  
Please configure the monitor’s message so that it will:
  Complete - Send you an email whenever the monitor triggers.
  Complete - Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
  Complete - Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
  Complete - When this monitor sends you an email notification, take a screenshot of the email that it sends you.
  
Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:
  Complete - One that silences it from 7pm to 9am daily on M-F,
  Complete - And one that silences it all day on Sat-Sun.
  Complete - Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

Collecting APM Data:
Given the following Flask app (Python) instrument this using Datadog’s APM solution:

Created .py file and executed ddtrace-run without error.

Bonus Question: What is the difference between a Service and a Resource?
A 'service' is a set of processes that does the same job. A simple web app may consist of 2 services, for example, a single webapp and a single databasase service.

A 'resource' is a particular action for a service. For example, a web app (/user/home/web.user.home) -- another example is a SQL DB, the query itself (SELECT * FROM users where id=?)

Final Question:
Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?
Yes, once onboard, I will answer this question in detail.

Dashboard links:
https://app.datadoghq.com/dashboard/98j-74w-uny/mysql-kernal-performance-ubuntu-1604?tile_size=l&page=0&is_auto=false&from_ts=1552008600000&to_ts=1552095000000&live=true

https://app.datadoghq.com/dashboard/gj6-kk7-u9u/mymetric-ubuntu-1604?tile_size=l&page=0&is_auto=false&from_ts=1551924000000&to_ts=1552096800000&live=true

https://app.datadoghq.com/dash/integration/12/mysql---overview?tile_size=m&page=0&is_auto=false&from_ts=1549540800000&to_ts=1552132800000&live=true

https://app.datadoghq.com/dash/integration/3/system---networking?tile_size=m&page=0&is_auto=false&from_ts=1552091520000&to_ts=1552095120000&live=true

https://app.datadoghq.com/dash/integration/1/system---metrics?tile_size=m&page=0&is_auto=false&from_ts=1551495600000&to_ts=1552100400000&live=true

https://app.datadoghq.com/dash/integration/2/system---disk-io?tile_size=m&page=0&is_auto=false&from_ts=1551495600000&to_ts=1552100400000&live=true

https://app.datadoghq.com/dashboard/fc6-g7k-8wj/daves---hello-world-timeboard?tile_size=m&page=0&is_auto=false&from_ts=1552080960000&to_ts=1552095360000&live=true



