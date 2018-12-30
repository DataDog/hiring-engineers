from datadog import initialize, api

options = {
    'api_key': '610080f148d9e4d47efed7c611e64d7d',
    'app_key': '740f642b84485d07b4282373ccb16f75f13664ae'
}

initialize(**options)

title = "Dipankar Barua Time Board"
description = "An informative timeboard."
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:system.mem.free{*}"}
        ],
        "viz": "timeseries"
    },
    "title": "Average Memory Free"
}]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:my-host"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)