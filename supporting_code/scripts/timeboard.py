from datadog import initialize, api

options = {
'api_key': '<api_key>',
'app_key': '<app_key>'
}
initialize(**options)

title = "my_metric Timeboard"
widgets = [
    {
        'definition': {
            'type': 'timeseries',
            'requests': [{'q': 'avg:my_metric{host:michelle_vm}'}],
            'title': 'michelle_vm my_metric'
        }
    },
    {
        'definition': {
            'type': 'timeseries',
            'requests': [{'q':"anomalies(avg:mysql.performance.cpu_time{*},'basic',2)"}],
            'title': 'michelle_vm mySQL cpu_time Anomalies'
        }
    },
    {
        'definition': {
            'type': 'query_value',
            # 'Tumble window' rollup of my_metric sum every 5 minutes (60s * 5min)
            'requests': [{'q': 'avg:my_metric{host:michelle_vm}.rollup(sum, 300)'}],
            'title': 'Rolling 5 Minute Sum of my_metric'
        }
    }
]

layout_type = 'ordered'
description = 'Visualizing Data: Utilize the Datadog API to create a Timeboard'
is_read_only = True
notify_list = ['mbray1013@gmail.com']
template_variables = [{
    'name': 'my_metric Timeboard'
}]


api.Dashboard.create(title=title,
                 widgets=widgets,
                 layout_type=layout_type,
                 description=description,
                 is_read_only=is_read_only,
                 notify_list=notify_list,
                 template_variables=template_variables)