##Level 0 (optional) - Setup an Ubuntu VM
My setup is an Ubuntu 16.04 server on AWS (EC2 instance). 

##Level 1 - Collecting your Data

####Bonus question: In your own words, what is the Agent?
The agent is a daemon running on a host server, collecting events and metrics and sending them to Datadog.
It is developed in the Open Source: https://github.com/DataDog/dd-agent. 
The data shipped to Datadog can then be processed and analysed with several tools that Datadog provides (monitoring system).

####Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog. 
See `tags.png`.
![Tags](tags.png?raw=true "Tags")

####Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
See `mysql.yaml` (saved in `/etc/dd-agent/conf.d`).

####Write a custom Agent check that samples a random value. 
See `mycheck_test.py` (saved in `/etc/dd-agent/checks.d`) and `mycheck_test.yaml` (in `/etc/dd-agent/conf.d`). I originally called this metric `random.metric` before renaming it to `test.support.random`.

##Level 2 - Visualizing your Data

####Since your database integration is reporting now, clone your database integration dashboard and add additional database metrics to it as well as your test.support.random metric from the custom Agent check.
See `cloned_dashboard.png`.

####Bonus question: What is the difference between a timeboard and a screenboard?
TimeBoards and ScreenBoards are the 2 types of dashboards Datadog allows to create:
- Timeboards: For troubleshooting purposes. Timecard can be shared individually. All graphs appear as a grid.
- Screenboards: more customizables, with drag and drop widgets, with a possibility to have different timeframes. Unlike timeboards, it is possible to generate a read-only link that allows everyone to access them.

####Take a snapshot of your test.support.random graph and draw a box around a section that shows it going above 0.90. Make sure this snapshot is sent to your email by using the @notification.
See `box_above0.9.png`

##Level 3 - Alerting on your Data

####Set up a monitor on this metric that alerts you when it goes above 0.90 at least once during the last 5 minutes.
See `alert_monitor.png`

####Give it a descriptive monitor name and message (it might be worth it to include the link to your previously created dashboard in the message). Make sure that the monitor will notify you via email. This monitor should alert you within 15 minutes. So when it does, take a screenshot of the email that it sends you.
See `alert_monitor_email.png`

####Bonus: Since this monitor is going to alert pretty often, you don't want to be alerted when you are out of the office. Set up a scheduled downtime for this monitor that silences it from 7pm to 9am daily. Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.
See `downtime.png` and `downtime_email.png`.
