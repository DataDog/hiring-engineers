import os
from datadog import initialize, api

# KEYS
options = {
    'api_key': "MY_API_KEY",
    'app_key': "MY_APP_KEY"
}

initialize(**options)

# Create Graphs
custom_metrics_graph = {
    "title": "Hello World Instance",
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:hello.world{*}"}
        ],
        "viz": "timeseries"
    }
}
anomaly_graph = {
    "title": "Anomaly Graph of PostgresQL",
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:postgresql.bgwriter.write_time{*}.as_count(), 'basic', 2)"}
        ],
        "viz": "timeseries"
    }
}

custom_rollup_graph = {
    "title": "Sum Rollup of Hello World for past hour",
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:hello.world{*}.rollup(sum, 3600)"}
        ],
        "viz": "timeseries"
    }
}

title       = "Custom Metrics for Timeboard"
description = "A Timeboard to display metrics, anomaly and rollup"
graphs      = []

graphs.append(custom_metrics_graph)
graphs.append(anomaly_graph)
graphs.append(custom_rollup_graph)

template_variables = [{
    "name": "Sanjana",
    "prefix": "host",
    "default": "host:sanjanaraj"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)
