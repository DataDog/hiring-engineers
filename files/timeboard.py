from datadog import initialize, api

options = {
    'api_key': '651ea7b72011ccd54f640d26830aeb3f',
    'app_key': '2db99acf33d1e8f8d283aea29199408c237b5b35'
}

initialize(**options)

title = "Stevie's Timeboard"
description = "3rd time's the charm timeboard."
graphs = [{
        "definition": {
            "events": [],
            "requests": [
                {"q": "avg:my_metric{host:ubuntu-xenial}"}
            ],
            "viz": "timeseries"
        },
        "title": "My Metric Scoped & Aggregated"
    },
    {
        "definition": {
            "events": [],
            "requests": [
                {"q": "anomalies(avg:postgresql.max_connections{host:ubuntu-xenial}, 'basic', 2)"}
            ],
            "viz": "timeseries"
        },
        "title": "PostgreSQL Connections Anomaly"
    },
    {
        "definition": {
            "events": [],
            "requests": [
                {"q": "avg:my_metric{host:ubuntu-xenial}.rollup(sum, 3600)"}
            ],
            "viz": "timeseries"
        },
        "title": "My Metric Rollup"
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
