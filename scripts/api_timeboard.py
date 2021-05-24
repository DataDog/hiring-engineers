from datadog import initialize, api

DATADOG_API_KEY = <DATADOG_API_KEY>
DATADOG_APP_KEY = <DATADOG_APP_KEY>

options = {
    'api_key': DATADOG_API_KEY,
    'app_key': DATADOG_APP_KEY
}

initialize(**options)

title = ' Project Timeboard'
description = 'Custom metrics over host for hiring project. This timeseries table was created using the Datadog API.'
graphs = [{
    'definition': {
        'events': [],
        'requests': [
            {'q':'max:my_metric{host:vagrant}','type':'line'}
        ],
        'viz': 'timeseries'
        },
    "title": "Custom Metric over Host"
    },
    {
    "definition": {
        "events": [],
        "requests": [
            {"q":"anomalies(avg:mongodb.stats.avgobjsize{*}, 'basic', 2)"}
            ],
        "viz": "timeseries"
        },
    "title": "MongoDB Object Size Anomilities"
    },
    {
    "definition": {
        "events": [],
        "requests": [
            {"q":"my_metric{*}.rollup(sum, 3600)"}
            ],
        "viz": "timeseries"
        },
    "title": "Custom Metric over Host - Rollup 3600s"
    },
    {
    "definition": {
        "events": [],
        "requests": [
            {"q":"my_metric{*}.rollup(sum, 60)"}
            ],
        "viz": "timeseries"
        },
    "title": "Custom Metric over Host - Rollup 60s"
    }
]

template_variables = [{
    'name': 'vagrant',
    'prefix': 'host',
    'default': 'host:my-host'
}]

read_only = False
results = api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)


print(results)
