import typer
import httpx
from datadog import initialize, api
from settings import options

""" Create a timeboard with custom metrics.

    * Your custom metric scoped over your host.
    * Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
    * Any metric from the Integration on your Database with the anomaly function applied.

    References
    ==========

    `https://docs.lightstep.com/docs/create-a-datadog-dashboard-to-monitor-satellite-health`_

"""
from datadog import initialize, api

initialize(**options)   # Use the imported settings to establish the connection.

title = 'My custom Metric'
widgets = [{
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'avg:system.mem.free{*}'}
        ],
        'title': 'Average Memory Free'
    }
}]



layout_type = 'ordered'
description = 'A Timeboard with a custom metric.'
is_read_only = True
notify_list = ['jitkelme@gmail.com']
template_variables = [{
    'name': 'host1',
    'prefix': 'host',
    'default': 'my-host'
}]

saved_view = [{
    'name': 'Saved views for hostname 2',
    'template_variables': [{'name': 'host', 'value': '<HOSTNAME_2>'}]}
]

api.Dashboard.create(title=title,
                     widgets=widgets,
                     layout_type=layout_type,
                     description=description,
                     is_read_only=is_read_only,
                     notify_list=notify_list,
                     template_variables=template_variables,
                     template_variable_presets=saved_views)

