from datadog import initialize, api

options = {
    'api_key': '0d3ec981a0ea90d5983c547fc3169ddf',
    'app_key': '9cf15dee3fa15d30e0421784a66336acaa271f41'
}
initialize(**options)

title = "My Challenge Timeboard22"
description = "A timeboard of randomness"
graphs = [
    {
    "definition": {
        "events": [],
        "requests": [
            {"q": "my_metric_value{host:ubuntu-xenial}"}
        ],
        "viz": "timeseries"
    },
    "title": "My metric scoped over my host"
    },
    {
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(mysql.innodb.data_reads{host:ubuntu-xenial}, 'basic', 2)"}
        ],
        "viz": "timeseries"
    },
    "title": "Anomaly rate of data reads in MySQL"
    },
    {
    "definition": {
        "events": [],
        "requests": [
            {"q": "my_metric_value{host:ubuntu-xenial}.rollup(sum,3600)"}
        ],
        "viz": "timeseries"
    },
    "title": "My metric summed over an hour"
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
