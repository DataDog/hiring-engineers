Your answers to the questions go here.

**Level 0 (optional) - Setup an Ubuntu VM**

* While it is not required, we recommend that you spin up a fresh linux VM via Vagrant or other tools so that you don't run into any OS or dependency issues. Here are instructions for setting up a Vagrant Ubuntu 12.04 VM.

[Bruce] - Please see the two below screenshots showing the "vagrant status", along with the Ubuntu VM running within Virtual Box:

![Preview](https://github.com/brucepenn/hiring-engineers/blob/solutions-engineer/Vagrant%20Status.png)

![Preview](https://github.com/brucepenn/hiring-engineers/blob/solutions-engineer/Virtual%20Box%20Showing%20VM%20Running%20.png)

**Level 1 - Collecting your Data**

* Bonus question: In your own words, what is the Agent?

[Bruce] - The agent is a python process that runs on a given host and monitors resources, applications, etc... on that host by executing a series of "checks".  The agent then sends the collected information from these checks to the Datadog Cloud to in order to monitor an  entire infrastucture with an emphasis on meeting performance SLAs.

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

[Bruce] - Please see the screenshot below showing my Ubuntu host and its tags on the Host Map page:

![Preview](https://github.com/brucepenn/hiring-engineers/blob/solutions-engineer/My%20host%20and%20its%20tags%20on%20the%20Host%20Map.png)

* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

[Bruce] - Please see a screenshot from Dashboard List showing the MySQL - Overview Dashboard being listed, along with a screenshot showing that the MySQL tag has now been added to the Host Map page:

![Preview](https://github.com/brucepenn/hiring-engineers/blob/solutions-engineer/Dashboard%20List.png)

![Preview](https://github.com/brucepenn/hiring-engineers/blob/solutions-engineer/My%20host%20and%20its%20tags%20on%20the%20Host%20Map%20with%20MySQL.png)

* Write a custom Agent check that samples a random value. Call this new metric: test.support.random

**Level 2 - Visualizing your Data**

* Since your database integration is reporting now, clone your database integration dashboard and add additional database metrics to it as well as your test.support.random metric from the custom Agent check.

[Bruce] - 

* Bonus question: What is the difference between a timeboard and a screenboard?

[Bruce] - With TimeBoards, all widgets/panels on a dashboard are always based on the same moment in time.  ScreenBoards provide a high-level view of a system and are very customizable, and each widget/panel can have different windows of time.

* Take a snapshot of your test.support.random graph and draw a box around a section that shows it going above 0.90. Make sure this snapshot is sent to your email by using the @notification

[Bruce] - Please see a screenshot of the Snapshot below:



**Level 3 - Alerting on your Data**

* Set up a monitor on this metric that alerts you when it goes above 0.90 at least once during the last 5 minutes.

[Bruce] - 

* Bonus points: Make it a multi-alert by host so that you won't have to recreate it if your infrastructure scales up.

[Bruce] - Please see the screenshot below in making it a multi-alert:

* Give it a descriptive monitor name and message (it might be worth it to include the link to your previously created dashboard in the message). Make sure that the monitor will notify you via email.
* This monitor should alert you within 15 minutes. So when it does, take a screenshot of the email that it sends you.

[Bruce] - Please see a screenshot of the alert email per the 0.9 monitor.

* Bonus: Since this monitor is going to alert pretty often, you don't want to be alerted when you are out of the office. Set up a scheduled downtime for this monitor that silences it from 7pm to 9am daily. Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

[Bruce] - Please see a screenshot of the scheduled downtime, along with the associated email:



**Helpful Links:**
