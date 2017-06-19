Your answers to the questions go here.
Level 1 :
What is an agent ?
An agent is a software which purpose is to be the interface between the user and a service.
When a user is browing the web, it connect to services throught its browser; in this case, the brower is the agent.
In the case of datadog, the agent is the software that connects to datadog server. 

Level 2 :
What is the difference between a timeboard and a screenboard?
A timeboard will provide a certain amount of data for a period of time. 
For example, the evolution of disk memory usage within the last hour.
A screenboard will provide a certain amount of data at a specific instant.
For example, the disk memory usage at the present moment.










from checks import AgentCheck

import random

class HelloCheck(AgentCheck):
    def check(self, instance):
        self.gauge('test.support.random', random.random())		

init_config:

instances:
    [{}]
from checks import AgentCheck

class HelloCheck(AgentCheck):
    def check(self, instance):
        self.gauge('test.support.max', 0.9)		

init_config:

instances:
    [{}]

{
	name alert mysql,
	type metric alert,
	query sum(last_5m)summysql.innodb.data_reads{hostDESKTOP-AE0VVCH}  20,
	message @hicham.bennis@hotmail.fr,
	tags [],
	options {
		notify_audit true,
		locked true,
		timeout_h 0,
		silenced {},
		include_tags false,
		thresholds {
			critical 20,
			warning 2
		},
		require_full_window false,
		new_host_delay 300,
		notify_no_data false,
		renotify_interval 0,
		evaluation_delay 60,
		no_data_timeframe 10
	}
}
{
	"name": "random test",
	"type": "metric alert",
	"query": "max(last_5m):avg:test.support.random{host:DESKTOP-AE0VVCH} > 0.9",
	"message": "@hicham.bennis@hotmail.fr there is a problem with the random metric, please take a look.",
	"tags": [],
	"options": {
		"notify_audit": false,
		"locked": false,
		"timeout_h": 0,
		"silenced": {
			"host:DESKTOP-AE0VVCH": 1497942000
		},
		"include_tags": true,
		"thresholds": {
			"critical": 0.9
		},
		"require_full_window": true,
		"new_host_delay": 300,
		"notify_no_data": false,
		"renotify_interval": 0,
		"evaluation_delay": "",
		"no_data_timeframe": 10
	}
}



