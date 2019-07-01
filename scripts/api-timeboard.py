from datadog import initialize, api

options = {
    'api_key': "DELETED API KEY",
    'app_key': "DELETED APP KEY"
}

initialize(**options)

my_metrics_graph = {
  "viz": "timeseries",
  "requests": [
    {
      "q": "avg:my_metric{host:C3PO} by {host}",
      "type": "area",
      "style": {
        "palette": "dog_classic",
        "type": "solid",
        "width": "normal"
      },
      "aggregator": "avg",
      "conditional_formats": []
    }
  ],
  "autoscale": true
}

mysql_cpu_anomaly_graph = {
  "viz": "timeseries",
  "requests": [
    {
      "q": "anomalies(avg:mysql.performance.cpu_time{host:C3PO}, 'basic', 2)",
      "type": "line",
      "style": {
        "palette": "dog_classic",
        "type": "solid",
        "width": "normal"
      },
      "aggregator": "avg",
      "conditional_formats": []
    }
  ],
  "autoscale": true
}

my_metric_rollup_graph = {
  "viz": "query_value",
  "requests": [
    {
      "q": "avg:my_metric{*}.rollup(sum, 3600)",
      "type": null,
      "style": {
        "palette": "dog_classic",
        "type": "solid",
        "width": "normal"
      },
      "aggregator": "avg",
      "conditional_formats": []
    }
  ],
  "autoscale": true
}
title       = "MyDashboard"
description = "A dashboard for the Datadog assessment"
graphs      = []

graphs.append(my_metrics_graph)
graphs.append(mysql_cpu_anomaly_graph)
graphs.append(my_metric_rollup_graph)

template_variables = [{
    "name": "DatadogExercise,
    "prefix": "host",
    "default": "C3PO"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)
