# Answers
___

Solutions Engineer
___


### Level 0 (optional) - Setup an Ubuntu VM
---

* While it is not required, we recommend that you spin up a fresh linux VM via Vagrant or other tools so that you don't run into any OS or dependency issues. [Here are instructions for setting up a Vagrant Ubuntu 12.04 VM.](https://www.vagrantup.com/docs/getting-started/)

Set up the Ubuntu VM by using Vagrant and started up the VM.

<img src="https://raw.githubusercontent.com/yuki0808/Images/master/20170902/20170902_000.png" width="50%" height="50%" alt="vagrant" title="vagrant">

### Level 1 - Collecting your Data
---
* Sign up for Datadog (use "Datadog Recruiting Candidate" in the "Company" field), get the Agent reporting metrics from your local machine.

Sign up with my email address(yuki.shimizu808@gmail.com) and installed the agent on the Ubuntu VM to report the metrics of the machine.


1. Sign up

<img src="https://raw.githubusercontent.com/yuki0808/Images/master/20170902/20170902_001_01.png" width="50%" height="50%" alt="signup01" title="signup01">

2. Installed Agent
 
Get API Key

<img src="https://raw.githubusercontent.com/yuki0808/Images/master/20170902/20170902_003.png" width="50%" height="50%" alt="installagent02" title="installagent02">

 Install Agent on VM

<img src="https://raw.githubusercontent.com/yuki0808/Images/master/20170902/20170902_004.png" width="50%" height="50%" alt="installagent03" title="installagent03">

<img src="https://raw.githubusercontent.com/yuki0808/Images/master/20170902/20170902_005.png" width="50%" height="50%" alt="installagent04" title="installagent04">

3. Dashboad Report Screen
 
  <img src="https://raw.githubusercontent.com/yuki0808/Images/master/20170902/20170902_006.png" width="50%" height="50%" alt="dashboard01" title="dashboard01">
 
  <img src="https://raw.githubusercontent.com/yuki0808/Images/master/20170902/20170902_007.png" width="50%" height="50%" alt="dashboard02" title="dashboard02">
 


* Bonus question: In your own words, what is the Agent?

The Datadog Agent is a software which developed in Python language and runs on various platforms such as Windows, Linux(CentOS, RedHat, Ubuntu...), and MacOS.
It collects the machine's system resources, data, metric, and events (e.g. CPU, Memory, Disk IO, Networking Usage) .
The agent gathers the machine's data and send the data to Datadog to monitor the machine's performance.


* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

1. Edit Agent config File

Agent config file on the VM

```
/etc/dd-agent/datadog.conf
```

Edit the config file to add tags.

  <img src="https://raw.githubusercontent.com/yuki0808/Images/master/20170902/20170902_008_01.png" width="50%" height="50%" alt="conffile01" title="conffile01">
 
  <img src="https://raw.githubusercontent.com/yuki0808/Images/master/20170902/20170902_008_02.png" width="50%" height="50%" alt="conffile02" title="conffile02">

Diff result of between the original file and edited file

  <img src="https://raw.githubusercontent.com/yuki0808/Images/master/20170902/20170902_008_03.png" width="50%" height="50%" alt="conffile03" title="conffile03">


2. Edit Agent config File

Before add the tags.

<img src="https://raw.githubusercontent.com/yuki0808/Images/master/20170902/20170902_008.png" width="50%" height="50%" alt="conffile04" title="conffile04">

After add the tags.

<img src="https://raw.githubusercontent.com/yuki0808/Images/master/20170902/20170902_009.png" width="50%" height="50%" alt="conffile05" title="conffile05">

* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

1. Install MySQL Datbase on the VM.

<img src="https://raw.githubusercontent.com/yuki0808/Images/master/20170902/20170902_010.png" width="50%" height="50%" alt="mysql01" title="mysql01">

<img src="https://raw.githubusercontent.com/yuki0808/Images/master/20170902/20170902_011.png" width="50%" height="50%" alt="mysql02" title="mysql02">


2. Install the respective Datadog integration for MySQL. 
 
Create the datadog user and grant privileges.

<img src="https://raw.githubusercontent.com/yuki0808/Images/master/20170902/20170902_012.png" width="50%" height="50%" alt="mysql03" title="mysql03">

<img src="https://raw.githubusercontent.com/yuki0808/Images/master/20170902/20170902_013.png" width="50%" height="50%" alt="mysql04" title="mysql04">

Create and edit the mysql configuration file.

```
/etc/dd-agent/conf.d/mysql.yaml
```

