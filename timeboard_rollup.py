import os
from datadog import initialize, api

api_key = os.environ['api_key']
app_key = os.environ['app_key']

options = {'api_key': api_key,
           'app_key': app_key}

initialize(**options)

title = "ddogd3m0 Timeboard"
description = "My Random Check"
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "my_random_check{*}.rollup(sum, 60)"}
        ],
        "viz": "timeseries"
    },
    "title": "My Random Check"
}]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:my-host"
}]

read_only = True
new_timeboard = api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)
