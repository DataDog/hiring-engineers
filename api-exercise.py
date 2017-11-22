# Configure the module according to your needs
from datadog import initialize

options = {
    'api_key':'hidden',
    'app_key':'hidden'
}

initialize(**options)

# Use Datadog REST API client
from datadog import api

title = "Hiring Exercise Timeboard"
description = """ Timeboard showing my custom metric, mongodb 
                resident memory, and my custom metric with the rollup
                function applied.. """

graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{host:ubuntu-srv.lightsail}"}
        ],
    "viz": "timeseries"
    },
    "title": "Custom Metric Timeseries on My Host"
},
{
    "definition": {
        "events": [],
        "requests": [
                {
                "q": """anomalies(avg:mongodb.mem.resident{server:
                mongodb://datadog:_localhost:27017}, 'basic', 2)"""
                }
        ],
    "viz": "timeseries"
    },
    "title": "Database Resident Memory with Anomaly Detection"
},
{
    "definition": {
        "events": [],
        "requests": [
                {"q": """avg:my_metric{host:ubuntu-srv.lightsail}
                        .rollup(sum, 3600)"""}
        ],
    "viz": "timeseries"
    },
    "title": "Custom Metric Timeseries with Rollup"
}]

read_only = True

api.Timeboard.create(title=title, description=description, 
        graphs=graphs, read_only=read_only)
