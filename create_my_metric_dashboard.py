from datadog import initialize, api
  
options = {
    'api_key': '0f30f2708421e161772b4369c28d7405',
    'app_key': '2dd747741348d513eda715b981219c2407a9d907'
}

initialize(**options)

title = 'Visualizing Data Exercise - Custom Metrics Timeboard'
widgets = [
  {
    'definition':
    {
        'type': 'timeseries',
        'requests': [
            {'q': 'avg:my_metric.gauge{host:i-098f778d8c7272ab2}'}
        ],
        'title': 'Value of my_metric over time scoped over my host'
    }
  },
  {
    'definition':
    {
        'type': 'timeseries',
        'requests': [
            {'q': "anomalies(avg:postgresql.percent_usage_connections{*}, 'basic', 2)"}
        ],
        'title': 'Metric from Integration on DB with anomaly function'
    }
  },
  {
    'definition':
    {
        'type': 'query_value',
        'requests': [
            {'q': 'avg:my_metric.gauge{host:i-098f778d8c7272ab2}.rollup(sum, 3600)'}
        ],
        'title': 'My custom metric with rollup function applied to sum up all the points'
    }
  }
]

layout_type = 'ordered'
description = 'A dashboard displaying value of my_metric'
is_read_only = True
notify_list = ['nwkhashan@yandex.com']
template_variables = [{
    'name': 'host1',
    'prefix': 'host',
    'default': 'my-host'
}]

saved_view = [{
    'name': 'Saved views for hostname 2',
    'template_variables': [{'name': 'host', 'value': 'i-098f778d8c7272ab2'}]}
]

api.Dashboard.create(title=title,
                     widgets=widgets,
                     layout_type=layout_type,
                     description=description,
                     is_read_only=is_read_only,
                     notify_list=notify_list,
                     template_variables=template_variables,
                     template_variable_presets=saved_view)
