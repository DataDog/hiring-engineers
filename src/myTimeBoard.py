from datadog import initialize, api

options = {
    'api_key': '01f50e7f7f522a300abcf6b851bcc1ef',
    'app_key': '3aee7aee5a1669c0fd007c6e3a16535ac3bc2c21'
}
initialize(**options)
title = "Hanting ZHANG's Timeboard"
description = "Demo Timeboard"
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {
                "q": "avg:mymetric{*}",
                "type": "line",
        }
        ],
        "viz": "timeseries"
    },
    "title": "Custom metric 'mymetric' scoped over my host"
},

{
"definition": {
        "events": [],
        "requests": [
            {
                "q": "anomalies(avg:postgresql.connections{db:datadog}, 'basic', 2)",
                "type": "line",
                "aggregator": "avg"
        }
        ],
        "viz": "timeseries"
    },
    "title": "Scope for Postgres with anomaly function applied"
},
{
"definition": {
        "events": [],
        "requests": [
            {
                "q": "sum:mymetric{*}.rollup(sum, 3600)",
                "aggregator": "avg"
        }
        ],
        "viz": "toplist"
    },
    "title": "My custom metric 'mymetric' with the rollup function applied to sum up all the points for the past hour into one bucket "
}]
read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     read_only=read_only)