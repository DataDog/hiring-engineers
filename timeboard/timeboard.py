from datadog import initialize, api

options = {
    'api_key': '75cc324da0bc265b8883ce646853b814',
    'app_key': '90010fe90c75c6ba58575f40fe0b5831b2db00fd'
}

initialize(**options)

title = 'My API Created Dashboard'
widgets = [{
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'avg:system.mem.free{*}'}
        ],
        'title': 'Average Memory Free'
    }
}]
layout_type = 'ordered'
description = 'A dashboard with memory info.'
is_read_only = True
notify_list = ['tomolry@optonline.net']
template_variables = [{
    'name': 'datadog1',
    'prefix': 'test',
    'default': 'datadog1'
}]

saved_view = [{
    'name': 'Saved views for hostname 2',
    'template_variables': [{'name': 'host', 'value': 'datadog1'}]}
]

api.Dashboard.create(title=title,
                     widgets=widgets,
                     layout_type=layout_type,
                     description=description,
                     is_read_only=is_read_only,
                     notify_list=notify_list,
                     template_variables=template_variables,
                     template_variable_presets=saved_views)
