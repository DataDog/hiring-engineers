from datadog import initialize, api

options = {
    'api_key': '0596bca0a5b64d7f8ac44ef1a24607fd',
    'app_key': 'feca7e879fdef26532188c730c0b3f5546384428'
}

initialize(**options)

title = 'Mahoney Dashboard-7'
widgets = [{
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'avg:my_metric{host:i-0b2438f9031697d3c}'}
        ],
        'title': 'My Metric'
    }
    },
    {
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'avg:my_metric{host:i-0b2438f9031697d3c}.rollup(sum, 3600)'}
        ],
       'title': 'My Metric - Rollup 1 Hour'
    }
    }
    ,
    {
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'anomalies(mongodb.opcounters.updateps{*}, "basic", 2)'}
        ],
        'title': 'MongoDB Writes/Sec - Anomalies Function'
    }
    }

    ]

layout_type = 'ordered'
description = 'A dashboard with memory info.'
is_read_only = True
notify_list = ['larrymahoney98@gmail.com']
template_variables = [{
    'name': 'host1',
    'prefix': 'host',
    'default': 'my-host'
}]

saved_view = [{
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
                     template_variable_presets=saved_view)
