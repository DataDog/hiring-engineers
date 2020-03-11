#!/usr/bin/python
from datadog import initialize, api

options = {
   'api_key': os.environ['DDOG_API_KEY'],
   'app_key': os.environ['DDOG_APP_KEY']
}

initialize(**options)

title = "Stage Timeboard - NP"
description = "Stage Timeboard for the National Parks app deployment."
graphs = [
{
  "title": "Database Host - My Metrics",
  "definition": {
  "requests": [
    {
      "q": "avg:my_metric{host:octodev01.billmeyer.corp}",
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
  "title": "Web Host - My Metrics",
  "definition": {
  "requests": [
    {
      "q": "avg:my_metric{host:octodev02.billmeyer.corp}",
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
  "title": "MongoDB Anomaly Function Applied",
  "definition": {
  "viz": "timeseries",
  "requests": [
    {
      "q": "anomalies(avg:mongodb.opcounters.queryps{*}, 'basic', 2)",
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
