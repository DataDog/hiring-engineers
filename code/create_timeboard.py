#!/usr/bin/env python3

from datadog import initialize, api
import os

# Loading DD keys, environment variables must be set
options = {'api_key': os.environ['DD_API_KEY'],
           'app_key': os.environ['DD_APP_KEY']}

initialize(**options)

title = 'API Created Timeboard'

widgets = [
{
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'avg:my_metric{host:ubuntu-xenial}'}
        ],
        'title': 'Custom Metric: my_metric'
    }
},
{
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': "anomalies(avg:mysql.performance.kernel_time{*}, 'basic', 2)"}
        ],
        'title': 'MySQL Kernel Time Anomalies'
    }
},
{
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': "avg:my_metric{host:ubuntu-xenial}.rollup(sum, 3600)"}
        ],
        'title': 'Custom Metric Rolled up every hour'
    }
}
]

layout_type = 'ordered'
description = 'A dashboard created via API.'

response = api.Dashboard.create(title=title,
                                widgets=widgets,
                                layout_type=layout_type,
                                description=description)

print(response)