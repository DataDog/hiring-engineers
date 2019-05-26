## Prerequisites - Setup the environment

I spun up a new Amazon Linux EC2 instance in AWS as my Datadog host for this exercise.  I then installed the Datadog agent

``DD_API_KEY=xxxxxx bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
``

(actual API key removed from command) 

The agent started and reported back to the Datadog UI


## Collecting Metrics:

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.


![ScreenShot](img/hostmap1.JPG)

(I also added the agent to a second EC2 host just to see what it looks like in the UI)

* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

I installed a MySQL database as you can see from the tag on my host - see mysql1.jpg

```
sudo yum install mysql-server
sudo service mysqld start
mysql -u root -p
```

and then created the Datadog MySQL users as per integration instuctions

* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.


![ScreenShot](img/mymetric1.JPG)

see files in the code directory in this repo:

/etc/datadog-agent/conf.d/custom_my_metric.yaml

/etc/datadog-agent/checks.d/custom_my_metric.py

[custom_my_metric.yaml](code/custom_my_metric.yaml)

[custom_my_metric.py](code/custom_my_metric.py)

* Change your check's collection interval so that it only submits the metric once every 45 seconds.

This is done in the yaml file: /etc/datadog-agent/conf.d/custom_my_metric.yaml

* **Bonus Question** Can you change the collection interval without modifying the Python check file you created?

Yes, change the YAML file instead of the python file as follows:

``min_collection_interval: 45
``

## Visualizing Data:

Utilize the Datadog API to create a Timeboard that contains:

* Your custom metric scoped over your host.
* Any metric from the Integration on your Database with the anomaly function applied.
* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

see script: api_call.py

Once this is created, access the Dashboard from your Dashboard List in the UI:

* Set the Timeboard's timeframe to the past 5 minutes

Timeboard can only be set to the last 15 mins as far as I can tell?

* Take a snapshot of this graph and use the @ notation to send it to yourself.


![ScreenShot](img/email_mymetric1.JPG)


* **Bonus Question**: What is the Anomaly graph displaying?

The anomaly graph is telling me that it doens't have enough historical data yet for this algorithm.

## Monitoring Data

Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.

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

I used the given Flask app in my exercise - see apm_app.py in the code folder


* **Bonus Question**: What is the difference between a Service and a Resource?

Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

Please include your fully instrumented app in your submission, as well.

## Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?
