Level 1 – Collect your data


Bonus question: In your own words, what is the Agent?
The Datadog agent is a program that runs on your host machine and monitors performance (CPU and memory usage) as well as events. The user can also specify custom metrics to allow the agent to keep track of. This is then all sent over by the agent to the Datadoghq site where the metrics are put to use.

Add tags in the Agent config file:



Screenshot of host and its tags on the Host Map page in Datadog:













Install a database on your machine (MySQL) and then install the respective Datadog integration for that database.


Write a custom Agent check that samples a random value. Call this new metric: test.support.random

random.py code that will send a random number to agent:

random.yaml put in config folder conf.d:







Level 2 – Visualize your Data 
Attached is an image showing a timeboard with the cloned information fom the database metrics as well as other metrics including the random test. Also attached is an image of a Screenboard test. 


Bonus question: What is the difference between a timeboard and a screenboard?
TimeBoards and ScreenBoards are two different ways that Datadog allows the user to visualize and encapsulate their data. With a TimeBoard the metrics are all synchronized and showing their data for the same time. This is useful for getting a look at all the relevant information of a system and the grid like representation of the data makes this a strong troubleshooting and correlations board. A ScreenBoard is much freer and more customizeable than a TimeBoard. With a ScreenBoard you get the feeling of having a pushboard where you can pin relevant information and keep track of everything on a much higher level. While ScreenBoards can be shared as a whole, TimeBoards can only share individual graphs.

snapshot of  test.support.random graph / draw a box around a section that shows it going above 0.90:

Make sure this snapshot is sent to your email by using the @notification







Level 3 – Alerting on your Data

Set up a monitor on this metric that alerts you when it goes above 0.90 at least once during the last 5 minutes. This is a multi-alert by host. (had to change the average to at least once)

Email alert from monitor:


Scheduled Downtime on Monitor:


