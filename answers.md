Thank you for taking the time to review my hiring exercise. I really enjoyed all the sections, got reacquainted with some tools such as Postman and learned a new one along the way – Vagrant. I especially got carried away with the APM section and ended up hosting my flask app on AWS with Nginx, uWSGI and an ec2 instance. More on that in section IV but if you would like to skip ahead, you can reach the web app at http://54.237.104.89/

After this exercise I am very impressed and excited about a potential opportunity at Datadog. It is easy to see that the product is powerful, flexible, and easy to use. I was most impressed with the tools provided for developers/ users. The docs are functional and elegant while the generated scripts (for things like agent install) work flawlessly, just to name a couple of highlights.

**Section I: Collecting Metrics**

My host tags can be seen in this image

![Alt text](https://la-psql-zebra.s3.amazonaws.com/DD_host_tags.PNG).

I choose to install PostgreSQL,a sample DVD rental collection and the Datadog Integration for Postgres. This can be verified in Section II by viewing my dashboard.

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

Hands down this was the best experience I have ever had getting to know an API. It was great to be able to download the Postman Environment and work from there! Not to mention the API docs being very user friendly. I generated this script below from Postman to create my dashboard.

```
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
                "title": "Postgres Table Count",
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

The sum of my metric is grouped into hours (per instructions) so it did not show properly in a 5 minute time span. I expanded the time period on the widget and included a snapshot here 
![Alt text](https://la-psql-zebra.s3.amazonaws.com/Sum_of_metric_per_hr.PNG)

*Bonus Question:* The anomaly graph is displaying expected behavior in shaded area and the actual behavior as the line. I choose to use a straightforward metric -- count of database tables. The anomaly function showed some interesting (but expected) behavior in my dashboard since I added and deleted some tables rapidly while the metric was still trying to establish a baseline. After a few minutes, the shaded "bounds" steadied out.

**Section III: Monitoring Data**
Again, I found this all very user-friendly and the variables very handy. I used the GUI to create a metric monitor that alerts on my_metric behavior. I exported the metric monitor as json and pasted at the bottom of this section to show exactly what I did. 

Here is a screenshot of an email notification for reaching alert status
![Alt text](https://la-psql-zebra.s3.amazonaws.com/my_metric_alert.PNG)

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

I used ddtrace to collect metrics on my "YaraDog" application. You can check it out here  http://54.237.104.89/ . The source code is in my github [HERE](https://github.com/ekufta0530/YaraDog/tree/master). There is not yet a comprehensive ruleset installed so it is a work in progress and a tool that I will definitely use in the future.

Credit goes to the original [Aegis](https://github.com/kittymagician/Aegis) app for the idea/ framework. I made some cosmetic changes, wrote some fun Yara rules and made lots of changes to it so it could be deployed out securely with nginx, uWSGI, ec2 and start/stop with systemd. I ran into an isses with ddtrace once I was using systemd to manage the app. The dashboards below are metrics from the dev server but I didn't walk away empty-handed from my efforts to monitor the deployed web app so I installed the Nginx integration.

The APM Dashboard
![Alt text](https://la-psql-zebra.s3.amazonaws.com/Yara_apm.PNG)

Dashboard for Infrastructure Monitor
![Alt text](https://la-psql-zebra.s3.amazonaws.com/infrastructure_metrics.PNG)

Dashboard for Nginx
![Alt test](https://la-psql-zebra.s3.amazonaws.com/nginx.PNG)

*Bonus Question:* A service "groups together a series of endpoints, queries, or jobs." For example, a user database or advertising server could be services. Resources "represent a particular domain of a customer application". An example would be a web endpoint or a database query.

**Is there anything creative you would use Datadog for?**

Datadog would be an excellent platform for monitoring and visualizing telemetry data on security indicators of compromise published by different threat intel feeds (i.e. ISAC’s, Cisco Talos, Emerging Threats, DHS). Log files of the IDS/IPS appliances could be received into the platform to see which indicators are firing most, or not at all. Layer on true/ false positive telemetry from security teams and you can easily see which rules are worthy and which are just noise.

This would also be very useful for predicting attack trends at scale and would be an excellent tool for those publishing the threat intelligence! One use case would be sending off notifications to subscribers if an indicator, or set of indicators, are firing often. For example, if a rule for a SYN flood DoS is firing at 300% normal capacity in the community, the rest of the sec community would love to have this information in real time to notify their relevant team members. 



Thanks again for reviewing my hiring exercise and I hope to talk more in the future. 

