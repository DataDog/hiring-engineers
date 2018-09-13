from datadog import initialize, api

options = {
    'api_key': 'ef6beb34bcb4b05c3ddca8d92b616d99',
    'app_key': '021c1515fee71183c6d3891fe5d727e251375cad'
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
