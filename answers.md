Your answers to the questions go here.

### Level 0 (optional) - Setup an Ubuntu VM
While it is not required, we recommend that you spin up a fresh linux VM via Vagrant or other tools so that you don't run into any OS or dependency issues. Here are instructions for setting up a Vagrant Ubuntu 12.04 VM.

I installed Vagrant and Virtual Box and very quickly, following the documentation, was able to spin up a Vagrant server `vagrant up` followed by `vagrant ssh`
![Alt text](./images/vagrant.jpg "Vagrant Server")

### Level 1 - Collecting your Data

Sign up for Datadog (use "Datadog Recruiting Candidate" in the "Company" field), get the Agent reporting metrics from your local machine.
Bonus question: In your own words, what is the Agent?
Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
Write a custom Agent check that samples a random value. Call this new metric: test.support.random
Here is a snippet that prints a random value in python:

import random
print(random.random())



# Bonus question: In your own words, what is the Agent?

### Level 2 - Visualizing your Data

 Since your database integration is reporting now, clone your database intergration dashboard and add additional database metrics to it as well as your `test.support.random` metric from the custom Agent check.		 +* Since your database integration is reporting now, clone your database integration dashboard and add additional database metrics to it as well as your `test.support.random` metric from the custom Agent check.
  * Bonus question: What is the difference between a timeboard and a screenboard?		  * Bonus question: What is the difference between a timeboard and a screenboard?
  * Take a snapshot of your `test.support.random` graph and draw a box around a section that shows it going above 0.90. Make sure this snapshot is sent to your email by using the @notification		  * Take a snapshot of your `test.support.random` graph and draw a box around a section that shows it going above 0.90. Make sure this snapshot is sent to your email by using the @notification


Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
Write a custom Agent check that samples a random value. Call this new metric: test.support.random
Here is a snippet that prints a random value in python:
