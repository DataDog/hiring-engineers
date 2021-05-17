from datadog import initialize, api

options = {
    'api_key': DATADOG_API_KEY,
    'app_key': DATADOG_APP_KEY
}

initialize(**options)

title = "Hiring Project Timeboard"
description = "Custom metrics over host. This timeseries table was created using the Datadog API."
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q":"max:my_metric{host:vagrant}","type":"line"}
            ],
        "viz": "timeseries"
    },
    "title": "Custom Metric over Host"
}]

template_variables = [{
    "name": "vagrant",
    "prefix": "host",
    "default": "host:my-host"
}]

read_only = False
results = api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)


print(results)