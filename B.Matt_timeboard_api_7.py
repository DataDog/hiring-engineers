from datadog import initialize, api
import json

options = {
    'api_key': '9a2e84eba6ae43746c099ab4cb4a9880',
    'app_key': '3cec17b02afe603efdfc54d11db37477cb1ebd3e'

}

initialize(**options)

title = "Matt Timeboard via API"
description = "Creating Timeboard via API 2"
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
    "title": "Anomaly: Avg MySql CPU "
},

   { "definition": {
        "events": [],
        "requests": [
            {"q": "my_metric{*} by {host}.rollup(sum,3600)"}
        ],
    "viz": "timeseries"
    },
    "title": "My_Metric Rollup 2"
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