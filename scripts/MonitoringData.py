from datadog import initialize, api

options = {
    'api_key': '4dc7304832d0ab2d0d1048ab35c0b86f',
    'app_key': '7e8dffc303beb44b4f83d36c3c22a6a84561db87'
}

initialize(**options)

options = {
    "notify_no_data": True,
    "no_data_timeframe": 10,
    "thresholds": `{'critical': 800, 'warning': 500}`
}


api.Monitor.create(
    type="metric alert",
    query="avg(last_5m):sum:my_metric{host:linuxkit-025000000001} > 800",
    name="Hitting alert threshold",
    message="We may need to add web hosts if this is consistently high.",
    options=options
)
