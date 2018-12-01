# Datadog Timeboard Script
# imports
from datadog import initialize, api
from json import dump

# API initialization parameters
options = {'api_key': '956b376eda4be274a4d8a54fbfb84a42',
           'app_key': 'ab521a571251baa8202cef85a2d1a95bb2e26ffd'}

initialize(**options)

title = "Datadog Lab - Timeboard"
description = "Timeboard generated through Datadog APIs"
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:system.mem.free{*}"}
        ],
        "viz": "timeseries"
    },
    "title": "Average Memory Free"
}]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:my-host"
}]

read_only = True
apiResponse = api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)

#this will create a file named output.json in the current folder
with open("output.json", "w") as f:
    dump(apiResponse, f)
