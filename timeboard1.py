from datadog import initialize, api

options = {
    'api_key': '6e09ef6531275496aef61e2180c1154a',
    'app_key': '969b68cc7c3af0967e858ed1d56e0e7a2a003fd8'
}

initialize(**options)

title = "Johanan's Timeboard"
description = "Timeboard showing my custom metric."
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{host:Prestige.local}"}
        ],
        "viz": "timeseries"
    },
    "title": "My custom metric"
    }, {
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(mysql.performance.bytes_sent{*}, 'basic', 3)"}
        ],
        "viz": "timeseries"
    },
    "title": "MySQL Performance: Bytes sent"
    }, {
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{host:Prestige.local}.rollup(sum, 3600)"}
        ],
        "viz": "timeseries"
    },
    "title": "My custom metric: Hourly rollup sum"
    }
]


template_variables = [{
    "name": "Prestige.local",
    "prefix": "host",
    "default": "host:my-host"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)
