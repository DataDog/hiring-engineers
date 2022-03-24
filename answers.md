## Collecting Metrics:

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

![Host Tags](/images/host-tags.png)

* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

![MySql Integration](/images/mysql-integration.png)

* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

![My Metric](/images/mymetric.png)

* Change your check's collection interval so that it only submits the metric once every 45 seconds.

![Min Collection Interval](/images/min_collection_interval.png)

**Finished Metric Report**

![My Metrics Graph](/images/mymetric-graph.png)

* **Bonus Question** Can you change the collection interval without modifying the Python check file you created?

Yes, this can be adjusted on the Metrics Explorer page. Choose your metric and then hit Edit. Under the "Metadata" section, you can input an interval.

![Bonus Question_1](/images/interval-option.png)

## Visualizing Data:

Utilize the Datadog API to create a Timeboard that contains:

* Your custom metric scoped over your host.
* Any metric from the Integration on your Database with the anomaly function applied.
* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

![Timeboard](/images/timeboard.png)

Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.

[Timeboard cURL Command](timeboard-api-request.txt)

Once this is created, access the Dashboard from your Dashboard List in the UI:

* Set the Timeboard's timeframe to the past 5 minutes

![Timeboard_Last5](/images/timeboard-last5.png)

* Take a snapshot of this graph and use the @ notation to send it to yourself.

![Snapshot](/images/snapshot.png)

![Snapshot Email](/images/snapshot-email.png)

* **Bonus Question**: What is the Anomaly graph displaying?

The way I have this graph set up displays any data that is "2" standard deviations off from the predicted values. This can help determine if current behavior of a metric is different than previous trends and patterns. For my graph specifically, the purple parts of the line graph are all CPU performance values within the predicted values, starting from 6.7e5 n% as a min. The red parts of the lines inidicate all instances in time when the performance was above or below those values.

## Monitoring Data

Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

* Warning threshold of 500
* Alerting threshold of 800
* And also ensure that it will notify you if there is No Data for this query over the past 10m.

![Monitor](/images/monitor.png)
[Monitor Export JSON](monitor-export.json)

Please configure the monitor’s message so that it will:

* Send you an email whenever the monitor triggers.
* Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
* Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
* When this monitor sends you an email notification, take a screenshot of the email that it sends you.

![Monitor Warning Email](/images/warning-email.png)

* **Bonus Question**: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

  * One that silences it from 7pm to 9am daily on M-F,
  * And one that silences it all day on Sat-Sun.
  * Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

![Downtimes](/images/downtimes.png)
![Weekday Downtime Email](/images/downtime-email.png)
![Weekend Downtime Email](/images/weekend-downtime-email.png)
