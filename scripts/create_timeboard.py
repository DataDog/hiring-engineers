#!/usr/bin/env python
from datadog import initialize, api

options = {
    'api_key': 'eac6a74dd2f40df0dfa9c2f390f09867',
    'app_key': '93398f1376c83a7179ab4a71a999532fa3921df2'
}

initialize(**options)

title = "Alicia Timeboard"
description = "An informative timeboard."
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{host:ubuntu-xenial}"}
        ],
        "viz": "timeseries"
    },
    "title": "my_metric status"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:mongodb.network.numrequestsps{*}, 'basic', 2)"}
        ],
        "viz": "timeseries"
    },
    "title": "Anomalies in MongoDB Number of requests per second"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{host:ubuntu-xenial}.rollup(sum, 3600)"}
        ],
        "viz": "timeseries"
    },
    "title": "my_metric sum of all points for the past hour"
}
]

read_only = True
response = api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     read_only=read_only)

print(response)