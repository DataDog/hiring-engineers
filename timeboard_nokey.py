from datadog import initialize, api

options = {
    'api_key': 'xxx',
    'app_key': 'xxx'
}

initialize(**options)

title = "Timeboard from API (python)"
description = "A dashboard created by API."
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{host:bamboo01}"}
        ],
    "viz": "timeseries"
    },
    "title": "My custom metric scoped over my host"
}, {
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:mysql.performance.user_time{*}, 'basic', 2)"}
        ],
    "viz": "timeseries"
    },
    "title": "Any metric from the Integration on my Database with the anomaly function applied"
}, {
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{*}.rollup(sum, 3600)"}
        ],
    "viz": "timeseries"
    },
    "title": "My custom metric with the rollup function applied to sum up all the points for the past hour into one bucket"
}]

template_variables = [{
    "name": "host",
    "prefix": "host",
    "default": "host:bamboo01"
}]

read_only = True

api.Timeboard.create(title=title, description=description, graphs=graphs, template_variables=template_variables, read_only=read_only)