from datadog import initialize, api

options = {
    'api_key': '8677a7b08834961d73c4e0e22dbd6e07',
    'app_key': 'c0b4b8b60f508a8c3d5f77064950efaaff3efc64'
}

initialize(**options)

title = "My First Timeboard"
description = "A custom first timeboard."
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "my_metric{host:ubuntu-xenial}"}
        ],
        "viz": "timeseries"
    },
    "title": "My_Metric for localhost"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(mysql.performance.user_time{host:ubuntu-xenial}, 'basic', 2)"}
        ],
        "viz": "timeseries"
     },
     "title": "MySQL CPU time (per sec), anomalies beyond two standard deviations indicated"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "my_metric{host:ubuntu-xenial}.rollup(sum,3600)"}
        ],
        "viz": "timeseries"
     },
     "title": "my_metric, summed over the last hour"
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

