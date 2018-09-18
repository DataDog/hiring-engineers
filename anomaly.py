from datadog import initialize, api

options = {
    'api_key': 'ef6beb34bcb4b05c3ddca8d92b616d99',
    'app_key': '021c1515fee71183c6d3891fe5d727e251375cad'
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
