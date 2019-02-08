from datadog import initialize, api

options = {
    'api_key': 'f98954a3916a1ee5b81f204fffe4c652',
    'app_key': '14491168f3c77a6bad06c7d7487be3ae5719e52e'
}

initialize(**options)

title = "Kyle's TimeBoard"
description = "Solution's Engineer Code Challenge Timeboard"
graphs = [{
    "definition": {
        "events": [],
        "requests": [{
            "q": "avg:my_metric{host:ubuntu-xenial}",
            "type": "line",
        }],
        "viz": "timeseries"
    },
    "title": "Metric Scoped With Host",
}, {
    "definition": {
        "events": [],
        "requests": [{
         "q": "avg:postgresql.bgwriter.checkpoints_timed{host:ubuntu-xenial}.as_count()",
         "type": "line",
        }],
        "viz": "timeseries"
    },
    "title": "Anomoly monitor for PostgreSQL",
}, {
    "definition": {
        "events": [],
        "requests": [{
            "q": "avg:my_metric{*}.rollup(sum, 3600)",
            "type": "line",
        }],
        "viz": "timeseries"
    },
    "title": "Metric Rollup Point Sum",
}]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:my-host"
}]

read_only = True

api.Timeboard.create(
    title=title,
    description=description,
    graphs=graphs,
    template_variables=template_variables,
    read_only=read_only
    )
