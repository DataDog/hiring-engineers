# Intro
This project is my demo of Datadog.  I used Docker (with compose) to set up my infrastructure.  My containers of choice were the official Datadog agent (Alpine) container and the official MySQL (Debian) container from dockerhub.  My repo contains everything needed to run the demo with the given pre-requisite that you will have Docker (with compose) installed already and run this on a Linux machine with bash, Ubuntu ideally.  I ran this on an Ubuntu 16.04.3 LTS VM (a.k.a worked on my machine).  A make file was written to simplify recreating the demo.  If you want to recreate it please do the following:

1.  git pull my branch
2.  cd into the ./demo/ folder
3.  make it_just_work

The one make command will take your Datadog API key, set up new MySQL creds, build and then start the containers.  Enjoy!


# Level 1 - Collecting Data

### What is an agent?

Agents are software programs that act on behalf of (and/or communicate with) another party, operating in a primarily autonomous manner in regards to a specific purpose or purposes. Agents are usually designed to be consume limited resources and ideally support extensible functionality.

So we've covered the definition of an agent but this will not likely bring the average user closer to understanding what an agent is.  Let’s look at some examples of agents and backtrack to the definition.  Running an antivirus is a common place to find an agent.  If you have a backup solution that pushes your data to the cloud, that will have an agent.  If you monitor your cloud infrastructure with a service like Datadog, you are running an agent.  

All of these examples are programs that are expected to do specific things like scan for viruses, check for new files or send report server metrics.  Your antivirus doesn't expect you to scan each file yourself, your backup solution doesn't expect you you to add upload each new file by hand and Datadog certainly doesn't expect you to manually push your metrics. These agents are designed to run in the autonomously in the background on your machine on behalf of your antivirus, backup provider and server monitor.

So agents are automated programs with specific purposes but having a specific purpose does not mean it can't be extensible too.  For example the Datadog agent provides several specific purposes including (but not limited to) sending your server metrics to Datadog's infrastructure.  You can write custom datadog checks and integrations to extend what you can monitor with the Datadog agent.  The agent's purpose is to monitor and report metrics but what you monitor and report on is the extensibility of the agent. Here is just some of the integrations offered by Datadog:


![alt text](https://github.com/flaresareawesome/hiring-engineers/blob/flaresareawesome-solutions-engineer/images/datadog-L1-integ-sample.png "Datadog Sample Integrations") 


So that is what an agent is.  As a side note, a good agent should ideally be lightweight as well.  How lightweight is the Datadog agent?  Using the official Alpine datadog-agent container consumed about 78.98 MiB of RAM (as per the blue line in the graph below) and less than 1% CPU at idle.  This is extremely small by today's computing standards.


![alt text](https://github.com/flaresareawesome/hiring-engineers/blob/flaresareawesome-solutions-engineer/images/datadog-L1-dd-alpine-agent-ram.png "Datadog Alpine RAM Usage")

### Add tags in Agent config
This screenshot shows how simple tagging resources in Datadog is.  In the right-corner you will find the Tags section.  Adding tags to Datadog is a simple as a config update (or updating environmental variables which is even easier if you use the Datadog container).  You can use both simple tags as well as key value pairs.

![alt text](https://github.com/flaresareawesome/hiring-engineers/blob/flaresareawesome-solutions-engineer/images/datadog-L1-host-tags.png "Datadog Agent Tags")

### Install a Database

For this demo the MySQL database engine was used.  The first screenshot in this document showing the multitude of integrations shows the MySQL integration was installed and configured.  

### Write a Custom Agent Function

Link to custom agent function



 
# Level 2 - Visualizing your Data

### Link to a Custom Database Dashboard
This is a sample dashboard created by cloning the stock MySQL database Dashboard.  Being able to do things like setting up custom formating rules was surprisingly easy.  
![alt text](https://github.com/flaresareawesome/hiring-engineers/blob/flaresareawesome-solutions-engineer/images/datadog-L2-custom-db-dash.png
 "Custom Database Dashboard")

### What is the difference between a timeboard and a screenboard?
The main differences between timeboards and screenboards is frame of reference.  Timeboards anchor all graphs to a specified time giving all graphs in a timeboard the same frame of reference.  If you change the scale (time)  all the boards in the timeboard will update to the new scale.  This is great for backtracking and seeing when issues occurred.   However for the current status of a system (such as a 30,000 foot view) screenboards offer a large range of customizations and graphs.  A screenboard would be great to use as a HUD (heads up display) whereas a timeboard is better suited for a troubleshooting or reviewing an incident in a  retrospective meeting.

### The test.support.random @notification
This is a notification from Datadog showing how easy it is to communicate with team members and stakeholders.  The area of concern is tagged and a simple @username will send the user an e-mail with the graph and conversation
![alt text](https://github.com/flaresareawesome/hiring-engineers/blob/flaresareawesome-solutions-engineer/images/datadog-L2-notification.png "Datadog User Notification")




# Level 3 - Alerting on your Data

### Alert when test.support.random is over 0.90 for 5 minutes
An alert was set up to fire if the test.support.random went over 0.90 for 5 minutes.  The screenshot below shows the test.support.random value did not climb high enough when using the 5 minute window sadly.
![alt text](https://github.com/flaresareawesome/hiring-engineers/blob/flaresareawesome-solutions-engineer/images/datadog-L3-alert-over-090.png
 "Alert over 0.90")

### Multi-Host Alert
The alert was set up as a multi-host alert and by changing the alert to fire if the average was 0.90 over 5 minutes to simply fire if the test.support.random when above 0.90 once in 5 minutes did the trick.  Here are some of the e-mail notifications that were received from the alert.  You can see there were two separate hosts that went into alert so that multi-host alerting could be confirmed.

![alt text](https://github.com/flaresareawesome/hiring-engineers/blob/flaresareawesome-solutions-engineer/images/datadog-L3-multihost-alert.png
 "Multi-host Alert")
 
 ### Mute the alarm
 Once the alarm was confirmed a recurring mainteance window was set up to avoid having an alarm fire all night long.
 
 
![alt text](https://github.com/flaresareawesome/hiring-engineers/blob/flaresareawesome-solutions-engineer/images/datadog-L3-maintenance-mode.png
 "Mute the Alert")
 
 
