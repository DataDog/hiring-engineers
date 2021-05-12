from datadog import initialize, api

options = {
    'api_key': '<MY_API_KEY>',
    'app_key': '<MY_APP_KEY>'
    }

initialize(**options)

title = 'My Metric - Timeboard 2'
description = 'An informative timeboard'
graphs = [{'definition': {'events': [],
                          'requests': [{
                            'q': 'avg:eoins_metric.gauge{*} by {host}'}],
                          'viz': 'timeseries'},
          'title': 'My_metric By Host'},
          {'definition': {'events': [],
              'requests': [{
                  'q': 'avg:eoins_metric.gauge{*}.rollup(sum, 3600)'}],
              'viz': 'timeseries'},
              'title': 'Rollup Function by Hour applied to my_metric'}]


template_variables = [{'name': 'vagrant_1', 'prefix': 'host',
                       'default': 'host:my-host'}]
read_only = False

res=api.Timeboard.update(
    id='9j9-t8k-f3e',
    title=title,
    description=description,
    graphs=graphs,
    template_variables=template_variables,
    read_only=read_only,
)

print(res)
