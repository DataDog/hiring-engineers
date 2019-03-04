#!/usr/bin/python3
import json
from datadog import initialize, api

options = {
    'api_key':'REDACTED',
    'app_key':'REDACTED'
}

initialize(**options)

graphs = [
    {
        'title': 'MyMetricRollup',
        'definition': {
            'type': 'timeseries',
            'requests': [
                {
                    'q': 'sum:my_metric{*}.rollup(sum,3600)'
                }
            ]
        }
    },
    {
        'title': 'MyMetric on Test',
        'definition': {
            'type': 'timeseries',
            'requests': [
                {
                    'q': 'avg:my_metric{host:test}'
                }
            ]
        }
    },
    {
        'title': 'MySQL CPU Time',
        'definition': {
            'type': 'timeseries',
            'requests': [
                {
                    'q': 'anomalies(avg:mysql.performance.cpu_time{*}, "basic", 2)'
                }
            ]
        }
    }
]
###Documentation was wrong. Need to run api.Timeboard vs api.Dashboard
### https://docs.datadoghq.com/api/?lang=python#dashboards << Fix please
print(json.dumps(api.Timeboard.create(
    title = 'McKeown SE Interview Timeboard',
    graphs = graphs,
    layout_type = 'ordered',
    description = 'Timeboard for SE position',
), indent = 4))