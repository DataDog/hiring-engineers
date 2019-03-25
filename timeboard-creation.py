from datadog import initialize, api

options = {
    'api_key': '#######################', # removed to be safe
    'app_key': '#########################' #removed to be safe
}

initialize(**options)

title = 'Challange Dashboard'
widgets = [
    {"definition": {
      "type": "timeseries",
      "requests": [
        {"q": "avg:my_metric{host:data-dog-test}"}
      ],
      "title": "My_Metric Info"
    }},
    {"definition": {
      "type": "timeseries",
      "requests": [
        {"q": "anomalies(avg:mysql.performance.cpu_time{*}, 'basic', 2)"}
      ],
      "title": "Anomaly graph for mysql performance cpu"
    }},
    {"definition": {
      "type": "timeseries",
      "requests": [
        {"q": "avg:my_metric{host:data-dog-test}.rollup(sum, 3600)"}
      ],
      "title": "My_Metric rollup sum Info"
    }}
   ]
layout_type = 'ordered'
description = '.'
is_read_only = True
notify_list = ['shterrel@gmail.com']
template_variables = [{
    'name': 'datadog-test',
    'prefix': 'host',
    'default': 'data-dog-test'
}]
api.Dashboard.create(title=title,
                     widgets=widgets,
                     layout_type=layout_type,
                     description=description,
                     is_read_only=is_read_only,
                     notify_list=notify_list,
                     template_variables=template_variables)
