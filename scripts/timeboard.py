# Datadog Timeboard Script

# imports
from datadog import initialize, api
from json import dumps

# API initialization parameters
options = {'api_key': '956b376eda4be274a4d8a54fbfb84a42',
           'app_key': 'ab521a571251baa8202cef85a2d1a95bb2e26ffd'}

initialize(**options)

# Timeboard API parameters
title = "Datadog Lab - Timeboard"
description = "Timeboard generated through Datadog APIs"
graphs = [{"definition": {"events": [],
                          "requests": [{
                            "q": "avg:my_metric.randnum{host:ubuntu-xenial}",
                            "type": "line"}],
                            "viz": "timeseries"},
                          "title": "My_Metric by Host"},
          {"definition": {"events": [],
                          "requests": [{
                            "q": "anomalies(avg:mysql.performance.cpu_time{*}, 'basic', 2)",
                            "type": "line"}],
                            "viz": "timeseries"},
                          "title": "MySQL CPU Time with Anomalies"},
          {"definition": {"events": [],
                          "requests": [{
                            "q": "avg:my_metric.randnum{*}.rollup(sum, 3600)",
                            "type": "line"}],
                            "viz": "timeseries"},
                          "title": "My_Metric Rolled Up Hourly"}
        ]

template_variables = [{
    "name": "ubuntu-xenial",
    "prefix": "host",
    "default": "host:ubuntu-xenial"
}]
read_only = True

apiResponse = api.Timeboard.create(
                     title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)

# apiResponse = api.Timeboard.update(
#                      1006685,
#                      title=title,
#                      description=description,
#                      graphs=graphs,
#                      template_variables=template_variables,
#                      read_only=read_only)

# API response outputted to screen
# print(dumps(apiResponse, indent=2));
