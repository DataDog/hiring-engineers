from datadog import initialize, api

options = {
    'api_key': '20dde7d1083c242f37c7583ea9ff7db6',
    'app_key': '537238d4599621b66bd0dacc4a6dfe2f4c182261'
}

initialize(**options)

title = "My Timeboard"
description = "An informative timeboard."

graphs = [
{
    "definition": {
        "events": [],
        "requests": [{"q": "avg:my_metric{admin:harry,host:training.localdomain}"}],
        "viz": "timeseries"
    },
    "title": "custom metric scoped over your host"
},
{
    "definition": {
        "events": [],
        "requests": [{"q": "anomalies(avg:mysql.innodb.buffer_pool_free{*}, 'basic', 2)"}],
        "viz": "timeseries"
    },
    "title": "Any metric from the Integration on your Database with the anomaly function applied"
},
{
    "definition": {
        "events": [],
        "requests": [{"q": "avg:my_metric{admin:harry,host:training.localdomain}.rollup(sum,3600)"}],
        "viz": "timeseries"
    },
    "title": "Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket"
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
#                     template_variables=template_variables,
                     read_only=read_only)