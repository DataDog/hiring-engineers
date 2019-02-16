#!/usr/bin/env python
from pprint import pprint
from myapi import api


options = {
	"notify_no_data": True,
	"no_data_timeframe": 10,
	"include_tags": True,
	"locked": False,
	"new_host_delay": 300,
	"no_data_timeframe": 10,
	"notify_audit": False,
	"notify_no_data": True,
	"renotify_interval": 0,
	"require_full_window": True,
	"thresholds": {"critical": 800.0, "warning": 500.0},
	"timeout_h": 0
}
tags = ["dev"]
res=api.Monitor.create(
    type="metric alert",
    query='avg(last_5m):avg:my_metric{host:en} > 800',
    name="Random Metric Monitor 1",
    message='''{{#is_alert}} Alert: Warning: random metric from {{host.name}} with {{host.ip}} with {{value}} reached the configured Alerting threshold of {{threshold}} {{/is_alert}}
            {{#is_warning}} Warning: random metric from {{host.name}}  with {{value}} reached the configured Warning threshold of {{threshold}} {{/is_warning}}
            {{#is_no_data}} No Data have been received for the random metric in the last 10 minutes {{/is_no_data}} @edennuriel@hotmail.com''',
    tags=tags,
    options=options)

print (res)
