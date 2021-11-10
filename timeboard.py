from datadog import initialize, api
  
options = {
    'api_key': '',
    'app_key': ''
}

initialize(**options)

title = 'Datadog Exercise Timeboard'
widgets = [{
    'definition': {
        'type': 'timeseries',
        'requests': [
             {'q': 'avg:my_metric{*}'}
        ],
        'title': 'Custom Metric Scoped Over Host'
    }},
    {
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'anomalies(avg:mysql.performance.open_files{*}, "basic", 2)'}
        ],
         'title': 'MySql mysql.performance.open_files Anomaly Funtion'
        }},
    {
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'sum:my_metric{*}.rollup(sum, 3600)'}
        ],
        'title': 'My_metric rolled up.'
    }
    }]
layout_type = 'ordered'
description = 'My_Metric scoped over host.'
is_read_only = True
notify_list = ['mccreadie34@gmail.com']
template_variables = [{
    'name': 'host1',
    'prefix': 'host',
    'default': 'my-host'
}]

api.Dashboard.create(title=title,
                     widgets=widgets,
                     layout_type=layout_type,
                     description=description,
                     is_read_only=is_read_only,
                     notify_list=notify_list,
                     template_variables=template_variables)
~                                                                                                    
"timeboard.py" 52L, 1334C
