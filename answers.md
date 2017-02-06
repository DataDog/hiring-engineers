Your answers to the questions go here.
 
#Level 1 - Collecting Data

#####Sign up for Datadog (use "Datadog Recruiting Candidate" in the "Company" field), get the Agent reporting metrics from your local machine.

Ans: 

I have signed up for Datadog as directed and installed Datadog agent for MAC by executing the following command in command prompt: 

` DD_API_KEY=dc22529b6dce1fd273d9ceedf378ddaf bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/dd-agent/master/packaging/osx/install.sh)" ` 

I am sharing here the [link](https://app.datadoghq.com/account/profile/u-qtTpIqw3eesO?r=t)to my profile in Datadog and a screenshot too: 

![Image ScreenShot] (https://github.com/sethu87/hiring-engineers/blob/master/ScreenShots/ScreenShot_profile.png)
    

References:
  - [Link1](http://docs.datadoghq.com/guides/basic_agent_usage/)
  - [Link2](https://app.datadoghq.com/account/settings#agent)

#####Bonus question: In your own words, what is the Agent?

Ans:  

An agent is an application to send data to Datadog. It brings events and metrics to Datadog so that the user can do something useful with the monitoring and performance data. The agent runs on user's host.
    
For Mac OS X Yosemite, version: 10.10.5 useful codes:

- To restart datadog agent : 
`/usr/local/bin/datadog-agent restart`
- Info command             : 
`/usr/local/bin/datadog-agent info`
- To start datadog agent   : 
`/usr/local/bin/datadog-agent start`
- To stop datadog agent    : 
`/usr/local/bin/datadog-agent stop`

Reference: 
 - [Link1](http://docs.datadoghq.com/guides/basic_agent_usage/osx/)

#####Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in  Datadog.
   
Ans: 

I tried to assign tags using both the Agent configuration file (datadog.conf) and manual tag creation using UI

Tags added to  Datadog agent config file [datadog.conf](https://github.com/sethu87/hiring-engineers/blob/master/datadog.conf) (location path : /opt/datadog-agent/etc/)

`nano ~/.datadog-agent/datadog.conf`
 
![Image ScreenShot0](https://github.com/sethu87/hiring-engineers/blob/master/ScreenShots/ScreenShot0_tags_added_to_datadog.conf.png)
     
I replaced the existing tag line (tags: mytags, env:prod, role:database) as above and removed the comment. I have included 'datadog.conf' file in repository for your reference'
    
Then the agent was restarted and the tags showed up on Host Map

![Image ScreenShot1.1](https://github.com/sethu87/hiring-engineers/blob/master/ScreenShots/ScreenShot1.1_%20tags.png)

![Image ScreenShot1](https://github.com/sethu87/hiring-engineers/blob/master/ScreenShots/Screenshot1_Tag_added_manually_through_UI.png)

![Image ScreenShot2.1](https://github.com/sethu87/hiring-engineers/blob/master/ScreenShots/ScreenShot2.1_HostMap.png)
    

Reference: 
 - [Link1](http://docs.datadoghq.com/guides/tagging/)

#####Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
   
Ans:

Installed MySQL and successfully completed Datadog integration for MySQL DB
   
On verifying by I obtained the following screen shots output

![Image ScreenShot3](https://github.com/sethu87/hiring-engineers/blob/master/ScreenShots/ScreenShot3_Check_Datadog_integration_for_MySQL.png)

![Image ScreenShot2](https://github.com/sethu87/hiring-engineers/blob/master/ScreenShots/ScreenShot2_%20Tags_through_Agent_config_and_UI.png)

![Image ScreenShot3.1](https://github.com/sethu87/hiring-engineers/blob/master/ScreenShots/ScreenShot3.1_mySQL_integration.png)

Reference: 
- [Link1](https://app.datadoghq.com/account/settings#integrations/mysql) (followed instructions in this link for mySQL integration, added the file 'mysql.yaml' in location /opt/datadog-agent/etc/conf.d/ which is also added in the repository for your reference)

#####Write a custom Agent check that samples a random value. Call this new metric: test.support.random

Ans: 

I understand that Agent check is used to collect metrics and events from a new data source.I have done the Agent check by adding the Python plugin to Datadog Agent .

Created the file [randomcheck.yaml](https://github.com/sethu87/hiring-engineers/blob/master/Agent%20check%20files/randomcheck.yaml) in location /opt/datadog-agent/etc/conf.d/


Also created, [randomcheck.py](https://github.com/sethu87/hiring-engineers/blob/master/Agent%20check%20files/randomcheck.py) in location /opt/datadog-agent/agent/checks.d/

On running the check got the output in following screenshot:

![Image ScreenShot4](https://github.com/sethu87/hiring-engineers/blob/master/ScreenShots/ScreenShot4_Agent_Check.png)

Reference: 
- [Link1](http://docs.datadoghq.com/guides/agent_checks/)

#Level 2 - Visualizing your Data

#####Since your database integration is reporting now, clone your database integration dashboard and add additional database metrics to it as well as your test.support.random metric from the custom Agent check.

Ans : 

My Dashboard List screenshot below,
![Image ScreenShot5](https://github.com/sethu87/hiring-engineers/blob/master/ScreenShots/ScreenShot5_cloned_MySQL_integration_dashboard.png)

Here is the [link to my dashboad](https://app.datadoghq.com/dash/list) and [cloned dashboard](https://app.datadoghq.com/dash/242946/mysql---overview-cloned?live=true&page=0&is_auto=false&from_ts=1486065282840&to_ts=1486079682840&tile_size=m)
        
Additional metric added is:

(Time Series graph)   Avg of test.support.random over host:Sethulakshmis-MacBook-Pro.local 

Thus I have added test.support.random metric from the custom Agent check which is shown in below screen shots.

![Image ScreenShot6](https://github.com/sethu87/hiring-engineers/blob/master/ScreenShots/ScreenShot6_MySQL_cloned_dashboard.png)
![Image ScreenShot7](https://github.com/sethu87/hiring-engineers/blob/master/ScreenShots/ScreenShot7_test.support.random%20metric.png)


#####Bonus question: What is the difference between a timeboard and a screenboard?

Ans:
    
Time board: With timeboard a user must be able to look at my data and scroll back in time.Enables user to see what happens now also at the same time what has been happening before, in the past. Thereby enables the user to have a time based performance analysis.
       
Screenboards: Screenboards are intended to show only the current status. User is able to get more types of information on screenboard but it shows only current info. Another feature of screenboard is that user can share out screenboard, user can create an external public URL for a screenboard and share that with the customers or executive teams.

#####Take a snapshot of your test.support.random graph and draw a box around a section that shows it going above 0.90. Make sure this snapshot is sent to your email by using the @notification
    
Ans: I have taken the snapshot as shown in screenshot below.  

![Image ScreenShot8](https://github.com/sethu87/hiring-engineers/blob/master/ScreenShots/ScreenShot8_%20test.support.graph.png)

I had also set the notification for email for alerting change in dashboard and added notification @lakssethu@gmail.com in comment

![Image ScreenShot9](https://github.com/sethu87/hiring-engineers/blob/master/ScreenShots/ScreenShot9_%20set_notification.png)

Notification on dashboard change
[Email1](https://github.com/sethu87/hiring-engineers/blob/master/Email%20Notifications/Gmail%20-%20%5BDatadog%5D%20Now%20tracking%20changes%20made%20to%20dashboard:%20'MySQL%20-%20Overview%20(cloned)'..pdf)
[Email2](https://github.com/sethu87/hiring-engineers/blob/master/Email%20Notifications/Gmail%20-%20%5BDatadog%5D%20%5BDash%20Modified%5D%20You%20made%20changes%20to%20the%20dashboard%20titled%20'MySQL....pdf)
    
Despite repeated attempts I couldn't get'email with the snapshot created as specified 

#Level 3 - Alerting on your Data

#####Since you've already caught your test metric going above 0.90 once, you don't want to have to continually watch this dashboard to be alerted when it goes above 0.90 again. So let's make life easier by creating a monitor.

#####Set up a monitor on this metric that alerts you when it goes above 0.90 at least once during the last 5 minutes.

Ans:   
I have created the monitor from the metric graph options

Monitor: 

[Link1](https://app.datadoghq.com/monitors#1577171/edit) (Monitor Set up)
![Image ScreenShot13](https://github.com/sethu87/hiring-engineers/blob/master/ScreenShots/ScreenShot13_Monitor_Setup.png)

[Link2](https://app.datadoghq.com/monitors#manage) (Manage Monitors)
![Image ScreenShot13.1](https://github.com/sethu87/hiring-engineers/blob/master/ScreenShots/ScreenShot13.1_Manage_monitor.png)

#####Bonus points: Make it a multi-alert by host so that you won't have to recreate it if your infrastructure scales up.

Ans: 

Multi alert option is chosen while creating monitor. Please see attached screenshot : ScreenShot11
![Image ScreenShot11](https://github.com/sethu87/hiring-engineers/blob/master/ScreenShots/ScreenShot11_%20multialert.png)

#####Give it a descriptive monitor name and message (it might be worth it to include the link to your previously created dashboard in the message). Make sure that the monitor will notify you via email.

Ans: Created monitor with following data,   

Monitor Name: Alerts when test.support.random goes above 0.90 at least once during the last 5 minutes

Monitor Message:

    {{#is_warning}} test.support.random metric went above 0.90 during last 5 minutes. Dashboard link: https://app.datadoghq.com/dash/242946/mysql---overview-cloned?live=true&page=0&is_auto=false&from_ts=1486064942141&to_ts=1486068542141&tile_size=m 
    {{/is_warning}}
    Notify: @lakssethu@gmail.com
    
I am receiving notification emails as per the monitor. [Email Notification](https://github.com/sethu87/hiring-engineers/blob/master/Email%20Notifications/Gmail%20-%20%5BMonitor%20Alert%5D%20Recovered:%20Alerts%20when%20test.support.random%20goes%20above%200.90%20at%20least%20once%20dur.pdf)

#####This monitor should alert you within 15 minutes. So when it does, take a screenshot of the email that it sends you.
   
Ans: 
![Image ScreenShot12] (https://github.com/sethu87/hiring-engineers/blob/master/ScreenShots/ScreenShot12_Email_Monitor.png)   

##### Bonus: Since this monitor is going to alert pretty often, you don't want to be alerted when you are out of the office. Set up a scheduled downtime for this monitor that silences it from 7pm to 9am daily. Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

Ans: 
    In 'Manage Monitor' I have added a 'Mute' to the created monitor (Alerts when test.support.random goes above 0.90 at least once during the last 5 minutes) . Afterwards this monitor was showed up in 'Manage Downtime'. Then on selecting the monitor in 'Manage Downtime' the scheduler window was obtained in which downtime has been set up. 

I have got email notification on passing the downtime but but not when it has started.
    
[Link](https://app.datadoghq.com/monitors#downtime?id=211656679)
![Image ScreenShot14](https://github.com/sethu87/hiring-engineers/blob/master/ScreenShots/ScreenShot14_Manage_downtime.png)
![Image ScreenShot14.1](https://github.com/sethu87/hiring-engineers/blob/master/ScreenShots/ScreenShot14.1_schedule_downtime.png)
    
