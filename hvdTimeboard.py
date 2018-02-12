from datadog import initialize, api

options = {
    'api_key': 'd81b4c03c052be98c0b368cf8606ba68',
    'app_key': '67f28e01e42e14f2273b8cfaca23ea88921574d5'
}

initialize(**options)

title = "Henry's Specialty Timeboard"
description = "Timeboard for Henry Doan's recruiting candidate exercise"
graphs = [{
	"definition": {
		"viz": "timeseries",
		"requests": [
       		  {
               		"q": "avg:hvd.my_metric{host:precise64}",
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
    	"title": "hvd.my_metric Value (Random Number 1-1000)"
},
{
   	"definition": {
  		"viz": "timeseries",
  		"requests": [
    		  {
      			"q": "avg:hvd.my_metric{host:precise64}.rollup(sum, 3600)",
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
	"title": "Sum of hvd.my_metric Over 1 Hour"
},
{
        "definition": {
                "viz": "timeseries",
                "requests": [
                  {
			"q": "anomalies(avg:mysql.performance.queries{host:precise64}, 'adaptive', 2)",
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
        "title": "MySQL Performance Queries (with Anomalies Detection)"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     read_only=read_only)
