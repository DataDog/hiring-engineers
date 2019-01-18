from datadog import initialize, api

options = {
    'api_key': 'abc',
    'app_key': 'def'
}

initialize(**options)

title = "My Timeboard from API"
description = "Hiring Test"


graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "my_metric{env:local}"}
        ],
        "viz": "timeseries"
    },
    "title": "my_metric"
},{
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:mysql.performance.cpu_time{*}, 'basic', 3)"}
        ],
        "viz": "timeseries"
    },
    "title": "Avg CPU time"
},{
    "definition": {
        "events": [],
        "requests": [
            {"q": "sum:my_metric{env:local}.rollup(sum, 3600)"}
        ],
        "viz": "query_value"
    },
    "title": "Sum of my_metric /hour"
}]

template_variables = [{
    "name": "host-name",
    "prefix": "host-pre",
    "default": "host:ubuntu-xenial"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)