    from datadog import initialize, api

    options = {'api_key': '0df5392e3fcf52b4ee65fef26c2f0cb7',
               'app_key': '958de7a7ae45656320a630d7de70ae4efbddac5f'}

    initialize(**options)

    options = {
        "notify_audit": "false",
        "locked": "false",
        "timeout_h": "0",
        "new_host_delay": "300",
        "require_full_window": "true",
        "notify_no_data": "true",
        "renotify_interval": "0",
        "escalation_message": "",
        "no_data_timeframe": "10",
        "include_tags": "false",
        "thresholds": {
            "critical": "800",
            "warning": "500"
        }
    }

    message = '''{{#is_alert}}ALERT: @alexander.guesnon@gmail.com {{host.name}} at IP {{host.ip}} is {{value}}!!!{{/is_alert}}\n\n{{#is_warning}}WARNING: @alexander.guesnon@gmail.com {{host.name}} at IP {{host.ip}} is {{value}}!{{/is_warning}} \n\n{{#is_no_data}} NODATA:@alexander.guesnon@gmail.com {{host.name}} at IP {{host.ip}} NO DATA{{/is_no_data}}'''

    response = api.Monitor.create(
        type="metric alert",
        query="avg(last_5m):avg:my_metric{host:vagrant} >= 800",
        name="My_Metric on Vagrent host",
        message=message,
        tags=["app:webserver"],
        options=options
    )

    print(response)
