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

##Level 2
<br>

- Since your database integration is reporting now, clone your database integration dashboard and add additional database metrics to it as well as your test.support.random metric from the custom Agent check.

- Bonus question: What is the difference between a timeboard and a screenboard?

- Take a snapshot of your test.support.random graph and draw a box around a section that shows it going above 0.90. Make sure this snapshot is sent to your email by using the @notification

##Level 3

- Since you've already caught your test metric going above 0.90 once, you don't want to have to continually watch this dashboard to be alerted when it goes above 0.90 again. So let's make life easier by creating a monitor.

- Set up a monitor on this metric that alerts you when it goes above 0.90 at least once during the last 5 minutes

- Bonus points: Make it a multi-alert by host so that you won't have to recreate it if your infrastructure scales up.

- Give it a descriptive monitor name and message (it might be worth it to include the link to your previously created dashboard in the message). Make sure that the monitor will notify you via email.

- This monitor should alert you within 15 minutes. So when it does, take a screenshot of the email that it sends you.

- Bonus: Since this monitor is going to alert pretty often, you don't want to be alerted when you are out of the office. Set up a scheduled downtime for this monitor that silences it from 7pm to 9am daily. Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.










    
    
    
    
