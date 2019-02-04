from datadog import initialize, api

options = {
    'api_key': '2ade393bb089f741e8781a2b4ab182c5',
    'app_key': 'ed8a54a6a53e9075e40cf4b9ae6d6187affd3dac'
}

initialize(**options)

title = "Test Timeboard"
description = "A test of creating a timeboard with the API."
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
    "title": "My Metric Visuals"
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
