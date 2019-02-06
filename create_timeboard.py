from datadog import initialize, api

options = {
    'api_key': '4f76a88afecfebe16d6c4942f8076374',
    'app_key': '8606b5f24521ab823d7bba5d64d012ae45b76ec6'
}

initialize(**options)

title = "Dale's Metrics"
description = "A timeboard built for the Datadog interview process"
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{host:precise64}"}
        ],
        "viz": "timeseries"
    },
    "title": "My Metric"
},{
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:mysql.performance.queries{host:precise64}, 'basic', 2)"}
        ],
        "viz": "timeseries"
    },
    "title": "MySQL Metric"
},{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{host:precise64}.rollup(sum, 3600)",
            "type": "bars"}
        ],
        "viz": "timeseries"
    },
    "title": "My Metric Rollup"
}]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:my-host"
}]

read_only = True
result = api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)

print result