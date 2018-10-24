# My answers

## Collecting Metrics:

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

![Host Map](ddimg1.png)

* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

Postgres and integration installed.

* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

[Python](mycheck.py)
[YAML](mycheck.-yaml)

* Change your check's collection interval so that it only submits the metric once every 45 seconds.

Already done, see YAML.

* Bonus Question Can you change the collection interval without modifying the Python check file you created?

Didnt change the Python, configured it via YAML (min_collection_interval: 45) straight away. Another solution would be to create a cron job or similar which calls the check with "udo -u dd-agent -- datadog-agent check mycheck",

## Visualizing Data:

* Your custom metric scoped over your host.
* Any metric from the Integration on your Database with the anomaly function applied.
* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
* Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.

[APICallScript](curlapi.sh) This curl script is not working properly. It throws an error with the anomaly function. This is an open issue, ticket:#176636.

* Once this is created, access the Dashboard from your Dashboard List in the UI:
* Set the Timeboard's timeframe to the past 5 minutes
* Take a snapshot of this graph and use the @ notation to send it to yourself.

![Dashboard](ddimg2.png)


* Bonus Question: What is the Anomaly graph displaying?

