Your answers to the questions go here.

# Collecting Metrics
```
tags:
  - test
  - role:pgs
  - env:poc
```
![tags](/tags.png) 

![Postgres Integration](/pgs_integration.png) 
Bonus Question:
You can modify the yaml file to change the collection interval
```
init_config:

instances:
  - min_collection_interval: 45

```

# Visualizing Data


https://app.datadoghq.com/dash/1033029/api-timeboard
created by apitimeboard.py

![Last 5 Minutes](/last5.png)

Bonus Question

The anomaly graph is showing my metric of postgresql rows returned in blue with the accepted range in grey. Where the line goes red , it shows values outside the accepted range.

# Monitoring Data
![Alert](/alert.png)
Bonus Question: 
![downtime](/downtime.png)
![downtimestartedemail](/downtimestarted.png)

# Collecting APM Data

![apmdashboard](/infaandapm.png)
https://app.datadoghq.com/dash/1033000/infrastructure-and-apm


Bonus Question
A service would be defined for a particular functional piece of your application such as a ui or backend microservices. A resource is a particular action in a service such as a specific endpoint in a service. 

# Final Question:



