Your answers to the questions go here.
+
Level 1 - Collecting your Data
  Sign up for Datadog (use "Datadog Recruiting Candidate" in the "Company" field), get the Agent reporting metrics from your local machine.

    I signed up for Datadog with an e-mail of midori.taniguchi2@gmail.com

  Bonus question: In your own words, what is the Agent?

    Agent is a software that visualizes collected data. Datadog enables collecting data from many data of AWS, database, system, etc. Agent helps collecting events and metrics.

  Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

    # Set the host's tags (optional)
    tags: mytag, env:prod, role:database

![ScreenShot](https://user-images.githubusercontent.com/32184362/30998494-f53242ee-a509-11e7-8c80-a86ee74a3697.png)

  https://app.datadoghq.com/infrastructure/map?fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=none&filter=mytag&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=false&palette=green_to_orange&paletteflip=false&host=345947026
  
  Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

    I installed PostgreSQL for database.
    Though I have a problem with postgres configuration. Reinstallation did not solve the problem.
    I checked the user data and password in the table I entered in the database to make sure to edit postgres.yaml file
    with a generated password.
    
    vagrant@precise64:/etc/dd-agent/conf.d$ sudo cat /etc/dd-agent/conf.d/postgres.yaml

    init_config:

    instances:
      - host: localhost
        port: 5432
        username: datadog
        password: YbWWVVPaJUVML98jz1HFMNPpq
        
    Then I receive the information with the datadog-agent info command and respons indicates there is authentication error.
    
      postgres (5.17.2)
    -----------------
      - instance #0 [ERROR]: '(\'FATAL\', \'28P01\', \'password authentication failed for user "datadog"\')'
      - Collected 0 metrics, 0 events & 1 service check
      
      I still look for a solution with seraching information online.

  Write a custom Agent check that samples a random value. Call this new metric: test.support.random

      vagrant@precise64:/etc/dd-agent/conf.d$ sudo cat /etc/dd-agent/conf.d/test.yaml    
      init_config:
  
      instances:
         [{}]
         
      vagrant@precise64:/etc/dd-agent/conf.d$ sudo cat /etc/dd-agent/checks.d/test.py 
      from random import random
      from checks import AgentCheck
      class TestRandomCheck(AgentCheck):
           def check(self, instance):
                self.gauge('test.support.random', random())

Level 2 - Visualizing your Data

  Since your database integration is reporting now, clone your database integration dashboard and add additional database metrics to it as well as your test.support.random metric from the custom Agent check.


  Bonus question: What is the difference between a timeboard and a screenboard?


  Take a snapshot of your test.support.random graph and draw a box around a section that shows it going above 0.90. Make sure this snapshot is sent to your email by using the @notification



Level 3 - Alerting on your Data

  Since you've already caught your test metric going above 0.90 once, you don't want to have to continually watch this dashboard to be alerted when it goes above 0.90 again. So let's make life easier by creating a monitor.

  Set up a monitor on this metric that alerts you when it goes above 0.90 at least once during the last 5 minutes
  Bonus points: Make it a multi-alert by host so that you won't have to recreate it if your infrastructure scales up.


  Give it a descriptive monitor name and message (it might be worth it to include the link to your previously created dashboard in the message). Make sure that the monitor will notify you via email.



  This monitor should alert you within 15 minutes. So when it does, take a screenshot of the email that it sends you.



  Bonus: Since this monitor is going to alert pretty often, you don't want to be alerted when you are out of the office. Set up a scheduled downtime for this monitor that silences it from 7pm to 9am daily. Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.
