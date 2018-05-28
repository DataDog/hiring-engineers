from datadog import initialize, api

options = {
    'api_key': '',
    'app_key': ''
}

initialize(**options)

# Create a new monitor with the anomaly function applied
options = {
    "notify_no_data": True,
    "no_data_timeframe": 20
}
tags = ["anomaly"]

api.Monitor.create(
    type="metric alert",
    query="avg(last_4h):anomalies(avg:mysql.net.connections{host:deep-learning-virtual-machine}, \
     'basic', 2, direction='both', alert_window='last_15m', interval=60, count_default_zero='true') >= 1",
    name="Anomaly Function (MySQL Net-connections)",
    message="Alert test",
    tags=tags,
    options=options
)
