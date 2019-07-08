from datadog import initialize, api

options = {
    'api_key': '329e0c344a47864d92ae0342f3797b3b',
    'app_key': 'a57a258b956ff7a5486da53dcb2c92c6e0926867'
}

initialize(**options)

title = "Hiring Engineer Timeboard"
description = "An informative timeboard."
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{host:datadog.foogaro.com}"}
        ],
        "viz": "timeseries"
    },
    "title": "Avg of my_metric over host:datadog.foogaro.com"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{host:datadog.foogaro.com}.rollup(sum, 3600)"}
        ],
        "viz": "query_value"
    },
    "title": "custom metric with the rollup function applied, 1 hour"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:mysql.net.connections{host:datadog.foogaro.com}, 'basic', 2)"}
        ],
        "viz": "timeseries"
    },
    "title": "Avg of mysql.net.connections, with anomaly detection applied"
}]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:879843aa76e1"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)
