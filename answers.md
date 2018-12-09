Collecting Metrics:
Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
![Alt text](Screenshots/host_with_tags_on_Host_Map.png "host with tags on Host Map")

Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
![Alt text](Screenshots/PostgreSQL_installed.png "PostgreSQL Installed")
![Alt text](Screenshots/status_check_ok_after_PostgreSQL_integration.png "Status Check OK")
![Alt text](Screenshots/check_ok_after_PostgreSQL_integration.png "Check OK after PostgreSQL installation")

Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
![Alt text](Screenshots/custom_metric_code.png "Code for Custom Metric")
![Alt text](Screenshots/status_check_ok_for_custom_metric.png "Status Check OK for Custom Metric")
![Alt text](Screenshots/custom_metric_check_ok.png "Check OK for Custom Metric")

Change your check's collection interval so that it only submits the metric once every 45 seconds.
![Alt text](Screenshots/yaml_code_for_custom_metric.png "yaml code for Custom Metric")

Bonus Question Can you change the collection interval without modifying the Python check file you created?

Yes, I updated the yaml file, not the Python file. Please see above.
