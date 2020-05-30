# Answers

# Prerequisites - Setup the environment

**Choose an environment!**
Decided to spin up a fresh linux VM via Vagrant.
Then signed up for  Datadog (used “Datadog Recruiting Candidate” in the “Company” field).

# Collecting Metrics!

## Task: Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

**What is an agent?**
The agent is the software that reports back to the Data Dog tool. 

**Where is it's config file?**
The config file is the file datadog.yaml in the /etc/datadog-agent folder. 

###### Resources used: 
Two helpful guides https://docs.datadoghq.com/tagging/assigning_tags/?tab=agentv6v7#configuration-files & https://docs.datadoghq.com/tagging/ 

**Add tags to your agents config file aka datadog.yaml Search for "tags" and add them there.**

I added :
environment:staging
app:Postgres

![](Images/TagConfigFile.png)

**Next! Show a screenshot of your host and its tags on the Host Map page in Datadog to prove you did it!** 
![](Images/TagsonHost.png)


**Task: Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.**
I installed MongoDB. 
###### Resources:
https://gist.github.com/shimar/13381bce5c5cbeb72d801d74099ba2ec 

After making sure MongoDB was running I proceeded to set up the integration for it following the instructions here: 
https://app.datadoghq.com/account/settings#integrations/mongodb

First step was creating the Data Dog user to the database.

## On MongoDB 3.x or higher, use the createUser command.
## db.createUser({
 ##  "user":"datadog",
##  "pwd": "abc123",
##  "roles" : [
 ##   {role: 'read', db: 'admin' },
  ##  {role: 'clusterMonitor', db: 'admin'},
  ##  {role: 'read', db: 'local' }
##  ]
## })

![](Images/successfullycreatedatadogmongodbuser.png)

Second step was to create a new mongo.d/conf.yaml file in the conf.d folder and make the necessary changes to reflect my local servers information:
![](Images/mangoyaml.png)

I then restarted the agent. 

## Task: Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
In order for you to create a custom Agent, you need to create two files. 
** Make sure the name of the files are the same in both directories. **

Create /etc/datadog-agent/conf.d/custom_mymetric.yaml containing the following: 
```
init_config:
instances:
          - min_collection_interval: 45
 ```
 and created custom_mymetric.py in /etc/datadog-agent/checks.d containing the following:
 
 ```
 ## the following try/except block will make the custom check compatible with any Agent version
try:
    # first, try to import the base class from new versions of the Agent...
    from datadog_checks.base import AgentCheck
except ImportError:
    # ...if the above failed, the check is running in Agent version < 6.6.0
    from checks import AgentCheck

# content of the special variable __version__ will be shown in the Agent status page
__version__ = "1.0.0"

import random 

class HelloCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', random.randrange(0,1000), tags=['TAG_KEY:TAG_VALUE']) 
```
        
## Task: Change your check's collection interval so that it only submits the metric once every 45 seconds.

Bonus Question Can you change the collection interval without modifying the Python check file you created?
