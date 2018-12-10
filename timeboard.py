from datadog import initialize, api

options = {
    'api_key': 'api_key',
    'app_key': 'app_key'
}

initialize(**options)

title = "Timeboard - API Created 3"
description = "Custom Timeboard"
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{host:DataDog01}"},
        ],
        "viz": "timeseries"
    },
    "title": "my_metric / host:DataDog01"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:mysql.innodb.data_writes{host:DataDog01}, 'basic', 2)"}
        ],
        "viz": "timeseries"
    },
    "title": "MySql Data Writes anomalies"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{host:DataDog01}.rollup(sum, 3600)"}
        ],
        "viz": "timeseries"
    },
    "title": "my_metric rollup 1 hour"
}
]

template_variables = [{
    "name": "DataDog01",
    "prefix": "host",
    "default": "host:DataDog01"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)