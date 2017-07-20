Level 0 (optional) - Setup an Ubuntu VM

•While it is not required, we recommend that you spin up a fresh linux VM via Vagrant or other tools so that you don't run into any OS or dependency issues. Here are instructions for setting up a Vagrant Ubuntu 12.04 VM.

Level 1 - Collecting your Data

•Sign up for Datadog (use "Datadog Recruiting Candidate" in the "Company" field), get the Agent reporting metrics from your local machine.

•Bonus question: In your own words, what is the Agent?

Simply put, the agent is a piece of communication software that is installed on a host.  The agent is responsible for securely reporting whatever metrics is required of it to the datadog platform.  The agent is fully customizable in that it can grab information from a script (in the case of the random number exercise) or from a multitude of supported integrations.  In the example I used for this exercise, I setup postgresql on the server, a user for datadog within the instance and the correct grants for access.  Once the yaml for that specific monitor was activated with the correct configuration, a variety of different postgresql specific metrics were available in the datadog platform.

•Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

•Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

•Write a custom Agent check that samples a random value. Call this new metric:  test.support.random 

Here is a snippet that prints a random value in python:

import random
print(random.random())

Level 2 - Visualizing your Data

•Since your database integration is reporting now, clone your database integration dashboard and add additional database metrics to it as well as your  test.support.random  metric from the custom Agent check.

•Bonus question: What is the difference between a timeboard and a screenboard?

Largest difference is in how much customization can be done.  Timeboards are use metric graphs can be viewed for a given interval of time. The layouts of timeboards are automatic and can’t be customized that much.  Usually timeboards are used for quick and dirty graphs to troubleshoot an issue.  Screenboards allow for more customization, allowing for drag and drop of multiple widgets built on different metrics and time periods.  

•Take a snapshot of your  test.support.random  graph and draw a box around a section that shows it going above 0.90. Make sure this snapshot is sent to your email by using the @notification

Level 3 - Alerting on your Data

Since you've already caught your test metric going above 0.90 once, you don't want to have to continually watch this dashboard to be alerted when it goes above 0.90 again. So let's make life easier by creating a monitor.

•Set up a monitor on this metric that alerts you when it goes above 0.90 at least once during the last 5 minutes

•Bonus points: Make it a multi-alert by host so that you won't have to recreate it if your infrastructure scales up.

•Give it a descriptive monitor name and message (it might be worth it to include the link to your previously created dashboard in the message). Make sure that the monitor will notify you via email.

•This monitor should alert you within 15 minutes. So when it does, take a screenshot of the email that it sends you.

•Bonus: Since this monitor is going to alert pretty often, you don't want to be alerted when you are out of the office. Set up a scheduled downtime for this monitor that silences it from 7pm to 9am daily. Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.
