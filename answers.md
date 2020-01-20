
# DataDog Hiring Exercise - William Karges Answers

## Section 1 - Collecting Metrics

### Tags

Installed DataDog agent on my local Windows machine and added tags in the datadog.yaml.  It took me longer than it should've as I'm admitedly not great at coming up with naming conventions.

*tags:*
    *- "availability-zone:us-west"*
    *- "machine:local"*
    *- "env:test"*
	
![HostMap_Tags.png](assets/HostMap_Tags.png)

### Relational Database Integration

Installed MySQL and HeidiSQL (so I could have a UI) on my local Windows machine.  Added the datadog user to the MySQL DB to grant access for the DD Agent.  Configured the MySQL conf.yaml file to pass the appropriate database credentials.

This process is almost identical to a typical OLE DB integration but the DataDog agent gives you the ability for far more detailed machine & database monitoring as opposed to a simple SELECT query that you see in most relational DB integrations.

[conf.yaml](configfiles/conf.yaml)

![mySQL_integration.png](assets/mySQL_integration.png)

### Custom Agent

Created a custom agent by placing a python file in the checks.d repository and a matching .yaml file in the config.d repository.

Uses python [random](https://docs.python.org/3/library/random.html) library (specifically the randint function) with data dog [guage](https://docs.datadoghq.com/developers/metrics/agent_metrics_submission/?tab=gauge) metric submission to submit my_metric with a random integer value between 0 and 1000.

Used the **min_collection_interval** function in the yaml file to set the collection to every 45 seconds without modifying the python check file.

[PythonFile](configfiles/custom_ac1.py)
[YamlFile](configfiles/custom_ac1.yaml)

![my_metric.png](assets/my_metric.png)

## Section 2 - Visualizing Data



