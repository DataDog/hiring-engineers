from datadog import initialize, api

options = {
    'api_key': '<DATADOG_API_KEY>',
    'app_key': '<DATADOG_APP_KEY>'
}

initialize(**options)

title = 'Ryan Hanson Custom Timeboard'
widgets = [{
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'my_metric.metric{*} by {host}'} #Item 1: Your custom metric scoped over your host.
        ],
        'title': 'My Custom Metric'
    }
},
{
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': "anomalies(avg:mongodb.mem.resident{host:vagrant}, 'basic', 2)"} #Item 2: Any metric from Database with the anomaly function applied.
        ],
        'title': 'MongoDB Memory Used with Anomaly Fn'
    }
},
{
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': "my_metric.metric{*}.rollup(sum, 3600)"} # Item 3: Custom Metric w/ Rollup Fuction to Sum all points over 1 hr
        ],
        'title': 'Average of my Metric over 1 Hour'
    }
}]

layout_type = 'ordered'
description = 'A custom timeboard using the API.'
is_read_only = True
notify_list = ['ryanmkhanson@gmail.com']
template_variables = [{
    'name': 'host1',
    'prefix': 'host',
    'default': 'my-host'
}]

saved_views = [{
    'name': 'Saved views for hostname 2',
    'template_variables': [{'name': 'host', 'value': 'test'}]}
]

api.Dashboard.create(title=title,
                     widgets=widgets,
                     layout_type=layout_type,
                     description=description,
                     is_read_only=is_read_only,
                     notify_list=notify_list,
                     template_variables=template_variables,
                     template_variable_presets=saved_views)
