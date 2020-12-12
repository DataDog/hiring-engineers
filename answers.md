**Section I: Collecting Metrics**

My host tags can be seen in this [screenshot](https://la-psql-zebra.s3.amazonaws.com/host_tags.PNG).

I choose to install PostgreSQL and installed the Datadog Integration for Postgres. This can be verified in Section II by viewing my [dasboard](https://la-psql-zebra.s3.amazonaws.com/my_first_dashboard_5min.PNG)

Here is my custom agent check, my_metric.py
```python
import random
import datadog_checks.base import AgentCheck

class MyCheck(AgentCheck):
      def check(self, instance):
              self.gauge('my_metric', random.randint(0, 1000))
```

*Bonus Question*  Yes, I changed the collection interval by adding `min_collection_interval: 45` to conf.d/my_metric.yaml.

**Section II: Visualizing Data**

Here is the link to the script I used to generate the timeseries (API and Application key redacted):
```json
curl --location --request POST 'https://api.datadoghq.com/api/v1/dashboard' \
--header 'Content-Type: application/json' \
--header 'Cookie: DD-PSHARD=217' \
--header 'DD-API-KEY: xxx' \
--header 'DD-APPLICATION-KEY: xxx' \
--data-raw '{
    "title": "My First Dashboard",
    "description": "Visualizing Data with the Datadog API",
    "layout_type": "ordered",
    "is_read_only": false,
    "widgets": [
        {
            "definition": {
                "type": "timeseries",
                "title": "my metric timeseries",
                "requests": [
                    {
                        "q": "my_metric{host:vagrant}"
                    }
                ]
            },
            "layout": {
                "x": 0,
                "y": 0,
                "width": 0,
                "height": 0
            }
        },
        {
            "definition": {
                "type": "timeseries",
                "title": "Postgres Disk Reads",
                "requests": [
                    {
                        "q": "anomalies(sum:postgresql.disk_read{*}, '\''basic'\'', 2)"
                    }
                ]
            },
            "layout": {
                "x": 0,
                "y": 0,
                "width": 0,
                "height": 0
            }
        },
        {
            "definition": {
                "type": "timeseries",
                "title": "Sum of my metric points per hour",
                "requests": [
                    {
                        "q": "sum:my_metric{*}.rollup(sum, 3600)"
                    }
                ]
            },
            "layout": {
                "x": 0,
                "y": 0,
                "width": 0,
                "height": 0
            }
        }
    ]
}'
```

Snapshot of my dashboard: https://la-psql-zebra.s3.amazonaws.com/my_first_dashboard_5min.PNG

*Bonus Question*: The anomoly graph is displaying expected behavior in shaded area and the actual behavior as the line.

**Section III: Monitoring Data**
I used the GUI to create a metric monitor that alerts on my_metric behavior. I exported the metric monitor as json and pasted at the bottom of this sectionbe.
[Here is a screenshot of an email notifcation for reaching warning status (still waiting for it to hit Alert!](https://la-psql-zebra.s3.amazonaws.com/my_metric_warn.PNG)

```json
{
	"id": 27366563,
	"name": "my_metric activity",
	"type": "metric alert",
	"query": "avg(last_5m):avg:my_metric{host:vagrant} > 800",
	"message": "{{#is_alert}}\n  my_metric has been unusually high ( {{value}} ) for {{host.name}} over the past 5 minutes  @eric.kufta@gmail.com \n{{/is_alert}}\n\n{{#is_warning}}\n  my_metric has been above average ( {{value}} ) for {{host.name}} over the past 5 minutes  \n{{/is_warning}}\n\n{{#is_no_data}}\n  my_metric has no data over the past 10 minutes  @eric.kufta@gmail.com \n{{/is_no_data}}",
	"tags": [],
	"options": {
		"notify_audit": false,
		"locked": false,
		"timeout_h": 0,
		"new_host_delay": 300,
		"require_full_window": false,
		"notify_no_data": true,
		"renotify_interval": "0",
		"escalation_message": "",
		"no_data_timeframe": 10,
		"include_tags": true,
		"thresholds": {
			"critical": 800,
			"warning": 500
		}
	}
}
```

**Section IV: Collecting APM Data***



