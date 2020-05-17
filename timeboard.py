from datadog import initialize, api

options = {
    'api_key': '77be3ef7547da187cd332cfc691bb304',
    'app_key': '3637663eeefed92bca57ad351d4da62b358f3162'
}

initialize(**options)

title = "Marc's Timeboard"
description = "Marc's Timeboard"
graphs = [
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric.gauge{*}"}
        ],
        "viz": "timeseries"
    },
    "title": "My Metric"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric.gauge{*} by {host}.rollup(sum, 3600)"}
        ],
        "viz": "timeseries"
    },
    "title": "My Metric Rollup"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(mysql.innodb.buffer_pool_total{*}, 'basic' ,3)"}
        ],
        "viz": "timeseries"
    },
    "title": "MySQL Buffer Pool Total Anomaly"
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