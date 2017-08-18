## Level 1 - Collecting your Data

> Bonus question: In your own words, what is the Agent?

The Datadog agent is software that is deployed onto an operating system for the purpose of conducting system, network and application monitoring functions.  With the Datadog agent installed onto each of your systems, you can gain granular insights into the underlying performance + availability of your hosts/systems in both a proactive and reactive manner for optimizing application delivery.

Because the Datadog agent has access to the local OS, it is able to provide a detailed view of the system.   Additionally, as the agent is onboard the host, there is no loss of data when the agent loses connectivity to Datadog.  The agent is also lightweight in its CPU/memory/disk footprint, while also offering action / command based capabilities in addition to the aforementioned data collection features (i.e. restart a process, reboot, etc.).

Some organizations may be “anti-agent” for any number of reasons.  Datadog understands this is the case for some environments, and as a result, an agent-optional approach can be taken whereby only a single Datadog agent needs to be deployed, from which remote monitoring metrics can be collected.    Some examples of elements where agentless data collection is applicable include the monitoring of hypervisors, network devices and more.  Cloud environments such as AWS can be monitored remotely via their API, or Datadog agents can be deployed on hosts for more granular and timely data collection.

To summarize, by strategically deploying Datadog agents across your environment, you can easily monitor local or remote systems, making this architecture ideal for managing cloud or hybrid infrastructures.

A high-level architecture diagram of Datadog can be found here:  

![arch](https://github.com/dbirck/hiring-engineers/blob/master/arch-overview.png)

> Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

I've included a copy of my datadog.conf file for reference.  The section within this file that I modified (30-32) looks like this:

    # Set the host's tags (optional)
    # tags: mytag, env:prod, role:database
    tags: Dans-Home-Network, env:testDev, role:database_managed_OS

A screen shot of the Host Map can be found here:  
![host map](https://github.com/dbirck/hiring-engineers/blob/master/datadog-host-map.png)

>Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

This process was straightforward and easy to follow due to the clear instructions provided when enabling the integration.  

>Write a custom Agent check that samples a random value. Call this new metric: test.support.random

By following the example instructions provided and replicating the file configurations for the test.support.random metric, the random value generator worked correctly and transmitted the samples to Datadog correctly.  I did need to work through this a few times, and the following command was very helpful in determining when it started to work:

    sudo -u dd-agent dd-agent check <CHECK_NAME>

I've included those 2 files with this submission:

    /etc/dd-agent/checks.d/support.py
    /etc/dd-agent/conf.d/support.yaml

## Level 2 - Visualizing your Data

> Since your database integration is reporting now, clone your database integration dashboard and add additional database metrics to it as well as your test.support.random metric from the custom Agent check.

A screen shot of my cloned database dashboard can be found here.  It contains graphs that display MySQL performance and my test.support.random metric in the lower right corner:  
![cloned dashboard](https://github.com/dbirck/hiring-engineers/blob/master/my-custom-dashboard.png)

> Bonus question: What is the difference between a timeboard and a screenboard?

The difference between a timeboard and a screenboard is that a timeboard represents a series of one or more time series graphs, while a screenboard can contain a mashup of various objects that may be related or unrelated in context and format.

A timeboard contains one or more graphs, each of which displays performance data plotted over the same time period (i.e. all graphs are always scoped to the same time) for comparison purposes and context in situations where troubleshooting is required.  Timeboards allow you to visually "align the bumps" in order to better understand performance relationships.

A screenboard can contain various objects that do not need to be related to one another in time context.  They are comprised of any number of widgets that can be dragged and dropped onto the screen to provide the author with many customization options to present relevant information as desired.  Screenboards can be shared in whole as well (while timeboards cannot).

A screenshot of a screenboard that I created during this exercise is found below:
![screenboard](https://github.com/dbirck/hiring-engineers/blob/master/my-screenboard.png)

> Take a snapshot of your test.support.random graph and draw a box around a section that shows it going above 0.90. Make sure this snapshot is sent to your email by using the @notification.

A screen shot of this email can be found below.  **Note:**  I actually did not receive this email immediately as my @notification was linked to my only Datadog email/admin user.  
![threshold](https://github.com/dbirck/hiring-engineers/blob/master/snapshot.png)

## Level 3 - Alerting on your Data

>This monitor should alert you within 15 minutes. So when it does, take a screenshot of the email that it sends you.

A screen shot of this email can be found below.  **Note:**  I actually did not receive this email immediately as my @notification was linked to my only Datadog email/admin user. 

![metric alert](https://github.com/dbirck/hiring-engineers/blob/master/metric-alert.png)

>Bonus: Since this monitor is going to alert pretty often, you don't want to be alerted when you are out of the office. Set up a scheduled downtime for this monitor that silences it from 7pm to 9am daily. Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

A screen shot of this email can be found below.  **Note:**  In this case, I had created a second Datadog user.  By mentioning @ this new user, I then received the email immediately (a nice learning experience here!).

![downtime notice](https://github.com/dbirck/hiring-engineers/blob/master/downtime.png)

## A bit more to share around integrations...

During this exercise, I also configured bi-directional integration with a popular incident management/notification product.  This combination of functionality delivers an excellent workflow between the 2 services.

A screenshot can be found below:
![PD1](https://github.com/dbirck/hiring-engineers/blob/master/pd1.png)

Thank you all for your time!
