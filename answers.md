### Level 0 - prerequisite
As prerequisite I setup a vagrant ubuntu vm for this exercise

### Level 1 - Collecting your Data

**Level1 - Question 1** - Sign up for Datadog (use "Datadog Recruiting Candidate" in the "Company" field), get the Agent reporting metrics from your local machine.

**Answer** - To install the datadog agent on ubuntu go to Integrations --> Agent --> Ubuntu and follow the installation instructions.

Please check out the screenshot of the install instructions below.

**Screenshot - Install instruction**
![](https://github.com/pareej/hiring-engineers/blob/master/q1-agentinstall.PNG?raw=true)



**Level1 - Question 2** - Bonus question: In your own words, what is the Agent?
**Answer** - Agent is a piece of software that runs on the host machines or the client servers on your behalf. the agent executes the instructions and collects information and brings them back to the main application in this case (Datadog).

**Level1 - Question 3** - Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

**Answer** - To add the tag in datadog agent follow the following steps:
  - Open datadog agent config file located in /etc/dd-agent/datadog.conf
  - add the tag syntax.

Tags are key value pair. For this exercise I have added the environment tag.

tag: environment:PareejTest

** Screenshot - setting up tags in datadog.conf**
![](https://github.com/pareej/hiring-engineers/blob/master/q1-AddingTags.PNG?raw=true)

Please check out the screenshot of my tag in the datadog agent config file.

** Screenshot - Host and its tags **
![](https://github.com/pareej/hiring-engineers/blob/master/q1-hosttag.PNG?raw=true)



**Level1 - Question 4** - Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

**Answer** - I installed MySQL database in my ububtu vm.
To install the MySQL integration for Datadog. I create mysql.yaml in /etc/dd-agent/conf.d directory
 The content of the yaml file

    -server: localhost
     user: datadog
     password: datadog
     options:localhost
     replication: 0
     pa  replication_non_blocking_status: false  # grab slave count in non-blocking manner (req. performance_schema)
     galera_cluster: 1        # Optional
     extra_status_metrics: true Connect via Unix Socket
     extra_innodb_metrics: true Alternate configuration mechanism
     extra_performance_metrics: true
     schema_size_metrics: false
     disable_innodb_metrics: false

Please check out my the screenshot of my configuration file below:

**Screenshot - MySQL yaml configuration file**
![](https://github.com/pareej/hiring-engineers/blob/master/q1-Mysql.yaml.cofig.PNG?raw=true)


**Level1 - Question 5** - Write a custom Agent check that samples a random value. Call this new metric: `test.support.random`

**Answer** - I created a custom check called randomcheck.
- First, I created a python script called randomcheck.py and put it in /etc/dd-agent/checks.d/randomcheck.py


Here is the python script for test.support.random

    import random

    from checks import AgentCheck
    class RandomCheck(AgentCheck):
       def check(self,instance):
           self.gauge('test.support.random',random.random())

** Screenshot of the python script in /etc/dd-agent/checks.d/randomcheck.py"**



- Then I created a yaml file with the same name as the python script randomcheck.yaml and put it in /etc/dd-agent/conf.d/randomcheck.yaml
- Then I restarted the agent by using /etc/init.d/datadog-agent restart


Here is the randomcheck yaml file for test.support.random

    init_config:

    instances:
       [{}]

Please check out the screenshot of customer agent python script and the yaml file.

**Screenshot of python script in in /etc/dd-agent/checks.d/randomcheck.py"**

![](https://github.com/pareej/hiring-engineers/blob/master/q1-randomchek.PNG?raw=true)

**Screenshot of yaml file /etc/dd-agent/conf.d/randomcheck.yaml**
![](https://github.com/pareej/hiring-engineers/blob/master/q1-randomconfig.PNG?raw=true)


###Level 2 - Visualizing your data

**Level 2 - Question 1** -
Since your database integration is reporting now, clone your database integration dashboard and add additional database metrics to it as well as your `test.support.random` metric from the custom Agent check.


**Answer** - To clone the database integration dashboard click on the settings icon and select clone.<br>Then to add the custom metrics click on Add Graphs and select timeseries. for Get - Select the test.support.random. from pareejTest environment.</br>

Please check out the screenshot for cloning the database dashboard.


**SCREENSHOT - of Dashboard with new random metrics is combined with mysql metrics**
![](https://github.com/pareej/hiring-engineers/blob/master/q2-PareejCombinedDash1.PNG?raw=true)


**Level2 - Question 2** - Bonus question: What is the difference between a timeboard and a screenboard?

**Answer** - The difference between timeboards and screenboards are as follows:

Timeboard:
- All graphs are scoped to the same time
- Graphs alwasys apprear in grid-like fashion
- Better for troubleshooting and correlation
- Graphs from timeboard can be shared individually.

screenboards:
- are flexible, customizable, good for high level view of the system.
- created by using drag and drop widgets.
- graphs can have different time frames.
- Can be shared as a whole live and as a read-only entity.

For more information please check out: (https://help.datadoghq.com/hc/en-us/articles/204580349-What-is-the-difference-between-a-ScreenBoard-and-a-TimeBoard-)


**Leve2 - Question 3** - Take a snapshot of your `test.support.random` graph and draw a box around a section that shows it going above 0.90. Make sure this snapshot is sent to your email by using the @notification

**Answer** - First open up the dashboard where you added the random check graph in the above question.
<br>To take a snapshot click on the camera icon on the graph.</br>
<br>Select the area that represents 0.9 or above in the graph and annotate it.</br>
Please look at screenshot to see the what snapshot.

**SCREENSHOT - Snapshot of the graph that show 0.9 annotation**
![](https://github.com/pareej/hiring-engineers/blob/master/q2-snaphostofRandomtest.PNG?raw=true)

###Level3 - Alerting your Data

**Level3 - Question 1** - Since you've already caught your test metric going above 0.90 once, you don't want to have to continually watch this dashboard to be alerted when it goes above 0.90 again.  So let's make life easier by creating a monitor.  
Set up a monitor on this metric that alerts you when it goes above 0.90 at least once during the last 5 minutes

**Answer** - To setup a monitor follow these steps:
- go to Monitor and create a new monitor.
- Select new metric to monitor as "test.support.random".
- Then add the alert threshold to 0.9
- add a meaningful title and the body. In body - add Notify - @email to send an email.

Please check out the screenshot to setup a monitor.

**SCREENSHOT - setting up a monitor**
![](https://github.com/pareej/hiring-engineers/blob/master/q3-setupmonitor.PNG?raw=true)

**Level3 - Question 2** - Bonus points:  Make it a multi-alert by host so that you won't have to recreate it if your infrastructure scales up.

**Answer** - To setup multi-layer alert select the alert to be multi alert and tigger a separage alert for each environment.
<br> Please check the screensoht for example. </br>

**SCREENSHOT - Multi-layer monitor**
![](https://github.com/pareej/hiring-engineers/blob/master/q3-multialertsetup.PNG?raw=true)


**Level3 - Question 3** - Give it a descriptive monitor name and message (it might be worth it to include the link to your previously created dashboard in the message).  Make sure that the monitor will notify you via email.

**Answer** - please use the notify @email so that you get the alert email. Here is the sample email you get when the alert is triggered.

**SCREENSHOT - Alert email**
![](https://github.com/pareej/hiring-engineers/blob/master/q3-emailfromdd.PNG?raw=true)


**Level3 - Question 4** - Bonus: Since this monitor is going to alert pretty often, you don't want to be alerted when you are out of the office. Set up a scheduled downtime for this monitor that silences it from 7pm to 9am daily. Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

**Answer** - To schedule a recurring downtime follow these steps:
- Go to Monitors and select Manage downtime.
- Select Schedule Downtime and select the monitor.
- Select Recurring schedule and put in the start and end time. put in a message that is meaningful. Makesure to put in @email to get email notification of the downtime.

Here is the sample email you get when the alert goes into downtime:


**SCREENSHOT - Monitor downtime alert**
![](https://github.com/pareej/hiring-engineers/blob/master/q3-alert-down-time-started.PNG?raw=true)
