from datadog import initialize, api

options = {
    'api_key': '',
    'app_key': ''
}

initialize(**options)


# Create a new Screenboard
board_title = "Rollup Function"
description = "For the home challenge"
widgets = [{
    "type": "query_value",
    "height": 20,
    "width": 32,
    "y": 7,
    "x": 32,
    "aggregator": "sum",
    "query": "my_metric{*}.rollup(sum,3600)"
}]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:my-host"
}]

read_only = True

api.Screenboard.create(board_title=board_title,
                       description=description,
                       widgets=widgets,
                       template_variables=template_variables)
