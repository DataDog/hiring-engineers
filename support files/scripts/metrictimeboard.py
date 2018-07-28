from datadog import initialize, api

options = {'api_key': 'c7a6aba39c8f0700da75095c154271b9', 'app_key': '5a8beb8d346927039585a6faaba8cb653d346523'}

initialize(**options)

# Timeboard
title = "My Timeboard"
description = "my metric data board"
graphs = [{
    "title": "Metric data",
    "definition": {
		"events": [],
		"requests": [
		    {"q": "anomalies(avg:my_metric{host:vagrant}, 'basic', 2)"},
		    {"q": "avg:my_metric{host:vagrant}.rollup(sum, 3600)"}
		],
    }
}]
read_only = False

api.Timeboard.create(title=title, description=description,graphs=graphs, read_only=read_only)
