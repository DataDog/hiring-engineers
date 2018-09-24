from datadog import initialize, api

options = {
    'api_key': '<api key>',
    'app_key': '<app key>'
}

initialize(**options)

# create new monitor with anomoly detection

options = {
    "notify_no_data": True,
    "no_data_timeframe": 20
}

tags = ["my_metric", "anomaly"]

print api.Monitor.create(
    type="metric alert",
    query="avg(last_1h):anomalies(avg:my_metric{*}, 'basic', 3, direction='both', alert_window='last_5m', interval=20, count_default_zero='true') >= 1",
    name="Anomaly detection",
    message="Anomaly detected.",
    tags=tags,
    options=options
)
