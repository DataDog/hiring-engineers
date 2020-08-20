from datadog import initialize, api

options = {
    'api_key': '0f446a99f43c6c64fa11e1e1da15b1e9',
    'app_key': 'ee95f05c7d5839108a1b90aa50036c7327a37661'
}

initialize(**options)

title = 'Basic Timeseries'
widgets = [{
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'my_metrics.my_metrics{host:vagrant}'}
        ],
        'title': 'My Custom Metric'
    }                                                                                                                                                                       },
{
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'anomalies(mysql.performance.cpu_time{host:vagrant}, "basic", 2)'}
        ],
        'title': 'Database Anomalies'                                                                                                                                           }                                                                                                                                                                       },                                                                                                                                                                          {
{
    'definition': {
        'type': 'timeseries',
        'requests': [
            {
                'q': 'sum:my_metrics.my_metrics{host:vagrant}.rollup(sum,3600)'
                }
        ],                                                                                                                                                                          'title': 'My Custom Metric Hourly Rollup'
    }}]

layout_type = 'ordered'
description = 'A dashboard for SE hiring exercise'
is_read_only = True
notify_list = ['dbsamuel12@gmail.com']
template_variables = [{
    'name': 'host1',
    'prefix': 'host',
    'default': 'vagrant-host'
}]
saved_view = [{
    'name': 'Saved views for vagrant',
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
