## Level 0 (optional) - Setup an Ubuntu VM

- While it is not required, we recommend that you spin up a fresh linux VM via Vagrant or other tools so that you don't run into any OS or dependency issues. Here are instructions for setting up a Vagrant Ubuntu 12.04 VM.

To be prepared for this exercise, the work was divided into two phases: The first phase was exploratory to understand the Datadog interface, the agent deployment options and some basic, hands-on functionality. In the second phase was to explore the deployment requirements for Cloud and more standard operating environment like Linux.

In all, there were three systems prepared for this exercise. Here is a quick list of those systems, and the Datadog integrations used. 


**Phase 1**

To get started in this exercise, I used a free desktop that runs OSX 10.11.6. 

| Environment | Operating Environment | App |
| ------------- |:-------------:| -----:|
| On-premise | OSX 10 | MySQL, Random |

**Phase 2**

| Environment | Operating Environment | App |
| ------------- |:-------------:| -----:|
| On-premise | OSX 10 | MySQL, Random |
| GCP | Debian | Apache, Random |
| GCP | Debian | MySQL |

Here is the final environment created for testing.

![alt text](https://github.com/gcastill0/hiring-engineers/blob/gcastill0-patch-1/screenshots/screenshot_000.png "All Systems")

It is important to note here that one of the most common customer objections is to see the systems working in their environment. While a good product demonstration is often a good for a quick jumpstart, setting up an agile environment from scratch has proven a convincing metaphor for engagement. 

I recommend that every systems engineer learns to deploy at least five (5) single stacks using a Cloud platform. In that manner, a “working” environment can be set up and automated within twenty minutes, and the customer can explore the Datadog value quickly.
 
The real value is the reduction of proof-of-concept work because the questions about “how-to” are removed from the stack of burden.

> In my personal catalogue, there are about one dozen operational stacks that can serve to demonstrate value quickly. I have not investigated the ease of use of the Datadog integrations with each, but I trust to learn that very quickly.
> 
> Here are some most popular stacks that customers typically request today, ranking from an ease of setup and delivery.
>  
> - Web Server: Apache (typically LAMP), and IIS
> - Database: MySQL (typically LAMP), Oracle RDBMS, and MS SQL
> - Operating Environment: RHEL, Ubuntu, CentOS, and Windows Server
> - Big Data: HDP Sandbox, Cloudera QuickStart, Splunk (on-prem and Cloud)
> - Middleware: WebSphere, WebLogic, or native JAVA/JMX


## Level 1 - Collecting Data

- Sign up for Datadog (use "Datadog Recruiting Candidate" in the "Company" field), get the Agent reporting metrics from your local machine.

### Signing up for Datadog

**Total time: 2 minutes**

The profile used to reflect my preferred online picture (from Gravatar)

Used the “Datadog Recruiting Candidate”

![alt text](https://github.com/gcastill0/hiring-engineers/blob/gcastill0-patch-1/screenshots/screenshot_001.png "Profile")

### Installing the Datadog Agent for OSX
**Total time: 3 minutes**

The installation process on OSX was straight forward. After downloading the disk image file and mounting in the system, the wizard offered easy steps to configure the installation location and to complete the process.

![alt text](https://github.com/gcastill0/hiring-engineers/blob/gcastill0-patch-1/screenshots/screenshot_002.png "Agent Install on OSX")

![alt text](https://github.com/gcastill0/hiring-engineers/blob/gcastill0-patch-1/screenshots/screenshot_003.png "Agent Install on OSX")

![alt text](https://github.com/gcastill0/hiring-engineers/blob/gcastill0-patch-1/screenshots/screenshot_004.png "Agent Install on OSX")

![alt text](https://github.com/gcastill0/hiring-engineers/blob/gcastill0-patch-1/screenshots/screenshot_005.png "Agent Install on OSX")

![alt text](https://github.com/gcastill0/hiring-engineers/blob/gcastill0-patch-1/screenshots/screenshot_006.png "Agent Install on OSX")

Notably at this stage was the need to obtain the system’s root password. This is not atypical for distributed software, but it is a source of pain for most software distribution processes inside of large organizations. 
The typical questions from clients at this stage may include the following:

  - What sort of privileges does the Datadog agent require?
  - Can we create a response file to align with our software distribution engine?
  - What does the package install?
  - Is there a way to collect the metrics without an agent?
  - We have 4,000 servers; how long will it take to deploy? And, what are your best practices?
  - How can we protect the API key?
  - How do you transfer the metric data? Is it secure while in transit?
  - Is there any identifiable data while in transit?

![alt text](https://github.com/gcastill0/hiring-engineers/blob/gcastill0-patch-1/screenshots/screenshot_007.png "Agent Install on OSX")

![alt text](https://github.com/gcastill0/hiring-engineers/blob/gcastill0-patch-1/screenshots/screenshot_008.png "Agent Install on OSX")

Once the Datadog agent installed, an installation check was done. Since there is only one user in the system, no sudo rights were used to run the commands. This procedure is vastly different from a more formal Linux or Windows environment where user privileges play a significant role in the process.

I used the command line because it is the most comfortable working environment for me. Given a Windows environment, it will require some light training to deep-dive and understand the appropriate permissions necessary for the agent installation.

![alt text](https://github.com/gcastill0/hiring-engineers/blob/gcastill0-patch-1/screenshots/screenshot_009.png "Environment Settings")

At this point, the agent has not been started, and this was confirmed using the command line. Given the environment settings were enough to handle the executable, we can run this command from any path location.

![alt text](https://github.com/gcastill0/hiring-engineers/blob/gcastill0-patch-1/screenshots/screenshot_010.png "Agent status check")

The Datadog Agent started and I checked its functional state. From the command line, we checked to see the required processes were running. In this case, we checked off the following local processes:

-	supervisord
-	dogstatd
-	ddagent, and 
-	agent

![alt text](https://github.com/gcastill0/hiring-engineers/blob/gcastill0-patch-1/screenshots/screenshot_011.png "Agent start-up")

Lastly, we checked for the actual state of the agent and checked for potential errors. For efficiency, the following is a record of the output from the datadog-agent info command:

    Benders-MacBook-Pro:etc bender$ datadog-agent info

    ====================
    Collector (v 5.11.3)
    ====================

      Status date: 2017-09-07 11:24:43 (5s ago)
      Pid: 53781
      Platform: Darwin-15.6.0-x86_64-i386-64bit
      Python Version: 2.7.12, 64bit
      Logs: <stderr>, /var/log/datadog/collector.log, syslog:/var/run/syslog

      Clocks
      ======
  
        NTP offset: -6.606 s
        System UTC time: 2017-09-07 15:24:49.650071
  
      Paths
      =====
  
        conf.d: /opt/datadog-agent/etc/conf.d
        checks.d: /opt/datadog-agent/agent/checks.d
  
      Hostnames
      =========
  
        socket-hostname: Benders-MacBook-Pro.local
        hostname: Benders-MacBook-Pro.local
        socket-fqdn: benders-macbook-pro.local
  
      Checks
      ======
  
        ntp
        ---
          - instance #0 [OK]
          - Collected 1 metric, 0 events & 1 service check
  
        disk
        ----
          - instance #0 [OK]
          - Collected 32 metrics, 0 events & 0 service checks
  
        network
        -------
          - instance #0 [OK]
          - Collected 0 metrics, 0 events & 0 service checks
  
  
      Emitters
      ========
  
        - http_emitter [OK]

    ====================
    Dogstatsd (v 5.11.3)
    ====================

      Status date: 2017-09-07 11:24:48 (1s ago)
      Pid: 53779
      Platform: Darwin-15.6.0-x86_64-i386-64bit
      Python Version: 2.7.12, 64bit
      Logs: <stderr>, /var/log/datadog/dogstatsd.log, syslog:/var/run/syslog

      Flush count: 1
      Packet Count: 0
      Packets per second: 0.0
      Metric count: 0
      Event count: 0
      Service check count: 0

    ====================
    Forwarder (v 5.11.3)
    ====================
    
      Status date: 2017-09-07 11:24:47 (2s ago)
      Pid: 53780
      Platform: Darwin-15.6.0-x86_64-i386-64bit
      Python Version: 2.7.12, 64bit
      Logs: <stderr>, /var/log/datadog/forwarder.log, syslog:/var/run/syslog

      Queue Size: 0 bytes
      Queue Length: 0
      Flush Count: 3
      Transactions received: 1
      Transactions flushed: 1
      Transactions rejected: 0
      API Key Status: API Key is valid

- Bonus question: In your own words, what is the Agent?

The Datadog Agent is a distributive software component that executes data collection methods, and collects and forwards the data to a master repository. It resides on endpoint systems, and it can serve as a collection point for multiple types of technology. Once it has a collection of data, the agent will forward the data securely to a centralized Datadog repository for analysis and presentation.

The Agent is configurable, autonomous and stateful. The underlying framework can be configured to collect data from multiple types of technology using existing templates, or by creating customized collection recipes. Once configured, the Agent will automatically gather and transfer the collected metrics to a centralized repository.

When the Agent is working, it maintains constant readiness with dedicated processes always-on; this means the Agent can fork other processes to collect metric data as needed, or on a scheduled basis.

What the Agent is not is a method of remote control for the system in which it is installed. Customers who install agents in their systems often ask if the software mechanism allows for the passing of instructions so that the system will alter its configurable state. For example, can a hacker use the Agent to shut-down, or open, a firewall port? From a cursory study, the Agent does not provide a direct call-back, or open connection, for interactive exchange of instructions.

In conclusion, the Agent is a software component to execute data collection processes, collect the data and forward the data. In its nature, the Agent is agnostic of the character of the data collection process, the collected data itself, and is security-sensitive of the destination repository to which it sends the collected data.


- Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

In this exercise we added three (3) tags to the configured system: 

### Adding tags to the configured system

**Total time: 15 minutes**

-	env:test
-	env:on-prem
-	os:osx

![alt text](https://github.com/gcastill0/hiring-engineers/blob/gcastill0-patch-1/screenshots/screenshot_012.png "Tags")

The following is a quick snapshot of the tags as configured in the system. 
From this perspective, the inclusion of the tags was quite easy. From experience, however, it is important to note that the logical association of identifiers (in this case tags) should not be arbitrary. I consider this a logical exercise, where we assign a hierarchical basis for each Agent based on their functional purpose, location, ownership, security zone, etc.
 
To handle this, I generally would enlist the help of an operations manager to define a draft and then use the output as guidance for the rest of the team. The main reason for the need is that making configuration changes to distributed agents in the field is easy within smaller environments, but very difficult with larger environments due to change control rules.

In the past, I have dealt with organizations that deal with strict change control rules. One of the prominent examples was when the change control task needed to get executed by union-based personnel. The economic impact was that updating the configuration of about 4,000 agents would require about six months of labour and about $1M in service fees.

From the exercise above, the agent was restarted for the changes to take effect. When we visited the Datadog front-end, we can see the representation of the monitored system as follows. Please pay attention to the tags as they reflect the changes made.

![alt text](https://github.com/gcastill0/hiring-engineers/blob/gcastill0-patch-1/screenshots/screenshot_013.png "Host map")

- Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

### Installing a database

**Total time: 13 minutes**

Typically, I would install this database using the LAMP stack in either Amazon Web Services, Google Cloud Platform, or as a Docker Container. At this stage, I no longer rely on VMware Virtual Machines as I don’t want to own any resources and keep an inventory of virtual machines.

For this process, the relational database of choice was MySQL. To install this, I downloaded the basic DMG version for the OSX system. After a quick installation, I also installed the MySQL Workbench and configured it to connect to the relational database.

The following screenshot shows the details of the database, some basic configuration, and proof of successful installation.

![alt text](https://github.com/gcastill0/hiring-engineers/blob/gcastill0-patch-1/screenshots/screenshot_014.png "MySQL Workbench")

Datadog Integration for MySQL

![alt text](https://github.com/gcastill0/hiring-engineers/blob/gcastill0-patch-1/screenshots/screenshot_015.png "Datadog privileged user in MySQL")

Validation:

![alt text](https://github.com/gcastill0/hiring-engineers/blob/gcastill0-patch-1/screenshots/screenshot_016.PNG "Validation")
 

![alt text](https://github.com/gcastill0/hiring-engineers/blob/gcastill0-patch-1/screenshots/screenshot_017.png "Damn you Yaml")

Yaml Configuration

![alt text](https://github.com/gcastill0/hiring-engineers/blob/gcastill0-patch-1/screenshots/screenshot_018.png "Permissions Error")
 
**Error**
 
The user privileges caused an error with the execution of the command. The MySQL instance requires privileged access in the system. In that configuration, the local user, Bender, runs as an unprivileged user and therefore did not have sufficient rights to contact execute the MySQL directives.

![alt text](https://github.com/gcastill0/hiring-engineers/blob/gcastill0-patch-1/screenshots/screenshot_019.png "Fix it, fix it, fix it... please")

The solution was to run the Agent as a privileged user. In this case, we used the following command to restart the agent. Notice the first command is a local user, whereas the second command invokes a privileged user. 

![alt text](https://github.com/gcastill0/hiring-engineers/blob/gcastill0-patch-1/screenshots/screenshot_021.png "MySQL Reporting")

After this quick fix, the configuration no longer reported an error. With this quick solution, the Agent collected all available of the metric data correctly.

![alt text](https://github.com/gcastill0/hiring-engineers/blob/gcastill0-patch-1/screenshots/screenshot_020.png "Thank goodness for Google")


Results

![alt text](https://github.com/gcastill0/hiring-engineers/blob/gcastill0-patch-1/screenshots/screenshot_022.png "Random Generator")

- Write a custom Agent check that samples a random value. Call this new metric: test.support.random

Here is a snippet that prints a random value in python:

```python
import random
print(random.random())
```

### Custom Agent Check

**Total time: 10 minutes**

Yaml Configuration

![alt text](https://github.com/gcastill0/hiring-engineers/blob/gcastill0-patch-1/screenshots/screenshot_023.png "I am OK with Yaml now.")


Python Snippet

![alt text](https://github.com/gcastill0/hiring-engineers/blob/gcastill0-patch-1/screenshots/screenshot_024.png "Python Snippet")

Error Message: There was an error message due to the carriage return and spacing in the Python code.

![alt text](https://github.com/gcastill0/hiring-engineers/blob/gcastill0-patch-1/screenshots/screenshot_025.PNG "Nothing to see here!")

To fix this, the file was written using the ```vi``` editor. It had been copied from a Atom and pasted onto a ```vi``` session.

![alt text](https://github.com/gcastill0/hiring-engineers/blob/gcastill0-patch-1/screenshots/screenshot_026.png "Let's move along people.")

**Results**

The following topology view from the Host Map dashboard shows the final result. Note that at this point, the system was collecting MySQL metrics.

![alt text](https://github.com/gcastill0/hiring-engineers/blob/gcastill0-patch-1/screenshots/screenshot_027.png "MySQL Metrics")

## Level 2 - Visualizing Data

- Since your database integration is reporting now, clone your database integration dashboard and add additional database metrics to it as well as your test.support.random metric from the custom Agent check.

### Clone a custom dashboard

**Total time: 10 minutes**

The dashboard sample below contains the cloned panels from the standard MySQL Overview. In this example there are two additional panels and we re-organized some of the most populous panels. Panel #1 shows the relationship between on-premise systems and those in the Cloud. Panel #2 showcases the values obtained from the Random Generator test. The entire dashboard works on a time-series that reflects the last hour by default.

![alt text](https://github.com/gcastill0/hiring-engineers/blob/gcastill0-patch-1/screenshots/screenshot_028.PNG "Cloned dashboard from MySQL Overview")
   
- Bonus question: What is the difference between a timeboard and a screenboard?

From my interpretation, a Timeboard is a time-series view of all relatable content in one dashboard. This permits the synchronization and correlation of events, and allows operators to compare results. A Screenboard offers the flexibility to explore data in different timeframes and to share with other users. A Screenboard can be authored with optional grid position for its panels.

I believe the user would likely pick a Timeboard for general, operational tasks which require efficiency and quick response.
A Screenboard may be used for exploration and discovery in order to determine scenarios that may be meaningful to the whole group.

- Take a snapshot of your test.support.random graph and draw a box around a section that shows it going above 0.90. Make sure this snapshot is sent to your email by using the @notification

### Create a snapshot

**Total time: 45 minutes**

From the panel describing the Random Generator test, the following snapshot was created. 

![alt text](https://github.com/gcastill0/hiring-engineers/blob/gcastill0-patch-1/screenshots/screenshot_029.png "Snapshot")

The comment in the snapshot mentioned ```@gilberto.castillo@rogers.com``` for notification. However, the messages did not show.

After waiting for the e-mail notification, I spent some time searching for a possible missing step in the setup. However, after reading the documentation and several blog posts, I was unable to find the need for an additional integration or Web-hook. I tried the basic procedure a few times and I was able to see the events in the Datadog portal, but they never arrived in my e-mail inbox.

The following is a short version of the many different attempts to complete this step.

![alt text](https://github.com/gcastill0/hiring-engineers/blob/gcastill0-patch-1/screenshots/screenshot_030.PNG "Events that reflect the dashboard capture")

My next recourse here would be to open a support ticket and request help. It should be noted, however, that the ```@notification``` does work as advertised with the monitor feature. With more time, and a little help, this should be resolved easily.


## Level 3 - Alerting on Data

- Since you've already caught your test metric going above 0.90 once, you don't want to have to continually watch this dashboard to be alerted when it goes above 0.90 again. So let's make life easier by creating a monitor.

The monitor was set according to the requirements. One thing that I noticed right away is that the default setting for the threshold was the '**average**' of the counter over the time period. The setting changed to the '**at least once**' over the time period.  

- Set up a monitor on this metric that alerts you when it goes above 0.90 at least once during the last 5 minutes

The time period in monitor was set to about 15 minutes. The main reason is that I feared alert flooding, so instead of receiving about twenty notifications per hour, I settled for about four per hour. That was a conscious choice on my part so I hope it is understood when you measure this exercise.

![alt text](https://github.com/gcastill0/hiring-engineers/blob/gcastill0-patch-1/screenshots/screenshot_031.png "Monitor for Random Generator above ninety percent")

- Bonus points: Make it a multi-alert by host so that you won't have to recreate it if your infrastructure scales up.

In order to gain a better understanding of this topic, I set up another test environment using the Google Cloud Platform. In that system, I set up a Debian system with Apache. Then I set up the integration for the Google Cloud Platform and deployed the appropriate agent.


>This additional work was an extremely good lesson in understanding the GCP API integration and the canonical differences in the Agent configuration. When working with a formal systems management structure, issuing commands, privileged access, and the location of configurations files falls under the expected tandem for that operating environment. For a simple comparison, when using the Debian '**apt**' the Agent inherits its configuration file location under ```/etc/rd.2```, ```/etc/dd``` and ```/opt/datadog-agent```. 

--

When the multi-alert was set, the issue with tags manifested. At this point, I realized that there was no easy way to consolidate the Random Test metric without a unifying term. For that reason, I grouped the values by ```env``` (a custom tag created for this exercise) and ```region``` (a default tag for the GCP integration).

![alt text](https://github.com/gcastill0/hiring-engineers/blob/gcastill0-patch-1/screenshots/screenshot_032.png "Create a multi-alert")

The results showed a breakdown in the series data, where the values are grouped by the Random Test metric value, across env:* and region:*. This was not elegant so given the same challenge again, I would be more cautious of the logical grouping. 

![alt text](https://github.com/gcastill0/hiring-engineers/blob/gcastill0-patch-1/screenshots/screenshot_033.png "Create a multi-alert")

The monitor was able to break down the different set of results and showcase them in separate series for the datagram. Note the different shades as each reflect either the on-premise location (blue) or the GCP instance (purple).


- Give it a descriptive monitor name and message (it might be worth it to include the link to your previously created dashboard in the message). Make sure that the monitor will notify you via email.

![alt text](https://github.com/gcastill0/hiring-engineers/blob/gcastill0-patch-1/screenshots/screenshot_034.png "Create a multi-alert")

- This monitor should alert you within 15 minutes. So when it does, take a screenshot of the email that it sends you.

The monitor sent an e-mail notification very quickly. The note read nicely from a mobile device and here is a sample.

![alt text](https://github.com/gcastill0/hiring-engineers/blob/gcastill0-patch-1/screenshots/screenshot_035.PNG "Notification")

- Bonus: Since this monitor is going to alert pretty often, you don't want to be alerted when you are out of the office. Set up a scheduled downtime for this monitor that silences it from 7pm to 9am daily. Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

The setup for this notification suppression was quite straight forward. Here is a quick snapshot of the event.

![alt text](https://github.com/gcastill0/hiring-engineers/blob/gcastill0-patch-1/screenshots/screenshot_038.PNG "Suppression Notification")

This is the notification received after 7PM EST regarding the event suppression.

![alt text](https://github.com/gcastill0/hiring-engineers/blob/gcastill0-patch-1/screenshots/screenshot_036.PNG "Suppression ON")

And, this is the notification received every morning before the suppression request was lifted.

![alt text](https://github.com/gcastill0/hiring-engineers/blob/gcastill0-patch-1/screenshots/screenshot_037.PNG "Suppression OFF")

