from datadog import initialize, api

# add authorization
options = {
    'api_key': '81a606ef523cf349697fc32eaa5ff3dc',
    'app_key': '3538dfbd5ffe0031a558083fbbe1c1acedacdc3d',
}

initialize(**options)

# Timeboard title
title = "Custom - Metrics"
description = "A demo timeboard with custom metric and postgres metric."

# Graph specifications
my_metric_avg = {
    "definition": {
        "requests": [
            {"q": "avg:my_metric{host:Dannis-MacBook-Air.local}"}
        ],
        "viz": "timeseries",
        "yaxis": {
            "min": "0",
            "max": "1000"
        }
    },
    "title": "my_metric_average"
}

my_metric_rollup = {
    "definition": {
        "requests": [{
            # query to apply the rollup function
            "q": "my_metric{host:Dannis-MacBook-Air.local}.rollup(sum,3600)",
            "style": {"palette": "purple"},
            "type": "bars"
        }],
        "viz": "timeseries",
    },
    "title": "my_metric_rollup"
}

postgres_rows_anomalies = {
    "definition": {
        "requests": [{
            # query to apply the anomalies function
            "q": "anomalies(avg:postgresql.rows_fetched{host:Dannis-MacBook-Air.local}, 'basic', 2)"
        }],
        "viz": "timeseries"
    },
    "title": "postgres_rows_fetched"
}

graphs = [my_metric_avg, my_metric_rollup, postgres_rows_anomalies]

template_variables = [{
    "name": "danni",
    "prefix": "host",
    "default": "host:danni"
}]

read_only = True

r = api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)

print(r)
