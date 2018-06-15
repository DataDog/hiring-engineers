from datadog import initialize, api

# keys added here for convenience, in production they should probably be passed as environment variables

options = {"api_key": "963dc35000c5cb12e12d5095ff38b861", "app_key":"969c206e89ef5a8147cf026176fbcba403dbd622" }

initialize(**options)

title = "Laura's Timeboard"
description = "Tracks my_metric"

graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{*}"}
        ],
        "viz": "timeseries"
    },
    "title": "my_metric over time"
}, {
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:mongodb.database_size{role:database:mongodb}, 'basic', 3)"
             }],
        "viz": "timeseries"
    },
    "title": "Database size anomalies"
}, {
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{*}.rollup(sum, 3600)"}
        ],
        "viz": "timeseries"
    },
    "title": "Hourly Rollup Sum of my_metric"
}]

template_variables = [{
    "name": "i-0a9ff2c19f22d237a",
    "prefix": "host",
    "default": "host:i-0a9ff2c19f22d237a"
}]

read_only = True

api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)

