from datadog import initialize, api

options = {
    'api_key':'2986a4e6213a075a1c413d820154a3c2',
    'app_key':'43e258881a7dca875f00184a001e7eb3626407bc'
}

initialize(**options)

title = "API Datadog Visualization"
description = "fawzi's Timeboard"
graphs = [{
    "definition": {
        "requests": [
            {"q": "avg:my_metric{host:fawzi}"}
        ],
        "viz": "timeseries"
    },
    "title": "my_metric"
},
{
    "definition": {
        "requests": [
            {"q": "avg:my_metric{host:fawzi}.rollup(sum, 3600)"}
        ],
        "viz": "timeseries"
    },
    "title": "1h buckets (sum) of my_metric"
},
{
    "definition": {
        "requests": [
            {"q": "anomalies(avg:mysql.performance.user_time{*}, 'basic', 2)"}
        ],
        "viz": "timeseries"
    },
    "title": "Anomaly: MySQL Connections Usage %"
}]

read_only = True
create_output = api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     read_only=read_only)
