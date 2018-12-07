from datadog import initialize, api

options = {
    'api_key': '3c658e247c0076099c7676f2d42460df',
    'app_key': '9afb3a081055cf3f3ef8a2d57d3ba9d0a9c72699'
}

initialize(**options)

api.Monitor.create(
    type="query alert",
    query="avg(last_5m):avg:system.load.5{host:william-Q325UA} < 0.15",
    name="Load of system.load.5",
    message="Load dropped below acceptable range of 0.15"
)

timeboard_title = "Timeboard with the 3 graphs"
timeboard_description = "Timeboard created with my_metric, system.load.5 with anomaly monitor and my_metric with rollup function"
timeboard_graphs = [{
        "definition": {
            "events": [],
            "requests": [
                {"q":"random.number.gen{*}"}
            ],
            "viz": "timeseries"
        },
        "title": "Random Number Timeboard (scoped over host)"
    },
    {
        "definition": {
            "events": [],
            "requests": [
                {"q":"system.load.5{*}"}
            ],
            "viz": "timeseries"
        },
        "title": "System load with monitor"
    },
    {
        "definition": {
            "events": [],
            "requests": [
                {"q":"random.number.gen{*}.rollup(sum,3600)"}
            ],
            "viz": "timeseries"
        },
        "title": "Random Number Timeboard (with rollup functin applied)"
    }
]

read_only = True

api.Timeboard.create(title=timeboard_title,
                     description=timeboard_description,
                     graphs=timeboard_graphs,
                     read_only=read_only)
