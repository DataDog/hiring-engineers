#!/usr/bin/python3
from datadog import initialize, api

options = {
    'api_key': '86e4ea22dab873115d8b80d72850d026',
    'app_key': '9fdc72abc9fc73c01a6474359a53d2f95f491446'
}

initialize(**options)

title = "My Timeboard Raimbault2"
description = "An informative timeboard."
graphs = [

{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:raimbault.my_metric{host:precise64}"}
        ],
        "viz": "timeseries"
    },
    "title": "Average my_metric over my host"
},

{
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:mysql.performance.user_time{host:precise64}, 'basic', 2)"}
        ],
        "viz": "timeseries"
    },
    "title": "Anomalies on mysql performance user time"
},

{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:raimbault.my_metric{host:precise64}.rollup(sum,3600)"}
        ],
        "viz": "timeseries"
    },
    "title": "Average my_metric with rollup"
}

]

template_variables = []

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)
