from datadog import initialize, api

options = {
    'api_key': '17c0a94e7406653961ec19a721345215',
    'app_key': '1787a0a04268b196f5839635c9d172c75cf2d85b'
}

initialize(**options)

title = "Datadog Timeboard"
description = "This timeboard displays the custom metric scoped over host, the max connections over PostGres, and the sum of the custom metric for the past hour"
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {
            "q": "avg:my_metric{host:koshas-MacBook.local}",
             "type": "line"
            },
            {
             "q": "anomalies(avg:postgresql.max_connections{*}, 'basic', 2)",
             "type": "line"
            },
            {
             "q": "avg:my_metric{*}.rollup(sum, 3600)",
             "type": "line"
            }
        ],
    "viz": "timeseries"
    },
    "title": "Custom Metric & PostGres"
}]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:my-host"
}]

read_only = True

res = api.Timeboard.create(title=title, description=description, graphs=graphs, template_variables=template_variables, read_only=read_only)

print(res)