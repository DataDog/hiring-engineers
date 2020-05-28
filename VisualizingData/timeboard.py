from datadog import initialize, api

options = {
    'api_key': '91300d2d9cd0ccf8b22dbd46124c3102',
    'app_key': '4d6730f87624f71e8dac1817951f3a1d35e0e8d0'
}

initialize(**options)

# Create a new monitor
monitor_options = {
    "notify_no_data": True,
    "no_data_timeframe": 20
}
tags = ["app:minikube", "vagrant"]
api.Monitor.create(
    type="query alert",
    query="avg(last_4h):anomalies(avg:postgresql.max_connections{host:vagrant,env:ddogeval}, 'basic', 2, direction='both', alert_window='last_15m', interval=60, count_default_zero='true') >= 1",
    name="Postgresql sync time",
    message="IDK this is a demo.",
    tags=tags,
    options=monitor_options
)

title = 'JRath My_Metric_Final'
widgets = [{
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'avg:my_metric{host:vagrant}'}
        ],
        'title': 'Value (Gauge)'
    }
},
    {
    'definition': {
        'type': 'alert_graph',
        'alert_id': '18827755',
        'viz_type': 'timeseries',
        #'requests': [
        #    {'q': 'avg:postgresql.max_connections{*}'}
       #],
        'title': 'Postgresql max connections with alert graph'
    }
},
    {
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'avg:my_metric{host:vagrant}.rollup(sum, 3600)'}
        ],
        'title': 'Rollup - Summed over 1 hour'
    }
}]

layout_type = 'ordered'
description = 'A dashboard with custom metric info.'
is_read_only = True
notify_list = ['john.rath202@gmail.com']
template_variables = [{
    'name': 'vagrant',
    'prefix': 'host',
    'default': 'vagrant'
}]

saved_view = [{
    'name': 'Saved views for my_metric',
    'template_variables': [{'name': 'host', 'value': 'vagrant'}]}
]

api.Dashboard.create(title=title,
                     widgets=widgets,
                     layout_type=layout_type,
                     description=description,
                     is_read_only=is_read_only,
                     notify_list=notify_list,
                     template_variables=template_variables,
                     template_variable_presets=saved_view)
