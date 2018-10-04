from datadog import initialize, api

options = {
    'api_key': 'e2153221b4caadb8f04b1a973d901dd2',
    'app_key': 'c002b47fde144736c6674e163a84dc7a35c3f467'
}

initialize(**options)

title = "Timeboard 3 - Custom metric scoped over ashif.com"
description = "Visualizing Data - Task 1"
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{*}"}
        ],
        "viz": "timeseries"
    },
    "title": "Average Customer Metric"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:system.cpu.idle{*}, 'basic', 3)"}
        ],
        "viz": "timeseries"
    },
    "title": "Average CPU Idle reported by MySQL Dashboard"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{*}.rollup(sum,3600)"}
        ],
        "viz": "timeseries"
    },
    "title": "Average Customer Metric Rollup"
}]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:ashif.com"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)

