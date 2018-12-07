from datadog import initialize, api

options = {
    'api_key': '8e038ca7151e23d24a7f1467ad224994',
    'app_key': '77555e4b421eb1677f81bc806e1f4689b3279534'
}

initialize(**options)

title = "Francisco Timeboard API v1"
description = "New timeboard to visualise our new metrics"
graphs = [{
	"definition": {
		"viz": "timeseries",
		"requests": [
       		  {
               		"q": "avg:my_metric{host:i-049121811f75016da}",
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
   	},
    	"title": "My_metric Time Series"
},
{
   	"definition": {
  		"viz": "timeseries",
  		"requests": [
    		  {
      			"q": "avg:my_metric{host:i-049121811f75016da}.rollup(sum, 75)",
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
	},
	"title": "Rollup of my_metric over 1h"
},
{
        "definition": {
                "viz": "timeseries",
                "requests": [
                  {
					"q": "anomalies(avg:mysql.performance.cpu_time{host:i-049121811f75016da}, 'adaptive', 2)",
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
        },
        "title": "MySQL Performance CPU Anomalies"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
read_only=read_only)