from datadog import initialize, api

options = {
    "api_key": "DD_API_KEY",
    "app_key": "DD_APP_KEY"
}

initialize(**options)

def CreateDashboard():
    title = 'Dashboard example for exercise'
    widgets = [
        {'definition': {
            'type': 'timeseries',
            'requests': [
                {
                    'q': 'avg:my_metric{host:i-0034421f8056d59b6}'
                },
                {
                    'q': 'avg:my_metric{*}.rollup(sum, 3600)'
                },
                {
                    'q': 'anomalies(avg:mysql.performance.cpu_time{*}, "basic", 2)'
                }
            ],
            'title': 'my_metric & MySQL CPU Time'
            }
        }
    ]
    layout_type = 'ordered'
    description = 'A dashboard for Solutions Engineer exercise.'

    response = api.Dashboard.create(title=title, widgets=widgets, layout_type=layout_type, description=description)

    return response


result = CreateDashboard()

print('You just created your dashboard, and you can see it at https://app.datadoghq.com{0}'.format(result['url']))

