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

## Change your check's collection interval so that it only submits the metric once every 45 seconds.


Bonus Question Can you change the collection interval without modifying the Python check file you created?


