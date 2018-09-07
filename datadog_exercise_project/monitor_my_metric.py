from datadog import initialize, api

options = {
    'api_key': '6ecfd1d61dff04a0547d44561ac09911',
    'app_key': '83bf20f58f0fcc8b3d891b7817ba5d02eefde58f'
}

initialize(**options)

# Create a new monitor
options = {
    "notify_no_data": True,
    "no_data_timeframe": 10,
    "timeout_h": 0,
    "notify_audit": True,
    "require_full_window": True,
    "new_host_delay": 300,
    "include_tags": False,
    "locked": False,
    "renotify_interval": "0",
    "thresholds": {
        "critical": 800,
        "warning": 500
    }
 
}
tags = []
api.Monitor.create(
    type="metric alert",
    query="avg(last_5m):avg:my_metric{host:datadog-project} > 800",
    name="my_metric monitor",
    message="{{#is_alert}}\n@zgroves19@gmail.com \nmy_metric's average is over 800! We're doomed! The last data point was {{value}} with the host ip of {{host.ip}} with a hostname of {{host.name}} .\n{{/is_alert}} \n\n{{#is_warning}}\n@zgroves19@gmail.com \nmy_metric's average is over 500. This may be the end. The last data point was {{value}} with the host ip of {{host.ip}} with a hostname of {{host.name}} .\n{{/is_warning}} \n\n{{#is_no_data}}\n@zgroves19@gmail.com \nmy_metric has not returned data for the last 10minutes. The host ip was {{host.ip}} with a hostname of {{host.name}} .\n{{/is_no_data}}",
    tags=tags,
    options=options
)
