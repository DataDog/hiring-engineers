from datadog import initialize, api

options = {
    'api_key': '68d7855cb7fc2cd9a83ea241a8bca120',
    'app_key': '2e046c6cba9a390beafe6c99f4f9f1c885c6cdb2'
}

initialize(**options)

title = 'My Custom Dashboard'
widgets = [
	{
		'definition': {
			'type': 'timeseries',
			'requests': [
				{'q': 'avg:ajp.my_metric{$host1}'}
			],
			'title': 'My Metric'
		}
	},
	{
		'definition': {
			'type': 'timeseries',
			'requests': [
				{'q':'anomalies(avg:mysql.innodb.rows_read{$host1}, "basic", "2")'}
			],
			'title': 'MySQL Metric CPU time with Anomalies enabled'
		}
	},
	{
		'definition': {
			'type': 'timeseries',
			'requests':[
				{'q':'avg:ajp.my_metric{$host1}.rollup(avg, 3600)', 'display_type':'bars'}
			],
			'title':'Average of My Metric with 1 hour rollup'}
	}
]
layout_type = 'ordered'
description = 'A custom dashboard with some selected metrics.'
is_read_only = True
notify_list = ['user@domain.com']
template_variables = [{
    'name': 'host1',
    'prefix': 'host',
    'default': 'ajp-ubuntu'
}]
resp = api.Dashboard.create(title=title,
                     widgets=widgets,
                     layout_type=layout_type,
                     description=description,
                     is_read_only=is_read_only,
                     notify_list=notify_list,
                     template_variables=template_variables)
print resp
