from datadog import initialize, api

options = {
    'api_key': 'c7c0572c87dc9c1295865e5fb4246307',
    'app_key': 'b0ce75a211360b93300465f78abfc8ce82443c5d'
}

initialize(**options)

title = "Vicente's Dashboard"
description = "Dashboard created through the API"
graphs = [
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:custom.mycheck{*}"}
        ],
        "viz": "timeseries"
    },
    "title": "Random Number"
},
{ 
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:mongodb.uptime{*}, 'basic', 2)"}
        ],
        "viz": "timeseries"
    },
    "title": "Anomalies for MongoDB"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:custom.mycheck{*}.rollup(sum, 3600)"}
        ],
        "viz": "timeseries"
    },
    "title": "Random number 1 hour rollup"
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

