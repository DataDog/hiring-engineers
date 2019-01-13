from datadog import initialize, api

options = {
    'api_key': 'c4dc0b5c7063b9e0fc14131c918b5e32',
    'app_key': '685db677bb60dbbe589ad55481daf531baf62500'
}


initialize(**options)

title = "Timeboard and Metric"
description = "A timeboard displaying metric data"
graphs = [
    {
        "definition": {
            "events": [],
            "requests": [
                {"q": "avg:my_metric{host:vagrant}"}
            ],
            "viz": "timeseries"
        },
        "title": "My Metric"
    },
    {
        "definition": {
            "events": [],
            "requests": [
                {"q": "anomalies(avg:postgresql.max_connections{host:vagrant}, 'basic', 2)"}
            ],
            "viz": "timeseries"
        },
        "title": "PostgreSQL Anomaly"
    },
    {
        "definition": {
            "events": [],
            "requests": [
                {"q": "avg:my_metric{host:vagrant}.rollup(sum, 3600)"}
            ],
            "viz": "timeseries"
        },
        "title": "Rollup"
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
