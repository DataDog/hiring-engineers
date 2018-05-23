from datadog import initialize, api

options = {
    'api_key': 'c945968ad75a78946ac20416243c6edc',
    'app_key': 'b2310752363106a4dc443fe39954eb80f8cf89e4'
}

initialize(**options)

title = "Matt Lee Timeboard - 5/22/2018 via API"
description = "An informative timeboard."
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
    "title": "My custom metric (my_metric) scoped over my host"
},
{
"definition": {
        "events": [],
        "requests": [
            {
                "q": "anomalies(max:postgresql.table.count{*}, 'basic', 1)",
                "type": "line",
                "aggregator": "avg"
        }
        ],
        "viz": "timeseries"
    },
    "title": "Postgres Table Counts (Anomalies)"
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
    "title": "Custom metric with rollup function and summed past hr pts"
}]


read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     read_only=read_only)
