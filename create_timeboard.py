#Using the new unified Dashboard endpoint
from datadog import initialize, api

options = {
    'api_key': '',#remove for security reasons
    'app_key': ''#remove for security reasons
}

initialize(**options)

title = 'My First Dashboard'
widgets = [{#my_metric
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'avg:my_metric{*}'}
        ],
        'title': 'Average Custom Metrics'
    }
},
{#my_metric with the rollup function applied to sum up all the points for the past hour
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'avg:my_metric{*}.rollup(sum,3600)'}
        ],
        'title': 'Custom Metric Rollupp Last Hour'
    }
},
{#DB metric with anomaly function applied
    'definition': {
        'type': 'timeseries',
        'requests': [
            {"q": "anomalies(avg:mysql.performance.user_time{*}, 'basic', 3)"}
        ],
        'title': 'Anomalies MySQL CPU Time'
    }
}
]
layout_type = 'ordered' # for Timeboard
description = 'A dashboard with my_metric, my_metric rollup and DB CPU info.'
is_read_only = True
notify_list = ['user@domain.com']
template_variables = [{
    'name': 'asalineroj',
    'prefix': 'host',
    'default': 'my-host'
}]
response = api.Dashboard.create(title=title,
                     widgets=widgets,
                     layout_type=layout_type,
                     description=description,
                     is_read_only=is_read_only,
                     notify_list=notify_list,
                     template_variables=template_variables)

print(response)
print('SUCCESS')
