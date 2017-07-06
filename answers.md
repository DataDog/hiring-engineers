Vinnakota - Support Engineer - Hiring Exercise

STEPS FOLLOWED:

Level 1 - Collecting data
1. Created an EC2 instance using Amazon Web services and a SSH client (Putty).
2. Installed MySQL on the EC2 instance.
3. Installed the Datadog integration for MySQL.
4. Configured the integration by adding Datadog as a user and granting required permissions for metric collection.
5. Installed the Datadog Agent for Windows.

![alt text](https://github.com/madhulikavinnakota/hiring-engineers/blob/screenshots/Screenshot%20of%20host%20dell-PC%20%20on%20hostmap.png "Screenshot of host map with Windows and AWS")

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

Level 2 - Visualizing data

1. Cloned the Mongodb integration dashboard.
2. Added the custom metric test.support.random to this clone dashboard.
3. Created a red marker to indicate on the graph, when the value of the custom metric goes above 0.90.

![alt text](https://github.com/madhulikavinnakota/hiring-engineers/blob/screenshots/Custom%20check%20metric%20on%20cloned%20dashboard.png "Screenshot of test metric on cloned dashboard")

4. Screenshot of email notification. It shows the test.support.random graph with a box around the section that shows it going above 0.90. 
![alt text](https://github.com/madhulikavinnakota/hiring-engineers/blob/screenshots/Notification%20email%20with%20red%20box%20on%20the%20graph.png "Email notification with graph highlighted in red")

Bonus section Answer:

tbd


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
