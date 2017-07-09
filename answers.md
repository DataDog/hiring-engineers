
# The Challenge Answer


## Questions


### Level 1 - Collecting your Data

* Sign up for Datadog (use "Datadog Recruiting Candidate" in the "Company" field), get the Agent reporting metrics from your local machine.</b>
* Bonus question: In your own words, what is the Agent?  
  - The Agent is a an authorized software that acts automatcially on behalf of the users. It can collect and send data from your local host to the remote DataDog server, such that the data can be visualized and managed in the platform of DataDog. In other words, it acts like a spy, who tracks on the events happening on the host, and 'steal' the data.
 
* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.  
  - The configuration file for the Agent is located at ~/.datadog-agent/datadog.conf.  
    <img src="https://github.com/YIYIZH/hiring-engineers/blob/master/Screen%20Shot%202017-07-09%20at%202.04.58%20PM.png" width="500" height="90">  
  - To restart the Agent and to reload the configuration files: /usr/local/bin/datadog-agent restart  
    <img src="https://github.com/YIYIZH/hiring-engineers/blob/master/Screen%20Shot%202017-07-09%20at%203.19.07%20PM.png">

* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database. 
  ```shell
  brew install mysql
  mysql.server start
  mysql -u root //Do the integration configuration inside the mysql shell
  ```
  - Configuration files for integrations are located in ~/.datadog-agent/conf.d/mysql.yaml.  
    While do the info command to check the mysql status, there was an error.
    <img src="https://github.com/YIYIZH/hiring-engineers/blob/master/Screen%20Shot%202017-07-09%20at%204.44.28%20PM.png">  
  - From the error message, I think there is something wrong with the privilege access. So I redo the configuration steps and grant the process privilege. It works this time.  
    <img src="https://github.com/YIYIZH/hiring-engineers/blob/master/Screen%20Shot%202017-07-09%20at%204.50.59%20PM.png" width="500" height="100">  
  - We can see the mysql intergration is installed in DataDog.  
    <img src="https://github.com/YIYIZH/hiring-engineers/blob/master/Screen%20Shot%202017-07-09%20at%204.54.20%20PM.png">  
  
* Write a custom Agent check that samples a random value. Call this new metric: `test.support.random`  
  - Write a mycheck.py  
    <img src="https://github.com/YIYIZH/hiring-engineers/blob/master/Screen%20Shot%202017-07-09%20at%205.50.30%20PM.png" width="400" height="90">  
  - Write a mycheck.yaml  
    <img src="https://github.com/YIYIZH/hiring-engineers/blob/master/Screen%20Shot%202017-07-09%20at%205.37.05%20PM.png" width="270" height="80">  
  - Restart and run the info command (check if mycheck works well)
    <img src="https://github.com/YIYIZH/hiring-engineers/blob/master/Screen%20Shot%202017-07-09%20at%205.54.21%20PM.png" width="370" height="180">

### Level 2 - Visualizing your Data

* Since your database integration is reporting now, clone your database integration dashboard and add additional database metrics to it as well as your `test.support.random` metric from the custom Agent check.  
  - Clone the database dashboard  
    <img src="https://github.com/YIYIZH/hiring-engineers/blob/master/Screen%20Shot%202017-07-09%20at%205.58.22%20PM.png">  
  - Add additional metrics  
    <img src="https://github.com/YIYIZH/hiring-engineers/blob/master/Screen%20Shot%202017-07-09%20at%206.12.06%20PM.png">  
    <img src="https://github.com/YIYIZH/hiring-engineers/blob/master/Screen%20Shot%202017-07-09%20at%206.30.48%20PM.png">  

* Bonus question: What is the difference between a timeboard and a screenboard?  
  - A screenboard consists of custom mixed widgets and graphs for sharing data:
    <img src="https://github.com/YIYIZH/hiring-engineers/blob/master/Screen%20Shot%202017-07-09%20at%206.48.07%20PM.png">  
  - A timeboard consists of real-time automic graphs recording time-synchronized metrics and events for troubleshooting:  
    <img src="https://github.com/YIYIZH/hiring-engineers/blob/master/Screen%20Shot%202017-07-09%20at%206.48.46%20PM.png">  
    
* Take a snapshot of your `test.support.random` graph and draw a box around a section that shows it going above 0.90. Make sure this snapshot is sent to your email by using the @notification  
  <img src="https://github.com/YIYIZH/hiring-engineers/blob/master/Screen%20Shot%202017-07-09%20at%207.47.41%20PM.png">  
  <img src="https://github.com/YIYIZH/hiring-engineers/blob/master/Screen%20Shot%202017-07-09%20at%207.27.34%20PM.png">  
  

### Level 3 - Alerting on your Data

Since you've already caught your test metric going above 0.90 once, you don't want to have to continually watch this dashboard to be alerted when it goes above 0.90 again.  So let's make life easier by creating a monitor.  
* Set up a monitor on this metric that alerts you when it goes above 0.90 at least once during the last 5 minutes  
  <img src="https://github.com/YIYIZH/hiring-engineers/blob/master/Screen%20Shot%202017-07-09%20at%207.56.57%20PM.png">  
  
* Bonus points:  Make it a multi-alert by host so that you won't have to recreate it if your infrastructure scales up.  
  <img src="https://github.com/YIYIZH/hiring-engineers/blob/master/Screen%20Shot%202017-07-09%20at%208.00.13%20PM.png">  
  
* Give it a descriptive monitor name and message (it might be worth it to include the link to your previously created dashboard in the message).  Make sure that the monitor will notify you via email.  
  <img src="https://github.com/YIYIZH/hiring-engineers/blob/master/Screen%20Shot%202017-07-09%20at%208.11.27%20PM.png">  
  
* This monitor should alert you within 15 minutes. So when it does, take a screenshot of the email that it sends you.  

* Bonus: Since this monitor is going to alert pretty often, you don't want to be alerted when you are out of the office. Set up a scheduled downtime for this monitor that silences it from 7pm to 9am daily. Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

## Instructions
If you have a question, create an issue in this repository.

To submit your answers:

1. Fork this repo.
2. Answer the questions in `answers.md`
3. Commit as much code as you need to support your answers.
4. Submit a pull request.
5. Don't forget to include links to your dashboard(s), even better links *and* screenshots.  We recommend that you include your screenshots inline with your answers.  
