from datadog import initialize, api
import os

options = {
    'api_key': os.getenv('DD_API_KEY') ,
    'app_key': os.getenv('DD_APP_KEY'),
    'api_host': "https://api.{}".format(os.getenv('DD_SITE'))
}

initialize(**options)

title = 'Data Wizard Visualisation - Via API - With Docker--'
widgets = [
    {
      'definition': {
        'type': 'timeseries',
        'requests': [
          {
            'q': 'avg:random.my_metric{*}',
            'display_type': 'line',
            'style': {
              'palette': 'dog_classic',
              'line_type': 'solid',
              'line_width': 'normal'
            }
          }
        ],
        'yaxis': {
          'label': '',
          'scale': 'linear',
          'min': 'auto',
          'max': 'auto',
          'include_zero': True
        },
        'markers': [
          {
            'value': '0 < y < 300',
            'display_type': 'warning dashed',
            'label': ' Up to 300 (We are below) '
          },
          {
            'value': '301 < y < 800',
            'display_type': 'ok dashed',
            'label': ' 300 - 800 (We good) '
          },
          {
            'value': '801 < y < 1000',
            'display_type': 'error dashed',
            'label': ' Above 800 (Panic!) '
          }
        ],
        'title': 'Avg. My Random Metric - SLA',
        'show_legend': False,
        'legend_size': '0'
      }
    },
    {
      'definition': {
        'type': 'timeseries',
        'requests': [
          {
            'q': 'anomalies(avg:postgresql.rows_fetched{*}, "basic", 2)',
            'display_type': 'line',
            'style': {
              'palette': 'dog_classic',
              'line_type': 'solid',
              'line_width': 'normal'
            }
          }
        ],
        'yaxis': {
          'label': '',
          'scale': 'linear',
          'min': 'auto',
          'max': 'auto',
          'include_zero': True
        },
        'title': 'Django Postgres Dbz (Fetched Rows)',
        'time': {},
        'show_legend': False
      }
    },
    {
      'definition': {
        'type': 'timeseries',
        'requests': [
          {
            'q': 'avg:random.my_metric{*}.rollup(sum, 3600)',
            'display_type': 'line',
            'style': {
              'palette': 'dog_classic',
              'line_type': 'solid',
              'line_width': 'normal'
            }
          }
        ],
        'yaxis': {
          'label': '',
          'scale': 'linear',
          'min': 'auto',
          'max': 'auto',
          'include_zero': True
        },
        'title': 'My Random Metric (Rollups over 1 Hour)',
        'show_legend': False,
        'legend_size': '0'
      }
    },
    {
      'definition': {
        'type': 'timeseries',
        'requests': [
          {
            'q': 'avg:system.cpu.user{*}, avg:system.cpu.user{*}*1000',
            'display_type': 'bars',
            'style': {
              'palette': 'dog_classic',
              'line_type': 'solid',
              'line_width': 'normal'
            }
          },
          {
            'q': 'avg:random.my_metric{*}',
            'display_type': 'line',
            'style': {
              'palette': 'dog_classic',
              'line_type': 'solid',
              'line_width': 'normal'
            }
          }
        ]
      }
    }
  ]

layout_type = 'ordered'
description = "## Data Wizard Visualisation\n\nA simple yet useful dashboard to show our Random Metric SLA, and the time series value scooped over our CUP"
is_read_only = True
notify_list = []
template_variables = []

results = api.Dashboard.create(title=title,
                     widgets=widgets,
                     layout_type=layout_type,
                     description=description,
                     is_read_only=is_read_only,
                     notify_list=notify_list,
                     template_variables=template_variables)

print(results)
