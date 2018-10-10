# Configure the module according to your needs
from datadog import initialize, api
options = {'api_key': 'efd6d9433248935024bd9ea0a28fca3d',
           'app_key': '3ef626877f7e5118e3ac65082a574bdfc5266887'}


initialize(**options)

# Use Datadog REST API client
title = "Test Timeboard"
description = "A timeboard with a defined Metric."
 
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{*}"}
        ],
        "viz": "timeseries"
    },
    "title": "scope"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:mysql.net.connections{*}.as_count(), 'basic', 2)"}
        ],
        "viz": "timeseries"
    },
    "title": "rollup"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{*}.rollup(sum, 3600)"}
        ],
        "viz": "timeseries"
    },
    "title": "rollup"
}
]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:my-host"
}]
read_only = True
print api.Timeboard.create(
        title=title,
        description=description,
        graphs=graphs,
        template_variables=template_variables,
        read_only=read_only
       )
