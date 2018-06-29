from datadog import initialize, api

options = {
    'api_key': '9980d8a4d4e1abf3b27302b85ac02a79',
    'app_key': 'f2e612719e2eaf93d1648efb730b71de3c16fb57'
}

initialize(**options)

title = "Hiring Engineers"
description = "Custom Metric timeboard."
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "my_metric{*} by {host}"}
        ],
        "viz": "timeseries"
    },
    "title": "my_metric: Random 0-1000"
}, {
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(mongodb.extra_info.page_faultsps{*}, 'basic',3,direction='above',alert_window='last_5m',interval=20,count_default_zero='true')"}
        ],
        "viz": "timeseries"
    },
    "title": "Anomaly graph: Page Faults/Second"
}, {
    "definition": {
        "events": [],
        "requests": [
            {"q": "my_metric{*}.rollup(avg, 3600)"}
        ],
        "viz": "timeseries"
    },
    "title": "Rollup: my_metric by hour"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)
