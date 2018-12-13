#!/usr/bin/python
from datadog import initialize, api

options = {
   'api_key': '17370fa45ebc4a8184d3dde9f8189c38',
   'app_key': 'b0d652bbd1d861656723c1a93bc1a2f22d493d57'
}

initialize(**options)

title = "Ryan Great Timeboard"
description = "My Timeboard that is super awesome"
graphs = [
{
  "title": "My Metric over my host",
  "definition": {
  "requests": [
    {
      "q": "avg:my_metric{host:secondaryhost.hennvms.net}",
      "type": "line",
      "style": {
        "palette": "dog_classic",
        "type": "solid",
        "width": "normal"
      },
      "conditional_formats": [],
      "aggregator": "avg"
    }
  ],
  "autoscale": "true",
  "viz": "timeseries"
  }
},
{
  "title": "MySQL Anomaly Function Applied",
  "definition": {
  "viz": "timeseries",
  "requests": [
    {
      "q": "anomalies(avg:mysql.performance.user_time{*}, 'basic', 2)",
      "type": "line",
      "style": {
        "palette": "dog_classic",
        "type": "solid",
        "width": "normal"
      },
      "conditional_formats": [],
      "aggregator": "avg"
    }
  ],
  "autoscale": "true"
  }
},
{
  "title": "My Metric Rollup Function",
  "definition": {
  "viz": "query_value",
  "requests": [
    {
      "q": "avg:my_metric{*}.rollup(sum, 60)",
      "type": "line",
      "style": {
        "palette": "dog_classic",
        "type": "solid",
        "width": "normal"
      },
      "conditional_formats": [],
      "aggregator": "avg"
    }
  ],
  "autoscale": "true"
  }
}]

api.Timeboard.create(title=title, description=description, graphs=graphs)
