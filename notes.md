# Notes on Datadog

This file was made to catalog my initial notes after reading through the reference material, before I started attempting Levels 1-3. I did this because I wanted to have and initial understanding of and be familiar with the software and components I'd be working with. 

## How to get started with Datadog

### Datadog Overview
Datadog is composed of multiple components. 
- **Integrations** - 100+ currently exist. Custom integrations can be created via the API. 
Agent is open source and a custom agent may be used. Data is treated the same whether it's in a local
datacenter or in an online service. Integrations can be SaaS, IaaS, App Servers, DBs, or pretty
much anything. AWS, Github, Apache, php, ubuntu, and slack were a few that caught my eye.
- **Infrastructure** - All monitored hosts will show up on the infrastructure overview page.
You can tag machines to indicate purpose. Tags can allow Datadog to automatically set up stats for
that host according to how the tag was previously set up. 
- **Events** - Events work lik a blog in that they are show by default as they were logged in time. 
All events can be commented on to provide addtl information for the rest of the team. e.g. "ignore
this error, I was testing something." Lots of filters available: source, tag, host, user, status, 
priority, incident. Users have lots of control, and can claim events as well as notify people and 
flag it for assistance from Datadog support
- **Dashboards** - Displays real-time performance metrics in Graphs. Each graph show event density, 
and you can zoom in on timeframes, and specify whether to display by zone, host, or total usage. 
The JSON editor of the graph is exposed to allow for addtl functions to be applied to metrics.
You can share snapshots of the graph in the stream (event stream?), click on it will take you to the
dashboard. Graphs can be embedded in an iFrame so you can display them on 3rd party sites without
granting access to your data. 
- **Monitoring** - Provides the notifications for your entire infrastructure. Choose any metrics, 
and alerts can be generated base on thresholds you set. E.g. This could be data center temp or CPU 
usage, and based on something simple like any host that goes over 100 degrees, or possibly complex 
such as alert me when 60% of hosts are over 80% CPU utilization. All data must be pushed to data dog

### Guide to Graphing in DataDog
- Graphing editor can be used both through the default GUI or by writing JSON directly 
[link](http://docs.datadoghq.com/graphingjson/)
- 3 Tabs. _Edit_ is the default and has the GUI editor, _JSON_ is the more flexible editor but 
I will need to know the Graph Def Language to use it, and _Share_ lets me embed on external web
pages (guessing this is where you get the line for the iFrame)
- For the GUI, you can add metrics, and if unsure about which ones, use the [metric explorer](https://app.datadoghq.com/metric/explorer). 
- After I select my metric(s), I can choose visuals. Timeseries, heat map, Toplist (like linux's top
command I'm guessing), change, etc.
- After visuals, I can apply filters or aggregtations (min, max, avg). 
- Graphs tend to be aggregated anyways, typically 300 points of data shown at a time. This is because
if you were polling a metric every sec, then 4 hrs of data is 14,400 data points. That might be a
bit much. 
- More advanced functions can be applied if needed
- can overlay multiple metrics for context
- Add title then save

### Guide to Monitoring in Datadog
More detail on [monitoring reference page](http://docs.datadoghq.com/monitoring)
- Monitors will do things like check metrics, show integration availability, provide alerts etc.
- Alerts work through email, hip chat, pagerduty, or thru other integrations
- Key terms: _Status_ - checks will show OK/WARNING/CRITICAL, _Check_ emits a status of course!,
 _Monitor_ - sends notifcations based on the checks, metric thresholds or alert conditions,
 _Monitor type_ - theres different kinds, _tags_ the labels discussed in overview of Infrastructure
- The main menu has atab for monitors and there is a new monitor button
- Monitors let you choose metrics to watch with 
[scopes](http://docs.datadoghq.com/graphingjson/#scope), choose 1 or more alerts, and set whether
alert is a threshold (breaches a value), or a change (if value changes or has % change, lets you
detect spikes in user sessions for an online store perhaps. Check for Black friday beginning haha)
- Can customize notifications, uses Markdown!
- can schedule downtime for monitors. Silences them for upgrades or stuff thatll throw alerts. 
Choose what is silenced, the schedule, and an optional message for notifying the team.

## The Datadog Agent and Metrics

### The Agent
- runs on all hosts so you can collect metrics, events and all the good stuff, and it sends it to 
datadog so you can use all the tools
- 3 parts: Collector - checks current machine for integrations, grabs system metrics (CPU, mem), 
Dogstatsd - can send custom metrics to this from an app, Forwarder - grabs data from the collector
and dogstatsd and sends it all to datadog
- the 3 parts are maintained by a supervisor process.
- if i dont see data in datadog, make sure there are no errors in the agent with the info command
`sudo /etc/init.d/datadog-agent info`
- [basic agent usage](http://docs.datadoghq.com/guides/basic_agent_usage/ubuntu/)
- Make sure machine time is close to datadog time, that causes problems
- integration problems, should also check info command

### Writing Agent Check
- [agent checks guide](http://docs.datadoghq.com/guides/agent_checks/)
- Agent checks are a python plugin to the agent. AgentCheck interface is where all agent checks
inherit from
- Agent checks serve a diff purpose than integrations. Agent check = from unique sys's or custom
apps. Integrations = from generally available app, or public service or open-src proj
- make sure agent is setup first
- methods similar to those in dogstatsd, all methods take same 5 args essentially. methods can be called at anypoint in check logic. at end of check function,  metrics are collected.
- can send an event at any point in check, structure more complex, make sure to read guide. 
- can report status of svc with self.service_check
- make sure to raise meaningful exceptions
- self.log is good for logging.
- all checks have config file. in conf.d. Written in YAML. file name must match check module. 
mycheck.YAML = mycheck.py
- There is a dir structure for checks, 2 places for files. /etc/dd-agent/checks.d and
/etc/dd-agent/conf.d
- HTTP checks let you check HTTP endpoints
- custom agent checks cant be called by python, call with agent 

## Notes while I was following the technical exercise

- can see my VM appear in https://app.datadoghq.com/infrastructure
- stop agent with `sudo /etc/init.d/datadog-agent stop`
- start agent with `sudo /etc/init.d/datadog-agent start`
- The configuration file for the Agent is located at /etc/dd-agent/datadog.conf
- Configuration files for integrations are located in /etc/dd-agent/conf.d/
- http://docs.datadoghq.com/integrations/postgresql/
- basic agent usage: http://docs.datadoghq.com/guides/basic_agent_usage/ubuntu/
