# Make sure you replace the API and/or APP key below
# with the ones for your account

from datadog import initialize, api
import json
import pprint

options = {
    'api_key': '3dd19598055ebd8d75813ed9cbf35a4a',
    'app_key': '1c28de1f5de3719b85c5789d1dd34ca360fe88c8'
}

initialize(**options)

title = "Example Timeboard"
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
    "name": "ubuntu",
    "prefix": "host",
    "default": "host:ubuntu"
}]

read_only = True

response = api.Timeboard.create(title=title, description=description, graphs=graphs, template_variables=template_variables, read_only=read_only)
pprint.pprint(response)