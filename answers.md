
# DataDog Hiring Exercise - William Karges Answers

## Section 1 - Collecting Metrics

### Tags

Installed DataDog agent on my local Windows machine and added tags in the datadog.yaml.  It took me longer than it should've as I'm admitedly not great at coming up with naming conventions.

*tags: - "availability-zone:us-west" - "machine:local" - "env:test"*
	
	
![HostMap_Tags.png](assets/HostMap_Tags.png)

### Relational Database Integration

Installed MySQL and HeidiSQL (so I could have a UI) on my local Windows machine.  Added the datadog user to the MySQL DB to grant access for the DD Agent.  Configured the MySQL conf.yaml file to pass the appropriate database credentials.

This process is almost identical to a typical OLE DB integration but the DataDog agent gives you the ability for far more detailed machine & database monitoring as opposed to a simple SELECT query that you see in most relational DB integrations.

[conf.yaml](configfiles/conf.yaml)

![mySQL_integration.png](assets/mySQL_integration.png)

### Custom Agent

Created a custom agent by placing a python file in the checks.d repository and a matching .yaml file in the config.d repository.

Uses the python [random](https://docs.python.org/3/library/random.html) library (specifically the **randint** function) with data dog [gauge](https://docs.datadoghq.com/developers/metrics/agent_metrics_submission/?tab=gauge) metric submission to submit my_metric with a random integer value between 0 and 1000.

Used the **min_collection_interval** function in the yaml file to set the collection to every 45 seconds without modifying the python check file.

[PythonFile](configfiles/custom_ac1.py)
[YamlFile](configfiles/custom_ac1.yaml)

![my_metric.png](assets/my_metric.png)

## Section 2 - Visualizing Data

Imported the DataDog API collection into Postman.  Customized the create dashboard POST requet to track my_metric averages and sum over the past hour as well as MySQL CPU usage anomalies.  See [WK_CustomTimeBoard JSON file](configfiles/WK_CustomTimeBoard.json)

### Create Dashboard API

![PostmanAPI_Success.png](assets/PostmanAPI_Success.png)

![TimeTable_1-21-2020.png](assets/TimeTable_1-21-2020.png)

Unfortunately I wasn't able to, "Set the Timeboard's timeframe to the past 5 minutes (see screenshot below).  While I can adjust individual graphs to 5 minutes, the timeboard itself seems to be restricted to 15 minute intervals.  Not sure if this is just a limitation of the trial version or maybe this was just a trick question.

### 5 Minute Snapshot

[TimeBoard Notification](assets/TimeBoard_Notification.eml)

![Error.png](assets/Error.png)

![5mGraph.png](assets/5mGraph.png)

![Notifications.png](assets/Notifications.png)

### **Bonus Question** What is the Anomaly graph displaying?




