from datadog import initialize, api

options = {
    'api_key': '822c3c10f88c65b74efed9f3934f9af5',
    'app_key': '1cef33e98cd63236aad2dfe1fa88c63fc86010b9'
}

initialize(**options)

title = 'Dashboard Example'
widgets = [{
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'avg:my_metric{*}'}
        ],
        'title': 'Scoped over host'
    }
    },
    {
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'avg:my_metric{*}.rollup(sum, 3600)'}
        ],
       'title': 'Rollup Function'
    }
    }
    ,
    {
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'anomalies(mongodb.opcounters.updateps{*}, "basic", 2)'}
        ],
        'title': 'Anomaly Function Applied'
    }
    }

    ]

layout_type = 'ordered'
description = 'A dashboard with memory info.'
is_read_only = True
notify_list = ['tony_bh@live.com']
template_variables = [{
    'name': 'host1',
    'prefix': 'host',
    'default': 'my-host'
}]

saved_view = [{
    'name': 'Saved views for hostname 2',
    'template_variables': [{'name': 'host', 'value': '<HOSTNAME_2>'}]}
]

print(api.Dashboard.create(title=title,
                     widgets=widgets,
                     layout_type=layout_type,
                     description=description,
                     is_read_only=is_read_only,
                     notify_list=notify_list,
                     template_variables=template_variables,
                     template_variable_presets=saved_view))