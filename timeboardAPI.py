# Make sure you replace the API and/or APP key below
# with the ones for your account

from datadog import initialize, api

options = {
    'api_key': 'aaf2a348158cadcc3879184d80500418',
    'app_key': '759aa880aeb746f779317e7de7431157207a9b37'
}

initialize(**options)

title = "My Timeboard"
description = "An informative timeboard."
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "my_metric{*} by {host}"},
            {"q": "mongodb.network.numrequestsps{*}.anomaly()"},
            {"q": "my_metric{*}.rollup(avg, 300)"}
        ],
    "viz": "timeseries"
    },
    "title": "Metrics"
}]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:my-host"
}]

read_only = True

api.Timeboard.create(title=title, description=description, graphs=graphs, template_variables=template_variables, read_only=read_only)
