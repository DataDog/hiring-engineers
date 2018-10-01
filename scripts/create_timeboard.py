from datadog import initialize, api

options = {'api_key': '6571cc08cd3423d3cb31bb4977745cbf',
           'app_key': 'c81f05555320c2ae7aa8bda4ba34ecd181cf3e96'}

initialize(**options)

title = "Girish Timeboard"
description = "Girish's timeboard showing custom metric."
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:girish.random{*}"}
        ],
        "viz": "timeseries"
    },
    "title": "Girish's random number"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:girish.random{*}, 'basic', 2)"}
        ],
        "viz": "timeseries"
    },
    "title": "Girish's anomaly"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:girish.random{*}.rollup(sum, 3600)"}
        ],
        "viz": "query_value"
    },
    "title": "Girish's rollup"
}]

template_variables = [{
    "name": "host",
    "prefix": "host",
    "default": "host:Girishs-MacBook-Pro.local"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)


