## Answers

### Level 0 (optional) - Setup an Ubuntu VM

* While it is not required, we recommend that you spin up a fresh linux VM via Vagrant or other tools so that you don't run into any OS or dependency issues. [Here are instructions for setting up a Vagrant Ubuntu 12.04 VM.](https://www.vagrantup.com/docs/getting-started/)


### Level 1 - Collecting your Data

* Sign up for Datadog (use "Datadog Recruiting Candidate" in the "Company" field), get the Agent reporting metrics from your local machine.

Signed up under ncracker@gmail.com with api key 03a07ca04e3f11e66378b961d4fdd374.

* Bonus question: In your own words, what is the Agent?

The Datadog agent is a small program which runs in the background. In falls within a domain of programs called daemons or services. Like other daemons, it's meant to start automatically with the Operating System and runs continuously in the background and it requires no user interaction. Its sole purpose is collecting and forwarding system and services information and metrics to your Datadog account. Its functionality can be extended to provide additional metrics, either via the ready-made integrations (which work out-of-the-box) or by the administrator via its API, which allows for custom designed agent checks. The agent begins to collect data and sends it immediately after it has been installed. Data communication channel is established by the agent, over an encrypted TCP connection. It can accommodate for network interruptions by storing the data locally until the outbound link can be re-established. Additional customization to the agent’s behavior can be made via its configuration files, but isn't required.

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

My agent configuration file was modified as such to include tags:

/etc/dd-agent/datadog.conf
```
[Main]
dd_url: https://app.datadoghq.com
api_key: 03a07ca04e3f11e66378b961d4fdd374
tags: mysql, env:aws, role:database
gce_updated_hostname: yes
additional_checksd: /etc/dd-agent/checks.d/
```
<a data-flickr-embed="true"  href="https://www.flickr.com/photos/syarov/34437279241/in/dateposted-public/" title="Datadog host map – host with tags"><img src="https://c1.staticflickr.com/5/4190/34437279241_6469909b56_c.jpg" width="800" height="494" alt="Datadog host map – host with tags"></a>

* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

Ubuntu 14.04 with MySQL 5.5 installed and the Datadog integration

<a data-flickr-embed="true"  href="https://www.flickr.com/photos/syarov/33757277873/in/dateposted-public/" title="MySQL integration"><img src="https://c1.staticflickr.com/5/4188/33757277873_34f1aeb593_c.jpg" width="800" height="208" alt="MySQL integration"></a>

* Write a custom Agent check that samples a random value. Call this new metric: `test.support.random`

My custom agent check looks like this:

/etc/dd-agent/checks.d/test.py
```
from random import random
from checks import AgentCheck
class TestSupportRandom(AgentCheck):
    def check(self, instance):
        self.gauge('test.support.random', random())
```
And this is its config:

/etc/dd-agent/conf.d/test.yaml
```
init_config:

instances:
    [{}]
```

### Level 2 - Visualizing your Data

* Since your database integration is reporting now, clone your database integration dashboard and add additional database metrics to it as well as your `test.support.random` metric from the custom Agent check.

Here’s what the cloned dashboard looks like in the web UI:

<a data-flickr-embed="true"  href="https://www.flickr.com/photos/syarov/34406453902/in/dateposted-public/" title="Cloned &amp; modified dashboard"><img src="https://c1.staticflickr.com/5/4174/34406453902_6d99959a59_c.jpg" width="800" height="538" alt="Cloned &amp; modified dashboard"></a>

You can take a look at the dashboard here -> https://goo.gl/vrujQS

* Bonus question: What is the difference between a timeboard and a screenboard?

Timeboards allow for plotting metrics over time, usually to establish event correlation. They are used mainly for plotting metrics in the traditional sense. Screenboards allow for additional elements – such as iFrames, notes or event images. They give the user greater number of elements to work with and greater freedom in the layout of their presentation.

* Take a snapshot of your `test.support.random` graph and draw a box around a section that shows it going above 0.90. Make sure this snapshot is sent to your email by using the @notification

<a data-flickr-embed="true"  href="https://www.flickr.com/photos/syarov/33758213173/in/dateposted-public/" title="Random over 0.9"><img src="https://c1.staticflickr.com/5/4193/33758213173_58882aee43_z.jpg" width="640" height="299" alt="Random over 0.9"></a>

