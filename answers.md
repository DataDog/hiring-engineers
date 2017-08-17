## Level 1 - Collecting your Data

> Bonus question: In your own words, what is the Agent?

The Datadog agent is software that is deployed onto an operating system for the purpose of conducting system, network and application monitoring functions.  With the Datadog agent installed onto each of your systems, you can gain granular insights into the underlying performance + availability of your hosts/systems in both a proactive and reactive manner for optimizing application delivery.

Because the Datadog agent has access to the local OS, it is able to provide a detailed view of the system.   Additionally, as the agent is onboard the host, there is no loss of data when the agent loses connectivity to Datadog.  The agent is also lightweight in its CPU/memory/disk footprint, while also offering action / command based capabilities in addition to the aforementioned data collection features (i.e. restart a process, reboot, etc.).

Some organizations may be “anti-agent” for any number of reasons.  Datadog understands this is the case for some environments, and as a result, an agent-optional approach can be taken whereby only a single Datadog agent needs to be deployed, from which remote monitoring metrics can be collected.    Some examples of elements where agentless data collection is applicable includes the monitoring of hypervisors, network devices and more.  Cloud environments such as AWS can be monitored remotely, or Datadog agents can be deployed on hosts for more granular data collection.

To summarize, by strategically deploying Datadog agents across your environment, you can easily monitor local or remote systems, making this architecture ideal for managing cloud or hybrid infrastructures.

A high level architecture diagram of Datadog can be found here:  

![arch](https://github.com/dbirck/hiring-engineers/blob/master/arch-overview-1.png)

> Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

A screen shot of this email can be found here:  https://www.dropbox.com/s/uw7hqk5by0s2jqi/datadog-host-map.png

-----

## Level 2 - Visualizing your Data

Bonus question: What is the difference between a timeboard and a screenboard?

The difference between a timeboard and a screenboard is that a timeboard represents a series of one or more time series graphs, while a screenboard can contain a mashup of various objects that may be related or unrelated in context and format.

A timeboard contains one more graphs, each of which displays performance data plotted over the same time period (i.e. all graphs are always scoped to the same time) for comparison purposes and context in situations where troubleshooting is required (i.e. enabling you "align the bumps" to understand performance relationships).

A screenboard can contain various objects that do not need to be related to one another in time context, and they are comprised of any number of widgets that can be dragged and dropped onto the screen to providing the author with a custom ability to present relevant information.  Screenboards can be shared in whole as well (while timeboards cannot).

Take a snapshot of your test.support.random graph and draw a box around a section that shows it going above 0.90. Make sure this snapshot is sent to your email by using the @notification.

A screen shot of this email can be found here:  
https://www.dropbox.com/s/bepjljwv2icuqoe/Screenshot%202017-08-16%2022.01.40.png?dl=0

-----

Level 3 - Alerting on your Data

This monitor should alert you within 15 minutes. So when it does, take a screenshot of the email that it sends you.

A screen shot of this email can be found here:  
https://www.dropbox.com/s/63wa6fal9914r0k/Screenshot 2017-08-16 21.44.34.png?dl=0

Bonus: Since this monitor is going to alert pretty often, you don't want to be alerted when you are out of the office. Set up a scheduled downtime for this monitor that silences it from 7pm to 9am daily. Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

A screen shot of this email can be found here:

https://www.dropbox.com/s/bf82ld4p2t4yj2p/Screenshot 2017-08-16 21.42.46.png?dl=0

## Level 3 - Alerting on your Data

>This monitor should alert you within 15 minutes. So when it does, take a screenshot of the email that it sends you.

A screen shot of this email can be found here:  

![my email](http://i.imgur.com/4UH2N1o.png)

>Bonus: Since this monitor is going to alert pretty often, you don't want to be alerted when you are out of the office. Set up a scheduled downtime for this monitor that silences it from 7pm to 9am daily. Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

A screen shot of this email can be found here:

