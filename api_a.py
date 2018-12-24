
from datadog import initialize, api

options = {
    'api_key': 'ef8e0d56ed095b6d2f4e2dde8b96ae19',
    'app_key': 'f95d08ebdf3c79370bf5c069c6ce4c0f6db46241'
}

initialize(**options)

title = "My Timeboard_1"
description = "An informative timeboard."
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:system.mem.free{*}"}
        ],
        "viz": "timeseries"
    },
    "title": "Average Memory Free"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:system.mem.free{*} by {host}.rollup(sum, 3600)"}
        ],
        "viz": "timeseries"
    },
    "title": "Average Memory Free"
},
{
    "definition": {
        "events": [],
        "requests": [
             {"q": "anomalies(avg:mysql.performance.com_select{*}, 'basic', 2)"}
        ],
        "viz": "timeseries"
    },
    "title": "Average Memory Free"
}]

template_variables = [{
    "name": "karino",
    "prefix": "host",
    "default": "host:my-host"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)

