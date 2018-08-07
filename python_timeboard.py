from datadog import initialize, api
import urllib3.contrib.pyopenssl
urllib3.contrib.pyopenssl.inject_into_urllib3()

options = {
    'api_key': '38f76825eaed29ec3678e684a2bb3a31',
    'app_key': '1d53d458b2e725a30dc42cf61fce010d7868fcd5'
}

initialize(**options)

title = "My Timeboard test"
description = "Visualizing metrics"
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{env:my_ubuntu1}" }
        ],
        "viz": "timeseries"
    },
    "title": "Avg of my_metric scoped over host"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q":"avg:mysql.performance.queries{mytag_hiring_challenge} by {host}"}],
        "viz": "timeseries"
    },
    "title": "mysql.performance.queries metric with anomaly function applied"
},

{
    "definition": {
        "events": [],
        "requests": [
            {"q": "sum:my_metric{mytag_hiring_challenge}.rollup(sum, 3600)" }
        ],
        "viz": "timeseries"
    },
    "title": "my_metric with roll up sum of points of past hour in one hour bucket"
}]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:my-host"
}]

read_only = True

api.Monitor.create(
    type="metric alert",
    query="avg(last_4h):avg:mysql.performance.queries{mytag_hiring_challenge} > 0.5",
    name="Anomalous check for metric from database.",
    message="Anomaly function applied on metric from database.",
)

api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)


