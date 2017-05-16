Level 0 - Setup
==============
Configured Ubuntu VDI 16.04 image

Level 1 - Collecting your Data
==============

- Sign up for Datadog (use "Datadog Recruiting Candidate" in the "Company" field), get the Agent reporting metrics from your local machine.
- Bonus question: In your own words, what is the Agent?

*The Datadog agent is a multi-use tool, deployable to hosts and enables metrics collection for the Datadog service in "on premise" environments. To support a wide variety of possible use cases, the agent contains a collector, a custom variant of statsd (a time based metrics aggregation sub-service), and forwarding state engine that securely relays data to the cloud.*

- Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

Tags: line 31/259 of /etc/dd-agent/datadog.conf
tags: Test, env:test, role:candidatetest, region:west
Screenshots: *Tags* screenshots in screenshots folder

- Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

MongoDB database integration install: See mongo.yaml in conf.d folder

- Write a custom Agent check that samples a random value. Call this new metric: test.support.random

test.support.random: Code can be found in conf.d and checks.d. I used 'testcheck' to learn and 'randomcheck' to poll 'test.support.random'. 
 
 
Level 2 - Visualizations
==============

- Since your database integration is reporting now, clone your database integration dashboard and add additional database metrics to it as well as your test.support.random metric from the custom Agent check.

Cloned MongoDB ScreenBoard to "DB Clone Dashboard", added custom metric and misc metrics.

- Bonus question: What is the difference between a timeboard and a screenboard?

*The biggest distinction between boards is that timeboards contain graphs or metrics scoped to the same time frame appearing in a grid format. You can use these for time series based root cause analysis and event correlation. TimeBoards can only be shared to individuals.*

*Screenboards are very customizable, widget based boards. They can have checks, status, queries or any data from the Datadog system in the dashboard. Screenboards are shareable as live entities within your organization. Very modular and multifunctional.*

- Take a snapshot of your test.support.random graph and draw a box around a section that shows it going above 0.90. Make sure this snapshot is sent to your email by using the @notification

Snapshot Notification are sent via TimeBoard *NOT* Screenboard. See screenshots folder of notification.png	for information sent to email notifier via UI. 


Level 3 - Alerting
==============

- Set up a monitor on this metric that alerts you when it goes above 0.90 at least once during the last 5 minutes
- Bonus points: Make it a multi-alert by host so that you won't have to recreate it if your infrastructure scales up.

See screenshot multialert.png in screenshots folder

- Give it a descriptive monitor name and message (it might be worth it to include the link to your previously created dashboard in the message). Make sure that the monitor will notify you via email.
- This monitor should alert you within 15 minutes. So when it does, take a screenshot of the email that it sends you.

Monitor notification via email: see monitoralert.png in screenshots folder

- Bonus: Since this monitor is going to alert pretty often, you don't want to be alerted when you are out of the office. Set up a scheduled downtime for this monitor that silences it from 7pm to 9am daily. Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

Please see downtimeschedule.png in screenshots folder
