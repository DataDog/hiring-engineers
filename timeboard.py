from datadog import initialize, api

options = {
    'api_key': '1852b8c40afd989d5e512340f1a0d3c8',
    'app_key': 'e5c3500cf4db158a732810c309ecda679675f00e'
}

initialize(**options)

title = "Random_Timeboard"
description = "A timeboard tracking random numbers."

graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{*}"}
        ],
        "viz": "timeseries"
    },
    "title": "random metric number over time"
}, {
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:postgresql.database_size{role:database:postgres}, 'basic',3)"
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
