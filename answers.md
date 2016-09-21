# The Challenge

## Answers

### Level 0 (optional) - Setup an Ubuntu VM
* Linux VM was spun up using vagrant.
  * ![Vagrant up](https://github.com/ls339/hiring-engineers/blob/support-engineer/Level_0/ScreenShots/Vagrant_up.png?raw=true)

### Level 1 - Collecting your Data
* Sign up for Datadog (use "Datadog Recruiting Candidate" in the "Company" field), get the Agent reporting metrics from your local machine.
  * _**Signed up for Datadog and successfully installed the agent.**_
  * ![Agent Running](https://github.com/ls339/hiring-engineers/blob/support-engineer/Level_1/ScreenShots/Agent_Running.png?raw=true)
* Bonus question: In your own words, what is the Agent?
  * _**The agent is software that runs on hosts machines. Its primary function is to collect metric and event data to be sent to a centralized location for processing. Communication from the agent is outbound only and runs over a secure HTTPS channel. 
The agent is written in Python and is an open source project. The code can be found [here](https://github.com/DataDog/dd-agent). 
Its three main functions are collections of system metrics, collection of application metrics, and forwarding of system and application metrics to Datadog.
The agent runs as a service and can be configured to work through a proxy. On Linux, the configuration file for the agent is /etc/dd-agent/datadog.conf.**_
* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
  * ![Host Map](https://github.com/ls339/hiring-engineers/blob/support-engineer/Level_1/ScreenShots/HostMap.png?raw=true)
* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
  * ![MySQL Integration](https://github.com/ls339/hiring-engineers/blob/support-engineer/Level_1/ScreenShots/MySQL_Integration.png?raw=true)
* Write a custom Agent check that samples a random value. Call this new metric: `test.support.random`
  * _**Writing a custom check is relatively straight forward using the AgentCheck interface available through the Datadog agent. It is as simple as writing a YAML configuration file and a python script of the same file name. On Linux, the configuration file gets read from /etc/dd-agent/conf.d and the custom check script is executed from /etc/dd-agent/checks.d.**_
  * [random.py](https://github.com/ls339/hiring-engineers/blob/support-engineer/Level_1/checks.d/random.py)
    ```python
    import random
    from checks import AgentCheck

      class RandomValueCheck(AgentCheck):
        def check(self, instance):
          self.gauge('test.support.random', random.random())
    ```
  * [random.yml](https://github.com/ls339/hiring-engineers/blob/support-engineer/Level_1/checks.d/random.py)
  * ![Check Info](https://github.com/ls339/hiring-engineers/blob/support-engineer/Level_1/ScreenShots/CustomCheckInfo.png?raw=true)
  
### Level 2 - Visualizing your Data

* Since your database integration is reporting now, clone your database integration dashboard and add additional database metrics to it as well as your `test.support.random` metric from the custom Agent check.
  * [Cloned Dashboard](https://app.datadoghq.com/dash/186169/lous-cloned-dashboard?live=true&page=0&is_auto=false&from_ts=1474448872829&to_ts=1474463272829&tile_size=m)
  * [Custom Timeboard](https://app.datadoghq.com/dash/185795/lewiss-timeboard-20-sep-2016-1140?live=true&page=0&is_auto=false&from_ts=1474454619150&to_ts=1474469019150&tile_size=m)
  * ![Cloned DashBoard](https://github.com/ls339/hiring-engineers/blob/support-engineer/Level_2/ScreenShots/MySQLClonedDashBoard.png?raw=true)
* Bonus question: What is the difference between a timeboard and a screenboard?
  * _**A timeboard is used for troubleshooting as it gives the user a view of  graphs scoped from the same time. You can use a timeboard to make correlations between metrics.
The screenboard give the user a high level look into the systems and can be used for monitoring. The biggest difference between a timeboard and a screenboard is that a screenboard can be shared where as a timeboard can not.**_
* Take a snapshot of your `test.support.random` graph and draw a box around a section that shows it going above 0.90. Make sure this snapshot is sent to your email by using the @notification
  * ![SnapShot 1](https://github.com/ls339/hiring-engineers/blob/support-engineer/Level_2/ScreenShots/SnapShot1.png?raw=true)
  * ![SnapShot 2](https://github.com/ls339/hiring-engineers/blob/support-engineer/Level_2/ScreenShots/SnapShot2.png?raw=true)

### Level 3 - Alerting on your Data

* Set up a monitor on this metric that alerts you when it goes above 0.90 at least once during the last 5 minutes 
* Bonus points:  Make it a multi-alert by host so that you won't have to recreate it if your infrastructure scales up.
  * The monitor was created as a multi-alert by host. It will trigger a separate alarm for each host. 
* Give it a descriptive monitor name and message (it might be worth it to include the link to your previously created dashboard in the message).  Make sure that the monitor will notify you via email.
  * The monitor is named "Random number spike on {{host.name}}. A link to the dashboard was provided in the message and used the @notification for messaging to team members.
  * ![Monitor Setup](https://github.com/ls339/hiring-engineers/blob/support-engineer/Level_3/ScreenShots/MonitorSetup.png?raw=true)
* This monitor should alert you within 15 minutes. So when it does, take a screenshot of the email that it sends you.
  * ![Monitor Email](https://github.com/ls339/hiring-engineers/blob/support-engineer/Level_3/ScreenShots/MonitorEmail.png?raw=true)
* Bonus: Since this monitor is going to alert pretty often, you don't want to be alerted when you are out of the office. Set up a scheduled downtime for this monitor that silences it from 7pm to 9am daily. Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.
  * ![Downtime Setup](https://github.com/ls339/hiring-engineers/blob/support-engineer/Level_3/ScreenShots/MonitorDowntimeSetup.png?raw=true)
  * ![downtime notification](https://github.com/ls339/hiring-engineers/blob/support-engineer/Level_3/ScreenShots/DowntimeNotification.png?raw=true)
  * [Monitor](https://app.datadoghq.com/monitors#944586?group=all&live=4h)
  * [Scheduled Downtime](https://app.datadoghq.com/monitors#downtime?id=195589910)
