from datadog import initialize, api

options = {
    'api_key': 'a66162b4c9e2bc72367ea862b583f23d',
    'app_key': 'b979000ff469ac5cf14dbc118b6c4f27a37c3c69'
}

initialize(**options)

title = "My Timeboard"
description = "An informative timeboard123."
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{*} by {host}"}
        ],
        "viz": "timeseries"
    },
    "title": "Random Metric"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:mysql.performance.user_time{*}, 'basic', 3)"}
        ],
        "viz": "timeseries"
    },
    "title": "mySQL view"

},
{
    "definition": {
        "events": [],
        "viz": "query_value",
        "requests": [
            {"q": "sum:my_metric{host:i-03cd49e6b870a06d7}","aggregator": "sum"}
        ]
     },
     "title":"sum of custom graph"
}
]

template_variables = [{
    "name": "host123",
    "prefix": "host123",
    "default": "host:i-03cd49e6b870a06d7"
}]

read_only = True
response = api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)

print(response)