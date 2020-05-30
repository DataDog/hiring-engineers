from datadog import initialize, api

options = {
    'api_key': 'e22ab28c0cbdef7ac4be4f9bc58927c9',
    'app_key': 'a4d1692da652f4e1d3fcc3ef8ed4785b68bfa2a5'
}

initialize(**options)

title = 'Avg Custom Metric'
widgets = [{
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'avg:my_metric{host:shirleyswork}'}
        ],
        'title': 'Average of my custom metric'
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

saved_views = [{
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
