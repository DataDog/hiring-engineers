from datadog import initialize, api

options = {
    'api_key': '6f5460febf9d8b13c7aae4ed55e2408f',
    'app_key': '09f5a5204e65728e0baa2923e7e06497a96f43f7'
}

initialize(**options)

title = "Datadog Timeboard 2"
description = "An informative timeboard."
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:mysql.performance.cpu_time{*}, 'basic', 2 "}
        ],
        "viz": "timeseries"
    },
    "title": "My mySQL"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:mymetric{*}"}
        ],
        "viz": "timeseries"
    },
    "title": "My Metric"
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
