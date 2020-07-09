from datadog import initialize, api

options = {
    'api_key': '55d71c56f9c021fdd2ab49f3b42b62c7',
    'app_key': 'fb2b02b7a1248c9e6f450ce226721c2f87238ef6'
}

initialize(**options)

title = 'Jackie Timeboard via the API'
widgets = [{
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'my_metric{host:vagrant}'}
        ],
        'title': 'Time series tracking my_metric on host:vagrant'
    }
}, {
'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'anomalies(mysql.performance.kernel_time{host:vagrant}, "basic", 2)'}
        ],
        'title': 'anomaly detection on the percentage of CPU time spent in kernel space by MySQL on host:vagrant'
    }
}, {
    'definition': {
        'type': 'query_value',
        'requests': [
            {'q': 'my_metric{*}.rollup(sum, 3600)'}
        ],
        'title': 'A rollup sum of all my_metric values for the past hour',
        'precision': 0
    }
}]
layout_type = 'ordered'
description = 'This is a great timeseries dashboard!'
is_read_only = True


api.Dashboard.create(title=title,
                     widgets=widgets,
                     layout_type=layout_type,
                     description=description,
                     is_read_only=is_read_only)