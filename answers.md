Your answers to the questions go here.

Collecting Metrics:
Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
  I attached the picture as hosttags.png

Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
  I installed MongoDB

Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
Change your check's collection interval so that it only submits the metric once every 45 seconds.
Bonus Question Can you change the collection interval without modifying the Python check file you created?

  I researched https://docs.datadoghq.com/agent/agent_checks/ in order to complete this section.  I attached the code accordingly for the check and the python code.  I was not able to modify the collection interval without modifying the check file.  I tried to see how to write in python to submit the metric every 45 seconds, but I was unable to do so.  The code used is in checkvalue.py and checkvalue.yaml

Visualizing Data:
Utilize the Datadog API to create a Timeboard that contains:

Your custom metric scoped over your host.
  Was able to do, attached the JSON i submitted via CURL called API

Any metric from the Integration on your Database with the anomaly function applied.
  Was not able to do.  I was investigating why the mongoDB was not providing data.  When viewing the checks, I noticed that I was getting an error because I was notusing -replset.  Looking up the error led me to a mongoDB page that was providing instruction on how to create a replica set:
https://docs.mongodb.com/manual/tutorial/deploy-replica-set/
I added my localhost accordingly, but was not able to get this done accordingly.  I am still trying to get this work, but I am submitting without this metric at this time.  I am also not sure what the "anomaly function" is.

Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timemboard.
  Attached the script and screenshot of each chart accordingly.


Once this is created, access the Dashboard from your Dashboard List in the UI:

Set the Timeboard's timeframe to the past 5 minutes
Take a snapshot of this graph and use the @ notation to send it to yourself.
Bonus Question: What is the Anomaly graph displaying?
  Attached timeboard screenshot as graph1, graph2, and dashboard

Monitoring Data
Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

Warning threshold of 500
Alerting threshold of 800
And also ensure that it will notify you if there is No Data for this query over the past 10m.
Please configure the monitor’s message so that it will:

Send you an email whenever the monitor triggers.

Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.

Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.

When this monitor sends you an email notification, take a screenshot of the email that it sends you.
  Attached screenshot of email called email in order to show the email.  I also attached two other pictures, monitorsetup and markdownscript.

Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

One that silences it from 7pm to 9am daily on M-F,
And one that silences it all day on Sat-Sun.
Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.
  Completed and attached email as downtime.

Collecting APM Data:
Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:

Note: Using both ddtrace-run and manually inserting the Middleware has been known to cause issues. Please only use one or the other.
  I inserted the middleware to the flask app provided.  I added the code as flaskproject.py
  
Bonus Question: What is the difference between a Service and a Resource?

Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.
  I am unsure what is considered an APM metric and an infrastructure metric.  I tried looking through the documentation, but was unable to determine it. I attached a picture of two metrics that I assume are APM and Infrastructure as APM.jpg

Please include your fully instrumented app in your submission, as well.
  Attached as flaskproject.py
  
Final Question:
Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?
  As mentioned, DataDog has beatend me to the blog post about Pokemon Go when it went down.  DataDog allows companies to measure performance of their applications.  Being a gamer myself, it would be interesting seeing how MOBA/online games use DataDog.  An interesting way would be with League of Legends and their matchmaking.  Not long ago, League of Legends updated their infrastructure to have all players go directly from their internet ISP to their services.  They were frustrated with ISP's they could not control, and wanted to make sure that if there was a problem, they could fix it.  With this change, I would also assume that a lot of their backend code has changed.  DataDog could measure the performance of the backend to see the improvement and if their servers are able to handle all the direct bandwidth.
