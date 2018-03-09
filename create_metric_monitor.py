from datadog import initialize, api

options = {
    'api_key': '8b61d94149b2d8718b1487ae2d76e6ba',
    'app_key': '9d72fc44a77f1394ef465e290f08141699579e19'
}

# Create Monitor with thresholds
initialize(**options)

options = {
	"thresholds": {
		"critical": 800,
		"warning": 500
	},
    "notify_no_data": True,
    "no_data_timeframe": 20
}

api.Monitor.create(
    type="metric alert",
    query="avg(last_5m):avg:my_metric{*} > 500",
    name="Warning Monitor",
    handle="tylerpwilmot@gmail.com",
    message="WARNING: my_metric is over 500! Alert is at 800.",
    options=options
)
