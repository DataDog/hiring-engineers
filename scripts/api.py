#Authentication

from datadog import initialize, api

options = {'api_key': '5b51a3a01c54d8424999428fb4298de4',
	   'app_key': '7321593bdd549b445f73dac828524ee6757b4225'
}

initialize(**options)

# Creating the Timeboard & Graphs

title = "API Timeboard"
description = "Timeboard for visualize metrics"
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:test.support.random{*} by {host}"}
	    
        ],
        "viz": "timeseries"
    },
    "title": "Random avg by host"
},
{
    "definition": {
        "events": [],
        "requests": [
	    {"q": "anomalies(avg:postgresql.percent_usage_connections{*}, 'basic', 3)"}
	    
        ],
        "viz": "timeseries"
    },
    "title": "Postgres w/ anomaly detection"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:test.support.random{*}.rollup(sum,3600)"}
	    
        ],
        "viz": "timeseries"
    },
    "title": "Random Rollup 1hr sum"
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
