from datadog import initialize, api
options = {
    'api_key': '3aa7b93fa4fec88be68f654e31caae23',
    'app_key': '297428ffc521ba14998cafe35822959dcd7ad3f4'
}
initialize(**options)
title = "My_Metric Timeboard"
description = ""
graphs = [
    {
        "definition": {
            "events": [],
            "requests": [
                {"q": "avg:my_metric{host:ubuntu-xenial}"}
            ],
            "viz": "timeseries"
        },
        "title": "my_metric Scoped"
    },
    {
        "definition": {
            "events": [],
            "requests": [
                {"q": "anomalies(avg:mongodb.connections.current{host:ubuntu-xenial}, 'basic', 2)"}
            ],
            "viz": "timeseries"
        },
        "title": "Anomalies Test Mongo Connections"
    },
    {
        "definition": {
            "events": [],
            "requests": [
                {"q": "avg:my_metric{host:ubuntu-xenial}.rollup(sum, 3600)"}
            ],
            "viz": "timeseries"
        },
        "title": "Rollup function my_metric"
    },
 ]
template_variables = [{
    "name": "ubuntu_xenial",
    "prefix": "host",
    "default": "host:my-host"
}]
read_only = True
api.Timeboard.create(title=title,description=description,graphs=graphs,template_variables=template_variables)