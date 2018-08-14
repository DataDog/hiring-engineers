# Rachel Jackson-Holmes - Answers

## Collecting Metrics:

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
<img width="1147" alt="hostmap-with-tags" src="https://user-images.githubusercontent.com/17325777/44066284-7e3ef2f2-9f3d-11e8-9be0-8dff5f40a48f.png">

* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

**Successful PostgreSQL integrations on dashboard**
<img width="1146" alt="psql-integration-successful-on-dashboard" src="https://user-images.githubusercontent.com/17325777/44066425-3d7786ca-9f3e-11e8-8e3e-b72db4f63aed.png">

**PostgreSQL integration info check in terminal**
<img width="1270" alt="psql-integration-datadogagent-info-check" src="https://user-images.githubusercontent.com/17325777/44066441-50e27b66-9f3e-11e8-92b6-83b60af82947.png">

* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

* Change your check's collection interval so that it only submits the metric once every 45 seconds.
