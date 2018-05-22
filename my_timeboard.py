from datadog import initialize, api

options = {'api_key': <API_KEY>,
           'app_key': <APP_KEY>}

initialize(**options)

title = "Elizabeth's Timeboard"
description = "SE challenge accepted!"
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "my_metric{*}"},
            {
                "q": "my_metric{*}.rollup(sum, 3600)",
                "type": "bars",
                "style": {
                  "palette": "cool",
                  "type": "solid",
                  "width": "normal"
                  }          
            },
            {"q": "anomalies(avg:system.net.bytes_sent{*}, 'basic', 2)"}
        ],
        "viz": "timeseries"
    },
    "title": "My Metric, My Metric sum over past 60 minutes, and MySQL bytes sent"
},]

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
