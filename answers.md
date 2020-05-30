Your answers to the questions go here.

#Prerequisites - Setup the environment

Decided to spin up a fresh linux VM via Vagrant.

Then signed up for  Datadog (used “Datadog Recruiting Candidate” in the “Company” field).

##Collecting Metrics!##

Task: Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

Where to start?! 

What is an agent? The agent is the software that reports back to the Data Dog tool. 

Where is it's config file? The config file is the file datadog.yaml in the /etc/datadog-agent folder. 

References used: Two helpful guides https://docs.datadoghq.com/tagging/assigning_tags/?tab=agentv6v7#configuration-files & https://docs.datadoghq.com/tagging/ 

Add tags to your agents config file aka datadog.yaml 
Search for "tags" and add them there. 

I added :
environment:staging
app:Postgres

![](Images/TagConfigFile.png)

Next! Show a screenshot of your host and its tags on the Host Map page in Datadog to prove you did it! 
![](Images/TagsonHost.png)





Task: Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

Task: Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

Task: Change your check's collection interval so that it only submits the metric once every 45 seconds.

Bonus Question Can you change the collection interval without modifying the Python check file you created?
