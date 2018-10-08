from datadog import initialize, api # import our modules from data dog

# set our api and app keys so we can authorise with datadog
options = {
    'api_key': 'de80ad2a1bffe3273e4765ac1b8a85d7',
    'app_key': '490954065d91b99b46fc59efc4a748141fae365b'
}
# pass in our options dictionary object
initialize(**options)

monitor_options = {
    "name": "STATUS EMAIL: my_metric",
        "type": "metric alert",
        "query": "avg(last_5m):avg:my_metric{host:ubuntu-xenial} >= 800",
        "message": "{{#is_alert}}\nALERT: my_metric has had a sustained value of 800 or above over the past 5 minutes!\n{{/is_alert}} \n\n{{#is_warning}}\nWARNING: my_metric has had a sustained value of 500 or above over the past 5 minutes.\n{{/is_warning}} \n\n{{#is_no_data}}\nmy_metric has had no data for the 10 minutes.\n{{/is_no_data}} @edmundcong1@gmail.com",
        "tags": [],
        "options": {
                    "notify_audit": False,
                    "locked": False,
                    "timeout_h": 0,
                    "new_host_delay": 300,
                    "require_full_window": True,
                    "notify_no_data": True,
                    "renotify_interval": "0",
                    "escalation_message": "",
                    "no_data_timeframe": 10,
                    "include_tags": False,
                    "thresholds": {
                                    "critical": 800,
                                    "warning": 500
                                }
                }
}

resp = api.Monitor.create(**monitor_options)

print resp
