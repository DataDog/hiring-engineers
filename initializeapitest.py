from datadog import initialize, api

options = {
    'api_key': '',
    'app_key': ''
}

initialize(**options)

title = 'zAPI Test'
widgets = [{
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'my_metric{*}'}
        ],
        'title': 'My Metric'
    }
},
{
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'postgresql.db.count{*}'}
        ],
        'title': 'Postgres DB Count'
    }
},
{
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'my_metric{*}.rollup(sum, 3600)'}
        ],
        'title': 'My Metric Rollup'
    }
}]
layout_type = 'ordered'
description = 'A dashboard my metric.'
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
                     template_variables=template_variables,
)
