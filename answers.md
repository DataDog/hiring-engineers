### Level 1 - Collecting your Data

1. Agent initialization

![Agent init](./screenshots/dd-agent-init.png)


2. *Bonus:* What is the Agent?
This is a daemon that is executing tasks in the background such as:
- collecting data
- sending data to the datadog cloud platform

3. Host map:

![Host map](./screenshots/dd-host-map.png)


4. MongoDB integration:

![Mongo init](./screenshots/dd-mongo-init.png)


5. The Agent check code is located in the `check` repository:

![Random event](./screenshots/dd-random-event.png)

---

### Level 2 - Visualizing your Data

1. Cloned dashboard with `test.support.random` metrics:

![Cloned dashboard](./screenshots/dd-cloned-dashboard.png)


2. *Bonus:* What is the difference between a TimeBoard and a ScreenBoard?
- A timeboard is a real-time dashBoard
- A ScreenBoard is intended to show metrics over a selected period of time.

---

### Level 3 - Alerting on your Data

1. Random alert settings on all hosts (*Bonus*):

![Random alert setting](./screenshots/dd-alert-setting.png)

**Monitor export:**
```
{
	"name": "test.support.random check is above 0.9",
	"type": "metric alert",
	"query": "max(last_5m):avg:test.support.random{*} by {host} > 0.9",
	"message": "The random number is above 0.9 @ncls.mitchell@gmail.com",
	"tags": [
		"*"
	],
	"options": {
		"timeout_h": 0,
		"notify_no_data": false,
		"no_data_timeframe": 10,
		"notify_audit": true,
		"require_full_window": true,
		"new_host_delay": 300,
		"include_tags": true,
		"escalation_message": "",
		"locked": false,
		"renotify_interval": "0",
		"evaluation_delay": "",
		"thresholds": {
			"critical": 0.9
		}
	}
}
```

2. Received alert and email:

![Received alert](./screenshots/dd-event-alert.png)

![Received email](./screenshots/dd-emailing-alert.png)


3. *Bonus:* Downtime settings

![Received email](./screenshots/dd-downtime-settings.png)
