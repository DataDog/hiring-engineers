from datadog import initialize, api
import json

options = {
    'api_key': 'xxx',
    'app_key': 'xxx',
    'api_host': 'https://api.datadoghq.eu'
}

try:
    initialize(**options)

    title = 'War Room Dashboard'
    widgets = [{
        'definition': {
            'type': 'timeseries',
            'requests': [
                {'q': 'avg:my_metric{host:ddx-nginx}'}
            ],
            'title': 'My Custom Metric Timeline'
            }
        },
        {
        'definition': {
            'type': 'timeseries',
            'requests': [
                {'q': "anomalies(avg:system.load.1{*}, 'basic', 2)"}
            ],
            'title': 'PSQL System Load'
            }
        },
        {
        'definition': {
            'type': 'timeseries',
            'requests': [
                {'q': 'avg:my_metric{*}.rollup(sum, 3600)'}
            ],
            'title': 'My Custom Metric Rolled Up Every Hour'
            }
        }]
    layout_type = 'ordered'
    description = 'A War Room Dashboard To Visualize KPIs'
    is_read_only = True
    notify_list = ['fermelone@gmail.com']

    response = api.Dashboard.create(title=title,
                        widgets=widgets,
                        layout_type=layout_type,
                        description=description,
                        is_read_only=is_read_only,
                        notify_list=notify_list)

    if len(response) > 1:
        print('Dashboard: ' + response['title'] + ' has been successfully created')
    else:
        print('There was a problem creating the dashboard specified, please check the dashboard configuration')
except:
    print('There was a problem creating the dashboard specified, please check your API configuration')
