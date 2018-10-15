from datadog import initialize, api

options = {
    'api_key': '717d7b8ca1536aa28d425f28f9256b45',
    'app_key': 'a3e0eadc84d51acd617b7bdb330d2f60fcee1ded'
}

initialize(**options)

title = "My Timeboard and My Metric"
description = "A timeboard displaying metric data."
graphs = [
    {
        "definition": {
            "events": [],
            "requests": [
                {"q": "avg:my_metric{*}"}
            ],
            "viz": "timeseries"
        },
        "title": "My Metric Scoped"
    },
    {
        "definition": {
            "events": [],
            "requests": [
                {"q": "anomalies(avg:postgresql.commits{*}, 'basic', 3)"}
            ],
            "viz": "timeseries"
        },
        "title": "PostgreSQL Commits Anomaly"
    },
    {
        "definition": {
            "events": [],
            "requests": [
                {"q": "avg:my_metric{*}.rollup(sum, 3600)"}
            ],
            "viz": "timeseries"
        },
        "title": "My Metric Rollup"
    },

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
