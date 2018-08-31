from datadog import initialize, api

options = {
    'api_key': '0d3ec981a0ea90d5983c547fc3169ddf',
    'app_key': '9cf15dee3fa15d30e0421784a66336acaa271f41'
}

initialize(**options)

# Create a new monitor
options = {
    "notify_no_data": True,
    "no_data_timeframe": 10,
    "thresholds": {
                        "critical": 800,
                        "warning": 500
                }
}
tags = []
api.Monitor.create(
    type="metric alert",
    query="avg(last_5m):avg:my_metric_value{*} > 800",
    name="my_metric_monitor2",
    message="{{#is_alert}}High Metric is too high {{value}}>{{threshold}} {{/is_alert}}{{#is_warning}}High Metric is high {{value}} > {{warn_threshold}}{{/is_warning}}{{#is_no_data}}No Metric is best if not high{{/is_no_data}}. @steven_yuen05@hotmail.com",
    tags=tags,
    options=options
)

