 # Datadog Solutions Engineering Challenge

Datadog (pronounced *day-ta-dog*) is a monitoring service for cloud-scale applications. The goal is to bring together data from servers, databases, tools, and services to present a unified view of an entire technical stack. Datadog can be used for testing, debugging, correlating and resolving issues commonly seen in the IT Ops and DevOps environments. These capabilities are provided by a simple deployable agent and a SaaS-based data analytics platform. 

<p align="center"><img width=55% src="https://github.com/bradweinstein/hiring-engineers/blob/master/images/datadoglogo.png"></p>


## Main features

* Seamlessly aggregates metrics and events across the full devops stack with a deployable agent or SaaS integrations
* Monitor, troubleshoot, and optimize application performance across distributed systems
* Built-in real-time interactive dashboards offering high resolution metrics for manipulation and graphing
* Built-in sharing and change tracking, in-context discussions, annotate changes and notify team members
* Built-in alert notifier with programmable logic for multiple trigger conditions, native integrations with favorites like Slack, Pagerduty and other channels. Complete with upgrade and maintenance modes.
* Full REST API access to capture events and metrics, creating or tag servers, query Datadog information or structure dashboards in JSON. 


# Table of Contents

* [Level 0 - Setup](#level-0-setup)
  * [Ubuntu Install](#ubuntu-install)
* [Level 1 - Collecting your Data](#level-1-collecting-your-data)
  * [Agent Install](#agent-install)
  * [Tags](#tags)
  * [Integrations](#integrations)
  * [Custom Agent Check](#custom-agent-check)
* [Level 2 - Visualizations](#level-2-visualizations)
  * [Dashboards](#dashboards)
  * [TimeBoard vs Screenboard](#timeboard-vs-screenboard)
  * [Snapshots](#snapshots)
* [Level 3 - Alerting](#level-3-alerting)
  * [Monitors](#monitors)
  * [Alerting](#alerting)
  * [Downtime Scheduling](#downtime-scheduling)
* [Misc Links](#misc-links)
 


# Level 0 - Setup

## Ubuntu Install
Downloaded ISO for [Ubuntu](https://www.ubuntu.com/download) version 16.04 (Xenial Xerus)

Installed [VirtualBox](https://www.virtualbox.org/wiki/Downloads) 5.1.22

Launched Ubuntu VM with a 1G memory, 10G disk for hosting the Datadog agent and associated integrations. Snapshots were saved every level to recreate/rebuild technical challenge if needed.





# Level 1 - Collecting your data

- Sign up for Datadog (use "Datadog Recruiting Candidate" in the "Company" field), get the Agent reporting metrics from your local machine.

## Agent Install

To install the agent, you simply navigate to the agent installer page under [Integrations > Agent](https://app.datadoghq.com/account/settings#agent/ubuntu) and paste the below command (with API key) into your Ubuntu linux console. The Datadog agent will self-install, verify communication with Datadog servers and add itself as a service on the host. 

Configuration files can be found at ```/etc/dd-agent/```

```bash
DD_API_KEY=[API KEY] bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/dd-agent/master/packaging/datadog-agent/source/install_agent.sh)"
```

- Bonus question: In your own words, what is the Agent?

*The Datadog agent is a multi-use tool, deployable to hosts and enables metrics collection for the Datadog service in "on premise" environments. To support a wide variety of possible use cases, the agent contains a collector, a custom variant of statsd (a time based metrics aggregation sub-service called dogstatsd), and event forwarding engine that securely relays data to the cloud.*



## Tags
- Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

tags: Test, env:test, role:candidatetest, region:west

Tags: line 31/259 of /etc/dd-agent/datadog.conf:
<p align="left"><img width=65% src="https://github.com/bradweinstein/hiring-engineers/blob/master/screenshots/VirtualBox_datadogvm_tags_15_05_2017_08_02_27.png"></p>

View from Datadog UI:
<p align="left"><img width=65% src="https://github.com/bradweinstein/hiring-engineers/screenshots/VirtualBox_datadogvm_tags2_15_05_2017_08_02_27.png"></p>


## Integrations

- Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

MongoDB database integration install: See mongo.yaml in conf.d folder

- Write a custom Agent check that samples a random value. Call this new metric: test.support.random

## Custom Agent Check 
test.support.random: Code can be found in conf.d and checks.d. I used 'testcheck' to learn and 'randomcheck' to poll 'test.support.random'. 
 
 
# Level 2 - Visualizations

## Dashboards
- Since your database integration is reporting now, clone your database integration dashboard and add additional database metrics to it as well as your test.support.random metric from the custom Agent check.

Cloned MongoDB ScreenBoard to "DB Clone Dashboard", added custom metric and misc metrics.


## TimeBoard vs Screenboard

- Bonus question: What is the difference between a timeboard and a screenboard?

*The biggest distinction between boards is that timeboards contain graphs or metrics scoped to the same time frame appearing in a grid format. You can use these for time series based root cause analysis and event correlation. TimeBoards can only be shared to individuals.*

*Screenboards are very customizable, widget based boards. They can have checks, status, queries or any data from the Datadog system in the dashboard. Screenboards are shareable as live entities within your organization. Very modular and multifunctional.*

## Snapshots

- Take a snapshot of your test.support.random graph and draw a box around a section that shows it going above 0.90. Make sure this snapshot is sent to your email by using the @notification

Snapshot Notification are sent via TimeBoard *NOT* Screenboard. See screenshots folder of notification.png	for information sent to email notifier via UI. 
<p align="left"><img width=65% src="https://github.com/bradweinstein/hiring-engineers/blob/master/screenshots/notification.png"></p>



# Level 3 - Alerting

- Set up a monitor on this metric that alerts you when it goes above 0.90 at least once during the last 5 minutes
- Bonus points: Make it a multi-alert by host so that you won't have to recreate it if your infrastructure scales up.

See screenshot multialert.png in screenshots folder
<p align="left"><img width=65% src="https://github.com/bradweinstein/hiring-engineers/blob/master/screenshots/multialert.png"></p>


- Give it a descriptive monitor name and message (it might be worth it to include the link to your previously created dashboard in the message). Make sure that the monitor will notify you via email.
- This monitor should alert you within 15 minutes. So when it does, take a screenshot of the email that it sends you.

Monitor notification via email: see monitoralert.png in screenshots folder
<p align="left"><img width=65% src="https://github.com/bradweinstein/hiring-engineers/blob/master/screenshots/monitoralert.png"></p>


- Bonus: Since this monitor is going to alert pretty often, you don't want to be alerted when you are out of the office. Set up a scheduled downtime for this monitor that silences it from 7pm to 9am daily. Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

I already had a downtime schedule setup, let's change that to 7p-9a OOTO hours. I helpfully included a link for the user to revisit the schedule inside the schedule message.

<p align="left"><img width=65% src="https://github.com/bradweinstein/hiring-engineers/blob/master/screenshots/downtimeschedule.png"></p>

