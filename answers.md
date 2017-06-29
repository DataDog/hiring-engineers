# Level 1 - Collecting your Data
#### Sign up for Datadog (use "Datadog Recruiting Candidate" in the "Company" field), get the Agent reporting metrics from your local machine.
* ![Local machine metrics](https://github.com/hichambennis/hiring-engineers/blob/master/System%20metrics.JPG)

#### Bonus question: In your own words, what is the Agent?
An agent is a software which purpose is to be the interface between the user and a service. When a user is browing the web, it connect to services throught its browser; in this case, the brower is the agent. In the case of datadog, the agent is the software that connects to datadog server

#### Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
* ![Hostmap](/Host_map.JPG)
* ![Hostmap with tags](/Hostmap + tags.JPG)
* ![Tags on agent](/tags_on_agent.JPG)
* ![Tags on WebUI](/tags_on_webUI.JPG)

#### Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
* ![Tags on WebUI](/Integrations.JPG)
* ![Apache dashboard integration](/Apache_Integration_dashboard.JPG)
* ![MySQL dashboard integration](/MySQL_Integration_dashboard.JPG)

#### Write a custom Agent check that samples a random value. Call this new metric: test.support.random
* First agent check that will produce a random value
```python
from checks import AgentCheck

import random

class HelloCheck(AgentCheck):
    def check(self, instance):
        self.gauge('test.support.random', random.random())
```

* Second agent check that will always send 0.9 (used for comparison with the first one)
```python
from checks import AgentCheck

class HelloCheck(AgentCheck):
    def check(self, instance):
        self.gauge('test.support.max', 0.9)		
```

# Level 2 - Visualizing your Data
#### Since your database integration is reporting now, clone your database integration dashboard and add additional database metrics to it as well as your test.support.random metric from the custom Agent check.
* ![Custom dashboard](/Custom_dashboard(MySQL clone + test.support.random + mysql.aborted_connects).JPG)

#### Bonus question: What is the difference between a timeboard and a screenboard?
A timeboard will provide a certain amount of data for a period of time. For example, the evolution of disk memory usage within the last hour. A screenboard will provide a certain amount of data at a specific instant. For example, the disk memory usage at the present moment.

#### Take a snapshot of your test.support.random graph and draw a box around a section that shows it going above 0.90. Make sure this snapshot is sent to your email by using the @notification
* ![Snapshot](/snapshot.JPG)


# Level 3 - Alerting on your Data

#### Set up a monitor on this metric that alerts you when it goes above 0.90 at least once during the last 5 minutes
* ![monitors](/Monitors.JPG)

* ![random_test_monitor](/random_test_monitor.JPG)
```json
{
	"name": "random test",
	"type": "metric alert",
	"query": "max(last_5m):avg:test.support.random{host:DESKTOP-AE0VVCH} > 0.9",
	"message": "@hicham.bennis@hotmail.fr there is a problem with the random metric, please take a look.",
	"tags": [],
	"options": {
		"notify_audit": false,
		"locked": false,
		"timeout_h": 0,
		"silenced": {
			"host:DESKTOP-AE0VVCH": 1497942000
		},
		"include_tags": true,
		"thresholds": {
			"critical": 0.9
		},
		"require_full_window": true,
		"new_host_delay": 300,
		"notify_no_data": false,
		"renotify_interval": 0,
		"evaluation_delay": "",
		"no_data_timeframe": 10
	}
}
```

* Another monitor that aims at send me a warning if my DB reads twice within the last 5 minutes and sends me an alert if reads reach 20. I did this for fun just to check when connecting with a real app.
```json
{
	name alert mysql,
	type metric alert,
	query sum(last_5m)summysql.innodb.data_reads{hostDESKTOP-AE0VVCH}  20,
	message @hicham.bennis@hotmail.fr,
	tags [],
	options {
		notify_audit true,
		locked true,
		timeout_h 0,
		silenced {},
		include_tags false,
		thresholds {
			critical 20,
			warning 2
		},
		require_full_window false,
		new_host_delay 300,
		notify_no_data false,
		renotify_interval 0,
		evaluation_delay 60,
		no_data_timeframe 10
	}
}
```

#### Bonus points: Make it a multi-alert by host so that you won't have to recreate it if your infrastructure scales up. Give it a descriptive monitor name and message (it might be worth it to include the link to your previously created dashboard in the message). Make sure that the monitor will notify you via email.
Please check previous question

#### This monitor should alert you within 15 minutes. So when it does, take a screenshot of the email that it sends you.
* ![email alert](/email_alert.JPG)
* ![email daily digest](/email_daily_digest.JPG)

#### Bonus: Since this monitor is going to alert pretty often, you don't want to be alerted when you are out of the office. Set up a scheduled downtime for this monitor that silences it from 7pm to 9am daily. Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.
* ![manage downtime](/Manage_downtime.JPG)
