from datadog import initialize, api

options = {
    'api_key': '2dbee3dcf0efb64aed9d7c036660e32c',
    'app_key': 'e1aa5905fd308d267e70985971be1b6983e28813'
}

initialize(**options)

title = "Sean Timeboard"
description = "An informative timeboard."
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{host:ubuntu-xenial}"},
            {"q": "anomalies(avg:mysql.performance.bytes_received{host:ubuntu-xenial}, 'basic', 2)"},
            {"q": "avg:my_metric{host:ubuntu-xenial}.rollup(sum, 3600)"}
        ],
        "viz": "timeseries"
    },
    "title": "Test Timeboard"
}]

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
