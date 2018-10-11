from datadog import initialize, api

options = {
    'api_key': '[REDACTED]',
    'app_key': '[REDACTED]'
}

initialize(**options)

title = "AllTheThings Metric Timeboard"
description = "Displays AllTheThings metrics"
graphs = [{
    "definition": {
        "requests": [
            {"q": "sum:allthethings.checker.random{host:ubuntu-xenial}"},
        ],
        "viz": "timeseries"
    },
    "title": "allthethings.checker.random"
},
{
    "definition" : {
        "requests": [
            {"q": "anomalies(avg:system.load.1{host:ubuntu-xenial}, 'basic', 2)"},
            {"q": "anomalies(avg:system.load.5{host:ubuntu-xenial}, 'basic', 2)"},
            {"q": "anomalies(avg:system.load.15{host:ubuntu-xenial}, 'basic', 2)"},
            {"q": "anomalies(avg:postgresql.percent_usage_connections{host:ubuntu-xenial}, 'basic', 2)"}
        ],
        "viz": "timeseries"
    },
    "title": "Postgresql System Load and Percent usage connections"
},
{
    "definition": {
        "requests": [
            {"q": "avg:allthethings.checker.random{host:ubuntu-xenial}.rollup(sum, 3600)"}
        ],
        "viz": "timeseries"
    },
    "title": "allthethings.checker.random with rollup applied"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     read_only=read_only)