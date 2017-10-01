Your answers to the questions go here.
+
Level 1 - Collecting your Data
  Sign up for Datadog (use "Datadog Recruiting Candidate" in the "Company" field), get the Agent reporting metrics from your local machine.

    I signed up for Datadog with an e-mail of midori.taniguchi2@gmail.com

  Bonus question: In your own words, what is the Agent?

    Agent is a software that visualizes collected data. Datadog enables collecting data from many data of AWS, database, system, etc. Agent helps collecting events and metrics.

  Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

    # Set the host's tags (optional)
    tags: mytag, env:prod, role:database

![ScreenShot](https://user-images.githubusercontent.com/32184362/30998494-f53242ee-a509-11e7-8c80-a86ee74a3697.png)

  https://app.datadoghq.com/infrastructure/map?fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=none&filter=mytag&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=false&palette=green_to_orange&paletteflip=false&host=345947026
  
  Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

    I installed PostgreSQL for database.
   
  Write a custom Agent check that samples a random value. Call this new metric: test.support.random

      vagrant@precise64:/etc/dd-agent/conf.d$ sudo cat /etc/dd-agent/conf.d/test.yaml    
      init_config:
  
      instances:
         [{}]
         
      vagrant@precise64:/etc/dd-agent/conf.d$ sudo cat /etc/dd-agent/checks.d/test.py 
      from random import random
      from checks import AgentCheck
      class TestRandomCheck(AgentCheck):
           def check(self, instance):
                self.gauge('test.support.random', random())

Level 2 - Visualizing your Data

  Since your database integration is reporting now, clone your database integration dashboard and add additional database metrics to it as well as your test.support.random metric from the custom Agent check.

	Cloned Postgres overview with test.support.random
![ScreenShot](https://user-images.githubusercontent.com/32184362/31056060-df5be4e4-a706-11e7-88ba-5913841fb178.png)

  Bonus question: What is the difference between a timeboard and a screenboard?


  Take a snapshot of your test.support.random graph and draw a box around a section that shows it going above 0.90. Make sure this snapshot is sent to your email by using the @notification

![ScreenShot](https://user-images.githubusercontent.com/32184362/31057341-3c15c0c8-a71c-11e7-93a8-0635a5317124.png)

Level 3 - Alerting on your Data

  Since you've already caught your test metric going above 0.90 once, you don't want to have to continually watch this dashboard to be alerted when it goes above 0.90 again. So let's make life easier by creating a monitor.

  Set up a monitor on this metric that alerts you when it goes above 0.90 at least once during the last 5 minutes
  
	Alert Setting.
![ScreenShot](https://user-images.githubusercontent.com/32184362/31056692-c775f8a6-a710-11e7-9aaf-855c8df4bde0.png)

	Configuration Data by JSON

	{
		"name": "Random value is very high (over 0.9) on test.support.random",
		"type": "metric alert",
		"query": "max(last_5m):avg:test.support.random{*} by {host} > 0.9",
		"message": "Error Occurred!\nTo fix this, follow these steps\n   1.restart service.\n   2.check xxxx.\n\nCheck http://www.xxxxx.com for more information.\n\n@midori.taniguchi2@gmail.com",
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

	The alert appears on event wall.
![ScreenShot](https://user-images.githubusercontent.com/32184362/31057343-423d5baa-a71c-11e7-89a6-02eb09066f50.png)

	The e-mail notification received from Datadog Alerting.
![ScreenShot](https://user-images.githubusercontent.com/32184362/31057342-3f0898e6-a71c-11e7-8a9c-4f0966bddbaf.png)
  
  Bonus points: Make it a multi-alert by host so that you won't have to recreate it if your infrastructure scales up.
	Setting a multi-alert on edit monitor view.
	
		Timeboard allows automatically collect time-syncronized metrics and event. Screenboard does not need to sync time. It enables layout whatever you like.
	
![ScreenShot](https://user-images.githubusercontent.com/32184362/31057558-af94995e-a71f-11e7-8540-edf45d9a92d4.png)

  Give it a descriptive monitor name and message (it might be worth it to include the link to your previously created dashboard in the message). Make sure that the monitor will notify you via email.

![ScreenShot](https://user-images.githubusercontent.com/32184362/31057560-afc0a418-a71f-11e7-9a62-7348bf4dd364.png)

  This monitor should alert you within 15 minutes. So when it does, take a screenshot of the email that it sends you.

	The e-mail notification received from Datadog Alerting.
![ScreenShot](https://user-images.githubusercontent.com/32184362/31057559-afc0137c-a71f-11e7-93e9-cf8101a0ed0f.png)

Bonus: Since this monitor is going to alert pretty often, you don't want to be alerted when you are out of the office. Set up a scheduled downtime for this monitor that silences it from 7pm to 9am daily. Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

	Screenshot of downtime schedule.
![ScreenShot](https://user-images.githubusercontent.com/32184362/31057753-bee0be08-a722-11e7-8b7a-76bb88c2ce43.png)
		
	Waiting for e-mail to receive
