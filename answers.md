# Answers

## Level 0 (optional) - Setup an Ubuntu VM

##### While it is not required, we recommend that you spin up a fresh linux VM via Vagrant or other tools so that you don't run into any OS or dependency issues. [Here are instructions for setting up a Vagrant Ubuntu 12.04 VM.](https://www.vagrantup.com/docs/getting-started/)

    vagrant up
    vagrant ssh

## Level 1 - Collecting your Data

#### Sign up for Datadog (use "Datadog Recruiting Candidate" in the "Company" field), get the Agent reporting metrics from your local machine.

Done.  Username:  **j@jeffkwiat.com**

#### Bonus question: In your own words, what is the Agent?
The agent is a small software app that sits on your machine(s), keeps track of its data (CPU, RAM, etc.), and reports back to Datadog.  From there, you can set up monitors and alerts based on what is important to you.

#### Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
See level-1-assets/screenshots/level1-step3.jpg

![Level1, Step3](https://github.com/jeffkwiat/hiring-engineers/blob/solutions-engineer/level-1-assets/screenshots/level1-step3.jpg)


#### Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
    sudo apt-get install postgresql postgresql-contrib    
    sudo su - postgres
    psql
    psql -h localhost -U datadog postgres -c "select * from pg_stat_database LIMIT(1);"  
    
See level-1-assets/postgres.yaml

    init_config:
    
    instances:
       -   host: localhost
           port: 5432
           username: datadog
           password: Datadog123!
           tags:
                - dd_database
                - dd_stats
                
See level-1-assets/screenshots/level1-step4.jpg

![Level1, Step4](https://github.com/jeffkwiat/hiring-engineers/blob/solutions-engineer/level-1-assets/screenshots/level1-step4.jpg)


##### Write a custom Agent check that samples a random value. Call this new metric: `test.support.random`

**random.py** - source code in level-1-assets/checks/random.py

    import random

    from checks import AgentCheck
    
    
    class RandomCheck(AgentCheck):
        """ Create a random sample. """
    
        def check(self, instance):
            self.gauge('test.support.random', random.random())
            
**random.yaml** - config code in level-1-assets/checks/random.py

    init_config:

    instances:
        [{}]
        
## Level 2 - Visualizing your Data

##### Since your database integration is reporting now, clone your database integration dashboard and add additional database metrics to it as well as your `test.support.random` metric from the custom Agent check.

**URL:  ** 
![Level2, Step1](https://github.com/jeffkwiat/hiring-engineers/blob/solutions-engineer/level-2-assets/screenshots/level2-step1.jpg)

##### Bonus question: What is the difference between a timeboard and a screenboard?

A **timeboard** is a way to easily view multiple metrics across the same time window.  This allows you to find correlations between the metrics and diagnose issues.

A **screenboard** is a more free-form dashboard, where you can have a wide range of metrics, images, text fields, etc. and instantly get a high-level status of your environment.  Each section of the board can use a different time window.

**Reference:**
https://help.datadoghq.com/hc/en-us/articles/204580349-What-is-the-difference-between-a-ScreenBoard-and-a-TimeBoard-

##### Take a snapshot of your `test.support.random` graph and draw a box around a section that shows it going above 0.90. Make sure this snapshot is sent to your email by using the @notification

![Level2, Step3a](https://github.com/jeffkwiat/hiring-engineers/blob/solutions-engineer/level-2-assets/screenshots/level2-step3-a.jpg)

NOTE:  I created this one just to explore the system.  It uses the last random result and highlights the field in either red or green based on the random value.
![Level2, Step3b](https://github.com/jeffkwiat/hiring-engineers/blob/solutions-engineer/level-2-assets/screenshots/level2-step3-b.jpg)

## Level 3 - Alerting on your Data

Since you've already caught your test metric going above 0.90 once, you don't want to have to continually watch this dashboard to be alerted when it goes above 0.90 again.  So let's make life easier by creating a monitor.  
* Set up a monitor on this metric that alerts you when it goes above 0.90 at least once during the last 5 minutes 
![Level3, Step1](https://github.com/jeffkwiat/hiring-engineers/blob/solutions-engineer/level-3-assets/screenshots/level3-step1.jpg)

* Bonus points:  Make it a multi-alert by host so that you won't have to recreate it if your infrastructure scales up.  
![Level3, Step2](https://github.com/jeffkwiat/hiring-engineers/blob/solutions-engineer/level-3-assets/screenshots/level3-step2.jpg)

* Give it a descriptive monitor name and message (it might be worth it to include the link to your previously created dashboard in the message).  Make sure that the monitor will notify you via email.
![Level3, Step3](https://github.com/jeffkwiat/hiring-engineers/blob/solutions-engineer/level-3-assets/screenshots/level3-step3.jpg)

* This monitor should alert you within 15 minutes. So when it does, take a screenshot of the email that it sends you.
![Level3, Step4](https://github.com/jeffkwiat/hiring-engineers/blob/solutions-engineer/level-3-assets/screenshots/level3-step4.jpg)

* Bonus: Since this monitor is going to alert pretty often, you don't want to be alerted when you are out of the office. Set up a scheduled downtime for this monitor that silences it from 7pm to 9am daily. Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.
![Level3, Step5](https://github.com/jeffkwiat/hiring-engineers/blob/solutions-engineer/level-3-assets/screenshots/level3-step3.jpg)
