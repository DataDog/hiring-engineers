from datadog import initialize, api

options = {
        'api_key': 'b74ec81aaf24f198a363625339a09f80',
        'app_key':'93a1305f00f40b578cfda50199ed7179da375ddc'
}

initialize(**options)

title = "Timeboards for the hiring exercise"
description = "An informative timeboard for my metric."
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "min:my_metric{host:vagrant}"}
        ],
        "viz": "timeseries"
    },
    "title": "Timeboard for my_metric"
    },
    {
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:mysql.performance.cpu_time{db:mysql}, 'basic', 2)",}
        ],
        "viz": "timeseries"
    },
    "title": "Avg MySql CPU Performace with the Anomaly Function applied"
    },
    {
    "definition": {
        "events": [],
        "requests": [
            {"q": "min:my_metric{host:vagrant}.rollup(sum, 3600)"}
        ],
        "viz": "timeseries"
    },
    "title": "my_metric with sum rollup function applied"}

]

template_variables = [{
    "name": "host",
    "prefix": "host",
    "default": "host:vagrant"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)