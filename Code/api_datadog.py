from datadog import initialize, api


options = {
    'api_key' : '17a7f314f7f3622fb507c40ecba42dbe',
    'app_key' : 'c192d7c2de3727a72a6685c4f714d5e98b8f3a74'
}

initialize(**options)

title = "Datadog my_metric Timeboard"
description = "Timeboard for my_metric"

graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{host:daeclan-MacBookPro}"}
        ],
        "viz": "timeseries"
    },
    "title": "Average of my metric scoped over host daeclan-MacBookPro"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{host:daeclan-MacBookPro}.rollup(sum, 3600)"}
        ],
        "viz": "query_value"
    },
    "title": "my_metric with rollup function applied to sum up all the points for past hour in one bucket"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(mongodb.opcounters.queryps{host:daeclan-MacBookPro}, 'basic', 2)"}
        ],
        "viz": "timeseries"
    },
    "title": "Queries per second with anomoly function applied"
}]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:my-host"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)
