Your answers to the questions go here.

Level 1 - Collecting your Data

Bonus question: In your own words, what is the Agent?
The agent is software that runs on hosts machines. Its primary function is to collect metric and event data to be sent to a centralized location for processing. Communication from the agent is outbound only and runs over a secure HTTPS channel. 
The agent is written in Python and is an open source project. The code can be found at https://github.com/DataDog/dd-agent. 
Its three main functions are collections of system metrics, collection of application metrics, and forwarding of system and application metrics to Datadog.
The agent runs as a service and works through a proxy. The configuration file for the agent is /etc/dd-agent/datadog.conf. 

Custom Check:
Writing a custom check is relatively straight forward using the AgentCheck interface available through the Datadog agent. It is a simple as writing a YAML configuration file and a python script of the same file name. On Linux, the configuration file gets read from /etc/dd-agent/conf.d and the custom check script is executed from /etc/dd-agent/checks.d.

Level 2 - Visualizing your Data

Bonus question: What is the difference between a timeboard and a screenboard?
A timeboard is used for troubleshooting as it gives the user a view of  graphs scoped from the same time. You can use a timeboard to make correlations between metrics.
The screenboard give the user a high level look into the systems and can be used for monitoring. The biggest difference between a timeboard and a screenboard is that a screenboard can be shared where as timeboard can not.

Cloned Dashboard:
https://app.datadoghq.com/dash/186169/lous-cloned-dashboard?live=true&page=0&is_auto=false&from_ts=1474448872829&to_ts=1474463272829&tile_size=m

Time Board:
https://app.datadoghq.com/dash/185795/lewiss-timeboard-20-sep-2016-1140?live=true&page=0&is_auto=false&from_ts=1474454619150&to_ts=1474469019150&tile_size=m

Level 3 - Alerting on your Data

Monitor:
https://app.datadoghq.com/monitors#944586?group=all&live=4h

Scheduled Downtime:
https://app.datadoghq.com/monitors#downtime?id=195589910
