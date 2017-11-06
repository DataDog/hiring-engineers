from datadog import initialize, api

options = {
    'api_key': '1add7bed49dbe35c708460d937ce3ea8',
    'app_key': 'dfd37e8f9392dae27e9f4cd935042c4728734b55'
}

initialize(**options)

title = "Visualizing Data Timeboard"
description = "A timeboard created using the Datadog API"
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {
            "q": "avg:my_metric",
             "type": "line"
            },
            {
             "q": "anomalies(datadog.agent.collector.collection.time over{*}, 'basic', 2)",
             "type": "line"
            },
            {
             "q": "avg:my_metric{*}.rollup(sum, 300)",
             "type": "line"
            }
        ],
    "viz": "timeseries"
    },
    "title": "Timeboard API"
}]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:my-host"
}]

read_only = False

api.Timeboard.create(title=title, description=description, graphs=graphs, template_variables=template_variables, read_only=read_only)
