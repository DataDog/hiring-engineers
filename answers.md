Your answers to the questions go here.

#Getting Started with DataDog

##Overview
This document will provide a walkthrough on how to set up a monitored host in Datadog, and from there, build custom a custom metric with checks and alerts.

##Level 0 (optional) - Setup an Ubuntu VM
Optional Step to avoid dependency issues

##Level 1 - Collecting your Data
You will create a DataDog Account, modify the Agent's configuration, install a database, add the DataDog integration for that DB, and write a custom agent check.

Bonus question: In your own words, what is the Agent?

##Level 2 - Visualizing your Data
You will clone the starting dashboard, add additional metrics, and make sure your email recieves a snapshot with @notification.

Bonus question: What is the difference between a timeboard and a screenboard?

##Level 3 - Alerting on your Data
You will set up a monitor for your metric (it should alert you within 15 minutes).

Bonus points: Make it a multi-alert by host so that you won't have to recreate it if your infrastructure scales up.  
Bonus: Since this monitor is going to alert pretty often, you don't want to be alerted when you are out of the office. Set up a scheduled downtime for this monitor that silences it from 7pm to 9am daily. Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.
