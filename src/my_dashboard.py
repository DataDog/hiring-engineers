from datadog import initialize, api

options = {
    'api_key': '7725c7d6cef083415b42e74df22fd9f1',
    'app_key': '1ac4081cb26ecc7ba50fe2fac77add43af52268d'
}

initialize(**options)

title = 'Solution Enigneering Test Dashboard'
widgets = [{
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'anomalies(avg:mysql.performance.user_time{host:vagrant}, \'basic\',2)'}
        ],
        'title': 'Anomalies graph Average MySQL CPU time (per sec)'
    }
},
{
    'definition': {
        'type': 'query_value',
        'requests': [
            {'q': 'my.metric{test:my_new_key}.rollup(sum,3600)'}
        ],
        'title': 'Custom \'my_metric\' graph with rollup sum'
    }
},
{
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'avg:my.metric{test:my_new_key}'}
        ],
        'title': 'Custom \'my_metric\' graph of my_new_key' 
    }
}]
layout_type = 'ordered'
description = 'This dashboard displaysa visualisation of a custom metric, an anomaly of mysql cpu usage and a rollup function applied on a custom metric'
is_read_only = False
notify_list = ['marek.steplewski@gmail.com']


api.Dashboard.create(title=title,
                     widgets=widgets,
                     layout_type=layout_type,
                     description=description,
                     is_read_only=is_read_only,
                     notify_list=notify_list)
