from datadog import initialize, api

options = {
  'api_key': 'xyz',
  'app_key': '13969b2a81854ff84b1705865086b4418830f0fb',
  'api_host': 'https://api.datadoghq.eu'
}

initialize(**options)

title = "Metric timeboard"
description = "my_metric timeboard."
a_graph = {
  "title": "my_metric",
  "definition": {
    "events": [],
    "requests": [
      {"q": "my_metric.gauge{*}"}
    ],
    "viz": "timeseries"
  }
}

anomaly_graph = {
  "title": "Metric anomaly graph",
  "definition": {
    "events": [],
    "requests": [
      {"q": "anomalies(avg:my_metric.gauge{*}.as_count(), 'basic', 2)"}
    ],
    "viz": "timeseries"
  }
}

rollup_graph = {
  "title": "Metric over one hour",
  "definition": {
    "events": [],
    "requests": [
      {"q": "avg:my_metric.gauge{*}.rollup(avg, 3600)"}
    ],
    "viz": "query_value"
  }
}

graphs = []
graphs.append(a_graph)
graphs.append(anomaly_graph)
graphs.append(rollup_graph)

host_variables = [{
  "name": "dgagent.glocal.lab",
  "prefix": "host",
  "default": "hosts:dgagent.glocal.lab"
}]

read_only = True

print(api.Timeboard.create(title=title,
                           description=description,
                           graphs=graphs,
                           template_variables=host_variables,
                           read_only=read_only))

