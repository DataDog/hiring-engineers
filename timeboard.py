from datadog import initialize, api

options = {
    'api_key': 'cb70192c7fc57a7a5a752bbe792f05ad',
    'app_key': 'f0259c978ad5d79405f54d2d913b955e0c4e98cb'
}

initialize(**options)

title = "My Timeboard"
description = "Blanton's Timeboard for his evaluation."
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{host:ubuntu.blanton.cloud}"}
        ],
        "viz": "timeseries"
    },
    "title": "My Custom Metric"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(sum:mysql.net.connections{*}, 'basic', 2, direction='both', alert_window='last_15m', interval=60, count_default_zero='true')"}
        ],
        "viz": "timeseries"
    },
    "title": "MySql Connection Anomaly"
},
{
    "definition": {
        "requests": [
            {"q": "avg:my_metric{host:ubuntu.blanton.cloud}.rollup(sum, 60)"}
        ],
        "viz": "timeseries"
    },
    "title": "Total Custom Metrics for last hour"
}]

template_variables = [{
    "name": "ubuntu.blanton.cloud",
    "prefix": "host",
    "default": "host:ubuntu.blanton.cloud"
}]

read_only = True
response = api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)
print(response)
