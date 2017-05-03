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


## The Datadog Agent and Metrics
