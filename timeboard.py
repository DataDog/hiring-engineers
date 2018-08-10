#!/usr/bin/env/python3.6
from datadog import initialize, api

# keys added here for convenience, in production they should probably be passed as environment variables

options = {"api_key": "fca79176336236ae32fb2548e0ea51a3", "app_key":"2f36f4bc5c64535d1ce24b6e93d03fb83b5aa882" }

initialize(**options)

title = "Laura's Timeboard"
description = "An informative timeboard."
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "my_metric.my_metric{host:ubuntu-bionic}"}
        ],
        "viz": "timeseries"
    },
    "title": "My Metric"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "my_metric.my_metric{host:ubuntu-bionic}.rollup(avg, 3600)"}
        ],
        "viz": "timeseries"
    },
    "title": "My Metric with Rollup Function"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:mongodb.connections.totalcreated{*}, 'basic', 2)"}
        ],
        "viz": "timeseries"
    },
    "title": "MongoDB Total Connections Created with Anomaly"
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

