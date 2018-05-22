# Answers from Ben Sunderland  -  May 18th 2017
====================================

## Part 1: Collecting Metrics
-------------------------------

After the agent installs on my Ubuntu VM, I added Tags as follows : 


Set the host's tags (optional) 

```
tags:
  - ben.com
  - env:dev1
  - role:docker_host1
```
Shown here is the host map view showing the custom tags : 

<img width="923" alt="host_map___datadog" src="https://user-images.githubusercontent.com/2524766/40302853-e0d357ce-5d33-11e8-89c0-52d8ef48f8b5.png">


# Install a database on your machine 

<img width="1371" alt="mysql_-_overview___datadog" src="https://user-images.githubusercontent.com/2524766/40284386-d879ea1e-5cd1-11e8-8c0d-eca87724a476.png">

# Create a custom Agent check ....

<img width="1364" alt="metric_explorer___datadog" src="https://user-images.githubusercontent.com/2524766/40287597-aafa9abe-5cf1-11e8-9025-891e5c8476be.png">

(you can change the interval via the check config "min_collection_interval: 45" )

## Part 2: Visualizing Data
-------------------------------
Here is my script with the 3 graphs in the Timeboard : 

```
from datadog import initialize, api

options = {
    'api_key': 'c18b36aebb7ed23a8fb3c53aad91c38e',
    'app_key': '3de69df6bb0d2662d12d543d8f8eecdf615cd269'
}

initialize(**options)

title = "Bens Timeboard v2"
description = "DD Timeboard."
graphs = [
{
          "title": "Bens check scoped",
          "definition": {
              "events": [],
              "requests": [
                  {"q": "avg:my_metric{host:osboxes}"}
              ]
          },
          "viz": "timeseries"
      },

      {
          "title": "Bens Check roll up",
          "definition": {
              "events": [],
              "requests": [
                  {"q": "my_metric{host:osboxes}.rollup(sum,3600)"}
              ]
          },
          "viz": "timeseries"
      },

      {
          "title": "mysql anomaly",
          "definition": {
              "events": [],
              "requests": [
                  {"q": "anomalies(avg:mysql.performance.user_time{*}, 'basic', 2)" }
              ]
          },
          "viz": "timeseries"
      }

]

read_only = True 
api.Timeboard.create(title=title,description=description,graphs=graphs,read_only=read_only)


```
Here is the resultant timeboard : 

<img width="1326" alt="timeboard v3" src="https://user-images.githubusercontent.com/2524766/40341495-e73495e8-5dc8-11e8-8da5-80aa5e6407dc.png">

Here is the @message of the MySQL graph with Anomalies :

<img width="522" alt="events___datadog" src="https://user-images.githubusercontent.com/2524766/40302424-66adeac8-5d32-11e8-8627-8392aaa2ef83.png">

Anomaly detection is an algorithmic feature that allows you to identify when a metric is behaving differently than it has in the past, taking into account trends, seasonal day-of-week and time-of-day patterns. It is well-suited for metrics with strong trends and recurring patterns that are hard or impossible to monitor with threshold-based alerting.

In this example we are looking at mysql.performance.user_time metric and the gray envelope shows the range + or - 2 std deviations from a calcualted normal. In this case we are using the 'basic' modifier which:
"... uses a simple lagging rolling quantile computation to determine the range of expected values, but it uses very little data and adjusts quickly to changing conditions but has no knowledge of seasonal behavior or longer trends."







