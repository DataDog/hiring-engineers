from datadog import initialize, api

options = {
    'api_key': 'xxxxxxxxxxxxxxxxxx',
    'app_key': 'xxxxxxxxxxxxxxxxxx'
}

initialize(**options)

title = 'My timeboard'
widgets = [{
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'avg:my_metric{*}'}
        ],
        'title': 'my_metric values'
    }
},
    {
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': "anomalies(avg:postgresql.max_connections{*}, 'basic', 3, direction='above', alert_window='last_5m', interval=20, count_default_zero='true')"}
        ],
        'title': 'PostgreSQL maximum number of client connections allowed'
    }
},
    {
    'definition': {
        'type': 'query_value',
        'requests': [
            {'q': "avg:my_metric{*}.rollup(sum, 3600)"}
        ],
        'title': 'my_metric sum of all points in the past hour'
    }
}]

layout_type = 'ordered'
description = 'My timeboard for the Technical Account Manager exercise'
is_read_only = True
notify_list = ['user@domain.com']
template_variables = [{
    'name': 'host1',
    'prefix': 'host',
    'default': 'docker-desktop'
}]

api.Dashboard.create(title=title,
                     widgets=widgets,
                     layout_type=layout_type,
                     description=description,
                     is_read_only=is_read_only,
                     notify_list=notify_list,
                     template_variables=template_variables)