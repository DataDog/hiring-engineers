Vinnakota - Support Engineer - Hiring Exercise

STEPS FOLLOWED:
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
