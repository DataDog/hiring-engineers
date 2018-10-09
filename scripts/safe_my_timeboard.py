
from datadog import initialize, api

options = {
    'api_key': 'YOUR_API_KEY', 
    'app_key': 'YOUR_APP_KEY'
}

initialize(**options)

title = "My Custom Timeboard"
description = "Metrics from my_metrics and MySQL."
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{host:vagrant}"}
        ],
        "viz": "timeseries"
    },
    "title": "My Metric Scope"
    },
    {
    "definition": {
            "events": [],
            "requests": [
                {"q": "avg:my_metric{host:vagrant}.rollup(sum, 3600)"}
            ],
            "viz": "timeseries"
        },
        "title": "My_metric Scope Roll up (1 hour)"
    },
    {
    "definition": {
            "events": [],
            "requests": [
                {"q": "anomalies(avg:mysql.performance.com_select{host:vagrant}, 'basic', 60)"}
            ],
            "viz": "timeseries"
        },
        "title": "SQL Query Anomaly "

    }]


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

options = {
    "notify_no_data": True,
    "no_data_timeframe": 20
}

tags = ["SQL Query", "anomaly"]

print api.Monitor.create(
    type="metric alert",
    query="avg(last_1h):anomalies(avg:mysql.performance.com_select{host:vagrant}, 'basic', 60, direction='both', alert_window='last_5m', interval=20, count_default_zero='true') >= 1",
    name="SQL Query Anomaly detection",
    message="Anomaly detected (SQL Query).",
    tags=tags,
    options=options
)