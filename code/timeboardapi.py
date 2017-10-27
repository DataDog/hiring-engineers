from datadog import initialize, api

options = {
    'api_key': 'YOUR_API_KEY_GOES_HERE',
    'app_key': 'YOUR_APP_KEY_GOES_HERE'
}

initialize(**options)

title = "Timeboard API"
description = "A timeboard created using the Datadog API"
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {
            "q": "avg:my_metric{host:datadoglabhost}",
             "type": "line"
            },
            {
             "q": "anomalies(avg:mysql.performance.queries{*}, 'basic', 2)",
             "type": "line"
            },
            {
             "q": "avg:my_metric{*}.rollup(sum, 3600)",
             "type": "line"
            }
        ],
    "viz": "timeseries"
    },
    "title": "Random Number and MySQL Queries"
}]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:my-host"
}]

read_only = False

api.Timeboard.create(title=title, description=description, graphs=graphs, template_variables=template_variables, read_only=read_only)
