from datadog import initialize, api

options = {'api_key': 'redacted',
           'app_key': 'redacted'}

initialize(**options)

#print api.Timeboard.get_all()

title = "Challenge Timeboard"
description = "For the challenge."
graphs = [
    {
        "definition": {
            "events": [],
            "requests": [
                {"q": "my_metric{host:ubuntu-xenial}"}
            ],
            "viz": "timeseries"
        },
        "title": "My Metric"
    },
    {
        "definition": {
            "events": [],
            "requests": [
                {"q": "anomalies(mysql.performance.cpu_time{host:ubuntu-xenial}, 'basic', 2)"}
            ],
            "viz": "timeseries"
        },
        "title": "MySQL Performance (CPU)"
    },
    {
        "definition": {
            "events": [],
            "requests": [
                {"q": "my_metric{host:ubuntu-xenial}.rollup(sum,3600)"}
            ],
            "viz": "timeseries"
        },
        "title": "My Metric Roll-up (60 min)"
    },
]

read_only = True
print api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     read_only=read_only)