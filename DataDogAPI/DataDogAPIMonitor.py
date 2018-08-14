from datadog import initialize, api

options = {'api_key': '0df5392e3fcf52b4ee65fef26c2f0cb7',
           'app_key': '958de7a7ae45656320a630d7de70ae4efbddac5f'}

initialize(**options)

# Create a new monitor
options = {
    "notify_no_data": True,
    "no_data_timeframe": 20
}
tags = ["app:webserver", "frontend"]
response = api.Monitor.create(
    type="metric alert",
    query="avg(last_1h):sum:system.net.bytes_rcvd{host:host0} > 100",
    name="Bytes received on host0",
    message="We may need to add web hosts if this is consistently high.",
    tags=tags,
    options=options
)

print (response)
