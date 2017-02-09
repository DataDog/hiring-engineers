Solutions engineer Exercise
Created by: Aaron Nassiry 2/8/2017
Screen recorded video:

      https://drive.google.com/open?id=0B49Pl4e8A5AeWHZZcDB1R0pxRTA

Level 1 – Collecting Data:

what is the Agent?

Datadog agent is a daemon like process that runs on the host where metrics are to be collected.
The agent is designed to collect default ‘out of the box’ metrics and performance data points for the specified Integrations and Checks, and aggregate those data points in the Datadog SaaS server. These useful metrics are then presented back to the Datadog user where they can monitor the health of their cloud scale applications and/or datacenter.

Tags:

Added below tags to datadog.conf file:

# Set the host's tags (default: no tags)	
tags: region:eastern, region:western, region:southern, region:northern

Here is the url for Infrastructure Host Map:
 https://app.datadoghq.com/infrastructure/map?fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=none&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=false&palette=green_to_orange&paletteflip=false

MongoDB Integration:  
 
 https://app.datadoghq.com/account/settings
 
Custom Check:
C:\Program Files (x86)\Datadog\Datadog Agent\checks.d\random.py content:

from checks import AgentCheck
from random import randint
class HelloCheck(AgentCheck):
    def check(self, instance):
        self.gauge('test.support.random', randint(84,1000))
        
C:\ProgramData\Datadog\conf.d\random.yaml content:
init_config:
instances:
    [{}]

Level 2 – Visualizing Data:

Cloned Dashboard called MongoDB2:  

https://app.datadoghq.com/screen/154908/mongodb2

Editing Dashboard MongoDB2: added test.support.random metric, added MongoDB Max Memory usage, and MongoDB. Uptime: 

Two types of Dashboards: ScreenBoards and Time Boards:

ScreenBoards : Can have different Widgets each pertaining to a different time frame. Comparing metrics from today with the previous week for example. ScreenBoards can be shared live and as a read-only, whereas TimeBoards cannot.

TimeBoards: all metrics are from the same time interval.
 
Level 3 – Alerting on Data
https://app.datadoghq.com/monitors#1604895?group=triggered&live=4h
https://app.datadoghq.com/monitors#1604895/edit

Schedule Downtime: https://app.datadoghq.com/monitors#downtime?
