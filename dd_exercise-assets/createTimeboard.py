# for the security purpose, I did not include API and Application keys.
# let me know if you need them.

from datadog import initialize, api

options = {
    'api_key': '***',
    'app_key': '***'
}

initialize(**options)

title = "Hiring Tech Exercise Timeboard"
description = "Created for Tech Exercise"
graphs = [{
    "definition": {
        "requests": [
            {"q": "avg:my_metric{datadogtechexcersie}"},
        ],
        "viz": "timeseries"
    },
    "title": "my_metric"
},
{
    "definition" : {
        "requests": [
            {"q": "anomalies(avg:mysql.performance.cpu_time{datadogtechexcersie}, 'basic', 2)"}
        ],
        "viz": "timeseries"
    },
    "title": "MySQL Performance CPU Time"
},
{
    "definition": {
        "requests": [
            {"q": "avg:my_metric{datadogtechexcersie}.rollup(sum, 3600)"},
        ],
        "viz": "timeseries"
    },
    "title": "my_metric with rollup function applied"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     read_only=read_only)