from datadog import initialize, api

options = {
    'api_key': '0faa49ba34b19d7ec50f5e4f6c7808fa',
    'app_key': 'f4e044e3711fb83c26431bd08b1ba66e6498d9f3'
}

initialize(**options)

title = 'Varun\'s Dashboard'
widgets = [{
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'hello.world{host:vagrant}'}
        ],
        'title': 'Hello.World'
    }
},
{
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'anomalies(mysql.performance.user_time{host:vagrant}, \'basic\', 2)'}
        ],
        'title': 'MySQL Anomalous CPU Activity'
    }
},
{
    'definition': {
        'type': 'timeseries',
        'requests': [
            {
                'q': 'sum:hello.world{host:vagrant}.rollup(sum,3600)'
                }
        ],
        'title': 'Hello.World (Hourly Rollup)'
    }}]
layout_type = 'ordered'
description = 'Datadog Hiring Exercise'
is_read_only = True
notify_list = ['varunr96@gmail.com']
template_variables = [{
    'name': 'host',
    'prefix': 'host',
    'default': 'vagrant'
}]

saved_views = [{
    'name': 'Saved views',
    'template_variables': [{'name': 'host', 'value': 'vagrant'}]}
]

api.Dashboard.create(title=title,
                     widgets=widgets,
                     layout_type=layout_type,
                     description=description,
                     is_read_only=is_read_only,
                     notify_list=notify_list,
                     template_variables=template_variables,
                     template_variable_presets=saved_views)