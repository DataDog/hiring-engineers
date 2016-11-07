Your answers to the questions go here.

##Level 0 
Downloaded and Installed  Vagrant and Virtual Box <br>
This is pretty neat, I was recently talking about virtual servers and how it generally works in AWS. 
![ScreenShot](/images/vargrant.png) <br>
![ScreenShot](/images/virtualbox.png)


##Level 1 
 - Signed up! 

<br>

![ScreenShot](/images/datadog_agent.png)

<br>
 - Bonus Question: What is an Agent? 

<br> 
 In general, An Agent is like an an authorized user who has permission to keep tally and retrieve information from whatever location you send. I really like to imagine the idea seeing the SPY vs. SPY  entering computers then collecting data, metrics. Once found, the spys report that information back to their "spy work place" see what can be done with the found knowledge. <br>
 With Datadog, the Agent is set into a server so it may know what is going on. With this information, it allows an user to have a clear understanding of what is going on and be able to use that data to find issues, solutions, etc. 
<br> 

- Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

![ScreenShot](/images/host_map.png)
<br> 
<br>
![ScreenShot](/images/datadog_conf.png)
<br> 
<br>

 - Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

<br>
helpful psql commands if you need to restart making a <code> ROLE </code>
![ScreenShot](/images/psql_role.png)
<br>
<br>
![ScreenShot](/images/psql_dd.png)
<br> 
<br>
I was having some confusion as to why the postgres checks were not showing up 
after checking syntax in the yaml file, restarting, and playing around with dbnames. However, the dashboard for postgres says it was properly intergrated. ** note ** went through the database with mysql not postgreSQL
![ScreenShot](/images/db_intergration.png)
<br> 
<br>
![ScreenShot](/images/db_info.png)
<br> 
<br>
![ScreenShot](/images/psql_dashboard.png)


This was an interesting point. There were a few things that had me at a wall. 
1. Did postgreSQL first, but was having trouble seeing the checks after <code> datadog-agent info </code> (later realized adding <code>-v</code> and <code> check check_rate</code> would have saved much time) <br>
2.There was slight decrepanices in the code commands when I compared it to the postgres setup that you see when you click on the icon and the Docs to intergrating postgreSQL <br> 
In the docs <code>psql -h localhost -U datadog postgres -c \
"select * from pg_stat_database LIMIT(1);"&& echo -e "\e[0;32mPostgres connection - OK\e[0m" || \ || echo -e "\e[0;31mCannot connect to Postgres\e[0m"</code> didn't want to work<br> 
In the postgreSQL setup <code>psql -h localhost -U datadog postgres -c "select * from pg_stat_database LIMIT(1);"&& echo -e "\e[0;32mPostgres connection - OK\e[0m" || \ || echo -e "\e[0;31mCannot connect to Postgres\e[0m"</code> This worked.<br>
Note for others: Line space is touchy with postgreSQL, so copy and paste should be double checked in an editor.
3. Taking off <code>.example</code> off the <code>.yaml</code> file helps as well. <br>
<br>
###I ended up using mysql instead - everything works. 
<br>
<br>
![ScreenShot](/images/checks.png)
<br> 
<br>

- Write a custom Agent check that samples a random value. Call this new metric: test.support.random

![ScreenShot](/images/mysql_py.png)
<br> 
<br>
![ScreenShot](/images/test.png)
<br> 
<br>
<a href="https://app.datadoghq.com/metric/explorer?live=true&page=0&is_auto=false&from_ts=1478488702062&to_ts=1478492302062&tile_size=m&exp_metric=test.support.random&exp_scope=&exp_agg=avg&exp_row_type=metric">Graph Link</a>

##Level 2
<br>

- Since your database integration is reporting now, clone your database integration dashboard and add additional database metrics to it as well as your test.support.random metric from the custom Agent check.

<br>
![ScreenShot](/images/clone.png)
<br> 
<br>
![ScreenShot](/images/clonestat.png)
<br> 
<br>


- Bonus question: What is the difference between a timeboard and a screenboard?

Timeboards focuses on time - which means that whatever is on this board, it's going to be all at the same time. This is helpful with troubleshooting. I think of this a focusing on a specific area instead of an entire picture. 

Screenboards focuses more of the broader perspective, that allows an user to see the bigger picture - not everything is on the same time and mix what you want to be displayed. 

- Take a snapshot of your test.support.random graph and draw a box around a section that shows it going above 0.90. Make sure this snapshot is sent to your email by using the @notification

<br> 
<br>
![ScreenShot](/images/notify.png)
<br> 
<br>
<br> 
<br>
![ScreenShot](/images/snap.png)
<br> 
<br>

##Level 3

- Since you've already caught your test metric going above 0.90 once, you don't want to have to continually watch this dashboard to be alerted when it goes above 0.90 again. So let's make life easier by creating a monitor.



- Set up a monitor on this metric that alerts you when it goes above 0.90 at least once during the last 5 minutes

<br>
![ScreenShot](/images/alert.png)
<br> 
<br>

- Bonus points: Make it a multi-alert by host so that you won't have to recreate it if your infrastructure scales up.

<br>
![ScreenShot](/images/monitor.png)
<br> 
<br>

- Give it a descriptive monitor name and message (it might be worth it to include the link to your previously created dashboard in the message). Make sure that the monitor will notify you via email.

<br>
![ScreenShot](/images/message.png)
<br> 
<br>

- This monitor should alert you within 15 minutes. So when it does, take a screenshot of the email that it sends you.

<br>
![ScreenShot](/images/email_alert.png)
<br> 
<br>

- Bonus: Since this monitor is going to alert pretty often, you don't want to be alerted when you are out of the office. Set up a scheduled downtime for this monitor that silences it from 7pm to 9am daily. Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

Not sure if it was I scheduled the downtime and it would send an email once downtime was over OR when it was initialized. Here it is on the dashboard. 

<br>
![ScreenShot](/images/dtime.png)
<br> 
<br>

<ahref="https://app.datadoghq.com/dash/208657/mysql---overview-cloned?live=true&page=0&is_auto=false&from_ts=1478493993037&to_ts=1478497593037&tile_size=m">Dashboard link</a>









    
    
    
    
