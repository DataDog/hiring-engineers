import datadog, os
from pprint import pprint

options = {
    'api_key': os.environ['API_KEY'],
    'app_key': os.environ['APP_KEY']
}

datadog.initialize(**options)

title = "My Metric"
description = "Timeboard for DD Interview"
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {
            	"q": "avg:app.my_metric{host:cachedemon}",
            	"type": "line"
            }
        ],
    "viz": "timeseries"
    },
    "title": "MyMetric"
},
{
	"definition": {
		"events": [],
		"requests": [
			{
				"q": "anomalies(avg:mysql.net.connections{$host}, 'basic', 3)",
      			"type": "lines",
			    "style": {
			      "palette": "orange"
			    }
			}
		],
	"viz": "timeseries"
	},
	"title": "MySQL Connections"
},
{
	"definition": {
		"events": [],
		"requests": [
			{
				"q": "sum:app.my_metric{cachedemon}.rollup(sum, 3600)",
				"type": "bars"
			}
		],
	"viz": "timeseries"
	},
	"title": "MyMetric Rollup (1hr)"
}]

template_variables = [{
    "name": "host",
    "prefix": "host",
    "default": "host:cachedemon"
}]

read_only = True

response = datadog.api.Timeboard.create(title=title, description=description, graphs=graphs, template_variables=template_variables, read_only=read_only)

pprint(response)