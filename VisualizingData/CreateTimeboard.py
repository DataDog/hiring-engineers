from datadog import initialize, api

options = {
    'api_key': '1b9f1b21e13774d14ad4077929a3b178',
    'app_key': '5a56c90fa5b63322f5a92b04c748034817c1e9c7'
}

initialize(**options)

title = "My Timeboard Trial"
description = "An informative timeboard"
graphs = [
    {            
       "definition": {
           "requests": [
                { 
                "q": "avg:my_metric.randomint{host:c-instance-3.asia-northeast1-b.c.trial-project-227315.internal}",
                     "style": {
                                 "palette": "purple",
                                 "width": "normal",
                                 "type": "dotted"
                    },
                    "type": "line"
                } 
            ],
            "viz": "timeseries"
        },                
        "title": "My Custom Metric over my host"
    },

    {
        "definition": {
            "requests": [
                {
                "q": "anomalies(avg:mysql.performance.cpu_time{host:c-instance-3.asia-northeast1-b.c.trial-project-227315.internal}, 'basic', 2)",
                    "style": {
                               "palette": "dog_classic",
                               "width": "normal",
                               "type": "solid"
                    },
                    "type": "line"
                }
            ],
            "viz": "timeseries"
        },
        "title": "CPU time from MySQL integration with the anomaly function applied"
    },

    {
        "definition": {
            "requests": [
                {
                "q": "sum:my_metric.randomint{host:c-instance-3.asia-northeast1-b.c.trial-project-227315.internal} by {instance-id}.rollup(sum, 3600)",
                    "style": {
                               "palette": "cool",
                               "width": "normal",
                               "type": "solid"
                    },
                    "type": "area"
                }
            ],
            "viz": "timeseries"
        },
        "title": "My Custom metric with the rollup function applied to sum up all the points for the past hour"
    }
]

template_variables = [{
    "default": "host:c-instance-3.asia-northeast1-b.c.trial-project-227315.internal",
    "prefix": "host",
    "name": "host1"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)