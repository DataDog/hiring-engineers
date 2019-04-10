from datadog import initialize, api

options = {
  'api_key': '<<>>',
  'app_key': '<<>>'
}

initialize( ** options)

title = 'Hiring Challenge Timeboard'
widgets = [{
    'definition': {
      'type': 'timeseries',
      'requests': [{
        "q": "avg:my_metric{host:ubuntu-xenial}"
      }],
      'title': 'Random number metric over host'
    }
  },
  {
    'definition': {
      'type': 'timeseries',
      'requests': [{
        "q": "anomalies(avg:postgresql.bgwriter.checkpoints_timed{host:ubuntu-xenial}, 'basic', 6)"

      }],
      'title': 'Anamloy detection on checkpoints timed in postgresql'
    }
  },
  {
    'definition': {
      'type': 'query_value',
      'requests': [{
        "q": "sum:my_metric{host:ubuntu-xenial}.rollup(sum, 3600)"
      }],
      'title': 'Random number metric rollup over last 1 hour'
    }
  }
]
layout_type = 'ordered'
description = 'Hiring challenge dashboard showcasing different metrics.'
is_read_only = True
notify_list = ['user@domain.com']
template_variables = [{
  'name': 'host1',
  'prefix': 'host',
  'default': 'ubuntu-xenial'
}]
api.Dashboard.create(title = title,
  widgets = widgets,
  layout_type = layout_type,
  description = description,
  is_read_only = is_read_only,
  notify_list = notify_list,
  template_variables = template_variables)
