from datadog import initialize, api

options = {
    'api_key': 'e05c62b16283be76411fc383d55eecba',
    'app_key': 'a9e09d8a7e25a602b6b5f059924f354643220fdf'
}

initialize(**options)

# Create a new monitor
options = {
    "notify_no_data": True,
    "no_data_timeframe": 20
}
tags = ["db:mongodb", "myTag:anomaly"]
api.Monitor.create(
    type="metric alert",
    query="avg(last_4h):anomalies(avg:mongodb.tcmalloc.tcmalloc.thread_cache_free_bytes{*}, 'agile', 2, direction='both', alert_window='last_15m', interval=60, count_default_zero='true') >= 1",
    name="Mongo Thread Cache Free Bytes",
    message="Anomaly detected!!!!!",
    tags=tags,
    options=options
)
