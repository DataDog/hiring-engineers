from datadog import initialize, api

options = {
    'api_key': 'xxxxxxx',
    'app_key': 'xxxxxxx'
}

initialize(**options)

title = 'My Custom Timeboard'
widgets = [
{
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'avg:my_metric{host:ec2.datadog}'}
        ],
        'title': 'my_metric scoped over host'
}},
     {
      'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': "anomalies(avg:mysql.performance.user_time{*}, 'robust', 2)"}
        ],
        'title': 'MySQL metric with Anamoly function'
}},
{
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'avg:my_metric{host:ec2.datadog}.rollup(sum, 3600)'}
        ],
        'title': 'my_metric with rollup for last hour'
}}
]

layout_type = 'ordered'
description = 'A dashboard with various metrics'
#is_read_only = True
#notify_list = ['user@domain.com']
#template_variables = [{
#    'name': 'host1',
#    'prefix': 'host',
#    'default': 'my-host'
#}]

api.Dashboard.create(title=title,
                     widgets=widgets,
                     layout_type=layout_type,
                     description=description,
#                     is_read_only=is_read_only,
#                     notify_list=notify_list,
#                     template_variables=template_variables
)
