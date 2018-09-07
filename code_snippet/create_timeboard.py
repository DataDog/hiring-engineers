from datadog import initialize, api

## Step1: create metric on system memory free
options = {
    'api_key': 'd00651cc0fc7da1417f4837b60570b71',
    'app_key': '989903e5da8834c819ef62cbc2f9fb38428e888d'
}

initialize(**options)

title = "Challenge_Timeboard"
description = "Timeboard created for datadog challenge"
graphs = [
    # graph1: my_metric
    {"definition": {
        "events": [],
        "requests": [
            {"q": "my_metric{*}"},
            {"q": "my_metric{*}.rollup(sum, 3600)"}
        ],
        "viz": "timeseries"
    },
    "title": "my_metric"
    },
    # graph2: database with anomaly function
    {"definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:postgresql.buffer_hit{*}, 'basic', 3)"}
        ],
        "viz": "timeseries"
    },
    "title": "PostgreSQL rows returned"}
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
