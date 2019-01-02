Your answers to the questions go here.

#Collecting Metrics
```
tags:
  - test
  - role:pgs
  - env:poc
```
(/tags.png "tags")

Integrations 
(postgresintegration.png "Postgres Integration")

Bonus Question:
You can modify the yaml file to change the collection interval
```
init_config:

instances:
  - min_collection_interval: 45

```

#Visualizing Data

Part 1 

Click Dashboards on the left 
Click New Dashboard on the Top Right
Enter a name for the dashboard (or use the default)
Click New Timeboard
Click Add Graph
Drag Timeseries onto the body of the graph below
Select your metric (in this case my_metric) in the metric section
Select your host from the "From" section
Click Done 

Part 2 

Drag another Timeseries onto your graph 
Choose the metric you would like anomaly function applied to. (in this case I chose postgres rows returned)
Click the + button and choose Algorithims , and then Anomalies
Click Done

Part 3 

Drag another Timeseries onto your graph 
Select your metric (in this case my_metric) in the metric section
Select your host from the "From" section
Click the + button and choose rollup and then sum
Since the period is in seconds enter 3600 (60*60) as the period 
click Done

(/last5.png "Last 5 minutes ")

Bonus Question

The anomaly graph is showing my metric of postgresql rows returned in blue with the accepted range in grey.

Monitoring Data
(/alert.png "Alert")


#Collecting APM Data

Bonus Question

From the documentation:
A service is a set of processes that do the same job.
A Resource is a particular action for a service.






