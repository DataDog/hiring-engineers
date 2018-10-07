#!/usr/bin/env python3.6

from datadog import initialize, api

options = {
    'api_key': 'b95c8e083ceec42accc4af841d80187d',
    'app_key': '0ee42a306f7a5aab45073e4a30587d5c0eb3408e'
}

initialize(**options)

title = "Aishwarya_TimeBoard"
description=""
graphs = [{
  "viz": "timeseries",
  "status": "done",
  "requests": [
    {
      "q": "avg:my_metric{host:AishVM-Vagrant}",
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
  "autoscale": true,
  "xaxis": {}
},{
  "viz": "timeseries",
  "status": "done",
  "requests": [
    {
      "q": "anomalies(avg:postgresql.bgwriter.checkpoints_timed{host:AishVM-Vagrant}.as_count(), 'basic', 2)",
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
  "autoscale": true,
  "xaxis": {}
},{
  "viz": "timeseries",
  "status": "done",
  "requests": [
    {
      "q": "avg:my_metric{host:AishVM-Vagrant}.rollup(sum, 3600)",
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
  "autoscale": true,
  "xaxis": {}
}]

template_variables = []

read_only = True

api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)
