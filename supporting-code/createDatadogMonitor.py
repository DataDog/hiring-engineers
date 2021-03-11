from datadog import initialize, api
from decouple import config
import os

"""
decouple allows for dynamic environment variable passing, locally, in a cloud environment, etc.
The simplest way to inject the environment variables below is to create a .env file with the env variables defined in <KEY>=<VALUE> form
"""
options = {
    'api_key': config('DATADOG_API_KEY'),
    'app_key': config('DATADOG_APPLICATION_KEY')
}

initialize(**options)

# Create a new monitor
monitor_options = {
    "notify_no_data": True,
    "no_data_timeframe": 20
}
tags = ["host:vagrant"]
api.Monitor.create(
        type="metric alert",
    query="avg(last_5m):sum:system.net.bytes_rcvd{host:host0} > 100",
    name="Bytes received on host0",
    message="We may need to add web hosts if this is consistently high.",
    tags=tags,
    options=monitor_options
)
