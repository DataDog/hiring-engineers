## Level 0 (optional) - Setup an Ubuntu VM

I used [Vagrant](https://www.vagrantup.com/intro/index.html) with the recommended [hashicorp precise64](https://atlas.hashicorp.com/hashicorp/boxes/precise64) box with Virtualbox which is a standard Ubuntu 12.04 LTS 64-bit box.

## Level 1 - Collecting your Data

**Bonus question: In your own words, what is the Agent?**

The Agent is software that runs on hosts, collecting valuable data and performance metrics about systems, applications, and select integrations to be sent to the Datadog dashboard. 

**Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.**

Added two tags `region:us-west-1` and `owner:alibaker` to Agent config file.

Modified agent config file - `/etc/dd-agent/datadog.conf`:

![agent config](http://i.imgur.com/vW6yIVY.png)

Screenshot of tags on the Host Map page:

![tags on host map](http://i.imgur.com/qXpur1S.png)

**Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.**

Installation of PostgreSQL on VM:

![postgresql installation](http://i.imgur.com/tRpfPbw.png)

Installation of PostgreSQL integration:

![postgresql integration](http://i.imgur.com/22kvHhI.png)

**Write a custom Agent check that samples a random value. Call this new metric: `test.support.random`**

Custom agent check file - `/etc/dd-agent/checks.d/test_support_random.py`:

![custom agent check file](http://i.imgur.com/3DiYAac.png)

Custom agent check config - `/etc/dd-agent/conf.d/test_support_random.yaml`:

![custom agent check config](http://i.imgur.com/b2lTBIB.png)

## Level 2 - Visualizing your Data

**Bonus question: What is the difference between a timeboard and a screenboard?**
Timeboards are for troubleshooting and correlations by viewing all graphs in the same time scope.The graphs are shown in a grid. Individual graphs can be shared on their own.

Screenboards are customizable and flexible with drag and drop widgets that can be scoped to their own custom timeframes. All graphs on the board can be shared  at once as a live, read-only version.

**Since your database integration is reporting now, clone your database integration dashboard and add additional database metrics to it as well as your `test.support.random` metric from the custom Agent check.**

Added `test.support.random`, `postgresql.max_connections`, and `system.uptime`:

![cloned dashboard added metrics](http://i.imgur.com/pkraiPS.png)

**Take a snapshot of your `test.support.random` graph and draw a box around a section that shows it going above 0.90. Make sure this snapshot is sent to your email by using the @notification.**

![random graph snapshot](http://i.imgur.com/wFK3h69.png)

## Level 3 - Alerting on your Data

**Set up a monitor on this metric that alerts you when it goes above 0.90 at least once during the last 5 minutes; Bonus points:  Make it a multi-alert by host so that you won't have to recreate it if your infrastructure scales up.**

![multi-alert by host](http://i.imgur.com/0SQJTdU.png)

**Give it a descriptive monitor name and message (it might be worth it to include the link to your previously created dashboard in the message).  Make sure that the monitor will notify you via email.This monitor should alert you within 15 minutes. So when it does, take a screenshot of the email that it sends you.**

![monitor email](http://i.imgur.com/IhZwMif.png)

**Bonus: Since this monitor is going to alert pretty often, you don't want to be alerted when you are out of the office. Set up a scheduled downtime for this monitor that silences it from 7pm to 9am daily. Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.**

![monitor downtime email](http://i.imgur.com/5DnZkYl.png)