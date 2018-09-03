from datadog import initialize, api

options = {
    'api_key': '2fafef04f82614a4dae4a36314e65a84',
    'app_key': '22e9975f9d71e51a19b5cfef01427d1d1ad34e52'
}

initialize(**options)

title = "My Timeboard"
description = "An informative timeboard."
graph1 = {
    "definition": {
        "events": [],
        "requests": [
            {"q": "my_metric{*}"},
            {"q": "my_metric{*}.rollup(avg, 3600)"}
        ],
        "viz": "timeseries"
    },
    "title": "my_metric"
}

graph2 = {
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:mysql.performance.user_time{*}, 'basic', 3)"}
        ],
        "viz": "timeseries"
    },
    "title": "Mysql CPU Metric"
}

res = api.Timeboard.create(title=title,
                     description=description,
                     graphs=[graph1, graph2])
print(res)