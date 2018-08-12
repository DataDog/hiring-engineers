from datadog import initialize, api
import json

options = {
    'api_key': '644abd01377d26f1772a50742ea1fbd6',
    'app_key': '82b19c85b999628e638a9f01edaf5c63e91e384e'
}

initialize(**options)

#Get all mySQL metrics
mysqlMetrics=api.Infrastructure.search(q="metrics:mysql")["results"]["metrics"]
nbrOfMySQLMetrics=len(mysqlMetrics)

# Create a new monitor
def CreateMonitor(metricQuery):
    optionsMonitor = {
        "notify_no_data": True,
        "no_data_timeframe": 20
    }
    tags = ["anomaly:mySQL"]
    api.Monitor.create(
        type="anomaly",
        query="avg:"+metricQuery+"{host:DESKTOP-5U5D1JV}",
        name="mySQL Anomalies",
        message="There are some anomalies on your mySQL integration",
        tags=tags,
        options=optionsMonitor
    )


#Create for each mySQL metric its monitor and prepare requests for timeboard creation
request="{\"response\":[{\"q\": \"hour_before(sum:my_metric{host:DESKTOP-5U5D1JV})\",\"type\": \"line\"},"

for i in range(0, nbrOfMySQLMetrics):
    CreateMonitor(mysqlMetrics[i])
    mysqlNextMetric="{\"q\": \"avg:"+mysqlMetrics[i]+"{host:DESKTOP-5U5D1JV}\",\"type\": \"line\"},"
    request+=mysqlNextMetric

requestJSON=json.loads(request[0:-1]+"]}")["response"]

#Create the timeboard containing the custom metric and all mySQL metrics
title = "myFirstTimeboard"
description = "Timeboard for my custom metric"
graphs = [{
    "definition": {
        "events": [],
        "requests": requestJSON,
        "viz": "timeseries"
    },
    "title": "sumRandomValues"
    }]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:DESKTOP-5U5D1JV"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)
