# Level 1 - Collecting your Data

    Bonus question: In your own words, what is the Agent?
The agent is a piece of software, you can install on a host to gather events and performance metrics. The agent collects this data and sends it over to the Datadog server for reporting and analysis purposes.

    Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
![screenshot hostmap.png](/hostmap.PNG)  
https://app.datadoghq.com/infrastructure/map?fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=none&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=false&palette=green_to_orange&paletteflip=false

    Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
Done. MySQL.

    Write a custom Agent check that samples a random value. Call this new metric: test.support.random
Done. Called "simrandom.py":

```
import random 
from checks import AgentCheck

class SimrandomCheck(AgentCheck):
    def check(self, instance):
        ran = random.random()
        self.gauge('test.support.random', ran)
```

# Level 2 - Visualizing your Data

    Since your database integration is reporting now, clone your database integration dashboard and add additional database metrics to it as well as your test.support.random metric from the custom Agent check.
![screenshot DB-Dashboard.png](/DB-Dashboard.PNG)  
https://app.datadoghq.com/dash/351945/mysql---test?live=true&page=0&is_auto=false&from_ts=1504440936426&to_ts=1504444536426&tile_size=m  

    Bonus question: What is the difference between a timeboard and a screenboard?
A timeboard is used to have time-synchronized charts of metrics and events in one dashboard. The layout of the dashboard is fixed, has 3 columns and multiple lines. Good for troubleshooting as one can see the behavior of multiple metrics at a given timerange.  
A screenboard is used to show status boards and other relevant information, also just text. It is flexible in its design. You may arrange and size the charts as you like.

    Take a snapshot of your test.support.random graph and draw a box around a section that shows it going above 0.90. Make sure this snapshot is sent to your email by using the @notification  
![screenshot SpikesGraph.png](/SpikesGraph.PNG)  
https://app.datadoghq.com/notebook/13743/Random-Test-Data?cell=dncqcam6  


# Level 3 - Alerting on your Data

Since you've already caught your test metric going above 0.90 once, you don't want to have to continually watch this dashboard to be alerted when it goes above 0.90 again. So let's make life easier by creating a monitor.

    Set up a monitor on this metric that alerts you when it goes above 0.90 at least once during the last 5 minutes  
    Bonus points: Make it a multi-alert by host so that you won't have to recreate it if your infrastructure scales up.
    Give it a descriptive monitor name and message (it might be worth it to include the link to your previously created dashboard in the message). Make sure that the monitor will notify you via email. 
In JSON Format 
```     
{
	"name": "Random test value larger than 0.9",
	"type": "metric alert",
	"query": "max(last_5m):avg:test.support.random{*} by {host} > 0.9",
	"message": "This is just to alert you, that the random value has crossed the 0.9 mark within the last 5 minutes.\n[Random Test Value Graph](https://app.datadoghq.com/notebook/13743/Random-Test-Data?cell=dncqcam6)\n\n\n@siegi.mueller@gmx.de",
	"tags": [
		"*"
	],
	"options": {
		"timeout_h": 0,
		"notify_no_data": false,
		"no_data_timeframe": 10,
		"notify_audit": false,
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
    This monitor should alert you within 15 minutes. So when it does, take a screenshot of the email that it sends you. 
![screenshot Alert-email.png](/Alert-email.PNG) 

    Bonus: Since this monitor is going to alert pretty often, you don't want to be alerted when you are out of the office. Set up a scheduled downtime for this monitor that silences it from 7pm to 9am daily. Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.
![screenshot downtime.png](/downtime.PNG) 
![screenshot downtime_schedule.png](/downtime_schedule.PNG) 

***Thanks for providing such useful stuff. You were right - this is really fun!***  
***Cheers, Siegi***  
