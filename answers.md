NOTE: All screenshots contained in screenshots.doc
==================================================

Level 0 Setup

I did the following:
* installed a new version of VirtualBox
* Installed Vagrant
* Installed the Ubuntu VM


Level 1 Collecting Data

I installed and started the agent on the Ubuntu VM.  Note: I had recently downloaded and installed the agent directly to my Mac.  That agent was still running, and I believe it interfered with the new agent on the Ubuntu VM.  When I shut down the Mac agent, the Ubuntu agent started reporting metrics.

What is an agent?
A piece of software that lives on or in some target and performs some local functions in a distributed system.  The functions are organized in and controlled from a central entity.

In the case of Datadog, the functions are about performance monitoring.  The agent retrieves desired data from some system target and sends it to a central server.  Depending on the nature of the agent and the target, the agent may live inside the target (as for example an app agent), live on the target (as for example a host agent), or connect to the target remotely (as for example a database integration).  In all cases, the agent retrieves the desired metrics on a regular schedule and sends them to the central destination.



I located and edited datadog.conf with three tags: os:ubuntu, host:mac, context:lab.

https://app.datadoghq.com/dash/host/344920647?live=true&page=0&is_auto=false&from_ts=1506134893187&to_ts=1506138493187&tile_size=m


I installed MySQL 5.5.

I wrote a custom check using random.random().  Code: (Random.py)

import random
from checks import AgentCheck
class RandomCheck( AgentCheck ):
  def check( self, instance ):
      self.gauge( 'test.support.random', random.random() )


I cloned the MySQL dashboard and added metrics to it
* To the graph of max open connections, I added max available connections
* To the graph of slow queries, I added all queries
* To the graph of Data Reads, I added Writes
* I added a new graph of the random numbers metric

https://app.datadoghq.com/dash/363587/custom-metrics---mysql-david?live=true&page=0&is_auto=false&from_ts=1506134855168&to_ts=1506138455168&tile_size=m

Question: timeboard vs screenboard

* Time board: a set of widgets that all have the same time range, to compare and juxtapose different metrics in the same time range.  The timeboard automatically synchronizes the time frames. Use this for troubleshooting.
* Screen board: a set of widgets that can pull together any combination of data and time ranges, with different views (gauges, pie charts, status lights as well as time series).  Use this to provide a broader view, such as to watch the overall health of a system.


Level 3 Alerting

I set up a monitor with these characteristics:
* Critical alert (red) when average over last 5 minutes value > .90 
* Warning (yellow) when average over last 5 minutes value > .75
* Use Multi-Alert on hosts
* Downtime: 7a - 10p every day

https://app.datadoghq.com/monitors#2878291?group=all&live=4h

Average was not producing any alerts, so I changed the setting to "At least once"

