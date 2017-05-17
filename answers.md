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


## Table of Contents

* [Level 0 - Setup](#level-0---setup)
  * [Ubuntu Install](#ubuntu-install)
* [Level 1 - Collecting your Data](#level-1---collecting-your-data)
  * [Agent Install](#agent-install)
  * [Tags](#tags)
  * [Integrations](#integrations)
  * [Custom Agent Check](#custom-agent-check)
* [Level 2 - Visualizations](#level-2---visualizations)
  * [Dashboards](#dashboards)
  * [TimeBoard vs Screenboard](#timeboard-vs-screenboard)
  * [Snapshots](#snapshots)
* [Level 3 - Alerting](#level-3---alerting)
  * [Monitors](#monitors)
  * [Alerting](#alerting)
  * [Downtime Scheduling](#downtime-scheduling)
* [Conclusion](#conclusion)
* [Helpful Links](#helpful-links)
 



## Level 0 - Setup



### Ubuntu Install
Downloaded ISO for [Ubuntu](https://www.ubuntu.com/download) version 16.04 (Xenial Xerus)

Installed [VirtualBox](https://www.virtualbox.org/wiki/Downloads) 5.1.22

Launched Ubuntu VM with a 1G memory, 10G disk for hosting the Datadog agent and associated integrations. Snapshots were saved every level to recreate/rebuild technical challenge if needed.



## Level 1 - Collecting your data

1. Sign up for Datadog (use "Datadog Recruiting Candidate" in the "Company" field), get the Agent reporting metrics from your local machine.

### Agent Install

To install the agent, you simply navigate to the agent installer page under [Integrations > Agent](https://app.datadoghq.com/account/settings#agent/ubuntu) and paste the below command (with API key) into your Ubuntu linux console. The Datadog agent will self-install, verify communication with Datadog servers and add itself as a service on the host. 

Configuration files can be found at ```/etc/dd-agent/```

```bash
DD_API_KEY=[API KEY] bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/dd-agent/master/packaging/datadog-agent/source/install_agent.sh)"
```

2. Bonus question: In your own words, what is the Agent?


> The Datadog agent is a multi-use tool, deployable to hosts and enables metrics collection for the Datadog service in "on-premise" environments. To support a wide variety of possible use cases, the agent contains a collector, a custom variant of statsd (a time based metrics aggregation sub-service called dogstatsd), and event forwarding engine that securely relays data to the cloud.



### Tags

3. Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

Tags can be easily added via API, editing configuration files in the Datadog agent, or via the UI. Tags are great when working with services and other objects at scale. From my experience, efficient tagging leads to amazing correlation!

Added ```tags: Test, env:test, role:candidatetest, region:west``` to `/etc/dd-agent/datadog.conf`

Tags: line 31/259 of `/etc/dd-agent/datadog.conf`:
<p align="left"><img width=65% src="https://github.com/bradweinstein/hiring-engineers/blob/master/screenshots/VirtualBox_datadogvm_tags_15_05_2017_08_02_27.png"></p>

View from Datadog UI:
<p align="left"><img width=65% src="https://github.com/bradweinstein/hiring-engineers/blob/master/screenshots/VirtualBox_datadogvm_tags2_15_05_2017_08_02_27.png"></p>


### Integrations

4. Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

I went with installing MongoDB via command line. Since we're using Ubuntu 16.04 there are a few additional steps we need to take before installing the Datadog MongoDB integration. If you're interested in how to do this yourself, check out the MongoDB [install page](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/). 

Because we're using Ubuntu 16.04 there is no need to muck around with as many configuration files. All hail `systemd`.

#### A. Import public security keys 
   
     sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 0C49F3730359A14518585931BC711F9BA15703C6
    
#### B. Create list files for MongoDB 
   
     echo "deb [ arch=amd64,arm64 ] http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.4.list
   
#### C. Update apt-get
   
     sudo apt-get update
   
#### D. Install MongoDB
   
     sudo apt-get install -y mongodb-org

#### E. MongoDB database integration install: 
Simply copy paste from the [Datadog UI](https://app.datadoghq.com/account/settings#integrations/mongodb) into the mongo console. Open the MongoDB console with the command `mongo`.
```mongodb
use admin
db.auth("admin", "admin-password")
db.createUser({"user":"datadog", "pwd": "PASSWORD", "roles" : [ {role: 'read', db: 'admin' }, {role: 'clusterMonitor', db: 'admin'}, {role: 'read', db: 'local' }]})
```

And edit [/etc/dd-agent/conf.d/mongo.yaml](/conf.d/mongo.yaml):
```yaml
init_config:

...

instances:
      -   server: mongodb://datadog:RwdqaIg2CjAN1n0mESxpHBvr@localhost:27016
          tags:
              - env:test
              - region:west
      -   server: mongodb://datadog:RwdqaIg2CjAN1n0mESxpHBvr@localhost:27017
          tags:
              - env:test
              - region:west
```

#### F. Verify Datadog MongoDB agent integration install:
```bash
root@datadogvm:~# dd-agent info
====================
Collector (v 5.13.2)
====================

  Status date: 2017-05-16 18:28:18 (14s ago)
  Pid: 1375
  Platform: Linux-4.8.0-49-generic-x86_64-with-Ubuntu-16.04-xenial
  Python Version: 2.7.13, 64bit
  Logs: <stderr>, /var/log/datadog/collector.log, syslog:/dev/log

  Clocks
  ======
  
    NTP offset: 19.3469 s
    System UTC time: 2017-05-17 01:28:33.186652
  
  Paths
  =====
  
    conf.d: /etc/dd-agent/conf.d
    checks.d: /opt/datadog-agent/agent/checks.d
  
  Hostnames
  =========
  
    socket-hostname: datadogvm
    hostname: datadogvm
    socket-fqdn: datadogvm
  
  Checks
  ======
  
    mongo (5.13.2)
    --------------
      - instance #0 [ERROR]: 'localhost:27016: [Errno 111] Connection refused'
      - instance #1 [OK]
      - Collected 114 metrics, 0 events & 2 service checks
      - Dependencies:
          - pymongo: 3.2

...

```

### Custom Agent Check 

5. Write a custom Agent check that samples a random value. Call this new metric: test.support.random

To create `test.support.random` I've learned how to write a Datadog check from scratch following [this](http://docs.datadoghq.com/guides/agent_checks/) guide. The process is very easy if you're familiar with `statsd`. Simply place a check execution script in `/etc/dd-agent/checks.d/` and a configuration file in `/etc/dd-agent/conf.d` and the custom checks will be executed like any native integration. I've used `testcheck` to learn and `randomcheck` to transmit `test.support.random` to Datadog. 
 
 [/etc/dd-agent/checks.d/testcheck.py](/checks.d/testcheck.py):
 ```python
 from checks import AgentCheck
class HelloCheck(AgentCheck):
    def check(self, instance):
        self.gauge('hello.datadoggers', 1)
```
[/etc/dd-agent/checks.d/randomcheck.py](/checks.d/randomcheck.py):
```python
import random

from checks import AgentCheck
class RandomCheck(AgentCheck):
    def check(self, instance):
    #    print('test.support.random', random.random())
    #     self.service_check('test.support.random', message='test.support.random:', random.random())
    # currentRandom=random.random()
    
     self.gauge('test.support.random', random.random())
```

[/etc/dd-agent/conf.d/testcheck.yaml](/conf.d/testcheck.yaml):
```yaml
init_config:

instances:
    [{}]
 ```
 
[/etc/dd-agent/conf.d/randomcheck.yaml](/conf.d/randomcheck.yaml):
```yaml
init_config:

instances:
    [{}]
 ```
 
 To test `randomcheck` I ran the following command: 
 ```bash
 root@datadogvm:~# dd-agent check randomcheck
2017-05-16 18:26:59,668 | INFO | dd.collector | config(config.py:1139) | initialized checks.d checks: ['mongo', 'randomcheck', 'ntp', 'disk', 'testcheck', 'network']
2017-05-16 18:26:59,669 | INFO | dd.collector | config(config.py:1140) | initialization failed checks.d checks: []
2017-05-16 18:26:59,669 | INFO | dd.collector | checks.collector(collector.py:542) | Running check randomcheck
Metrics: 
[('test.support.random',
  1494984419,
  0.7399072281918588,
  {'hostname': 'datadogvm', 'type': 'gauge'})]
Events: 
[]
Service Checks: 
[]
Service Metadata: 
[{}]
    randomcheck (5.13.2)
    --------------------
      - instance #0 [OK]
      - Collected 1 metric, 0 events & 0 service checks
```
 
 
## Level 2 - Visualizations

### Dashboards
1. Since your database integration is reporting now, clone your database integration dashboard and add additional database metrics to it as well as your test.support.random metric from the custom Agent check.

Cloned MongoDB ScreenBoard to "DB Clone Dashboard", added custom metric and misc metrics:
<p align="left"><img width=65% src="https://github.com/bradweinstein/hiring-engineers/blob/master/screenshots/VirtualBox_datadogvm_screenboardclone_16_05_2017_18_54_40.png"></p>

I felt that screenboard was a bit too cluttered and created my own:
<p align="left"><img width=65% src="https://github.com/bradweinstein/hiring-engineers/blob/master/screenshots/VirtualBox_datadogvm_screenboard_16_05_2017_18_54_40.png"></p>




### TimeBoard vs Screenboard

2. Bonus question: What is the difference between a timeboard and a screenboard?

*The biggest distinction between boards is that timeboards contain graphs or metrics scoped to the same time frame appearing in a grid format. You can use these for time series based root cause analysis and event correlation. TimeBoards can only be shared to individuals.*

*Screenboards are very customizable, widget based boards. They can have checks, status, queries or any data from the Datadog system in the dashboard. Screenboards are shareable as live entities within or outside your organization. Very modular and multifunctional.*

### Snapshots

3. Take a snapshot of your test.support.random graph and draw a box around a section that shows it going above 0.90. Make sure this snapshot is sent to your email by using the @notification

Fun fact for newbies: Snapshot Notification are sent via TimeBoard *NOT* Screenboard. Maybe that will change in the future?

<p align="left"><img width=65% src="https://github.com/bradweinstein/hiring-engineers/blob/master/screenshots/datadogevent.png"></p>
<p align="left"><img width=65% src="https://github.com/bradweinstein/hiring-engineers/blob/master/screenshots/emailnotification.png"></p>



## Level 3 - Alerting

### Monitors
1. Set up a monitor on this metric that alerts you when it goes above 0.90 at least once during the last 5 minutes
2. Bonus points: Make it a multi-alert by host so that you won't have to recreate it if your infrastructure scales up.

<p align="left"><img width=65% src="https://github.com/bradweinstein/hiring-engineers/blob/master/screenshots/datadogmonitor.png"></p>
<p align="left"><img width=65% src="https://github.com/bradweinstein/hiring-engineers/blob/master/screenshots/multialert.png"></p>

### Alerting
3. Give it a descriptive monitor name and message (it might be worth it to include the link to your previously created dashboard in the message). Make sure that the monitor will notify you via email.

<p align="left"><img width=65% src="https://github.com/bradweinstein/hiring-engineers/blob/master/screenshots/monitormessage.png"></p>

4. This monitor should alert you within 15 minutes. So when it does, take a screenshot of the email that it sends you.

Monitor notifications via email:
<p align="left"><img width=65% src="https://github.com/bradweinstein/hiring-engineers/blob/master/screenshots/monitoralert.png"></p>



### Downtime Scheduling
5. Bonus: Since this monitor is going to alert pretty often, you don't want to be alerted when you are out of the office. Set up a scheduled downtime for this monitor that silences it from 7pm to 9am daily. Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

I already had a downtime schedule setup, let's change that to 7p-9a OOTO hours. I helpfully included a link for the user to revisit the schedule inside the schedule message.

<p align="left"><img width=65% src="https://github.com/bradweinstein/hiring-engineers/blob/master/screenshots/downtimeschedule2.png"></p>
<p align="left"><img width=65% src="https://github.com/bradweinstein/hiring-engineers/blob/master/screenshots/downtimeemail.png"></p>





## Conclusion

After completing this technical challenge I feel confident with a Datadog troubleshooting or installation session would look like. I'd like to give my thanks to the Datadog crew for letting me attempt this challenge.

If there are any questions please feel free to reach out via [email](mailto:bradleyseth.weinstein@gmail.com) or [LinkedIn](https://www.linkedin.com/in/bradleysweinstein/)


##### Helpful Links
* [Datadog Solutions Engineering github branch](https://github.com/DataDog/hiring-engineers/tree/solutions-engineer)
* [Datadog Docs: Agent Checks](https://docs.datadoghq.com/guides/agent_checks/)
* [Datadog Docs: Tagging Guide](https://docs.datadoghq.com/guides/tagging/)
