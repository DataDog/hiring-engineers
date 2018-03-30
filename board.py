from datadog import initialize, api

options = {'api_key': '14c9f5ec062ac10cc3b51e6e09cf6dd5',
           'app_key': '16c300d450bf39850b07890d4b5db6aa9f09a099'}

initialize(**options)


title = "My Timeboard"
description = "An informative timeboard."
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{host:vagrant-ubuntu-trusty-64}"},
        ],
        "viz": "timeseries"
    },
    "title": "My Metric"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:mysql.net.connections{*}, 'basic', 2)"}
        ],
        "viz": "timeseries"
    },
    "title": "MySQL Connection Anomalies"

},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{*}.rollup(sum, 3600)",
            "type":"bar"}
        ],
        "viz": "timeseries"
    },
    "title": "Sum of My Metric over the last hour"
}]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:vagrant-ubuntu-trusty-64"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)
