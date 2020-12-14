**Section I: Collecting Metrics**

My host tags can be seen in this image

![Alt text](https://la-psql-zebra.s3.amazonaws.com/host_tag_vagrant.PNG).

I choose to install PostgreSQL and installed the Datadog Integration for Postgres. This can be verified in Section II by viewing my [dashboard](https://la-psql-zebra.s3.amazonaws.com/my_first_dashboard.PNG).

Here is my custom agent check, my_metric.py
```python
import random
import datadog_checks.base import AgentCheck

class MyCheck(AgentCheck):
      def check(self, instance):
              self.gauge('my_metric', random.randint(0, 1000))
```

*Bonus Question:*  Yes, I changed the collection interval by adding `min_collection_interval: 45` to conf.d/my_metric.yaml.

**Section II: Visualizing Data**

Here is the the script I used to generate the timeseries (API and Application keys redacted)
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
                        "q": "anomalies(sum:postgresql.table_count{*}, '\''basic'\'', 5)"
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
Here is my dashboard over 5 minutes
![Alt text](https://la-psql-zebra.s3.amazonaws.com/my_first_dashboard.PNG)

The sum of my metric grouped into hours so it did not show properly in a 5 minute time span. I expanded the time period on the widget and included a snapshot here. 
![Alt text](https://la-psql-zebra.s3.amazonaws.com/Sum_of_metric_per_hr.PNG)

*Bonus Question:* The anomaly graph is displaying expected behavior in shaded area and the actual behavior as the line. It showed some interesting behavior in my dashboard since I added and deleted some tables rapidly while the metric was still trying to establish a baseline. After a few minutes, the shaded "bounds" steadied out. 

**Section III: Monitoring Data**
I used the GUI to create a metric monitor that alerts on my_metric behavior. I exported the metric monitor as json and pasted at the bottom of this section to show exactly what I did. 

Here is a screenshot of an email notification for reaching warning status
![Alt text](https://la-psql-zebra.s3.amazonaws.com/my_metric_warn.PNG)

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

I used ddtrace to collect metrics on the provided application. I had to modify the datadog-agent config file slightly to get infrastructure metrics by including a value for env and added a tag for service.

Dashboard for APM
![Alt text](https://la-psql-zebra.s3.amazonaws.com/apm_dashboard.PNG)

Dashboard for Infrastructure Monitor
![Alt text](https://la-psql-zebra.s3.amazonaws.com/apm_dashboard.PNG)

*Bonus Question:* A service "groups together a series of endpoints, queries, or jobs." For example, a user database or advertising server could be services. Resources "represent a particular domain of a customer application". An example would be a web endpoint or a database query.

**Is there anything creative you would use Datadog for?**

Datadog would be an excellent platform for monitoring and visualizing telemetry data on security indicators of compromise published by different threat intel feeds (i.e. ISAC’s, Cisco Talos, Emerging Threats, DHS). Log files of the IDS/IPS appliances could be received into the platform to see which indicators are firing most, or not at all. Layer on true/ false positive telemetry from security teams and you can easily see which rules are worthy and which are just noise.

This would also be very useful for predicting attack trends at scale and would be an excellent tool for those publishing the threat intelligence! One use case would be sending off notifications to subscribers if an indicator, or set of indicators, are firing often. For example, if a rule for a SYN flood DoS is firing at 300% normal capacity in the community, the rest of the sec community would love to have this information in real time to notify their relevant team members. 

