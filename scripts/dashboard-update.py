from datadog import initialize, api

options = {
    'api_key': 'KEY',
    'app_key': 'KEY'
}

initialize(**options)

dashboard_id = '3zw-8gj-5pd'

title = 'My Metrics Updated'
widgets = [{
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'avg:mysql.performance.cpu_time{host:i-0fcaadedac4ac5b29}'}
        ],
        'title': 'MySQL CPU Time'
                }
    }, 
    {
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'avg:my_metric{host:i-08021c29f543d000a}'}
        ],
        'title': 'Last 1 hr Metrics'
                    }
    },
    {
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': "anomalies(avg:my_metric{host:i-08021c29f543d000a}, 'basic', 2)"}
        ],
        'title': 'Anomaly Detection'
                    }
    },
    {
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': "sum:my_metric{host:i-08021c29f543d000a}.rollup(3600)"}
        ],
        'title': 'Metric Sum Roll Up'
                    }
    }
]

layout_type = 'ordered'
description = 'MySQL DB Information Updated'
is_read_only = True
notify_list = ['creativevikram@gmail.com']
api.Dashboard.update(dashboard_id,
                     title=title,
                     widgets=widgets,
                     layout_type=layout_type,
                     description=description,
                     is_read_only=is_read_only,
                     notify_list=notify_list
                                         )