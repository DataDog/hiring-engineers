from datadog import initialize, api

options = {
    'api_key':'d0a4908319aeeefd84c2974790a9628e',
    'app_key':'654cc55c3e083968d2c15ac2f57ad2cfcecf2f6b'
}

initialize(**options)

title = "API Datadog Visualization"
description = "Timeboard built with an API call"
graphs = [{
    "definition": {
        "requests": [
            {"q": "avg:my_metric{host:datadog}"}
        ],
        "viz": "timeseries"
    },
    "title": "my_metric"
},
{
    "definition": {
        "requests": [
            {"q": "avg:my_metric{host:datadog}.rollup(sum, 3600)"}
        ],
        "viz": "timeseries"
    },
    "title": "One hour buckets (sum) of my_metric"
},
{
    "definition": {
        "requests": [
            {"q": "anomalies(avg:postgresql.percent_usage_connections{*}, 'basic', 2)"}
        ],
        "viz": "timeseries"
    },
    "title": "Anomaly: Postgres Connections Usage %"
}]

read_only = True
create_output = api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     read_only=read_only)



