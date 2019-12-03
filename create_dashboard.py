from datadog import initialize, api

options = {'api_key': 'f67113fe21437826d50f343b7e90ec6f',
           'app_key': 'e22273f49f471ddcbf85b6df6749cd4c886623b0',
           'api_host': 'https://api.datadoghq.eu'}

initialize(**options)

scope = 'host:dd-host-mysql'
title = 'API - My Dashboard'

widgets = [
  {
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'my_metric{'+scope+'}'}
        ],
        'title': 'My Custom Metric'
    }
  },
    {
    'definition': {
        'type': 'query_value',
        'requests': [
            {'q': 'my_metric{'+scope+'}.rollup(sum,3600)'}
        ],
        'autoscale': True,
        'title': 'My Custom Metric with Rollup'
    }
  },
  {
    'definition': {
         'type':'timeseries',
         'requests': [ 
               { 
                  'q':'anomalies(system.load.1{'+scope+'}, "basic", 2)'
               },
               { 
                  'q':'anomalies(system.load.5{'+scope+'}, "basic", 2)'
               },
               { 
                  'q':'anomalies(system.load.15{'+scope+'}, "basic", 2)'
               }
            ],
            'title':'MySQL System load',
            'show_legend': False,
            'legend_size': '0'
    }
  }
]
layout_type = 'ordered'
description = 'Dashboard created through API'
is_read_only = True
notify_list = ['gmendes.ferreira@gmail.com']
template_variables = []
print(api.Dashboard.create(title=title,
                     widgets=widgets,
                     layout_type=layout_type,
                     description=description,
                     is_read_only=is_read_only,
                     notify_list=notify_list,
                     template_variables=template_variables))