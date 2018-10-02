from datadog import initialize, api

options = {
    'api_key': '02f734414a40cee6e9861fa0cee0fb3a',
    'app_key': '04a248ce38eeb00900e4528122c6e337e4468e0a'
}

initialize(**options)

title = "My Timeboard"
description = "An informative timeboard."
graphs = [
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "my_metric{*}"}
        ],
        "viz": "timeseries"
    },
    "title": "Custom metric"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "my_metric{*}.rollup(sum,3600)"}
        ],
        "viz": "timeseries"
    },
    "title": "custom metric rollup"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:postgresql.percent_usage_connections{*}, 'basic', 2)"}
        ],
        "viz": "timeseries"
    },
    "title": "anomalies postgresql connections percentage"
}
]

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

