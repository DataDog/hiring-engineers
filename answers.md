Dashboard link: https://app.datadoghq.com/dashboard/lists
Datadog agent installed to host running on Vagrant VM
Mysql DB installed to same host

Collecting Metrics:
Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
- The following tags were added to the /etc/datadog-agent/datadog.yaml file 

-----------------------------
tags:
        - testtag1:test1
        - testtag2:test2
        - testtag3:test3
----------------------------

The uploaded screenshot (Datadog_Dashboard.PNG) shows these tags on the Host Map page of Datadog.

Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
- MySQL database is installed on the same host as where the Datadog Agent is installed
- Datadog integration with the MySQL was done by following the documentation: https://docs.datadoghq.com/integrations/mysql/

Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
- A my_metric.yaml was created 

Change your check's collection interval so that it only submits the metric once every 45 seconds.
- The my_metric.yaml was updated so the collection interval would be 45 seconds

Bonus Question Can you change the collection interval without modifying the Python check file you created?
- The collection interval can be modified at the instance level (/.datadog-agent/conf.d/<name>.yaml) by setting the following property:
  min_collection_interval 
  

