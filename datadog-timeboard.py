from datadog import initialize, api

options = {
    'api_key': 'cf5ac1d6ae09bc0d3797f8705657545c',
    'app_key': 'd99012671b8fc96f247a09e82da2b46664a8880d'
}

initialize(**options)

title = 'Solutions Engineer Demo Timeboard'
widgets = [{
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'my_metric{host:vagrant}'}
        ],
        'title': 'my_metric on host:vagrant'
    }
}, {
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'anomalies(postgresql.percent_usage_connections{host:vagrant}, "basic", 2)'}
        ],
        'title': 'anomaly detection on postgres percent usage (connections) on host:vagrant'
    }
}, {
    'definition': {
        'type': 'query_value',
        'requests': [
            {'q': 'my_metric{*}.rollup(sum, 3600)'}
        ],
        'title': 'aggregate my_metric on all hosts over T-60 min',
        'precision': 0
    }
}]
layout_type = 'ordered'
description = 'Hooray this is a demo description'
is_read_only = True

api.Dashboard.create(title=title,
                     widgets=widgets,
                     layout_type=layout_type,
                     description=description,
                     is_read_only=is_read_only)
