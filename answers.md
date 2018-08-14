# Rachel Jackson-Holmes - Answers

## Collecting Metrics:

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
<img width="1147" alt="hostmap-with-tags" src="https://user-images.githubusercontent.com/17325777/44066284-7e3ef2f2-9f3d-11e8-9be0-8dff5f40a48f.png">

* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

**Successful PostgreSQL integrations on dashboard**
<img width="1146" alt="psql-integration-successful-on-dashboard" src="https://user-images.githubusercontent.com/17325777/44066425-3d7786ca-9f3e-11e8-8e3e-b72db4f63aed.png">

**PostgreSQL integration info check in terminal**
<img width="900" alt="psql-agent-check" src="https://user-images.githubusercontent.com/17325777/44067267-ade4eca0-9f42-11e8-9acd-8ecbf54be1ca.png">

**PostgreSQL integration confirmation via Datadog Agent Manager - Checks Summary**
<img width="1029" alt="checks-summary" src="https://user-images.githubusercontent.com/17325777/44067358-13131304-9f43-11e8-9b71-71982cbd498f.png">

* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

**Agent Check metric script w/random value**
<img width="1054" alt="custom-metric" src="https://user-images.githubusercontent.com/17325777/44067501-d74def14-9f43-11e8-9794-9bef800cd07c.png">

* Change your check's collection interval so that it only submits the metric once every 45 seconds.

**collection interval of cutsom metric changed to submit metric once every 45 seconds**
<img width="1018" alt="interval" src="https://user-images.githubusercontent.com/17325777/44067817-4401e4fc-9f45-11e8-9d7a-2ff138d7648e.png">

## Visualizing Data:

Utilize the Datadog API to create a Timeboard that contains:

* Your custom metric scoped over your host.
* Any metric from the Integration on your Database with the anomaly function applied.
* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.

Once this is created, access the Dashboard from your Dashboard List in the UI:

* Set the Timeboard's timeframe to the past 5 minutes
* Take a snapshot of this graph and use the @ notation to send it to yourself.
* **Bonus Question**: What is the Anomaly graph displaying?