Snapshots are also covered in a daily daigest email.

<a data-flickr-embed="true"  href="https://www.flickr.com/photos/syarov/33804890723/in/dateposted-public/" title="Discussions"><img src="https://c1.staticflickr.com/5/4165/33804890723_c8f65091d3_c.jpg" width="800" height="505" alt="Discussions"></a>

### Level 3 - Alerting on your Data

Since you've already caught your test metric going above 0.90 once, you don't want to have to continually watch this dashboard to be alerted when it goes above 0.90 again.  So let's make life easier by creating a monitor.  

* Set up a monitor on this metric that alerts you when it goes above 0.90 at least once during the last 5 minutes 

Here’s the monitor’s JSON configuration
```
{
	"name": "test.support.random over 0.9 on {{host.name}}",
	"type": "metric alert",
	"query": "avg(last_5m):avg:test.support.random{*} by {host} > 0.9",
	"message": "Host {{host.name}} alerting\n\n[For more details see] (https://app.datadoghq.com/dash/286404/mysql---overview-cloned--testsupportrandom?live=true&page=0&is_auto=false&from_ts=1494301714055&to_ts=1494305314055&tile_size=m) @ncracker@gmail.com",
	"options": {
		"notify_audit": false,
		"locked": false,
		"timeout_h": 0,
		"thresholds": {
			"critical": 0.9
		},
		"new_host_delay": 300,
		"require_full_window": true,
		"notify_no_data": false,
		"renotify_interval": 0,
		"evaluation_delay": "",
		"no_data_timeframe": 10
	}
}
```
* Bonus points:  Make it a multi-alert by host so that you won't have to recreate it if your infrastructure scales up.  

An alert can be made a “Multi alert” rather than the default “Simple alert”. To do that, select Multi alert in the dropdown in step 1 – “Define the metric” when creating a new alert or when editing an existing one.  See below

<a data-flickr-embed="true"  href="https://www.flickr.com/photos/syarov/33724868134/in/dateposted-public/" title="multi-alert"><img src="https://c1.staticflickr.com/5/4164/33724868134_1fd9a33719_c.jpg" width="800" height="333" alt="multi-alert"></a>

* Give it a descriptive monitor name and message (it might be worth it to include the link to your previously created dashboard in the message).  Make sure that the monitor will notify you via email.

Here’s what the monitor alert looks like in the web UI

<a data-flickr-embed="true"  href="https://www.flickr.com/photos/syarov/34406116822/in/dateposted-public/" title="Monitor Alert"><img src="https://c1.staticflickr.com/5/4182/34406116822_9be5ea43ce_c.jpg" width="800" height="371" alt="Monitor Alert"></a>

* This monitor should alert you within 15 minutes. So when it does, take a screenshot of the email that it sends you.

Here’s the email the monitor sends

<a data-flickr-embed="true"  href="https://www.flickr.com/photos/syarov/34181430210/in/dateposted-public/" title="Screenshot 2017-05-08 21.59.58"><img src="https://c1.staticflickr.com/5/4174/34181430210_c6f49cee7f_c.jpg" width="800" height="645" alt="Screenshot 2017-05-08 21.59.58"></a>

* Bonus: Since this monitor is going to alert pretty often, you don't want to be alerted when you are out of the office. Set up a scheduled downtime for this monitor that silences it from 7pm to 9am daily. Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

Alerts can be muted during certain periods. This can be done for multiple business reasons such as scheduled outages or maintenance windows. This can be accomplished by creating a scheduled downtime. To create a scheduled downtime click on Monitors > Manage Downtime > Schedule Downtime
Here’s my scheduled downtime applied to the monitor we previously created:

<a data-flickr-embed="true"  href="https://www.flickr.com/photos/syarov/33757768753/in/dateposted-public/" title="Monitor Downtime"><img src="https://c1.staticflickr.com/5/4186/33757768753_53f0d3d7e0_z.jpg" width="565" height="640" alt="Monitor Downtime"></a>

And here’s the actual notification email:

<a data-flickr-embed="true"  href="https://www.flickr.com/photos/syarov/34567099305/in/dateposted-public/" title="Screenshot 2017-05-09 19.45.47"><img src="https://c1.staticflickr.com/5/4181/34567099305_5e0a563808_c.jpg" width="800" height="512" alt="Screenshot 2017-05-09 19.45.47"></a>