<img src="https://raw.githubusercontent.com/yuki0808/Images/master/20170902/20170902_014.png" width="50%" height="50%" alt="mysql05" title="mysql05">

Restart Agent

<img src="https://raw.githubusercontent.com/yuki0808/Images/master/20170902/20170902_015.png" width="50%" height="50%" alt="mysql06" title="mysql06">

Check the status by using [info] command.

<img src="https://raw.githubusercontent.com/yuki0808/Images/master/20170902/20170902_016.png" width="50%" height="50%" alt="mysql07" title="mysql07">


3. Dashboard Report

See the dashboard report so that the mysql joined the part of the metric targets.

<img src="https://raw.githubusercontent.com/yuki0808/Images/master/20170902/20170902_017.png" width="50%" height="50%" alt="mysql07" title="mysql07">


* Write a custom Agent check that samples a random value. Call this new metric: `test.support.random`

1. Create and edit the custom agent check file.

```
/etc/dd-agent/checks.d/test_random.py
```
<img src="https://raw.githubusercontent.com/yuki0808/Images/master/20170902/20170902_018.png" width="50%" height="50%" alt="custage01" title="custage01">


2. Create and edit the config file.

```
/etc/dd-agent/conf.d/test_random.yaml
```
<img src="https://raw.githubusercontent.com/yuki0808/Images/master/20170902/20170902_019.png" width="50%" height="50%" alt="custage02" title="custage02">

3. Validate the custome agent check

<img src="https://raw.githubusercontent.com/yuki0808/Images/master/20170902/20170902_020.png" width="50%" height="50%" alt="custage03" title="custage03">

4. Check the new metric `test.support.random` is monitoring on Datadog.

<img src="https://raw.githubusercontent.com/yuki0808/Images/master/20170902/20170902_020_01.png" width="50%" height="50%" alt="custage04" title="custage04">


### Level 2 - Visualizing your Data
---
* Since your database integration is reporting now, clone your database integration dashboard and add additional database metrics to it as well as your `test.support.random` metric from the custom Agent check.

1. Clone the database dashboard.

<img src="https://raw.githubusercontent.com/yuki0808/Images/master/20170902/20170902_022.png" width="50%" height="50%" alt="clone01" title="clone01">

<img src="https://raw.githubusercontent.com/yuki0808/Images/master/20170902/20170902_023.png" width="50%" height="50%" alt="clone02" title="clone02">

<img src="https://raw.githubusercontent.com/yuki0808/Images/master/20170902/20170902_024.png" width="50%" height="50%" alt="clone03" title="clone03">


2. Add `test.support.random` metric to the cloned dashboard.

<img src="https://raw.githubusercontent.com/yuki0808/Images/master/20170902/20170902_025.png" width="50%" height="50%" alt="clone04" title="clone04">

<img src="https://raw.githubusercontent.com/yuki0808/Images/master/20170902/20170902_026.png" width="50%" height="50%" alt="clone05" title="clone05">

<img src="https://raw.githubusercontent.com/yuki0808/Images/master/20170902/20170902_027.png" width="50%" height="50%" alt="clone06" title="clone06">

<img src="https://raw.githubusercontent.com/yuki0808/Images/master/20170902/20170902_028.png" width="50%" height="50%" alt="clone07" title="clone07">


* Bonus question: What is the difference between a timeboard and a screenboard?

■Timeboards 

All graphs are always scoped to the same time and graphs will always appear in a grid-like fashion. This makes them generally better for troubleshooting and correlation. Graphs from a TimeBoard can be shared individually.

■ScreenBoards 

These are flexible, far more customizable and are great for getting a high-level look into a system. They are created with drag-and-drop widgets, which can each have a different time frame.
ScreenBoards can be shared as a whole live and as a read-only entity, whereas TimeBoards cannot.


* Take a snapshot of your `test.support.random` graph and draw a box around a section that shows it going above 0.90. Make sure this snapshot is sent to your email by using the @notification

1. Set the line maker at 0.9 so easy-to-recognize to find the alert metric values.

<img src="https://raw.githubusercontent.com/yuki0808/Images/master/20170902/20170902_029_01.png" width="50%" height="50%" alt="checkvalue01" title="checkvalue01">

2. Took a snapshot of the graph status and drew the box(above 0.90) and sent via email notification(I used my other email to confirm that I get the email from the notification correctly).

<img src="https://raw.githubusercontent.com/yuki0808/Images/master/20170902/20170902_029.png" width="50%" height="50%" alt="checkvalue02" title="checkvalue02">

