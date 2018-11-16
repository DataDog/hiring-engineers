from datadog import initialize, api

options = {
    'api_key': '00be3f7ddc76e24f79a24a979ebb7172',
    'app_key': 'fd311bf2ce2a0da52a1c9c45ccaecf06011b4cb3'
}

initialize(**options)

title = "Technical Exercise Timeboard"
description = "This Timeboard contains three graphs that "
graphs = [
    {
        "definition": {
            "events": [],
            "requests": [
                {"q": "avg:my_metric{host:ubuntu-xenial}"}
            ],
            "viz": "timeseries"
        },
        "title": "My_Metric Scoped Over Host"
    },
    {
        "definition": {
            "events": [],
            "requests": [
                {"q": "anomalies(avg:mysql.performance.kernel_time{host:ubuntu-xenial}, 'basic', 2)"}
            ],
            "viz": "timeseries"
        },
        "title": "Anomoly Function over MySQL Peformance Kernel Time"
    },
    {
        "definition": {
            "events": [],
            "requests": [
                {"q": "avg:my_metric{host:ubuntu-xenial}.rollup(sum, 3600)"}
            ],
            "viz": "timeseries"
        },
        "title": "Sum of my_metric per hour, Rollup"
    },
]
template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:xenial"
}]
read_only = True
api.Timeboard.create(title=title,description=description,graphs=graphs,template_variables=template_variables,read_only=read_only)

