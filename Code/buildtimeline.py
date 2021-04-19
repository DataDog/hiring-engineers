import os
import yaml
import json
import requests


def get_settings(settings_file_name):
    try:
        class_file_path = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.split(class_file_path)[0]
        print(base_path)
        settings_file_path = os.path.join(base_path, 'timeBoardProject')
        settings_file = os.path.join(settings_file_path, settings_file_name)
        # print('settings_handler.py - get_settings - Path to settings: ' + settings_file)
        with open(settings_file, 'r') as settings_file:
            settings = yaml.load(settings_file, Loader=yaml.FullLoader)
    except IOError as error:
        print('Got an IO Error: ' + error.description)

    return settings


def build_time_line(settings):
    time_board_data = {
        "title": "Curryware TimeBoard",
        "description": "New Hire Challenge TimeBoard",
        "layout_type": "ordered",
        "widgets": [{
            "id": 6031072804338302,
            "definition": {
                "title": "",
                "title_size": "16",
                "title_align": "left",
                "show_legend": True,
                "legend_layout": "auto",
                "legend_columns": ["avg", "min", "max", "value", "sum"],
                "type": "timeseries",
                "requests": [{
                    "q": "avg:curryware_metric{*}",
                    "style": {
                        "palette": "dog_classic",
                        "line_type": "solid",
                        "line_width": "normal"
                    },
                    "display_type": "line"
                }],
                "yaxis": {
                    "scale": "linear",
                    "label": "",
                    "include_zero": True,
                    "min": "auto",
                    "max": "auto"
                },
                "markers": []
            }
        }, {
            "id": 364738882911382,
            "definition": {
                "title": "Sum of Curryware for Last Hour",
                "title_size": "16",
                "title_align": "left",
                "time": {},
                "type": "query_value",
                "requests": [{
                    "q": "sum:curryware_metric{*}",
                    "aggregator": "sum"
                }],
                "autoscale": False,
                "precision": 0
            }
        }, {
            "id": 0,
            "definition": {
                "title": "Postgres fetched / returned / inserted / updated (per sec)",
                "show_legend": False,
                "type": "timeseries",
                "requests": [{
                    "q": "avg:postgresql.rows_fetched{$scope}"
                }, {
                    "q": "avg:postgresql.rows_returned{$scope}"
                }, {
                    "q": "avg:postgresql.rows_inserted{$scope}"
                }, {
                    "q": "avg:postgresql.rows_updated{$scope}"
                }]
            }
        }, {
            "id": 9469658219438844,
            "definition": {
                "title": "",
                "title_size": "16",
                "title_align": "left",
                "show_legend": True,
                "legend_layout": "auto",
                "legend_columns": ["avg", "min", "max", "value", "sum"],
                "time": {},
                "type": "timeseries",
                "requests": [{
                    "q": "anomalies(avg:system.cpu.user{host:scotc-a01.vmware.com}, 'basic', 2)",
                    "style": {
                        "palette": "dog_classic",
                        "line_type": "solid",
                        "line_width": "normal"
                    },
                    "display_type": "line"
                }],
                "yaxis": {
                    "scale": "linear",
                    "label": "",
                    "include_zero": True,
                    "min": "auto",
                    "max": "auto"
                },
                "markers": []
            }
        }],
    }
    json_string = json.dumps(time_board_data)
    headers = {'Content-Type': 'application/json', 'DD-API-KEY': settings['data_dog_api_key'], 'DD-APPLICATION-KEY'
    : settings['data_dog_application_key']}
    dd_url = 'https://api.datadoghq.com/api/v1/dashboard'
    response = requests.post(url=dd_url, headers=headers, data=json_string)
    if response.status_code == 200 or response.status_code == 202:
        print('Timeboard Created')
    else:
        print(response.status_code)


if __name__ == '__main__':
    dd_settings = get_settings('settings.yaml')
    build_time_line(dd_settings)
