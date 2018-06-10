from datadog import initialize, api

options = {
    'api_key': '12318cf8e1de09d4dc4094199a043548',
    'app_key': 'c7f0eaf7400f66ff09c245b0f438ea3e609f2169'
}

initialize(**options)

title = "Hadhemi Samaali : My timeboard"
description = "Datadog technical task"
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {
                "q": "avg:my_metric{*}",
                "type": "line",
        }
        ],
        "viz": "timeseries"
    },
    "title": "Average values sent by my_metric"
},
{
"definition": {
        "events": [],
        "requests": [
            {
                "q": "anomalies(max:my_metric{*}, 'basic', 1)",
                "type": "line",
                "aggregator": "avg"
        }
        ],
        "viz": "timeseries"
    },
    "title": "My metric anomalies"
},
{
"definition": {
        "events": [],
        "requests": [
            {
                "q": "sum:my_metric{*}.rollup(sum, 3600)",
                "aggregator": "avg"
        }
        ],
        "viz": "toplist"
    },
    "title": "my_metric with rollup function during the last hour"
}]


read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     read_only=read_only)