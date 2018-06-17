from datadog import initialize, api

options = {
    'api_key': '2efb60934301e2e78970e9d6cf48c0cb',
    'app_key': 'f192e131e61400bca9ef338a03a8654b6c3146f7'
}

initialize(**options)

title = "MongoDB Metric"
description = "MongoDB metric"
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:mongodb.stats.collections{*}, 'basic', 2)"}
        ],
        "viz": "timeseries"
    },
    "title": "Mongodb stats collection"
}]

template_variables = [{
    "name": "timeboard",
    "prefix": "mongodbMetric",
    "default": "host:datadogvm-windows"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)