# Level 1

1. Sign up for Datadog (use "Datadog Recruiting Candidate" in the "Company" field), get the Agent reporting metrics from your local machine.

![ScreenShot](/screenshots/Signup.png)

Bonus question: In your own words, what is the Agent?

   The Agent is small software that collects data and events that runs on a host. It will collect data such as memory and CPU and send the metrics to the monitoring system application.

2. Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

Completed
Tags were added through the Datadog config file as brianlee, hosttest, tagtest
This is the result from adding tags to the Agent config file.
![ScreenShot](/screenshots/Tags.png)

3. Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

Completed
PostgreSQL was installed and the database was named datadog, the user however was my computer name under 'ProfoundPupil'.
Below is the screenshot of postgresql showing up in checks using info command.
![ScreenShot](/screenshots/Postgresql1.png)

Below is the postgres.yaml config code.
![ScreenShot](/screenshots/Postgresql2.png)

Below is the confirmation from the Datadog application that postgres was integrated.
![ScreenShot](/screenshots/Postgresql3.png)

4. Write a custom Agent check that samples a random value. Call this new metric: test.support.random

Here is a snippet that prints a random value in python:

import random
print(random.random())

I have included the files for making a custom Agent check of random under the checks folder.
It includes the python and yaml files.

Below is the screenshot of running the custome Agent check.
![ScreenShot](/screenshots/RandomCheck.png)

# Level 2 - Visualizing your Data

1. Since your database integration is reporting now, clone your database integration dashboard and add additional database metrics to it as well as your test.support.random metric from the custom Agent check.

Completed
![ScreenShot](/screenshots/ScreenboardClone.png)

Bonus question: What is the difference between a timeboard and a screenboard?
   A timeboard has all the graphs always scoped at the same time and can be shared individually. These are more suitable 

   A screenboard can be shared as a whole and is a read-only entity. The screenboard can have widgets and timeframes and custom drag and drop layouts.

2. Take a snapshot of your test.support.random graph and draw a box around a section that shows it going above 0.90. Make sure this snapshot is sent to your email by using the @notification

Completed
![ScreenShot](/screenshots/MonitorRandomGraph.png)

# Level 3 - Alerting on your Data

1. Since you've already caught your test metric going above 0.90 once, you don't want to have to continually watch this dashboard to be alerted when it goes above 0.90 again. So let's make life easier by creating a monitor.

Set up a monitor on this metric that alerts you when it goes above 0.90 at least once during the last 5 minutes

Bonus points: Make it a multi-alert by host so that you won't have to recreate it if your infrastructure scales up.

Completed
![ScreenShot](/screenshots/HostAlert.png)

   I setup the alert to retrieve from the host tag rather than the host itself so the user can just add the tag to whatever host they want this monitor to be on.


2. Give it a descriptive monitor name and message (it might be worth it to include the link to your previously created dashboard in the message). Make sure that the monitor will notify you via email.
This monitor should alert you within 15 minutes. So when it does, take a screenshot of the email that it sends you.

Completed
![ScreenShot](/screenshots/DatadogEmail.png)

Bonus: Since this monitor is going to alert pretty often, you don't want to be alerted when you are out of the office. Set up a scheduled downtime for this monitor that silences it from 7pm to 9am daily. Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

Completed
![ScreenShot](/screenshots/DowntimeSetup.png)

This is the email notification for the start of the downtime scheduled.
![ScreenShot](/screenshots/DowntimeConfirm.png)