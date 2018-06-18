from datadog import initialize, api

options = {
    'api_key': '5032023d686e6bd9b5e0b376a59bb27f',
    'app_key': '94846c5a071f7c2dc77381214fed18614987250a'
}

initialize(**options)


# Create a new Timeboard
title = "Show my_metric"
description = "For the home challenge"
graphs = [{
    "definition": {
        "events": [],
        "viz": "timeseries",
        "requests": [
            {"q": "my_metric{host:deep-learning-virtual-machine}",
            "type": "line",
            "style": {
                "palette": "dog_classic",
                "type": "solid",
                "width": "normal"},
            "conditional_formats": [],
            "aggregator": "avg"
            },
            {"q": "sum:my_metric{host:deep-learning-virtual-machine}.rollup(sum, 3600)",
            "type": "line",
            "style": {
                "palette": "orange",
                "type": "solid",
                "width": "normal"}
            }
        ],
    },
    "title": "My Metric (custom metric)"
}]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:my-host"
}]

read_only = True

try:
    api.Timeboard.create(title=title,
                            description=description,
                            graphs=graphs,
                            template_variables=template_variables,
                            read_only=read_only)
except:
    print 'Error occurred!'
else:
    print 'Sent API request successfully.'
 
