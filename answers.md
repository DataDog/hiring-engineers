Vinnakota - Support Engineer - Hiring Exercise

STEPS FOLLOWED:

Level 1 - Collecting data
1. Created an EC2 instance using Amazon Web services and a SSH client (Putty).
2. Installed MySQL on the EC2 instance.
3. Installed the Datadog integration for MySQL.
4. Configured the integration by adding Datadog as a user and granting required permissions for metric collection.
5. Installed the Datadog Agent for Windows.
6. Added the tags vinnakotatag0 an vinnakotatag1 in datadog.config. See screenshot of the host and its tags on the Host Map page in Datadog below:

![alt text](https://github.com/madhulikavinnakota/hiring-engineers/blob/screenshots/Screenshot%20of%20host%20dell-PC%20on%20hostmap.png "Screenshot of host map with dell-PC and tags")

The Datadog Agent Manager for Windows:

![alt text](https://github.com/madhulikavinnakota/hiring-engineers/blob/screenshots/Agent%20manager.png "Screenshot of Datadog Agent Manager for Windows")

6. Installed mongodb on Windows.
7. Installed the Datadog integration for Mongo.

![alt text](https://github.com/madhulikavinnakota/hiring-engineers/blob/screenshots/Mongo%20running%20on%20dell-PC.png "Screenshot of Mongo running on Windows host")

8. Wrote a custom check my_check to collect the metric test.support.random.
   a) Used the following code in my_check.py and placed it in C:\Program Files\Datadog\Datadog Agent\agent\checks.d:
   # (C) Datadog, Inc. 2010-2016
   # Hiring Engineers
   # Vinnakota Custom Check to send a random value on each call
   import time
   #storing randomly generated value in n
   import random
   n = random.random()
   # Sends the value of n for the test.support.random metric on each call
   from checks import AgentCheck
   class CustomCheck(AgentCheck):
       def check(self, instance):
           self.gauge('test.support.random', n, tags=['custom_check'])
           
   b) Used the following code in my_check.yaml and placed it in C:\ProgramData\Datadog\conf.d:
   init_config:
   min_collection_interval: 10
   instances:
         [{}]

9. Restarted the Datadog agent on Windows using Datadog Agent Manager

![alt text](https://github.com/madhulikavinnakota/hiring-engineers/blob/screenshots/Custom%20check%20metric%20test.support.random%20on%20windows%20host.png "Screenshot of test metric running on Windows host")

Bonus section answer:
The Datadog agent is a program that runs on host systems and integrations. It monitors the systems that it runs on and collects several types of data for example performance metrics, latency, throughput etc. It can also be configured to collect custom metrics.

A number of enterprises today no longer own data centers but instead use cloud storage for the same purpose. The datadog Agent can be a useful tool to monitor and troubleshoot cloud infrastructure. The data from the agent can then be visualised on the dashboard to create alerts and events as required.

![alt text](https://github.com/madhulikavinnakota/hiring-engineers/blob/screenshots/Datadog%20agent%20structure.png "Datadog agent structure")

Level 2 - Visualizing data

1. Cloned the Mongodb integration dashboard.
2. Added the custom metric test.support.random to this clone dashboard.
3. Created a red marker to indicate on the graph, when the value of the custom metric goes above 0.90.

![alt text](https://github.com/madhulikavinnakota/hiring-engineers/blob/screenshots/Custom%20check%20metric%20on%20cloned%20dashboard.png "Screenshot of test metric on cloned dashboard")

4. Screenshot of email notification. It shows the test.support.random graph with a box around the section that shows it going above 0.90. 
![alt text](https://github.com/madhulikavinnakota/hiring-engineers/blob/screenshots/Notification%20email%20with%20red%20box%20on%20the%20graph.png "Email notification with graph highlighted in red")

Bonus section Answer:

Difference between a screenboard and a timeboard:
Datadog allows the user to create two types of dashboards - a screenboard and a timeboard.

SCREENBOARD
1. It is used to create status boards and data visualisations that can be shared with others. 
It also allows the user to specify a different time scope for each metric and each graph that they have on the board.
2. It allows the user to drag and drop widgets on to the board. It has a greater number of widgets available for use.
3. It also allows the user to customise the display on the board in order to create our own layout.
Therefore, the screenboard is more suitable for reporting.

TIMEBOARD
1. It is used to track time-varying metrics for e.g. average system load over a particular host. 
However, ALL the graphs are required to have the same time scope. This means that if the time scope is set as "Show past hour", every graph on the board display metrics collected over the past 1 hour.
2. While the timeboard allows for drag-and-drop widgets, there are fewer widget available in comparison to the Screenboard. Also, it does not allows the user to create a custom layout and all graphs are laid out according to an automatic layout.
Therefore, the timeboard is more useful for troubleshooting.

Level 3 - Alerting on data
1. Set up multi-alert by host monitor on the test.support.random metric.

![alt text](https://github.com/madhulikavinnakota/hiring-engineers/blob/screenshots/Monitor%20set%20up%20on%20custom%20metric.png "Screenshot of monitor on test metric")

Bonus section step:
Setting up of a multi-alert by host on the metric.
![alt text](https://github.com/madhulikavinnakota/hiring-engineers/blob/screenshots/Setting%20up%20a%20multi-alert%20by%20host.png "Setting up a multi-alert by host on the monitor")

2. Added a descriptive name and message for the alert notification as shown below.

![alt text](https://github.com/madhulikavinnakota/hiring-engineers/blob/screenshots/Monitor%20set%20up%20on%20custom%20metric%202.png "Screenshot of descriptive monitor on test metric")

3. Received an alert notification via email from the monitor when the value of the test metric breached 0.9. Screenshot of the email below.
Since it is a multi-alert by host, it includes the description of the host (dell-PC in this case) in the subect line of the notification email.

![alt text](https://github.com/madhulikavinnakota/hiring-engineers/blob/screenshots/Notification%20email%20from%20monitor.png "Screenshot of notification email from the monitor on test metric")

Bonus section step:
4. Set up a scheduled downtime to silence notifications between 7PM and 9AM daily. See monitor management screen below:
![alt text](https://github.com/madhulikavinnakota/hiring-engineers/blob/screenshots/Scheduled%20downtime%20on%20monitor.png "Screenshot of scheduled downtime on the monitor")

Screenshot of notification email that signals the start of scheduled downtime.
![alt text](https://github.com/madhulikavinnakota/hiring-engineers/blob/screenshots/Notification%20email%20for%20scheduled%20downtime.png "Notification email for start of scheduled downtime on the monitor")

MAIN ISSUES ENCOUNTERED:

1. RESOLVED
While installing the Datadog integration for AWS, I encountered several issues with authentication. The permissions included for the role and policy were not sufficient to allow Datadog to assume a third-party role with my AWS account.
I then referred to the required policy permissions at http://docs.datadoghq.com/integrations/aws/
Once I changed the required permissions on the AWS IAM console, the integration was installed and configured correctly.
See screenshot of AWS on hostmap below:

![alt text](https://github.com/madhulikavinnakota/hiring-engineers/blob/screenshots/AWS%20host%20map.png "Screenshot of AWS instance on host map")

2. RESOLVED
I encounted the following error when I tried to test my custom check using the shell.exe prompt:

![alt text](https://github.com/madhulikavinnakota/hiring-engineers/blob/screenshots/shell%20error%20for%20config.png "Testing error for yaml file")

I used an online YAML parser to fix the indentation and text in my yaml file, in order to resolve the issue.

3. NOT RESOLVED 
I got a MySQL client to run on my AWS EC2 instance. I also managed to get Datadog running on it. I added Datadog as a user and granted the required permissions to collect metrics. Screenshot of verification query result below:
![alt text](https://github.com/madhulikavinnakota/hiring-engineers/blob/screenshots/datadog%20running.png "Datadog added and running on MySQL")
My SSH client became inactive after I left my computer to hibernate overnight. When I logged back in, Datadog seemed to have lost the data collection from the MySQL integration. It did not start collecting even after I restarted a fresh SSH client window.
I have not managed to resolve this issue yet, so I used MongoDB installed on my Windows host as my database integration.

LINKS TO MY DATADOG DASHBOARDS:

1. Cloned dashboard with custom metric monitor:
https://app.datadoghq.com/screen/200676/mongodb-cloned

2. Screenboard:
https://app.datadoghq.com/screen/200915/madhulikas-screenboard-6-jul-2017-1618
