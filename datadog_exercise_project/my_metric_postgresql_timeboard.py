from datadog import initialize
from datadog import api
options = {
    'api_key':'6ecfd1d61dff04a0547d44561ac09911',
    'app_key':'83bf20f58f0fcc8b3d891b7817ba5d02eefde58f'	
}

initialize(**options)

title = "Timeboard of my_metric and database anomalies"
description = "my_metric check and postgresql anomalies"

graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{*}"}
        ],
        "viz": "timeseries"
    },
    "title": "my_metric"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "sum:my_metric{*}.rollup(sum, 3600)"}
        ],
        "viz": "timeseries"
    },
    "title": "my_metric Hourly"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:postgresql.buffer_hit{*}, 'basic', 2)"}
        ],
        "viz": "timeseries"
    },
    "title": "Postgresql Buffer Hit Anomalies"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     read_only=read_only)


