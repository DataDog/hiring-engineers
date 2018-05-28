from datadog import initialize, api

options = {
    'api_key': '5032023d686e6bd9b5e0b376a59bb27f',
    'app_key': '94846c5a071f7c2dc77381214fed18614987250a'
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
