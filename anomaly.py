from datadog import initialize, api

options = {
    'api_key': '29df0174a45acb5a3bf99f1b619fc1f9',
    'app_key': '0c8c550b9d5c08306d08bc03af07a0570e68f089'
}

initialize(**options)

title = 'Anomaly Test'
widgets = [{
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'anomalies(avg:mysql.performance.cpu_time{*}, "basic", 2)'}
        ],
        'title': 'SQL Anomalies'
    }

}]
layout_type = 'ordered'
description = 'A dashboard with memory info.'
is_read_only = True
notify_list = ['user@domain.com']
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

