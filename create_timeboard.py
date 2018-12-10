from datadog import initialize, api

options = {
    'api_key': '1e4bc1602c9a7eeac37718d0b4fcd482',
    'app_key': '02e9c8a50a650907e979279ba2dd227deef90094'
}

initialize(**options)

title = "My Timeboard"
description = "An informative timeboard."
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "my_metric{*}"}
        ],
        "viz": "timeseries"
    },
    "title": "My Metric"},
    {
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(mysql.innodb.buffer_pool_utilization{*},'basic', 3, direction='above', alert_window='last_5m', interval=20, count_default_zero='true')"}
        ],
        "viz": "timeseries"
    },
    "title": "MySQL Buffer Pool Utilization"},
    {
    "definition": {
        "events": [],
        "requests": [
            {"q": "my_metric{*}.rollup(sum,1200)"}
        ],
        "viz": "timeseries"
    },
    "title": "My Metric Rollup"}
]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:ubuntu-xenial"
}]

read_only = True
res = api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)

print(res)
