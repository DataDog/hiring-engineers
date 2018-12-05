from datadog import initialize, api

options = {'api_key': 'xxx',
           'app_key': 'xxx'}
#
#
initialize(**options)

title = "Tom's Timeboard"
description = "Tom's random metric"
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{*}.rollup(sum, 3600)"}
        ],
        "viz": "timeseries"
    },
    "title": "my_metric - Tom's Random"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:mysql.performance.user_time{*}, 'basic',2)"}
        ],
        "viz": "timeseries"
    },
    "title": "MySQL Performance User Time"
}]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:my-host"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)