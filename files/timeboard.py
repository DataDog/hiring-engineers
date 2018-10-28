from datadog import initialize, api

options = {
    'api_key': 'c982086410a8e020add0deaf1b1f7600',
    'app_key': '068f3e525c273756d1901ef6f1877619fb746bd4'
}

initialize(**options)

title = "My Timeboard and My Metric"
description = "A timeboard displaying metric data."
graphs = [
    {
        "definition": {
            "events": [],
            "requests": [
                {"q": "avg:my_metric{host:ubuntu-xenial}"}
            ],
            "viz": "timeseries"
        },
        "title": "My Metric Scoped"
    },
    {
        "definition": {
            "events": [],
            "requests": [
                {"q": "anomalies(avg:postgresql.max_connections{host:ubuntu-xenial}, 'basic', 2)"}
            ],
            "viz": "timeseries"
        },
        "title": "PostgreSQL Connections Anomaly"
    },
    {
        "definition": {
            "events": [],
            "requests": [
                {"q": "avg:my_metric{host:ubuntu-xenial}.rollup(sum, 3600)"}
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
