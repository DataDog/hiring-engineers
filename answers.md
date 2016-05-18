Your answers to the questions go here.

### Level 1 - Collecting your Data

* Sign up for Datadog (use "Datadog Recruiting Candidate" in the "Company" field), get the Agent reporting metrics from your local machine.

I already had a Datadog account under my personal email address (stephaniesher18@gmail.com), from my Marketing days, so the "Company" field for my account was populated with "Datadog". For this challenge, I renamed my admin organization to "Datadog".

I installed the agent following in-app instructions. 

![Agent installed](https://farm8.staticflickr.com/7404/27083751985_519a09d6c5_z.jpg)

Upon successful agent installation, I saw my local host up on the Datadog agent.

![Localhost up on agent](https://farm8.staticflickr.com/7205/26479969873_9b418a62c4_b.jpg)

* Bonus question: In your own words, what is the Agent?

The Datadog Agent is software that runs on a user's servers and lets users monitor, visualize, and manage data in one place. It has three components: 1. the collector, which runs checks on the host machine for the user's selected integrations and captures system metrics (ie CPU, memory, load average); 2. DogStatsD, a backend server to which the user can send custom application metrics; and 3. the forwarder, which transfers to Datadog data from both DogStatsD and the collector.

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

In the Agent config file (~/.datadog-agent/agent/datadog.conf), I un-commented line 27, 'tags', and set four sample tags for my host: env:prod, role:database, region:ne, and app:system.

![Edited datadog.conf to set sample tags](https://farm8.staticflickr.com/7199/26989098282_cd3b3cd302_z.jpg)

Then I was able to see my host and associated tags on the Host Map page.

![Host and tags on Host Map page](https://farm8.staticflickr.com/7226/27015292961_35778b79dd_b.jpg)

* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

I installed MongoDB on my local host, and then installed the MongoDB integration in Datadog using in-app configuration instructions. 

![Installed MongoDB](https://farm8.staticflickr.com/7008/26479827943_143d165d1f_b.jpg)

![Installed MongoDB in the Datadog Agent](https://farm8.staticflickr.com/7538/27015292881_17b77051e7_z.jpg)

I accidentally attempted to configure the MongoDB integration twice using an extraneously generated password, so I had to reset the admin user password using the db.changeUserPassword() command. 

![Reset admin user password](https://farm8.staticflickr.com/7205/26479827993_eee88995a9.jpg)

* Write a custom Agent check that samples a random value. Call this new metric: test.support.random

Once again following Datadog's [Docs](http://bit.ly/1sitxHf), I wrote a custom Agent check sampling a random value.

In the configuration file, at conf.d/hello.yaml:

``` 
init_config:

instances:
    [{}]
```

In the check module, at checks.d/hello.py:

```
from checks import AgentCheck
import random

class HelloCheck(AgentCheck):
  def check(self, instance):
    self.gauge('test.support.random', random.random())
```

### Level 2 - Visualizing your Data

* Since your database integration is reporting now, clone your database integration dashboard and add additional database metrics to it as well as your test.support.random metric from the custom Agent check.

I cloned my MongoDB dashboard, naming the new dash "Steph's Mongo Dashboard". I added additional database metrics, including test.support.random. 

![Added database metrics](https://farm8.staticflickr.com/7035/27015292651_45775c86f5_b.jpg) 

![Added test.support.random](https://farm8.staticflickr.com/7325/27083651095_1669a0f939_b.jpg)

* Bonus question: What is the difference between a timeboard and a screenboard?

Timeboards appear in a grid layout and are always scoped to the same time period, making them the tool of choice for correlating events across systems. Data is retained for up to a year, with one-second granularity, allowing for easier correlation and troubleshooting. Timeboard graphs can also be shared individually.

Timeboard example: https://app.datadoghq.com/dash/131778/stephs-mongo-dashboard?live=true&page=0&is_auto=false&from_ts=1463536320000&to_ts=1463539920000&tile_size=m

![Timeboard example](https://farm8.staticflickr.com/7772/27083651065_00b4de5e90_b.jpg

A screenboard is better for showing statuses and sharing information. Users can use the precise, drag-and-drop layout to mix and match widgets and timeframes in a customized, visually pleasing way, rendering it unnecessary for devops teams to painstakingly build their own custom dashboards simply to get critical data across their IT infrastructure to fit on one screen. Screenboards also support varied widget types: time series, color-coded numbers, event streams, text notes, and images.

Link to screenboard example: https://app.datadoghq.com/screen/85406/stephs-screenboard-example

![Screenboard example](https://farm8.staticflickr.com/7433/27015292551_b38b193bd6_b.jpg)

* Take a snapshot of your test.support.random graph and draw a box around a section that shows it going above 0.90. Make sure this snapshot is sent to your email by using the @notification

I was unable to send an email notification from my admin account to my admin email account, so I hypothesized that perhaps one cannot email-notify oneself. I created a second Datadog account using a test email and used it to notify my admin account. To double check, I also notified the test user account from my admin account. In each case, I received email notifications immediately.

I used the camera widget to take a snapshot of the test.support.random graph going above .90.

![test.support.random exceeding .90](https://farm8.staticflickr.com/7173/27015292431_b68eed5285_z.jpg)

Then I annotated the graph and mentioned '@stephaniesher18@gmail.com', which sent a snapshot to my admin email from the test account.

![Notified admin email of metric exceeding .90](https://farm8.staticflickr.com/7078/26479827753_34c6e641f8_z.jpg)

I immediately received an email notification in my admin email account.

![Received notification in admin email account](https://farm8.staticflickr.com/7296/27015292371_71603799ab_b.jpg)

To gain another data point, I reversed the process and annotated the graph from within my admin Datadog account. I annotated the test.support.random graph and sent a snapshot to my test email account.

![Notified test email of metric exceeding .90](https://farm8.staticflickr.com/7374/27083651045_cc34f517a2.jpg)

I immediately received an email notification in my test email account.

![Received email notification in test email account](https://farm8.staticflickr.com/7323/27083651055_9d30499791_b.jpg)


### Level 3 - Alerting on your Data

Since you've already caught your test metric going above 0.90 once, you don't want to have to continually watch this dashboard to be alerted when it goes above 0.90 again. So let's make life easier by creating a monitor.

* Set up a monitor on this metric that alerts you when it goes above 0.90 at least once during the last 5 minutes

Defined metric and set alert conditions: http://ge.tt/8kJUkYa2

* Bonus points: Make it a multi-alert by host so that you won't have to recreate it if your infrastructure scales up.

In the 'Monitors' tab in the Agent, I clicked into 'Manage Monitors' and defined the metric. Then I created a new multi-alert, which should trigger for new hosts as the infrastructure scales, and set alert conditions.  

![Multi-alert by host](https://farm8.staticflickr.com/7048/27015292271_f50e194ba2_b.jpg)

Here is the monitor as it appears in the list of monitors currently managed in the account: 

![Multi-alert in 'Manage Monitors'](https://farm8.staticflickr.com/7039/26479827603_6a0465fe20_b.jpg)

* Give it a descriptive monitor name and message (it might be worth it to include the link to your previously created dashboard in the message). Make sure that the monitor will notify you via email.

I kept things straightforward and named the monitor 'Metric test.support.random exceeds .90'. I included the following message: 

'''
Mongo metric test.support.random exceeds .90. See Mongo dashboard here: http://bit.ly/1TKTfKT  

To fix, follow these steps: {{fix}}

If {{solution}}, then fixed. 

Notify: @stephaniesher18@gmail.com
'''

Link to the monitor: https://app.datadoghq.com/monitors#616213?group=all&live=4h

* This monitor should alert you within 15 minutes. So when it does, take a screenshot of the email that it sends you.

Shortly after creating the monitor, I received an email notification in my admin email account that the test.support.random exceeded .90.

![test.support.random monitor triggered](https://farm8.staticflickr.com/7033/26989097902_6a0465fe20_z.jpg)

* Bonus: Since this monitor is going to alert pretty often, you don't want to be alerted when you are out of the office. Set up a scheduled downtime for this monitor that silences it from 7pm to 9am daily. Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

Scheduled downtime for out-of-office hours: 

![weekdays](https://farm8.staticflickr.com/7064/26481120543_f47616af98_b.jpg) 

![and weekends](https://farm8.staticflickr.com/7783/27051745556_9afabc84cc_b.jpg)

Received email notification at 7pm on Friday night for downtime through Monday 9am.

![Weekend downtime email notification](https://farm8.staticflickr.com/7408/27083651115_cb29a1131d_b.jpg) 

Received email notification at 7pm Monday night for downtime through Tuesday 9am, to be repeated Mon-Thurs.

![Weekday downtime email notification](https://farm8.staticflickr.com/7667/27050458766_e2ce14b6e6_b.jpg)