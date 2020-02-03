from datadog import initialize, api

options = {
    'api_key': 'XXX',
    'app_key': 'XXX'
}

initialize(**options)

# #################### Create MySQL Monitor #####################
monitor_options = {
    'notify_audit': False,
    'locked': False,
    'timeout_h': 0,
    'silenced': {},
    'include_tags': True,
    'no_data_timeframe': None,
    'require_full_window': False,
    'new_host_delay': 300,
    'notify_no_data': False,
    'renotify_interval': 0,
    'escalation_message': '',
    'threshold_windows': {
        'recovery_window': 'last_15m',
        'trigger_window': 'last_5m'
    },
    'thresholds': {
        'critical': 1,
        'critical_recovery': 0
    }
}

tags = []
monitor_creation_response = api.Monitor.create(
    type="query alert",
    query="avg(last_1h):anomalies(avg:mysql.innodb.data_writes{*}, 'basic', 2, direction='both', alert_window='last_5m', interval=20, count_default_zero='true') >= 1",
    name="MySQL data-writes Anomaly Detection Monitor",
    message="Looks like there might have been some anomalous data write activity to the database.",
    tags=tags,
    options=monitor_options
)

monitor_id = str(monitor_creation_response['id'])

# #################### Create Dashboard #####################
title = '2.1 Dashboard via API'
widgets = [
    {
        'definition': {
            'type': 'timeseries',
            'requests': [
                {
                    'q': 'avg:my_metric{host:docker-desktop}'
                }
            ],
            'title': 'my_metric time-series graph'
        }
    },
    {
        'definition': {
            'type': 'alert_graph',
            'title': 'MySQL \'Data Writes\' Anomaly Detection',
            'alert_id': monitor_id,
            'viz_type': 'timeseries'
        }
    },
    {
        'definition': {
            'type': 'query_value',
            'requests': [
                {
                    'q': 'avg:my_metric{host:docker-desktop}.rollup(sum, 3600)',
                    'aggregator': 'sum'
                }
            ],
            'title': 'my_metric 1-hr Rollup Sum',
            'precision': 0
        }
    }
]

layout_type = 'ordered'
description = """
# Dashboard
*Created via Python API*

**Contents**

- Simple time-series graph showing the values of my_metric over the last 15 minutes
- Anomaly detection monitoring graph showing potential anomalies in the MySQL database's data_writes metric
- Sum of the values of reported by my_metric over the last hour
"""
is_read_only = False
notify_list = ['email@domain.com']
template_variables = []
saved_views = []

dashboard_creation_response = api.Dashboard.create(title=title,
                                                   widgets=widgets,
                                                   layout_type=layout_type,
                                                   description=description,
                                                   is_read_only=is_read_only,
                                                   notify_list=notify_list,
                                                   template_variables=template_variables,
                                                   template_variable_presets=saved_views)
