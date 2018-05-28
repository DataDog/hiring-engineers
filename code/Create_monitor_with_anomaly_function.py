from datadog import initialize, api

options = {
    'api_key': '5032023d686e6bd9b5e0b376a59bb27f',
    'app_key': '94846c5a071f7c2dc77381214fed18614987250a'
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
