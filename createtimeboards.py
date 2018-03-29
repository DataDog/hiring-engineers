from datadog import initialize, api

options = {'api_key': 'f14548e57383aa4c4d9a458ffe119ad0',
           'app_key': '8442487bf36036009b593998145053dbfeb89e04'}

initialize(**options)

title = "BB Demo Timeboard via API"
description = "The quickest timeboard ever created."


graphs = [{
    "definition": {
	  "viz": "timeseries",
	  "status": "done",
	  "requests": [
		{
		  "q": "avg:my_metric{host:precise64}",
		  "type": "line",
		  "style": {
			"palette": "dog_classic",
			"type": "solid",
			"width": "normal"
		  },
		  "conditional_formats": []
		}
	  ],
	  "autoscale": "true"
	},
    "title": "my_metric"
},
	{
	"definition": {
	  "viz": "timeseries",
	  "status": "done",
	  "requests": [
		{
		  "q": "anomalies(avg:mongodb.network.bytesinps{host:precise64}, 'basic', 2)",
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
	  "autoscale": "true"
	},
	"title": "mongodb.network.bytesinps"
},
	{
	"definition": {
	  "viz": "query_value",
	  "status": "done",
	  "requests": [
		{
		  "q": "avg:my_metric{host:precise64}.rollup(sum, 60)",
		  "type": "line",
		  "style": {
			"palette": "dog_classic",
			"type": "solid",
			"width": "normal"
		  },
		  "conditional_formats": [],
		  "aggregator": "sum"
		}
	  ],
	  "autoscale": "false",
	  "precision": "0"
	},
	"title": "Last-hour Sum (my_metric)"
}]


read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     read_only=read_only)