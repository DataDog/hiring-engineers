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

![Bonus Question](/images/interval-option.png)
