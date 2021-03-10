from datadog import initialize, api
from decouple import config
import os

"""
decouple allows for dynamic environment variable passing, locally, in a cloud environment, etc.
The simplest way to inject the environment variables below is to create a .env file with the env variables defined in <KEY>=<VALUE> form
"""
options = {
    'api_key': config('DATADOG_API_KEY'),
    'app_key': config('DATADOG_APPLICATION_KEY')
}

initialize(**options)

title = 'Timeboard Sales Engineer Hiring Exercise'
widgets = [{
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'my_metric{*}'}
        ],
        'title': 'Custom Metric Full Scope, Unaggregated'
    }},
    {
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'anomalies(mysql.innodb.data_reads{*},"basic",2)'}
        ],
        'title': 'MySQL reads'
    }},
    {
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'my_metric{*}.rollup(sum,3600)'}
        ],
        'title': 'Custom Metric Full Scope, Summed up by hour'
    }}]
layout_type = 'ordered'
description = 'A Dashboard for the Sales Engineer Hiring Exercise'
is_read_only = True
notify_list = ['caterinayantonio@gmail.com']
template_variables = [{
    'name': 'host1',
    'prefix': 'host',
    'default': 'my-host'
}]

saved_views = [{
    'name': 'Saved views for hostname 2',
    'template_variables': [{'name': 'host', 'value': '<HOSTNAME_2>'}]}
]

print(api.Dashboard.create(title=title,
                     widgets=widgets,
                     layout_type=layout_type,
                     description=description,
                     is_read_only=is_read_only,
                     notify_list=notify_list,
                     template_variables=template_variables,
                     template_variable_presets=saved_views))
