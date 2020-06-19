from datadog import initialize, api
import pprint

options = {
    'api_key': 'd7afa42139e5f46b428466e4e935f8b5',
    'app_key': '43d17872e83a15abc8196ded43689d73c4a49bb7',
    'api_host': 'https://api.datadoghq.eu'
}

initialize(**options)


title = 'Steves Dashboard created by API number 5'
widgets = [{
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'avg:my_metric.gauge{host:vagrant}'}
        ],
        'title': 'Avg of my_metric.gauge over host:vagrant'
    }
},
{
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': "anomalies(avg:mysql.performance.user_time{host:vagrant}, 'basic', 2)"}
        ],
        'title': 'Avg of mysql.performance.user_time over host:vagrant with Basic Anomaly detection'
    }
},
{
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'sum:my_metric.gauge{host:vagrant}.rollup(sum,3600)',
                'display_type': 'bars'}
        ],
        'title': 'Rolled up sum of my_metric.gauge over host:vagrant'
    }
},
]
layout_type = 'ordered'
description = 'A dashboard created via API.'

result=api.Dashboard.create(title=title,
                     widgets=widgets,
                     layout_type=layout_type,
                     description=description)


pprint.pprint(result)

