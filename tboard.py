from datadog import initialize, api

options = {
    'api_key': 'e05c62b16283be76411fc383d55eecba',
    'app_key': 'a9e09d8a7e25a602b6b5f059924f354643220fdf'
}

initialize(**options)

title = "Michael's Timeboard"
description = "Final Timeboard"
graphs = [
{    # Graph of my_metric
    "definition": {
        "events": [],
        "requests": [
            {"q": "my_metric{host:ubuntuyhivi}"},
        ],
        "viz": "timeseries"
    },
    "title": "my_metric"
}, 
{   # Query value of sum of my_metric past 1 hr
    "definition": {
        "events": [],
        "requests": [
            {
                "q": "sum:my_metric{*}.rollup(sum, 3600)",
                "type": None,
                "style": {
                  "palette": "dog_classic",
                  "type": "solid",
                  "width": "normal"
                },
                "conditional_formats": [],
                "aggregator": "sum"
            }
        ],
        "viz": "query_value",
        "autoscale": True
    },
    "title": "Rollup - Sum of my_metric past hr"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     read_only=read_only)
