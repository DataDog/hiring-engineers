from datadog import initialize, api

options = {
    'api_key': '8b61d94149b2d8718b1487ae2d76e6ba',
    'app_key': '94a5f73e754612fe5c027e4bae0c9cfee8705cbd'
}

initialize(**options)

title = "Hiring Exercise Timeboard"
description = "Hiring Exercise Timeboard"
graphs = [{
	"definition": {
		"events": [],
		"requests": [
			{
				"q": "avg:my_metric{*}"
			},
			{
				"q": "anomalies(avg:postgresql.buffer_hit{*}*100, 'basic', 2)"
			},
			{
				"q": "sum:my_metric{*}.rollup(3600)"
			}
		],
		"viz": "timeseries"
	},
	"title": "Visualizing Data"
}]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:my-host"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)
