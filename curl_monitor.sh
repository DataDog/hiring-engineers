#!/bin/bash
#submits a curl request to Datadog API to create a monitor

api_key=abc
app_key=def

#create monitor for random.number
curl -X POST -H "Content-type: application/json" \
-d '{
	"name": "Random Numbers",
	"type": "metric alert",
	"query": "max(last_1m):avg:random.number{*} by {host} > 800",
	"message": "{{#is_alert}}Oh no! Your random number coming from {{host.name}} just exceeded 800, it'\''s all the way at {{value}}  This can'\''t be good. {{/is_alert}} \n{{#is_warning}}Be careful, your random number coming from {{host.name}} exceeded 500, reaching {{value}}. You can'\''t do anything about it, but it is troubling.\n {{/is_warning}} \n\n{{#is_no_data}} Your random numbers are missing? What will you stress about now??? {{/is_no_data}}  @devlin.nicholasj@gmail.com",
	"tags": [
		"random",
		"number"
	],
	"options": {
		"timeout_h": 0,
		"notify_no_data": true,
		"no_data_timeframe": 10,
		"notify_audit": true,
		"require_full_window": true,
		"new_host_delay": 300,
		"include_tags": false,
		"escalation_message": "",
		"locked": false,
		"renotify_interval": "0",
		"evaluation_delay": "",
		"thresholds": {
			"critical": 800,
			"warning": 500
		}
	}
}' \
    "https://app.datadoghq.com/api/v1/monitor?api_key=${api_key}&application_key=${app_key}"


#schedule downtime for weekends
curl -X POST -H "Content-type: application/json" \
-d '{
      "scope": "env:prod",
      "messsage":"Disable Random Number Monitoring on weekends. @devlin.nicholasj@gmail.com",
      "recurrence": {
        "type": "weeks",
        "period": 1,
        "week_days": ["Sun", "Sat"]
      }
}' \
    "https://app.datadoghq.com/api/v1/downtime?api_key=${api_key}&application_key=${app_key}"