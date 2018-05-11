from datadog import initialize, api

options = {
    'api_key': '1fb7eafb0c00427eba0dd20070d2bbb6',
    'application_key': '7214295e75df236125e7dd8c535b94b57683be73',
}

initialize(**options)

title = "Jake's First Timeboard"
description = "A super informative Timeboard of random metrics"
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {
                "q": "my_metric{host:ubuntu}",
                "type": "line",
                "style": {
                    "palette": "cool",
                    "type": "dash",
                    "width": "thin"
                }
            }
        ],
        "viz": "timeseries"
    },
    "title": "my_metric Value from Ubuntu host"
},
    {
    "definition": {
        "viz": "timeseries",
        "events": [],
        "requests": [
            {
                "q": "anomalies(avg:mongodb.extra_info.heap_usage_bytesps{role:database:mongo}, 'basic', 1.5)",
                "type": "line",
                "style": {
                    "palette": "cool",
                    "type": "solid"
                }
            }
        ],
    },
    "title": "Average MongoDB heap usage with Anomaly Detection"
},
    {
    "definition": {
        "viz": "timeseries",
        "requests": [
            {
                "q": "avg:my_metric{*}.rollup(sum, 3600)",
                "type": "line",
                "style": {
                    "palette": "cool",
                    "type": "solid",
                    "width": "thick"
                },
            }
        ],
    },

    "title": "Sum of random metric over 1 hour duration"
}
]

template_variables = [{
    "name": "test",
    "prefix": "host",
    "default": "host:ubuntu"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)
