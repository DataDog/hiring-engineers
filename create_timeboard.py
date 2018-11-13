from datadog import initialize, api

options = {'api_key': '33aa0a665a544113052cf2efba7ac54f',
           'app_key': 'd31a5814782cd258bda63d18b1db2839ab91fac7'}


initialize(**options)

title = "My Timeboard"
description = "For the assignment."
graphs = [{
    "definition": {
        "events": [],
        "requests": [
        {
		"q": "avg:assignment.my_metric{host:i-0dbff323b9d5bd74e}",
      		"type": "line",
      		"style": {
    		    	"palette": "dog_classic",
        		"type": "solid",
        		"width": "normal"
           	},
           	"conditional_formats": [],
           	"aggregator": "avg"
    	}
        ],
        "viz": "timeseries"
    },
    "title": "assignment.my_metric"
},

{
    "definition": {
        "events": [],
        "requests": [
        {
      		"q": "avg:postgresql.bgwriter.checkpoints_timed{host:i-0dbff323b9d5bd74e}.as_count(), anomalies(avg:postgresql.bgwriter.checkpoints_timed{host:i-0dbff323b9d5bd74e}.as_count(),'basic',1)",
      		"type": "bars",
      		"style": {
        		"palette": "dog_classic",
        		"type": "solid",
        		"width": "normal"
      	   	},
      		"conditional_formats": [],
      		"aggregator": "avg"
    	}
        ],
        "viz": "timeseries"
    },
    "title": "bgwriter.checkpoints_timed"
},

{
    "definition": {
        "events": [],
        "requests": [
        {
		"q": "avg:assignment.my_metric{host:i-0dbff323b9d5bd74e}.rollup(sum, 3600)",
      		"type": "line",
      		"style": {
    		    	"palette": "dog_classic",
        		"type": "solid",
        		"width": "normal"
           	},
           	"conditional_formats": [],
           	"aggregator": "avg"
    	}
        ],
        "viz": "timeseries"
    },
    "title": "assignment.my_metric with rollup of 1 hour"
},
]

template_variables = []

read_only = False
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)
