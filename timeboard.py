from datadog import initialize, api

options = {
    'api_key': '16ff05c7af6ed4652a20f5a8d0c609ce',
    'app_key': 'e6a169b9b337355eef90002878fbf9a565e9ee77'
}

initialize(**options)

title = "Mymetric timeboard"
description = "Mymetric Timeboard"
graphs = [
    {
        "definition": {
            "events": [],
            "requests": [
                {"q": "avg:mymetric{host:ubuntu-xenial}"}
            ],
            "viz": "timeseries"
        },
        "title": "mymetric in timeseries"
    },
    {
        "definition": {
            "events": [],
            "requests": [
                {"q": "anomalies(avg:postgres.connections.current{host:ubuntu-xenial}, 'basic', 2)"}
            ],
            "viz": "timeseries"
        },
        "title": "PostgreSQL connections"
    },
    {
        "definition": {
            "events": [],
            "requests": [
                {"q": "avg:mymetric{host:ubuntu-xenial}.rollup(sum, 3600)"}
            ],
            "viz": "timeseries"
        },
        "title": "Rollup function mymetric"
    },
 ]
template_variables = [{
    "name": "ubuntu_xenial",
    "prefix": "host",
    "default": "host:my-host"
}]
read_only = True
api.Timeboard.create(title=title,description=description,graphs=graphs,template_variables=template_variables)