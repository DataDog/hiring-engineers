from datadog import initialize, api

options = {
    'api_key': '<api key>',
    'app_key': '<app key>'
}

initialize(**options)

title = "My Metric"
description = "all about my metric"
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{*}"}
        ],
        "viz": "timeseries"
    },
    "title": "scope"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{*}.rollup(sum, 3600)"}
        ],
        "viz": "timeseries"
    },
    "title": "rollup"
}
]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:my-host"
}]

read_only = True

print api.Timeboard.create(
        title=title,
        description=description,
        graphs=graphs,
        template_variables=template_variables,
        read_only=read_only
       )
