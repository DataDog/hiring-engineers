import argparse
import requests
import json
from datadog import initialize, api

parser = argparse.ArgumentParser()
parser.add_argument('--api-key', required=True, help='Your Datadog API key')
parser.add_argument('--app-key', required=True, help='Your Datadog App key')

if __name__ == '__main__':
    args = parser.parse_args()

    initialize(api_key=args.api_key, app_key=args.app_key)

    result = api.Dashboard.create(
        title='Visualizing Data Demo',
        description='Visualizes Postgres anonmalies and all randomly generated metrics in the `chaos` event prefix '
        'submitted by the `chaos_machine` host.',
        is_read_only=True,
        layout_type='ordered',
        widgets=[
            {
                'definition': {
                    'type': 'group',
                    'layout_type': 'ordered',
                    'title': 'My Metric',
                    'widgets': [
                        {
                            'definition': {
                                'type': 'timeseries',
                                'title': 'Value over time',
                                'requests': [{
                                    'q': 'avg:chaos.my_metric{host:chaos-engine}',
                                    'display_type': 'line',
                                    'style': {
                                        'palette': 'classic',
                                        'line_type': 'solid',
                                        'line_width': 'normal'
                                    }
                                }],
                                'yaxis': {
                                    'scale': 'linear',
                                    'min': '0',
                                    'max': '1000',
                                    'include_zero': True
                                },
                                'markers': [{
                                    'value': '0 <= y < 500',
                                    'display_type': 'ok solid',
                                    'label': 'ACCEPTABLE'
                                }, {
                                    'value': '500 < y < 800',
                                    'display_type': 'warning solid',
                                    'label': 'A BIT TOO MUCH METRIC'
                                }, {
                                    'value': 'y >= 800',
                                    'display_type': 'error solid',
                                    'label': "WE CAN'T HANDLE THE TRUTH"
                                }]
                            }
                        },
                        {
                            'definition': {
                                'type': 'timeseries',
                                'title': 'Total value over time (1hr rollup)',
                                'requests': [{
                                    'q': 'avg:chaos.my_metric{host:chaos-engine}.rollup(sum, 3600)',
                                    'display_type': 'line',
                                    'style': {
                                        'palette': 'classic',
                                        'line_type': 'solid',
                                        'line_width': 'normal'
                                    }
                                }],
                                'yaxis': {
                                    'scale': 'linear',
                                    'min': 'auto',
                                    'max': 'auto',
                                    'include_zero': True
                                }
                            }
                        },
                        {
                            'definition': {
                                'type': 'query_value',
                                'title': 'Current Value',
                                'autoscale': True,
                                'precision': 0,
                                'text_align': 'center',
                                'requests': [{
                                    'q': 'avg:chaos.my_metric{host:chaos-engine}',
                                    'aggregator': 'last',
                                    'conditional_formats': [
                                        # Must be in descending order
                                        {
                                            'comparator': '>=',
                                            'value': 800,
                                            'palette': 'white_on_red'
                                        },
                                        {
                                            'comparator': '>=',
                                            'value': 500,
                                            'palette': 'white_on_yellow'
                                        },
                                        {
                                            'comparator': '>=',
                                            'value': 0,
                                            'palette': 'white_on_green'
                                        }
                                    ]
                                }],
                            }
                        }
                    ]
                }
            },
            {
                'definition': {
                    'type': 'group',
                    'layout_type': 'ordered',
                    'title': 'Postgres',
                    'widgets': [{
                        'definition': {
                            'type': 'timeseries',
                            'title': 'Write Latencies',
                            'requests': [{
                                'q':
                                    "anomalies(avg:postgresql.bgwriter.write_time{host:postgresql}.as_count(), 'basic', 1)",
                                'display_type': 'line',
                                'style': {
                                    'palette': 'classic',
                                    'line_type': 'solid',
                                    'line_width': 'normal'
                                }
                            }, {
                                'q':
                                    "anomalies(avg:postgresql.bgwriter.sync_time{host:postgresql}.as_count(), 'basic', 1)",
                                'display_type': 'line',
                                'style': {
                                    'palette': 'classic',
                                    'line_type': 'solid',
                                    'line_width': 'normal'
                                }
                            }],
                            'yaxis': {
                                'scale': 'linear',
                                'min': 'auto',
                                'max': 'auto',
                                'include_zero': True
                            }
                        }
                    }, {
                        'definition': {
                            'type': 'timeseries',
                            'title': 'Percent of Used Connections',
                            'requests': [{
                                'q': 'avg:postgresql.percent_usage_connections{host:postgresql}',
                                'style': {
                                    'palette': 'classic',
                                    'line_type': 'solid',
                                    'line_width': 'normal'
                                }
                            }],
                            'yaxis': {
                                'scale': 'linear',
                                'min': '0',
                                'max': '1',
                                'include_zero': True
                            }
                        }
                    }]
                }
            }
        ]
    )
    print(f'Success! https://app.datadoghq.com{result["url"]}\n')
    print('You can use the following json to to import the dashbaord into the GUI:\n')
    print(json.dumps(result, indent=4))