<img src="https://raw.githubusercontent.com/yuki0808/Images/master/20170902/20170902_030.png" width="50%" height="50%" alt="checkvalue03" title="checkvalue03">

<img src="https://raw.githubusercontent.com/yuki0808/Images/master/20170902/20170902_031.png" width="50%" height="50%" alt="checkvalue04" title="checkvalue04">


### Level 3 - Alerting on your Data
---
Since you've already caught your test metric going above 0.90 once, you don't want to have to continually watch this dashboard to be alerted when it goes above 0.90 again.  So let's make life easier by creating a monitor.  
* Set up a monitor on this metric that alerts you when it goes above 0.90 at least once during the last 5 minutes

Set the monitor on the metric like the screenshots below. [Monitors]->[New Monitor]->[Metric].

<img src="https://raw.githubusercontent.com/yuki0808/Images/master/20170902/20170902_033.png" width="50%" height="50%" alt="alert01" title="alert01">

Export JSON file

<img src="https://raw.githubusercontent.com/yuki0808/Images/master/20170902/20170902_034.png" width="50%" height="50%" alt="alert02" title="alert02">

```
{
	"name": "Alerting Test Random Value over 0.9",
	"type": "metric alert",
	"query": "max(last_5m):avg:test.support.random{*} > 0.9",
	"message": " [ALERT]Caught the test metric value which is going above 0.90. @yuki.shimizu808@gmail.com",
	"tags": [
		"*"
	],
	"options": {
		"timeout_h": 0,
		"notify_no_data": false,
		"no_data_timeframe": 10,
		"notify_audit": true,
		"require_full_window": false,
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

From the metric setting screen, change the settig value "Simple alert" to "Multi alert" from the dropdown menu at Step 2 [Define the metric].

<img src="https://raw.githubusercontent.com/yuki0808/Images/master/20170902/20170902_035.png" width="50%" height="50%" alt="alert03" title="alert03">


* Give it a descriptive monitor name and message (it might be worth it to include the link to your previously created dashboard in the message).  Make sure that the monitor will notify you via email.

From the metric setting screen, edit the message as the screenshot below at Step 4 [Say what's happening].
To descriptive the message I added the server's hostname and IP address on the title part and added the link to my dashboard on the message part.

<img src="https://raw.githubusercontent.com/yuki0808/Images/master/20170902/20170902_036.png" width="50%" height="50%" alt="alert04" title="alert04">

Export JSON file

<img src="https://raw.githubusercontent.com/yuki0808/Images/master/20170902/20170902_037.png" width="50%" height="50%" alt="alert05" title="alert05">

```
{
	"name": "Alerting Test Random Value over 0.9 on HOST {{host.name}}  {{host.ip}} ",
	"type": "metric alert",
	"query": "max(last_5m):avg:test.support.random{*} by {host} > 0.9",
	"message": " [ALERT]Caught the test metric value which is going above 0.90. \n\nRefer URL below...\nhttps://app.datadoghq.com/dash/351905/custom-metrics---mysql-cloned?live=true&page=0&is_auto=false&from_ts=1504338822746&to_ts=1504342422746&tile_size=m&fullscreen=false \n\n@yuki.shimizu808@gmail.com ",
	"tags": [
		"*"
	],
	"options": {
		"timeout_h": 0,
		"notify_no_data": false,
		"no_data_timeframe": 10,
		"notify_audit": true,
		"require_full_window": false,
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

* This monitor should alert you within 15 minutes. So when it does, take a screenshot of the email that it sends you.

The screenshot below is the alert mail that I got from Datadog monitor.

<img src="https://raw.githubusercontent.com/yuki0808/Images/master/20170902/20170902_038.png" width="50%" height="50%" alt="alert06" title="alert06">


* Bonus: Since this monitor is going to alert pretty often, you don't want to be alerted when you are out of the office. Set up a scheduled downtime for this monitor that silences it from 7pm to 9am daily. Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

To set up the scheduled downtime, I set up the settings as screenshot below. 
[Monitors]->[Manage Downtime]->[Schedule Downtime]

<img src="https://raw.githubusercontent.com/yuki0808/Images/master/20170902/20170902_039.png" width="50%" height="50%" alt="alert07" title="alert07">

The screenshot below is the  mail that I got from Datadog monitor on downtime.

<img src="https://raw.githubusercontent.com/yuki0808/Images/master/20170902/20170902_040.png" width="50%" height="50%" alt="alert08" title="alert08">
