# I created a file in /etc/datadog-agent directory and added this code to it. I then ran this from vagrant@ubuntu-xenial. 
from datadog import initialize, api

options = {
    'api_key': 'f1939bb97730746da2a69d15c07b5901',
    'app_key': '4c77d168fad964f68b4cd340ca63c0f5a009694c'
}

initialize(**options)

title = "My Timeboard"
description = "An informative timeboard displaying my_metric and integration data."
graphs = [
  {
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{host:ubuntu-xenial}"}
        ],
        "viz": "timeseries"
    },
    "title": "My custom metric"
  },
  {
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:postgresql.percent_usage_connections{host:ubuntu-xenial}, 'basic', 2)"}
        ],
        "viz": "timeseries"
    },
    "title": "PostgreSQL integration anomaly"
  },
  {
    "definition": {
        "events": [],
                "requests": [
            {"q": "avg:my_metric{host:ubuntu-xenial}.rollup(sum, 3600)"}
        ],
        "viz": "timeseries"
    },
    "title": "My custom metric rollup"
  }
]

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



