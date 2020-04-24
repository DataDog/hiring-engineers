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



Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

Change your check's collection interval so that it only submits the metric once every 45 seconds.


Bonus Question Can you change the collection interval without modifying the Python check file you created?


