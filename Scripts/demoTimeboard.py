from datadog import initialize, api

options = {
    'api_key': '<DD_API_KEY>',
    'app_key': '<DD_APP_KEY>'
}

initialize(**options)

title = "Troy's Demo Timeboard"
description = "a timeboard created using the datadog api"

graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:agent.random.num{host:stretch.localdomain}"}
        ],
        "viz": "timeseries",
    },
    "title": "Random Number"

},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:mysql.net.connections{host:stretch.localdomain}, 'basic', 1)"}
        ],
        "viz": "timeseries"
    },
    "title": "Average Net MySQL connections per host (anomaly detect)"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:agent.random.num{host:stretch.localdomain}.rollup(sum, 3600)"}
        ],
        "viz": "timeseries"
    },
    "title": "Sum of Random Numbers (previous hour)"
}
]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     read_only=read_only)
