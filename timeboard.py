from datadog import initialize, api

options = {
    'api_key': 'b94670e66009a0332312afdeec0ca939',
    'app_key': 'cbdd2353176dfca0df90a7558e10067c255ccc4a'
}

initialize(**options)

title = "Nawfel Timeboard"
description = "New timeboard to visualise our new metrics"
graphs = [{
	"definition": {
		"viz": "timeseries",
		"requests": [
       		  {
               		"q": "avg:my_metric{host:nawmest-Aspire-E5-575G}",
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
    	"title": "my_metric random values"
},
{
   	"definition": {
  		"viz": "timeseries",
  		"requests": [
    		  {
      			"q": "avg:my_metric{host:nawmest-Aspire-E5-575G}.rollup(sum, 3600)",
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
	"title": "Sum of my_metric over 1h"
},
{
        "definition": {
                "viz": "timeseries",
                "requests": [
                  {
			"q": "anomalies(avg:mongodb.connections.totalcreated{host:nawmest-Aspire-E5-575G}, 'adaptive', 2)",
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
        "title": "MongoDb Total number of connections created"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     read_only=read_only)
