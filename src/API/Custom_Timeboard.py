# Make sure you replace the API and/or APP key below
# with the ones for your account

from datadog import initialize, api
import json
import pprint

options = {
    'api_key': '3dd19598055ebd8d75813ed9cbf35a4a',
    'app_key': '1c28de1f5de3719b85c5789d1dd34ca360fe88c8'
}

initialize(**options)

# Set Timeboard general settings
title = "Steve's Custom Timeboard"
description = "An informative custom timeboard."

# Define the graphs that will be created on the Timeboard
graphs = [
    {
        "definition": {
            "events": [],
            "requests": [
                {"q": "avg:custom.my_metric{*}"}
            ],
            "viz": "timeseries"
        },
        "title": "Custom Random Metric"
    },
    {
        "definition": {
            "autoscale": True,
            "events": [],
            "requests": [
                {"q": "anomalies(max:mysql.performance.com_select{*}, 'basic', 3)"}
            ],
            "viz": "timeseries"
        },
        "title": "MySQL Queries Per Second (Anomaly Detection)"
    },
    {
        "definition": {
            "precision": 0,
            "events": [],
            "requests": [
                {  
                    "aggregator": "sum",
                    "q": "hour_before(custom.my_metric{*})"
                }
            ],
            "viz": "query_value"
        },
        "title": "Sum of custom metric over the last hour"
    }
]

# Restrict the scope to the ubuntu host
template_variables = [{
    "name": "ubuntu",
    "prefix": "host",
    "default": "host:ubuntu"
}]

read_only = True

# Call the Datadog API and print the JSON results in a more readable format
response = api.Timeboard.create(title=title, description=description, graphs=graphs, template_variables=template_variables, read_only=read_only)
pprint.pprint(response)