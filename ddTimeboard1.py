from datadog import initialize, api

options = {
    'api_key': 'xxxxx',
    'app_key': 'xxxxx'
}

initialize(**options)

title = "My Timeboard"
description = "Created Timeboard by Datadog API"
graphs = [{
    "definition": {
        "requests": [
            {
                "q": "avg:my_metric{host:ubu-dd1}",
                "type": "line",
                "style": {
                    "palette": "dog_classic",
                    "type": "solid",
                    "width": "normal"
                }
            }
        ],
        "yaxis": {
            "max": "auto",
            "scale": "linear",
            "min": "auto",
            "label": "",
            "includeZero": "true"
        },
        "markers": [],
        "viz": "timeseries"
    },
    "title": "my_metric: ubu-dd1"
},{
    "definition": {
        "requests": [
            {
                "q": "anomalies(avg:mysql.performance.cpu_time{*}, 'basic', 2)",
                "type": "line",
                "style": {
                    "palette": "dog_classic",
                    "type": "solid",
                    "width": "normal"
                }
            }
        ],
        "yaxis": {
            "max": "auto",
            "scale": "linear",
            "min": "auto",
            "label": "",
            "includeZero": "true"
        },
        "markers": [],
        "viz": "timeseries"
    },
    "title": "CPU Average Time"
},{
    "definition": {
        "requests": [
            {
                "q": "avg:my_metric{host:ubu-dd1}.rollup(sum, 3600)",
                "type": "bars",
                "style": {
                    "palette": "dog_classic",
                    "type": "solid",
                    "width": "normal"
                },
                "on_right_yaxis": "false"
            }
        ],
        "yaxis": {
            "max": "auto",
            "scale": "linear",
            "min": "auto",
            "label": "",
            "includeZero": "true"
        },
        "markers": [],
        "viz": "timeseries"
    },
    "title": "me_metric RoolUp 1 Hour"
}]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:ubu-dd1"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)
