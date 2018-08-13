#!/usr/bin/python

from datadog import initialize, api

options = {
    'api_key': 'REDACTED',
    'app_key': 'REDACTED'
}

initialize(**options)

title = "Anoop Atre's Timeboard"
description = "Customized timeboard."
graphs = [
	{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{host:dt2018}"}
        ],
        "viz": "timeseries"
    },
    "title": "my_metric"
	},
	{
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:mysql.net.connections{host:dt2018}, 'basic', 2)"}
        ],
        "viz": "timeseries"
    },
    "title": "anomoly_mysql_connections"
	},
	{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{host:dt2018}.rollup(sum,3600)"}
        ],
        "viz": "timeseries"
    },
    "title": "rollup_my_metric"
	}
]

template_variables = [{
    "name": "dt2018",
    "prefix": "host",
    "default": "host:my-host"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)
