from datadog import initialize, api

options = {
    'api_key': '3bbb7f03d9149346d029d93eced23910',
    'app_key': 'd4cfbbe0ba46215141977bd6e75f975e541b1569'
}

initialize(**options)

title = "My Timeboard"
description = "Custom Metric Timeboards."
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:custom_my_metric{host:Josephs-MBP-2.fios-router.home}"},
        ],
        "viz": "timeseries"
    },
    "title": "Custom My Metric Timeseries"
},
{
      "definition": {
        "events": [],
        "requests": [
             {"q": "anomalies(avg:system.cpu.system{*}, 'basic', 2)"},
        ],
        "viz": "timeseries"
    },
    "title": "CPU Anomalies "
},
{
      "definition": {
        "events": [],
        "requests": [
            {"q": "avg:custom_my_metric{*}.rollup(sum, 3600)"},
        ],
        "viz": "query_value"
    },
    "title": "Custom Metric Rollup Sum"
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
