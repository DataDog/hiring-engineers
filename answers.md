## Questions

### Level 0 (optional) - Setup an Ubuntu VM
Ubuntu 12.04 is set up on Vagrant 1.9.7 on macOS 10.11.6

### Level 1 - Collecting your Data

* Bonus question: In your own words, what is the Agent?

The datadog agent is a typical daemon program.  It runs as a small program behind a target system called Integration/s.  The major purpose of the program is collecting and sending system information to your datadog account in a cloud service which is hosted by Datadog.　　
The 1st strong differentiator is its extensibility.  You can define new metrics as you needed. And also using tags makes you able to get very various types of reports(called dashboard) which makes your daily operation fun.  2nd merit is its easiness.  The steps to integrate other services is almost automated, or pre-defined.  You can install an agent with pre-defined manner to reduce opeartion cost.

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

<img width="1279" alt="2017-08-19 11 53 47" src="https://user-images.githubusercontent.com/7159697/29482992-38d8c61a-84d7-11e7-8cff-2d5508f79d00.png">


* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

<img width="857" alt="2017-08-19 13 50 30_mysql_integration" src="https://user-images.githubusercontent.com/7159697/29519089-0613287e-86b7-11e7-98ec-17b1957b476f.png">

<img width="1279" alt="2017-08-21 15 06 59" src="https://user-images.githubusercontent.com/7159697/29519113-211e07ba-86b7-11e7-8b6c-9214a320cc85.png">


* Write a custom Agent check that samples a random value. Call this new metric: `test.support.random`
/etc/dd-agent/checks.d/test.py

```
import random
from checks import AgentCheck
class TestSpprtRand(AgentCheck):
    def check(self, instance):
        self.gauge('test.support.random', random.random())
```
/etc/dd-agent/conf.d/test.yaml
```
init_config:

instances:
    [{}]
```

<img width="883" alt="2017-08-23 23 20 30" src="https://user-images.githubusercontent.com/7159697/29620779-da2d59ec-8859-11e7-9a67-136bd7265013.png">


### Level 2 - Visualizing your Data

* Since your database integration is reporting now, clone your database integration dashboard and add additional database metrics to it as well as your `test.support.random` metric from the custom Agent check.
<img width="1017" alt="2017-08-23 23 30 06" src="https://user-images.githubusercontent.com/7159697/29621327-659c8a92-885b-11e7-95c3-3ca7bd07c755.png">

* Bonus question: What is the difference between a timeboard and a screenboard?

A timeboard is typical mash-up view.  It's good for portal.  The most important feature is the time.  It shows any data in same timing.  Thus it provides easiness to compare each data as same event.  On the other hand, a screenboard has no such limitation. Even the layout, it's like iFrame. You can put any location as you like.  Thus the main pourpose of this is reporting and sharing the information you'd like to provide.

* Take a snapshot of your `test.support.random` graph and draw a box around a section that shows it going above 0.90. Make sure this snapshot is sent to your email by using the @notification

<img width="574" alt="2017-08-24 00 01 30" src="https://user-images.githubusercontent.com/7159697/29622821-6ccf70aa-885f-11e7-8c55-5ba63c7a0077.png">



### Level 3 - Alerting on your Data

Since you've already caught your test metric going above 0.90 once, you don't want to have to continually watch this dashboard to be alerted when it goes above 0.90 again.  So let's make life easier by creating a monitor.  
* Set up a monitor on this metric that alerts you when it goes above 0.90 at least once during the last 5 minutes

```
{
	"name": "{{host.name}} 上で、test.support.random が 0.9以上",
	"type": "metric alert",
	"query": "max(last_5m):avg:test.support.random{*} by {host} > 0.9",
	"message": "{{host.name}} \n詳細は以下を確認。 \nhttps://app.datadoghq.com/dash/346429/mysql---overview-cloned?live=true&page=0&is_auto=false&from_ts=1503487579122&to_ts=1503501979122&tile_size=m\n\n\n @takashi117@gmail.com",
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
		"include_tags": false,
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

* Bonus points:  Make it a multi-alert by host so that you won't have to recreate it if your infrastructure scales up.  

<img width="1219" alt="2017-08-24 00 24 32" src="https://user-images.githubusercontent.com/7159697/29623871-ab7991d4-8862-11e7-8bdb-bd5a127eabfd.png">

* Give it a descriptive monitor name and message (it might be worth it to include the link to your previously created dashboard in the message).  Make sure that the monitor will notify you via email.

<img width="1215" alt="2017-08-24 00 28 06" src="https://user-images.githubusercontent.com/7159697/29624048-217c49d0-8863-11e7-9bd1-4ae167deed90.png">


* This monitor should alert you within 15 minutes. So when it does, take a screenshot of the email that it sends you.
<img width="1090" alt="2017-08-24 00 31 39" src="https://user-images.githubusercontent.com/7159697/29624297-aae3646a-8863-11e7-8d26-ad3466c79d5d.png">


* Bonus: Since this monitor is going to alert pretty often, you don't want to be alerted when you are out of the office. Set up a scheduled downtime for this monitor that silences it from 7pm to 9am daily. Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

From [Monitors] - [Manage Downtime] , you can set up it.
<img width="770" alt="2017-08-24 00 37 46" src="https://user-images.githubusercontent.com/7159697/29624622-85dcca48-8864-11e7-8e70-f84c1bceb3a2.png">

