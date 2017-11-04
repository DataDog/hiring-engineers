from datadog import initialize, api
import time

options = {
    'api_key': 'ff94d89120c8d3e70c3d48b8143dc7d2',
    'app_key': 'd297d103eff1681b71d019d813bb3da5e7e4c8c0'
}

initialize(**options)

title = 'Emma''s Timeboard 3 Nov 2017 00:08'
description = 'Graphing my_metric and a database metric'
graphs = [{
    'definition': {
        'events': [],
        'requests': [
            {'q': 'avg:my_metric{host:emma-VirtualBox}'}
        ],
        'viz': 'timeseries'
    },
    'title': 'My_Metric Over Host'
},
{
    'definition': {
        'events': [],
        'requests': [
            {'q': 'avg:my_metric{host:emma-VirtualBox}.rollup(sum, 3600)'}
        ],
        'viz': 'timeseries'
    },
    'title': 'My_Metric Hourly Rollup'
},{
    'definition': {
        'events': [],
        'requests': [
            {'q': "anomalies(avg:postgresql.rows_fetched{db:test_db}, 'basic', 2)"}
        ],
        'viz': 'timeseries'
    },
    'title': 'Avg of postgresql.rows_fetched over db:test_db'
}]

read_only= True

print api.Timeboard.create(4952, title=title, description=description, graphs=graphs, read_only=read_only)
