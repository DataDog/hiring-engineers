from datadog import initialize, api

options = {
  'api_key': '*****',
  'app_key': '*****'
}

initialize(**options)

title = "Exercise Timeboard"
description = "Timeboard created via API"
graphs = [{
    "definition": {
        "events": [],
        "requests": [
        {"q": "random.number{host:ubuntu-bionic}"}
        ],
        "viz": "timeseries"
    },
    "title": "Random number check value"
},
{
    "definition": {
        "events": [],
        "requests": [
        {"q": "random.number{host:ubuntu-bionic}.rollup(sum, 3600)"}
        ],
        "viz": "timeseries"
    },
    "title": "Random number rolling hourly sum"
},
{
    "definition": {
        "events": [],
        "requests": [
        {"q": "anomalies(mongodb.mem.resident{host:ubuntu-bionic}, 'basic', 3, direction='above')"}
        ],
        "viz": "timeseries"
    },
    "title": "MongoDB memory usage"
}]


read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     read_only=read_only)