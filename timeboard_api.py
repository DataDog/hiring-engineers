from datadog import initialize, api

options = {
    'api_key': '0f5e12b6cad2c2377d8daca88f80cadd',
    'app_key': 'a2274c35675c0adcb35b7375c4700f6dc79b8c24'
}

initialize(**options)

title = "Timeboard - API Method"
widgets = [
    {
        'definition': {
            'type': 'timeseries',
            'requests': [{'q': 'avg:my_metric{host:dd-hiring}'}],
            'title': 'my_metric from dd-hiring host; api method'
        }
    },
    {
        'definition': {
            'type': 'timeseries',
            'requests': [{'q': "anomalies(  avg:postgresql.rows_inserted{host:dd-hiring}, 'basic', 2)"}],
            'title': 'postgres rows inserted anomalies from dd-hiring host; api method'
        }
    },
    {
        'definition': {
            'type': 'query_value',
            'requests': [{'q': 'avg:my_metric{host:dd-hiring}.rollup(sum, 3600)'}],
            'title': 'rolling hour sum of my_metric (rollup); api method'
        }
    }
]

layout_type = 'ordered'
description = 'dashboard for dd-hiring process'
is_read_only = True
notify_list = ['sjcip@umich.edu']
template_variables = [{
    'name': 'timeboard - api method'
}]

output = api.Dashboard.create(title=title,
                     widgets=widgets,
                     layout_type=layout_type,
                     description=description,
                     is_read_only=is_read_only,
                     notify_list=notify_list,
                     template_variables=template_variables)

print(output)
