from datadog import initialize, api

options = {
	'api_key': 'c1a1bf2d95c1258d546019cfc7d1edae',
	'app_key': '2cde06fd67efc07965f3b57b32679c5a557f96ac'
}

initialize(**options)

title = "My Timeboard"
description = "An informative timeboard"
graphs = [{
	"definition": {
		"events": [],
		"requests": [
			{"q": "my_metric{*}"}
		],
	"viz": "timeseries"
	},
	"title": "my_metric Random Number Generator"
},
{
	"definition": {
		"events": [],
		"requests": [
			{"q": "anomalies(avg:mysql.performance.kernel_time{*}, 'basic', 3)"}
		],
	"viz": "timeseries"
	},
	"title": "% of CPU Time in kernal space by MySQL with Anomoly Function" 
},
{
	"definition": {
		"events": [],
		"requests": [
			{"q": "my_metric{*}.rollup(sum, 3600)"}
		],
	"viz": "timeseries"
	},
	"title": "my_metric Sum Using Rollup"
}]

template_variables = [{
	"name": "host1",
	"prefix": "host",
	"default": "host:my-host"
}]

read_only = True

api.Timeboard.create(title=title, description=description, graphs=graphs, template_variables=template_variables, read_only=read_only)
