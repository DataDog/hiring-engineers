import os
import sys

from datadog import initialize, api


options = {
    'api_key': os.getenv('API_KEY'),
    'app_key': os.getenv('APP_KEY')
}

if options['api_key'] is None:
    print("Please set your Datadog API key in the 'API_KEY' environment variable")
    sys.exit(1)

if options['app_key'] is None:
    print("Please set your Datadog APP key in the 'APP_KEY' environment variable")
    sys.exit(1)

initialize(**options)

title = "My Timeboard"
description = "An informative timeboard."
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:system.mem.free{*}"}
        ],
    "viz": "timeseries"
    },
    "title": "Average Memory Free"
},{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{host:ubuntu-xenial}"}
        ],
    "viz": "timeseries"
    },
    "title": "My Custom Metric (check_random)"
},{
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:postgresql.max_connections{*}, 'adaptive', 2)"}
        ],
    "viz": "timeseries"
    },
    "title": "PostgreSQL Max Connections w/ Anomalies"
},{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{*}.rollup(sum, 3600)"}
        ],
    "viz": "query_value"
    },
    "title": "my_metric sum over 3600s"
}]

template_variables = [{
    "name": "hostname",
    "prefix": "host",
    "default": "host:*"
}]

read_only = True

result = api.Timeboard.create(title=title, description=description, graphs=graphs, template_variables=template_variables, read_only=read_only)

if 'errors' in result:
    print("Creating failed")
    print(result.errors)
    sys.exit(1)
else:
    print("View the dashboard at: https://app.datadoghq.com{}".format(result['url']))
