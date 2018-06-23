from datadog import initialize, api

options = {
    'api_key': 'c5ef15520895549edf48d66ac0afebf6',
    'app_key': '554ea12553d8d40bb1719757034e1f7c2cb3723b'
}

initialize(**options)

title = "Data Visual Timeboard (created through datadog API)"
description = "An informative timeboard created through the Datadog API."
graphs = [{
        "title": "My metric by host",
        "definition": {
            "events": [],
            "requests": [
                {
                    "q": "sum:my_metric{host:gcp.dev}",
                    "type": "bars"
                }
            ],
            "viz": "timeseries"
        }
    },{
        "title": "Queries p/second to the MongoDB, with anomaly detection in place",
        "definition": {
            "events": [],
            "requests": [
                {
                    "q": "anomalies(sum:mongodb.opcounters.queryps{database:mongodb}, 'basic', 2)",
                    "type": "line"
                }
            ],
            "viz": "timeseries"
        }
    },{
        "title": "My metric rolled up and summed by the past hour"
        "definition": {
            "events": [],
            "requests": [
                {
                    "q": "sum:my_metric{host:gcp.dev}.rollup(sum, 3600)",
                    "type": "line"
                }
            ],
            "viz": "timeseries",
            "autoscale": true
        }
    }
]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     read_only=read_only)