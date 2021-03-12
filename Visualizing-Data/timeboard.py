from datadog import initialize, api

options = {
    'api_key': 'e9b27986ed73af798b529e9852e89aa4', 'app_key': '55fcc32aa469aee233224a23b51247442a03faad'
}

initialize(**options)

title = "Kyvaune\'s Timeboard"
description = "An informative timeboard."
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "my_metric{*} by {host}"}
        ],
        "viz": "timeseries"
        },
    "title": "my_metric Scoped over Host"
    },
    {'definition': {'events': [],
                    'requests': [{
                        'q': "anomalies(mysql.performance.kernel_time{*}, 'robust', 2)"}],
                    'viz': 'timeseries'},
     'title': 'Agile Anomaly Function (2 bound)'},
    {'definition': {'events': [],
                    'requests': [{
                        'q': "sum:my_metric{*}.rollup(sum, 3600)"}],
                    'viz': 'timeseries'},
     'title': 'my_metric over Last Hour'}
]

template_variables = [{
    "name": "kyvaunes-dd-vm",
    "prefix": "host",
    "default": "host:my-host"
}]

read_only = True
response = api.Timeboard.update(2785799,
                                 title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)

print(response)