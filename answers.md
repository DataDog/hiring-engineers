# Datadog Hiring Challenge

## Level 0 - Setup an Ubuntu VM
I used Vagrant to spin up an Ubuntu VM.

## Level 1 - Collecting Your Data

I added some [Host map tags](https://app.datadoghq.com/infrastructure/map?fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=none&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=false&palette=green_to_orange&paletteflip=false&host=303670348 "DataDog host map tags") in the Agent config file.

![alt text](http://res.cloudinary.com/dtk22y6kq/image/upload/v1497284251/tags_txgh1g.png "tags screen shot")


After installing postgresql and the respective integration with Datadog, I wrote a custom Agent check called `test.support.random`, ensuring the installations were successful with the info command - `sudo /etc/init.d/datadog-agent info
`

![alt text](http://res.cloudinary.com/dtk22y6kq/image/upload/v1497283642/pginstall2_hatx2x.png "cmd postgres and custom agent installation")

Checking the [metrics summary](https://app.datadoghq.com/metric/summary) page is another way to make sure the metric came through:


![alt text](http://res.cloudinary.com/dtk22y6kq/image/upload/v1497284676/metricsSummary_ntbmr8.png "metrics summary page")


### Bonus Question: What is the Agent?

The Agent is software that runs in the background on your hosts, collects events and metrics from your applications, stores them, and sends them to the datadog dashboard for analysis. 

The 3 components of the Agent are the collector, which checks for integrations and metrics, dogstatsd, a server that stores all the metrics, and forwarder, which helps format the data to send to the Datadog dashboard.

## Level 2 - Visualizing Your Data

After cloning my [database integration dashboard](https://app.datadoghq.com/dash/list):

![alt text](http://res.cloudinary.com/dtk22y6kq/image/upload/v1497285220/cloned_uhfm2g.png "cloned database integration dashboard")

I added additional metrics as well as my `test.support.random` metric:

![alt text](http://res.cloudinary.com/dtk22y6kq/image/upload/v1497285138/Screen_Shot_2017-06-12_at_9.28.14_AM_o00oul.png "dashboard with added metrics")

When the graph for `test.support.random` went over .90, I highlighted the specific region and tagged myself...

![alt text](http://res.cloudinary.com/dtk22y6kq/image/upload/v1497285637/over90dash_jhqy8k.png "graph over .90")

...in order to receive an email notification:

![alt text](http://res.cloudinary.com/dtk22y6kq/image/upload/v1497285925/emailTagged_lokhdd.png "tagged in email")


### Bonus Question: What is the difference between a timeboard and a screenboard?


Timeboard | Screenboard 
------------------------ | ------------------------
Better for troubleshooting and comparison | Better for high level analysis
All graphs scoped to the same time  | Each graph can be scoped to different time 
Graphs can be shared individually | Graphs can be shared all at once
Always displayed in a grid | Custom drag and drop layout

A timeboard displays all metrics for the same scope of time.

![alt text](http://res.cloudinary.com/dtk22y6kq/image/upload/v1497286254/timeboard_iwww5r.png "timeboard")


## Level 3 - Alerting on your Data
The multi-alert by host monitor alerts me when my `test.support.random` metric goes above .90:

![alt text](http://res.cloudinary.com/dtk22y6kq/image/upload/v1497287082/monitor_q2ihwf.png "monitor configuration")

Here is the email the monitor triggers when the graph meets this threshold: 

![alt text](http://res.cloudinary.com/dtk22y6kq/image/upload/v1497288873/alertEmailTriggered_v2k0gy.png "email alert")

Since I don't want to be alerted when I'm out of the office, I scheduled downtime that silences the alert from 7pm - 9am...

![alt text](http://res.cloudinary.com/dtk22y6kq/image/upload/v1497288873/downtimeAlert_zilslh.png "downtime alert")

I enjoyed completing this challenge and look forward to next steps!
