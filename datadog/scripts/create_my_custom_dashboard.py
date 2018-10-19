from datadog import initialize, api

options = {
    'api_key': '',
    'app_key': ''
}

initialize(**options)

title = "My Datadog Timeboard by Yuya"
description = "Timeboard for my custom metric and postgres metrics."
graphs = [
{ "definition": {
        "events": [],
        "requests": [
            {"q": "top(max:my_metric{*} by {host}, 10, 'last', 'desc'), top(max:my_metric{*} by {host}, 10, 'max', 'desc'), top(max:my_metric{*} by {host}, 10, 'min', 'desc'), top(max:my_metric{*} by {host}, 10, 'mean', 'desc')"}
        ],
        "viz": "timeseries"
    },
    "title": "Data for my_metric over host."
},
{ "definition": { 
        "events": [],
        "requests": [
            {"q": "anomalies(avg:postgresql.buffer_hit{*}, 'basic', 2)"}
        ],
        "viz": "timeseries"
    },
    "title": "Avg of postgresql.buffer_hit w/ anomaly function applied"
},
{ "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{*}.rollup(sum, 3600)"}
        ],
        "viz": "timeseries"
    },
    "title": "Rollup of my_metric for past hour"
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
