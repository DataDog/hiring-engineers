Level 1 - Collecting your Data

###Sign up for Datadog (use "Datadog Recruiting Candidate" in the "Company" field), get the Agent reporting metrics from your local machine.
###Bonus question: In your own words, what is the Agent?

 The Agent is software, written in python, that can be installed on the user's hosts to help monitor them. It is what allows the user to easily configure and customize what metrics they need to monitor.

###Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

I have added a copy of the config file to this github repo, indicating the tags I attached to the local host and a screenshot of the hostmap.
![Host map](/Hostmap.png)


Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
Write a custom Agent check that samples a random value. Call this new metric: test.support.random
