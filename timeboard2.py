# Make sure you replace the API and/or APP key below
# with the ones for your account

from datadog import initialize, api

options = {
    'api_key': '9579b60af86e761cba333fbe4e87610c',
    'app_key': 'b0e7461baf69881c5dc6dbbecb87540d7114cc99'
}

initialize(**options)

title = "Wyatt Timeboard"
description = "Wyatt Timeboard for SE Assessment"
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "my_metric{*} by {host}"},
        ],
    "viz": "timeseries"
    },
    "title": "My_Metric"
},

   { "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(mysql.performance.cpu_time{*}, 'basic', '1e-3', direction='above')"},
        ],
    "viz": "timeseries"
    },
    "title": "Average MySql CPU Time with Anomaly Function"
},

   { "definition": {
        "events": [],
        "requests": [
            {"q": "my_metric{*} by {host}.rollup(sum,3600)"}
        ],
    "viz": "timeseries"
    },
    "title": "My_Metric Hourly Rollup"
}

]

template_variables = [{
    "name": "precise64",
    "prefix": "host",
    "default": "host:precise64"
}]

read_only = False
api.Timeboard.create(title=title, 
                    description=description, 
                    graphs=graphs, 
                    template_variables=template_variables, 
                    read_only=read_only)