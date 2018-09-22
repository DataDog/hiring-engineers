Prerequisites - Setup the environment

16.04 LTS on IBM Softlayer in Seattle
<p><img src="http://spaceneedle.tancow.net/datadog/img1a.png" width="500" height="332">
<p><img src="http://spaceneedle.tancow.net/datadog/img1a.png" width="500" height="332">


Collecting Metrics:

Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
<p><img src="http://spaceneedle.tancow.net/datadog/img2a.png" width="500" height="332">
<p><img src="http://spaceneedle.tancow.net/datadog/img2b.png" width="500" height="332">

Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
<p><img src="http://spaceneedle.tancow.net/datadog/img3a.png" >
<p><img src="http://spaceneedle.tancow.net/datadog/img3b.png" >
<p><img src="http://spaceneedle.tancow.net/datadog/img3c.png" >
<p><img src="http://spaceneedle.tancow.net/datadog/img3d.png" >
<p><img src="http://spaceneedle.tancow.net/datadog/img3e.png" >

Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

Agent check is here: <a href=https://github.com/robdanz/hiring-engineers/blob/master/mymetric.py>mymetric.py</a>

Change your check's collection interval so that it only submits the metric once every 45 seconds.
<p><img src="http://spaceneedle.tancow.net/datadog/img5a.png">
<p><img src="http://spaceneedle.tancow.net/datadog/img5b.png" width="500" height="332">
    
Bonus Question Can you change the collection interval without modifying the Python check file you created?

I did this by setting the min_collection_interval to 45 in the <a href=https://github.com/robdanz/hiring-engineers/blob/master/mymetric.yaml>mymetric.yaml</a> file.

Visualizing Data:

Utilize the Datadog API to create a Timeboard that contains:

Your custom metric scoped over your host.
Any metric from the Integration on your Database with the anomaly function applied.
Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.

Link to dashboard:
https://app.datadoghq.com/dash/923684

Script is here:  <a href=https://github.com/robdanz/hiring-engineers/blob/master/createTimeboard.py>createTimeboard.py</a>

Once this is created, access the Dashboard from your Dashboard List in the UI:
Set the Timeboard's timeframe to the past 5 minutes
Take a snapshot of this graph and use the @ notation to send it to yourself.
<p><img src="http://spaceneedle.tancow.net/datadog/img6.png" width="500" height="332">
    
Bonus Question: What is the Anomaly graph displaying?
    Anomaly graph is automatically highlighting in red the data points are out of bounds of the typical historical measurements for this monitor.
<p><img src="http://spaceneedle.tancow.net/datadog/img7.png">

Monitoring Data

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

Warning threshold of 500
Alerting threshold of 800
And also ensure that it will notify you if there is No Data for this query over the past 10m.
<p><img src="http://spaceneedle.tancow.net/datadog/img8a.png" width="500" height="332">

Please configure the monitor’s message so that it will:

Send you an email whenever the monitor triggers.
Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
<p><img src="http://spaceneedle.tancow.net/datadog/img8b.png" width="500" height="332">

When this monitor sends you an email notification, take a screenshot of the email that it sends you.
<p><img src="http://spaceneedle.tancow.net/datadog/img9a.png" width="500" height="332">

Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

One that silences it from 7pm to 9am daily on M-F,
<p><img src="http://spaceneedle.tancow.net/datadog/img10a.png" width="500" height="332">
And one that silences it all day on Sat-Sun.
<p><img src="http://spaceneedle.tancow.net/datadog/img10b.png" width="500" height="332">

Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.
<p><img src="http://spaceneedle.tancow.net/datadog/img10c.png" width="500" height="332">

Collecting APM Data:

Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:

Bonus Question: What is the difference between a Service and a Resource?
   Service is the name of a set of processes that work together to provide a feature set.
   A resource is particular query to a service. 
   (this was admittedly Googled and copied from Nicholas Muesch's article from Aug 7)

Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.
   https://app.datadoghq.com/dash/923358/
<p><img src="http://spaceneedle.tancow.net/datadog/img11.png" width="500" height="332">
   
Please include your fully instrumented app in your submission, as well.
   I did this by manually inserting the Middleware into the provided Flask app, which you can find here:
   
   <a href=https://github.com/robdanz/hiring-engineers/blob/master/instrumentedApp.py>instrumentedApp.py</a>
   
   
   
