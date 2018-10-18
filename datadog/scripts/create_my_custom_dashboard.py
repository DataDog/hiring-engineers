from datadog import initialize, api

options = {
    'api_key': '50124dda46d1303b859f2d75d83beea2',
    'app_key': 'a3c67a67eaebcbc3755f82d5d07217b59ae2a321'
}

initialize(**options)

title = "My Datadog Timeboard by Yuya"
description = "Timeboard for my custom metric and postgres metrics."
graphs = [
{ "definition": {
        "events": [],
        "requests": [
            {"q": "top(max:my_metric{host:i-0ee8948d804858200} by {host}, 10, 'last', 'desc'), top(max:my_metric{host:i-0ee8948d804858200} by {host}, 10, 'max', 'desc'), top(max:my_metric{host:i-0ee8948d804858200} by {host}, 10, 'min', 'desc'), top(max:my_metric{host:i-0ee8948d804858200} by {host}, 10, 'mean', 'desc')"}
        ],
        "viz": "timeseries"
    },
    "title": "Data for my_metric over host."
},
{ "definition": { 
        "events": [],
        "requests": [
            {"q": "anomalies(avg:postgresql.buffer_hit{role:db}, 'basic', 2)"}
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
