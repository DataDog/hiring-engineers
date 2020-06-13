from datadog import initialize, api

options = {
    'api_key': 'XXXXXXXXX',
    'app_key': 'XXXXXXXXX'
}

initialize(**options)

title = 'Jeremy\'s Timeboard'
widgets = [{
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'avg:my_metric{host:kalachakra.local}'}
        ],
        'title': 'Average of my_metric'
    }
},
    {
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': "anomalies(avg:mysql.performance.open_files{*},'basic',2)"}
        ],
        'title': 'Anomalies in MySQL open files'
    }
},
    {
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'sum:my_metric{host:kalachakra.local}.rollup(sum,60)'}
        ],
        'title': 'Roll up sum of my_metric'
    }
}]

layout_type = 'ordered'
description = 'Awesome Dashboard'
is_read_only = True
notify_list = ['jeremy.daggett@gmail.com']

api.Dashboard.create(title=title,
                     widgets=widgets,
                     layout_type=layout_type,
                     description=description,
                     is_read_only=is_read_only,
                     notify_list=notify_list)
