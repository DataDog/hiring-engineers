## Collecting Metrics:

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

 <img src="https://i.imgur.com/ZEhmwqB.png" width="600" height="300" alt=""> </a>
 <img src="https://i.imgur.com/dd4nkFk.png" width="600" height="300" alt=""> </a>

* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
 <img src="https://i.imgur.com/jutJVM9.png" width="600" height="300" alt=""> </a>
 <img src="https://i.imgur.com/ZVXWcKe.png" width="600" height="300" alt=""> </a>

* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
 <img src="https://i.imgur.com/01gUMrt.png" width="600" height="300" alt=""> </a>


* Change your check's collection interval so that it only submits the metric once every 45 seconds.
 <img src="https://i.imgur.com/LTkY5VY.png" width="600" height="300" alt=""> </a>


* **Bonus Question** Can you change the collection interval without modifying the Python check file you created?
 ANSWER: Yes, you can update the min_collection_interval value in the YAML config file of the corresponding check.

## Visualizing Data:

Utilize the Datadog API to create a Timeboard that contains:

* Your custom metric scoped over your host. 
 https://app.datadoghq.com/graph/embed?from_ts=1531762405184&to_ts=1531766005184&token=a22525f1cb91e94ae1416244645b138430ee7a2b8de5436931780f5a31ae2b96&height=300&width=600&legend=true&tile_size=m&live=true
* Any metric from the Integration on your Database with the anomaly function applied.
 https://app.datadoghq.com/graph/embed?token=d555bccdbf9fa979ba3b2410ccf31c1d02eacd95b7ed3151d170a670c55d8457&height=300&width=600&legend=true
* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
 https://app.datadoghq.com/graph/embed?token=bea6c08e445447b861664863ec2f044bd704c5cebe467d5af73cc4f3f0849652&height=300&width=600&legend=true
 
  <img src="https://i.imgur.com/vtuuIiZ.png" width="600" height="300" alt=""> </a>
 
 
Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.
Script found here: https://github.com/johanesteves/hiring-engineers/blob/solutions-engineer/createTimeboard.rb

Once this is created, access the Dashboard from your Dashboard List in the UI:

* Set the Timeboard's timeframe to the past 5 minutes
  <img src="https://i.imgur.com/KR9obUH.png" width="600" height="300" alt=""> </a>
* Take a snapshot of this graph and use the @ notation to send it to yourself.
  <img src="https://i.imgur.com/ERhJuOs.png" width="600" height="300" alt=""> </a>
* **Bonus Question**: What is the Anomaly graph displaying?
 ANSWER: Detects anomalous behaviour for a metric based on historical data

## Monitoring Data

Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

* Warning threshold of 500
* Alerting threshold of 800
* And also ensure that it will notify you if there is No Data for this query over the past 10m.

 <img src="https://i.imgur.com/M4WMrDo.png" width="450" height="500" alt=""> </a>

Please configure the monitor’s message so that it will:

* Send you an email whenever the monitor triggers.
* Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
* Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
 
  <img src="https://i.imgur.com/kg3LC7q.png" width="600" height="300" alt=""> </a>

 
* When this monitor sends you an email notification, take a screenshot of the email that it sends you. 
   <img src="https://i.imgur.com/e9Pzcaq.png" width="600" height="300" alt=""> </a>

* **Bonus Question**: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

  * One that silences it from 7pm to 9am daily on M-F,

   <img src="https://i.imgur.com/X7VaH8C.png" width="450" height="500" alt=""> </a>

  * And one that silences it all day on Sat-Sun.

   <img src="https://i.imgur.com/VSourSS.png" width="450" height="500" alt=""> </a>

  * Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.
  
   <img src="https://i.imgur.com/veFIrQn.png" width="600" height="300" alt=""> </a>

## Collecting APM Data:

Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

   <img src="https://i.imgur.com/sn9K5X6.png" width="600" height="300" alt=""> </a>


Please include your fully instrumented app in your submission, as well.
Link to App: https://github.com/johanesteves/hiring-engineers/blob/solutions-engineer/apmtest.py

* **Bonus Question**: What is the difference between a Service and a Resource?
ANSWER: a service is a set of processes that do the same job	, while a resource is a certain action for a service.

## Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?
