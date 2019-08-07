from datadog import initialize, api

options = {
        'api_key': '8661becd6d0b8a1ca58cf10bcdc5daf5',
        'app_key': '3c0afd9ba4e06d356e47d481ebb6d0c58e59ac3f'
}

initialize(**options)

title = 'My TimeBoard'
widgets = [{
        'definition': {
                'type': 'timeseries',
                'requests': [
                    {'q': 'avg:rdata.my_metric{*}'}
              ],
              'title': 'My Custom Metric Graph'
    }
},
{       'definition': {
                'type': 'timeseries',
                'requests': [
                    {"q": "anomalies(avg:mysql.performance.cpu_time{*}, 'basic', 2)"}
              ],
              'title': 'MySQL with Anomalies Graph'
     }
},
{        "definition": {
                "type": "timeseries",
                "requests": [
                     {'q': 'rdata.my_metric{*}.rollup(sum,3600)'}
                ],
                "title": "My Custom Metric Roll-up Graph"
      }
}]
layout_type = 'ordered'
description = 'A dashboard with random data'
is_read_only = True
notify_list = ['sin.daryl@gmail.com']
template_variables = [{
    'name': 'host1',
    'prefix': 'host',
    'default': 'host1'
}]
api.Dashboard.create(title=title,
                     widgets=widgets,
                     layout_type=layout_type,
                     description=description,
                     is_read_only=is_read_only,
                     notify_list=notify_list,
                     template_variables=template_variables)
