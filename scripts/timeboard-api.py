from datadog import initialize, api

options = {
    'api_key': "api_key",
    'app_key': "app_key"
}

initialize(**options)

my_metrics_graph = {
    "title": "My_Metric Stats",
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{*}"}
        ],
        "viz": "timeseries"
    }
}
mysql_cpu_anomaly_graph = {
    "title": "MySQL CPU Anomaly Detection",
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:mysql.performance.cpu_time{*}, 'basic', 2)"}
        ],
        "viz": "timeseries"
    }
}

my_metric_rollup_graph = {
    "title": "My_Metric Rollup Over The Past 1Hr",
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{*}.rollup(sum, 3600)"}
        ],
        "viz": "query_value"
    }
}

title       = "MyDashboard"
description = "A dashboard for the Datadog assessment"
graphs      = []

graphs.append(my_metrics_graph)
graphs.append(mysql_cpu_anomaly_graph)
graphs.append(my_metric_rollup_graph)

template_variables = [{
    "name": "Datadog Engineer",
    "prefix": "host",
    "default": "host:ubuntu-xenial"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)
