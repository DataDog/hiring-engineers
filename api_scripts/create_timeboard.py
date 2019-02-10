from datadog import initialize, api
from pprint import pprint

options = {
    'api_key': '81ea6f015908fcb85d3e7e963ca9aa75',
    'app_key': '74d54a491ab8678eee5bccc48d108d4148e98aa4'
}

initialize(**options)

title = "Adam's Custom Timeboard"
description = "Simple Host Overview"
graphs = [
{
    "title": "my_metric scoped over host:adam_host",
    "definition": {
        "viz": "timeseries",
        "requests": [{
            "q": "anomalies(avg:my_metric{host:adams_host}, 'basic', 2)",
            "type": "area",
            "style": {
                "palette": "purple",
                "type": "solid",
                "width": "normal",
            },
            "aggregator": "avg",
        }],
    },
},
{
    "title": "MySQL Queries and Anomalies",
    "definition": {
        "viz": "timeseries",
        "requests": [{
            "q": "anomalies(avg:mysql.performance.queries{*}, 'basic', 2)",
            "type": "line",
            "style": {
                "palette": "cool",
                "type": "solid",
                "width": "normal",
            },
            "aggregator": "avg",
        }],
    },
},
{
    "title": "my_metric Hourly Sums",
    "definition": {
        "viz": "timeseries",
        "requests": [
            {
            "q": "avg:my_metric{*}.rollup(sum, 3600)",
            "type": "bars",
            "style": {
                "palette": "dog_classic",
                "type": "solid",
                "width": "normal"
            },
            "aggregator": "avg",
            }
        ],
    },
},
]

read_only = True
response = api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     read_only=read_only)
pprint(response)