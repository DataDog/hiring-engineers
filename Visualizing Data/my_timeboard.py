from datadog import initialize, api

options = {
    'api_key': '6b6aca5a303d9c08e1db89cddadd837a',
    'app_key': 'b5b91b7aed4fd27423ce537c7949a9ff710291f2'
}

initialize(**options)

title = "My Timeboard"
description = "Timeboard for Arlen Techincal Exercise"
graphs = [
{
    "definition": {
        "requests": [
           {
             "q": "avg:my_metric{*}",
             "type": "line",
             "aggregator": "avg",
           },
        ],
        "viz": "timeseries",
        "autoscale": "true"
    },
    "title": "My Metric"
},
{
    "definition": {
       "requests": [
           {
             "q": "anomalies(avg:mysql.performance.cpu_time{*}, 'basic', 3, direction='both', alert_window='l
ast_5m')",
             "type": "line",
           }
        ],
        "viz": "timeseries"
    },
    "autoscale": "true",
    "title": "MySQL Anomaly"
},
{
    "definition": {
        "requests": [
           {
             "q": "sum:my_metric{*}.rollup(sum,60)",
             "type": "line"
           }
        ],
        "viz": "query_value"
    },
    "autoscale": "true",
    "title": "My Metric Rollup"
} ]

template_variables = [{
    "name": "HOST",
    "prefix": "host",
    "default": "host:my-host"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)
