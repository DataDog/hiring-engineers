#!/usr/bin/python
from datadog import initialize, api

options = {
    'api_key': 'c9d7be44f890c53fb51a6219247db32a',
    'app_key': '19b238a5ddd0fb3fed7c34384047b176995c69ce'
}

initialize(**options)

title = "HUFF Dashboards"
description = "HUFF Timeboard for Solutions Engineer Challeng"
graphs = [
{
  "title": "MYSQL Database Metrics over time",
  "definition": {
  "requests": [
    {
      "q": "avg:mysql.performance.cpu_time{*}",
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
########## Widget 2
{
  "title": "HUFF - My_Metrics over time",
  "definition": {
  "requests": [
    {
      "q": "anomalies(avg:my_metric.count{*}.as_count(), 'basic', 2)",
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
########## Next Widget
{
  "title": "My_Metric Count over time",
  "definition": {
  "viz": "timeseries",
  "requests": [
    {
      "q": "avg:my_metric.count{host:vagrant}.as_count()",
      "type": "query_value",
      "style": {
        "palette": "dog_classic",
        "type": "solid",
        "width": "normal"
      },
      "conditional_formats": [],
      "aggregator": "sum"
    }
  ],
  "autoscale": "true"
  }
},
{
  "title": "My Metric Rollup Function",
  "definition": {
  "requests": [
    {
      "q": "avg:my_metric{*}.rollup(sum, 60)",
      "type": "line",
      "style": {
        "palette": "dog_classic",
        "type": "query_value",
        },
      "aggregator": "sum"
    }
  ],
  "autoscale": "true"
  }
}]

api.Timeboard.create(title=title, description=description, graphs=graphs)
