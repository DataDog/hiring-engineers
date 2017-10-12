Bonus Question #1. In your own words, what is the Agent?

The Agent is software that runs on your hosts, it collects events and metrics and sends them to Datadog. Datadog then allows you to easily observe and use your monitoring and performance data.

The Agent is made up of three parts: 
1. Collector: runs checks on your machine for your integrations and captures system metrics
2. Dogstatsd: statsd backend server that recieves custom metrics from an application
3. Forwarder: sends data from dogstatsd and the collecter to datadog

Bonus Question #2. What is the difference between a timeboard and a screenboard?

Timeboards or for troubleshooting, seeing correlations, and tirage investigations.  They help pinpoint what is happening across metrics and services at the same time.  All graphs are scoped to the same time, and will appear in a grid like fashion, these graphs can only be shared individually.

Screenboards show you general status boards with the overall helath.  Screen are more flexible and customizebale than timeboards and useful for getting a high-level look into a system. These can be customized with widgets, graphs (with different time frames!), images, and visual cues to make your data presentable in any way you like. Screenboards can be shared with a public url as a read-only entity.
