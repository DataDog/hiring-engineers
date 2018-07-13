import os
from datadog import initialize, api

api_key = os.environ['api_key']
app_key = os.environ['app_key']

options = {'api_key': api_key,
           'app_key': app_key}

initialize(**options)

# create MySQL max connections timeseries
title = "ddogd3m0 MySQL Timeboard"
description = "MySQL Check"
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "mysql.net.max_connections{*}"}
        ],
        "viz": "timeseries"
    },
    "title": "MySQL Cluster Check"
}]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:my-host"
}]

read_only = True
new_timeboard = api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)

# Create a monitor with the anomoly function applied
options = {
    "notify_no_data": True,
    "no_data_timeframe": 20
}
tags = ["app:db", "backend"]
api.Monitor.create(
    type="metric alert",
    query="avg(last_4h):anomalies(avg:mysql.net.max_connections{*}, \'agile\', 2, direction=\'above\', " \
          "alert_window=\'last_15m\', interval=60, count_default_zero=\'true\', seasonality=\'hourly\') >= 1",
    name="Maximum connection higher than historical max",
    message="We may need to check access.",
    tags=tags,
    options=options
)
