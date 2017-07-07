## Level 1 - Collecting your Data
Sign up for Datadog (use "Datadog Recruiting Candidate" in the "Company" field), get the Agent reporting metrics from your local machine.
![system - overview](https://user-images.githubusercontent.com/29982897/27965598-e94fd076-6301-11e7-913a-1ee7eb05675b.PNG)

Bonus question: In your own words, what is the Agent?
**The agent is a metrics collector for the host machines.  This provides the most flexibility and control for collecting metrics from the host and its applications.  The agent is also a forwarder to the Datadog service.  This allows the agent to queue information and bulk send to limit the network traffic as well as route through a proxy if needed.**

Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
![host map w custom tags](https://user-images.githubusercontent.com/29982897/27965768-72f9d088-6302-11e7-93d6-e6fe75b6d2ea.PNG)

Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
![postgres](https://user-images.githubusercontent.com/29982897/27966206-04f78bfa-6304-11e7-9179-d4a370b4e708.PNG)

Write a custom Agent check that samples a random value. Call this new metric: test.support.random
Here is a snippet that prints a random value in python:
![agent check](https://user-images.githubusercontent.com/29982897/27966275-4f034720-6304-11e7-80d6-b68744f8ba36.PNG)

## Level 2 - Visualizing your Data
Since your database integration is reporting now, clone your database integration dashboard and add additional database metrics to it as well as your test.support.random metric from the custom Agent check.
![dashboard](https://user-images.githubusercontent.com/29982897/27966476-f93d9fce-6304-11e7-8289-e9df2b07f036.PNG)

Bonus question: What is the difference between a timeboard and a screenboard?
**A timeboard and a screenboard are both types of dashboards.  A timeboard is focused on a particular slice of time for all its graphs and is excellent for event correlation.  A screenboard allows the user to customize the graphs with any timeslice and is great for getting a general overview of your system health.**

Take a snapshot of your test.support.random graph and draw a box around a section that shows it going above 0.90. Make sure this snapshot is sent to your email by using the @notification
![snapshot](https://user-images.githubusercontent.com/29982897/27966574-5529f85a-6305-11e7-948a-8736ff9f2071.PNG)


## Level 3 - Alerting on your Data
Set up a monitor on this metric that alerts you when it goes above 0.90 at least once during the last 5 minutes
![monitor status](https://user-images.githubusercontent.com/29982897/27966658-9e78711c-6305-11e7-9d37-87c002bf414d.PNG)

Bonus points: Make it a multi-alert by host so that you won't have to recreate it if your infrastructure scales up.
![monitor](https://user-images.githubusercontent.com/29982897/27966668-a6f81ffe-6305-11e7-9fe6-6488e1413b71.PNG)

Give it a descriptive monitor name and message (it might be worth it to include the link to your previously created dashboard in the message). Make sure that the monitor will notify you via email.
![monitor 2](https://user-images.githubusercontent.com/29982897/27966737-fc1f1960-6305-11e7-81fc-2bac0505e123.PNG)

This monitor should alert you within 15 minutes. So when it does, take a screenshot of the email that it sends you.
![alert email](https://user-images.githubusercontent.com/29982897/27966728-f6804ec0-6305-11e7-9352-cf50ef2bf282.PNG)

Bonus: Since this monitor is going to alert pretty often, you don't want to be alerted when you are out of the office. Set up a scheduled downtime for this monitor that silences it from 7pm to 9am daily. Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.
![downtime schedule](https://user-images.githubusercontent.com/29982897/27966838-5477fe4c-6306-11e7-86d5-2e6991e37471.PNG)

![downtime](https://user-images.githubusercontent.com/29982897/27966792-24767656-6306-11e7-8db7-0d5a7c194d0a.PNG)

## Summary
This was a fun excercise that exposed me to some new technologies and took me back to my development days.  I really enjoyed exploring the potential of the Datadog product.  The possibilities seems endless and the setup was remarkably simple.  Thank you for the opportunity, and I look forward to hearing from you.

### Links
https://app.datadoghq.com/dash/317271/postgres---level-2?live=true&page=0&is_auto=false&from_ts=1499441575500&to_ts=1499445175500&tile_size=m
