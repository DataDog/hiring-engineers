from datadog import initialize, api

options = {
    'api_key': '2a0708e9834bae3406d529ff17eed087',
    'app_key': 'e61919868778dfa9a4f26fab673aeefdc1e48402'
}
# app_key - testkey - e61919868778dfa9a4f26fab673aeefdc1e48402
# api_key: 2a0708e9834bae3406d529ff17eed087
initialize(**options)

title = "My Timeboard Test 1"
description = "Anomaly Detection Graphs on a Timeboard"
graphs = [
{
# graph 1 - custom metric summed up
    "definition": {
        "events": [],
         "requests": [
            {
            "q": "sum:customtest.my_metric{host:datadogtest} by {env}",
            "style": {
                "palette": "dog_classic",
                "type": "solid",
                "width": "normal"
            },
            "conditional_formats": [
                {
                "palette": "white_on_green",
                "comparator": ">",
                "value": "1000"
                },
                {
                "palette": "white_on_red",
                "comparator": "<=",
                "value": "1000"
                }
            ],
            "aggregator": "sum"
        }
    ],
    "viz": "query_value"
    },
    "title": "Custom Metric is Growing"
},
{
    # graph 2 - custom metric timeseries
    "definition": {
        "events": [],
        "requests": [
            {
                "q": "avg:customtest.my_metric{datadogtest}",
                "type": "line",
                "style": {
                "palette": "dog_classic",
                "type": "solid",
                "width": "normal"
            },
            "conditional_formats": [],
            "aggregator": "avg"
            }
        ],
        "viz": "timeseries"
    },
    "title": "Custom Metric Over Time"
},
{
    # graph 3 - anomaly detection
    "definition": {
        "events": [],
        "requests": [
        {
            "q": "anomalies(avg:mysql.performance.user_time{datadogtest}, 'basic', 3)",
            "type": "line",
            "style": {
                "palette": "dog_classic",
                "type": "solid",
                "width": "normal"
            },
            "conditional_formats": [],
            "aggregator": "avg"
        }
        ],
        "viz": "timeseries"
    },
    "title": "Anomalies of MySQL performance"
}]

template_variables = [{
    "name": "datadogtest",
    "prefix": "host",
    "default": "host:datadogtest"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)
