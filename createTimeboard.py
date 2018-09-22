from datadog import initialize, api

options = {
    'api_key': 'c3d5e000d3cf32c3da9a0754cd4534d0',
    'app_key': '6905d0e8b5ba89fbf414e4fe8e5536d09d1e1c9f'
}

initialize(**options)

title = "Timeboard via API"
description = "Created via API"
graphs = [
  {
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{*}"}
        ],
        "viz": "timeseries"
    },
    "title": "Average of My Metric"
  },
  {
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:mysql.innodb.data_reads{*}, 'basic', 2)",}
        ],
        "aggregator": "avg",
        "viz": "timeseries"
    },
    "title": "Average of InnoDB Data Reads - Anomaly"
  },
  {
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{*}.rollup(sum, 3600)"}
        ],
        "aggregator": "avg",
        "viz": "timeseries"
    },
    "title": "My Metric - 1 hour rollup"
  }
]
template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:my-host"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)

