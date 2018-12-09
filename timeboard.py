from datadog import initialize, api

#My API generated Timeboard
#Note:There is one aditional value added showing the same data as the 1h timelapse graph on my_metric

options = {
    'api_key': '21029214ec3586e84737353678dc1493',
    'app_key': 'f5ee20312de5ce3e5becb0cec6f4972dca98ce51'
}

initialize(**options)

title = "Custom Timeboard - API Generated"
description = "An informative timeboard."


graphs = [
{
    "definition": {
        "events": [],
        "requests": [
            {
				"q": "top(avg:my_metric{host:testmachine.smit.net}, 10, 'mean', 'desc')",
				"type": "line",
				"style": 
				{
					"palette": "dog_classic",
					"type": "solid",
					"width": "normal"
				},
				"conditional_formats": [],
				"aggregator": "avg"
			}
        ],
        "viz": "timeseries",
    },
    "title": "Timelapse of my_metric"
},

{
    "definition": {
        "events": [],
        "requests": [
            {
				"q": "anomalies(avg:mysql.innodb.data_writes{host:testmachine.smit.net}, 'basic', 2)",
				"type": "line",
				"style": 
				{
					"palette": "dog_classic",
					"type": "solid",
					"width": "normal"
				},
				"conditional_formats": [],
				"aggregator": "avg"
			}
        ],
        "viz": "timeseries",
    },
    "title": "DB writes w/ anomaly detection"
},	
{
    "definition": {
        "events": [],
        "requests": [
            {
				"q": "avg:my_metric{host:testmachine.smit.net}.rollup(sum, 3600)",
				"type": "line",
				"style": 
				{
					"palette": "dog_classic",
					"type": "solid",
					"width": "normal"
				},
				"conditional_formats": [],
				"aggregator": "avg"
			}
        ],
    },
    "title": "Timelapse of my_metric w/ 1h rollup"
},
{
    "definition": {
		"viz": "query_value",
        "events": [],
        "requests": [
            {
				"q": "avg:my_metric{host:testmachine.smit.net}.rollup(sum, 3600)",
				"style": 
				{
					"palette": "dog_classic",
					"type": "solid",
					"width": "normal"
				},
				"conditional_formats": 
				[
						{
							"comparator": ">",
							"palette": "white_on_red",
						},
						{
							"comparator": ">=",
							"palette": "white_on_yellow",
						},
						{
							"comparator": "<",
							"palette": "white_on_green",
						}
				],
				"aggregator": "avg"
			}
        ],
		"custom_unit": "gens",
    },
    "title": "Timelapse of my_metric w/ 1h rollup"
}
]

template_variables = [{
    "name": "testmachine.smit.net",
    "prefix": "host",
    "default": "host:my-host"
}]

read_only = True

api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)