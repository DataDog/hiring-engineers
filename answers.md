# Answers

**Candidate Name: Raj S** :smile:

## Collecting Metrics:

Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

**The following tags were added to the /etc/datadog-agent/datadog.yaml file**

tags:
   - environment:RajsEnv
   - OS:Ubuntu18.04
   - Monitoredby:DataDog
   
**As shown below by the arrow mark**

<img src="cm1.png">


## Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

I installed PostgreSQL on my Ubuntu 18.04.4 LTS (GNU/Linux 4.15.0-96-generic x86_64) VM

raj@raj-replicated:~$ sudo service postgresql status
● postgresql.service - PostgreSQL RDBMS
   Loaded: loaded (/lib/systemd/system/postgresql.service; enabled; vendor preset: enabled)
   Active: active (exited) since Thu 2020-04-23 21:11:12 CDT; 46min ago
 Main PID: 1081 (code=exited, status=0/SUCCESS)
    Tasks: 0 (limit: 4660)
   CGroup: /system.slice/postgresql.service

Apr 23 21:11:12 raj-replicated systemd[1]: Starting PostgreSQL RDBMS...
Apr 23 21:11:12 raj-replicated systemd[1]: Started PostgreSQL RDBMS.

<img src="cm2.png">

<img src="cm3.png">



## Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

This is a 2 step process as shown below.

**First I created the following file in /etc/datadog-agent/checks.d/mymetric.py 

>>>
```
import random

# the following try/except block will make the custom check compatible with any Agent version
try:
    # first, try to import the base class from new versions of the Agent...
    from datadog_checks.base import AgentCheck
except ImportError:
    # ...if the above failed, the check is running in Agent version < 6.6.0
    from checks import AgentCheck

# content of the special variable __version__ will be shown in the Agent status page
__version__ = "1.0.0"

class mymetric(AgentCheck):
    def check(self, instance):
        self.gauge('goawaycovid19.my_metric', random.randint(0,1000), tags=['TAG_KEY:TAG_VALUE'])
```

>>>>>>

## Change your check's collection interval so that it only submits the metric once every 45 seconds.

**Second is to create a corresponding file in /etc/datadog-agent/conf.d/mymetric.yaml

```
init_config:

instances:
   - host: datadograj
   - min_collection_interval: 45
```

>>>>>>>

Bonus Question Can you change the collection interval without modifying the Python check file you created?

This can be accomplished by changing the jmx_check_period parameter in the /etc/datadog-agent/datadog.yaml as shown below.
```
raj@raj-replicated:/etc/datadog-agent/conf.d$ sudo cat /etc/datadog-agent/datadog.yaml | grep jmx_check
## @param jmx_check_period - integer - optional - default: 15000
# jmx_check_period: 15000
```

<hr>

#Visualizing Data:
Utilize the Datadog API to create a Timeboard that contains:

Your custom metric scoped over your host.

<img src="cm4.png">


Any metric from the Integration on your Database with the anomaly function applied.
Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.

Once this is created, access the Dashboard from your Dashboard List in the UI:

Set the Timeboard's timeframe to the past 5 minutes
Take a snapshot of this graph and use the @ notation to send it to yourself.
Bonus Question: What is the Anomaly graph displaying?

