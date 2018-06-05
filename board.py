from datadog import initialize, api

options = {
    'api_key': '5bab16b0df59af671f2175448d0b71c2',
    'app_key': '45122f91c2e1fe8db22fc43559ae42ac54f5b443'
}

initialize(**options)

title = "A Usful Timeboard"
description = "An informative timeboard."
graphs = [
    {#Graph 1 - my_metric over host
        "title": "my_metric over host",
        "definition": {
            "events": [],
            "requests": [
                {"q": "my_metric{host:bt-book}"}
            ],
        },
        "viz": "timeseries"
    },
    { #Graph2 - database data with anomaly function
        "title": "Anomalies in total number of connections to DB",
        "definition": {
      			"events": [],
      			"requests": [
      				{"q": "anomalies(mongodb.connections.current{host:bt-book}, 'basic', 2)"}]
      	},
      	"viz": "timeseries"
    },
    { #Graph 3 - my_metric with rollup function for past hour
        "title": "Rollup function applied sum of point for past hour",
        "definition": {
            "events": [],
            "requests": [
                {
                    "q": "sum:my_metric{*}.rollup(sum, 3600)",
                    "aggregator": "sum"
                }
            ],
        },
        "viz": "query_value"
    }
]

template_variables = [{
    "name": "bt-book",
    "prefix": "host",
    "default": "host:bt-book"
}]
read_only = True

api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)
