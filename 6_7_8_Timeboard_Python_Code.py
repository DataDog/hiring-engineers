#!/opt/datadog-agent/embedded/bin/python

import datadog
from datadog import initialize, api

options = {
    'api_key': 'cd02ee5f618e30da34729601c6b4a57f',
    'app_key': 'fe990d6d6fc005c91a4e76a5504dc346175f699a'
}

initialize(**options)

title = "My Metric Timeboard"
description = "My Metric Timeboard."
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:random.my_metric{*}"}
        ],
        "viz": "timeseries"
    },
    "title": "My_Metric"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:mongodb.extra_info.heap_usage_bytesps{*}, 'basic', 3)"}
        ],
        "viz": "timeseries"
    },
    "title": "Mongo_Heap_Usage_Anomaly"
},

{
 "definition": {
        "events": [],
        "requests": [
            {"q": "sum:random.my_metric{*}.rollup(sum,3600)"}
        ],
        "viz": "timeseries"
    },
    "title": "My_Metric_1Hour_Rollup"

}

]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:ubuntu-xenial"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)
