Your answers to the questions go here.

** Level 1 - Collecting your Data

A. Sign up for Datadog (use "Datadog Recruiting Candidate" in the "Company" field), get the Agent reporting metrics from your local machine.

# I already had a Datadog account under my personal email address (stephaniesher18@gmail.com), from my Marketing days, so the "Company" field for my account is populated with "Datadog".

# I installed the agent following in-app instructions: http://ge.tt/8xFqjWa2

# Upon successful agent installation, I saw my local host up on the Datadog agent: http://ge.tt/8qvuXWa2

# Snapshot of ~1 hour of metrics: http://ge.tt/9tbWVWa2

B. Bonus question: In your own words, what is the Agent?

# The Datadog Agent is software that runs on a user's servers and lets users monitor, visualize, and manage data in one place. It has three components: 1. the collector, which runs checks on the host machine for the user's selected integrations and captures system metrics (ie CPU, memory, load average); 2. DogStatsD, a backend server to which the user can send custom application metrics; and 3. the forwarder, which transfers to Datadog data from both DogStatsD and the collector.

C. Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

# In the Agent config file (~/.datadog-agent/agent/datadog.conf), I un-commented line 27, 'tags', and set four sample tags for my host: env:prod, role:database, region:ne, and app:system.

# Host and tags on Host Map page: http://ge.tt/81GZlWa2

D. Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

# I installed MongoDB and then installed the MongoDB integration in Datadog using in-app configuration instructions: http://ge.tt/2nGV6Xa2 && http://ge.tt/7ykAraa2

# I accidentally attempted to configure the MongoDB integration twice using an extraneously generated password, so I had to reset the admin user password using the db.changeUserPassword() command: http://ge.tt/5X3Csaa2. 


E. Write a custom Agent check that samples a random value. Call this new metric: test.support.random

# Once again following Datadog Docs (http://bit.ly/1sitxHf), I wrote a custom Agent check sampling a random value: http://ge.tt/9QGyKXa2

# In the configuration file, at conf.d/hello.yaml:

``` 
init_config:

instances:
    [{}]
```

# In the check module, at checks.d/hello.py:

```
from checks import AgentCheck
import random

class HelloCheck(AgentCheck):
  def check(self, instance):
    self.gauge('test.support.random', random.random())
```

** Level 2 - Visualizing your Data

A. Since your database integration is reporting now, clone your database integration dashboard and add additional database metrics to it as well as your test.support.random metric from the custom Agent check.

# I cloned my MongoDB dashboard, naming the new dash "Steph's Mongo Dashboard". I added additional database metrics, including test.support.random: http://ge.tt/2TEAtaa2 && http://ge.tt/7DwZYXa2

B. Bonus question: What is the difference between a timeboard and a screenboard?

- https://help.datadoghq.com/hc/en-us/articles/204580349-What-is-the-difference-between-a-ScreenBoard-and-a-TimeBoard-

- https://www.datadoghq.com/blog/introducing-screenboards-your-data-your-way/

# Timeboards appear in a grid layout and are always scoped to the same time period. Data is retained for up to a year, with one-second granularity, allowing for easier correlation and troubleshooting. Timeboard graphs can be shared individually.

# Timeboard example: http://ge.tt/1kYfGca2

# A screenboard is better for showing statuses and sharing information. Users can use the precise, drag-and-drop layout to mix and match widgets and timeframes in a customized, visually pleasing way, rendering it unnecessary for devops teams to painstakingly build their own custom dashboards simply to get critical data across their IT infrastructure to fit on one screen. Screenboards also support varied widget types: time series, color-coded numbers, event streams, text notes, and images.

# Screenboard example (from Datadog blog): http://ge.tt/7aMdGca2

C. Take a snapshot of your test.support.random graph and draw a box around a section that shows it going above 0.90. Make sure this snapshot is sent to your email by using the @notification

# I was unable to send an email notification from my admin account to my admin email account, so I hypothesized that perhaps one cannot email-notify oneself. To test this, I created a second Datadog account using a test email and used it to notify my admin account. To double check, I also notified the test user account from my admin account. In each case, I received email notifications immediately.

# Snapshot of test.support.random graph going above .90: http://ge.tt/2OK6BZa2

# Annotated graph and sent snapshot to admin email from test account: http://ge.tt/7FPFBZa2

# Received email notification in admin account: http://ge.tt/6ck0BZa2

# Annotated graph and sent snapshot to test email from admin account: http://ge.tt/6CpdFea2

# Received email notification in test account: http://ge.tt/5ONuFea2


** Level 3 - Alerting on your Data

Since you've already caught your test metric going above 0.90 once, you don't want to have to continually watch this dashboard to be alerted when it goes above 0.90 again. So let's make life easier by creating a monitor.

A. Set up a monitor on this metric that alerts you when it goes above 0.90 at least once during the last 5 minutes

# Defined metric and set alert conditions: http://ge.tt/8kJUkYa2

B. Bonus points: Make it a multi-alert by host so that you won't have to recreate it if your infrastructure scales up.

# Made a multi-alert by host: http://ge.tt/825hlYa2

# Monitor, set up in Datadog: http://ge.tt/271O4ea2

C. Give it a descriptive monitor name and message (it might be worth it to include the link to your previously created dashboard in the message). Make sure that the monitor will notify you via email.

# Created a descriptive monitor name and message: http://ge.tt/4oDymYa2

D. This monitor should alert you within 15 minutes. So when it does, take a screenshot of the email that it sends you.

# Received email notification in admin email account: http://ge.tt/7a48nYa2

# Notified test user from admin account in agent, received email notification test email account: http://ge.tt/4t21EZa2

E. Bonus: Since this monitor is going to alert pretty often, you don't want to be alerted when you are out of the office. Set up a scheduled downtime for this monitor that silences it from 7pm to 9am daily. Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

# Scheduled downtime for out-of-office hours: weekends (http://ge.tt/51Xytaa2) and weekdays (http://ge.tt/7ci4uaa2)

# Received email notification at 7pm on Friday night: http://ge.tt/1FJT9Za2 //ADD SCREENSHOT of email notification of weekday downtime notification here