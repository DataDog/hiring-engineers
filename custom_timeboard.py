from datadog import initialize, api

options = {
    'api_key': '',
    'app_key': ''
}

initialize(**options)

title = "My Timeboard"
description=""
graphs = [{
  "viz": "timeseries",
  "status": "done",
  "requests": [
    {
      "q": "avg:system.uptime{host:WINDOWS-9I109KK}",
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
      "q": "anomalies(avg:mysql.performance.cpu_time{host:WINDOWS-9I109KK}.as_count(), 'basic', 2)",
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
      "q": "avg:system.uptime{host:WINDOWS-9I109KK}.rollup(sum, 3600)",
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