from datadog import initialize, api

options = {
    "api_key": "0daa6e51915ecb5f4e82e8dbbe4a863a",
    "app_key": "9ba542ca4d23ed6fbdf522cd6e4de2ca0ee24dda"
}

initialize(**options)

title = "My Awesome Timeboard!"
description = "This is the best Timeboard ever created ;)"
graphs = [
    {
        "definition": {
            "events": [],
            "requests": [
                {"q": "avg:my_metric{*}"}
            ],
            "viz": "timeseries"
        },
        "title": "Value of my_metric!"},
    {
        "definition": {
            "events": [],
            "requests": [
                {"q": "avg:my_metric{*}.rollup(sum, 3600)"}
            ],
            "viz": "timeseries"
        },
        "title": "Value of my_metric with rollup(sum, 3600) function applied"},
    {
        "definition": {
            "events": [],
            "requests": [
                {"q": "anomalies(avg:postgresql.rows_fetched{*}, 'basic', 1.2)"}
            ],
            "viz": "timeseries"
        },
        "title": "Rows fetched from PostgreSQL DB"
    }]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:slazien-ThinkPad-W530"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)
