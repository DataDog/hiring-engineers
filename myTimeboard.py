from datadog import initialize, api

options = {
    'api_key': '9fcece82deb81b6846ad9d9b85893fda',
    'app_key': 'f06fdf0ac3ab382b8e33ecc2d4462b6588a00bca'
}

initialize(**options)

#print api.Timeboard.get_all()

title = "My hiring test custom timeboard"
description = "Custom timeboard."
graphs = [
	{ 
		"definition": {
   		"events": [],
			"requests": [
				{
					"q": "avg:my_metric{*}",
					"type": "line"
				}
			],
			"viz": "timeseries",
			"autoscale": True
		},
		"title": "My custom metric over my host"
	},
	{
		"definition": {
   		"events": [],
			"requests": [
				{
					"q": "anomalies(avg:mysql.performance.cpu_time{*}, 'basic', 2)",
					"type": "line"
				}
			],
			"viz": "timeseries",
			"autoscale": True
		},
		"title": "My SQL server CPU time"
	},
	{
		"definition": {
   		"events": [],
			"requests": [
				{
					"q": "avg:my_metric{*}.rollup(sum, 3600)",
					"type": "line"
				}
			],
			"viz": "timeseries",
			"autoscale": True
		},
		"title": "My custom metric rolled up into 1 hour"
	}
]


template_variables = [{
    "name": "host",
    "prefix": "host",
    "default": "host:ubuntu-xenial"
}]

api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables)
