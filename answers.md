Your answers to the questions go here.

Level 1 - Collecting your Data

- Sign up for Datadog (use "Datadog Recruiting Candidate" in the "Company" field), get the Agent reporting metrics from your local machine.
  
  I signed up successfully and included a screenshot of the Agent reporting metrics from my local machine.

  screenshot: '/screenshots/level1_agent_rept_metrics'

- Bonus: In your own words, what is the Agent?

  The Agent is the software that collects data from a website, app, or local system. You can configure your Agent to write checks, and integrate with databases.

- Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

  I added the tags tag1, tag2, andrewtag and they were displayed on the host map page.

  screenshot:'/screenshots/level1_host_map_page'

- Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

  I installed the Datadog integration for MongoDB, and have included screenshots of my hostmap with mongodb and a screenshot of the confirmation page that the integration is working.

  screenshot: '/screenshots/level1_mongo_hostmap'
  screenshot: '/screenshots/level1_mongo_confirmation'

- Write a custom Agent check that samples a random value. Call this new metric: test.support.random

  In order to learn how to write an Agent check, I read the guide provided on the Datadog documentation. I went through the tutorials writing hello.py/hello.yaml and http.py/http.yaml. I've included these tutorials along with the test.support.random Agent check in my repo.
  
  available for view in '/code': random.py, random.yaml, hello.py, hello.yaml, http.py, http.yaml

Level 2 - Visualizing your Data

- Since your database integration is reporting now, clone your database integration dashboard and add additional database metrics to it as well as your test.support.random metric from the custom Agent check.

  I have cloned my database integration, mongodb, and have added the database metrics mongodb.connections.available and mongodb.network.numrequestsps along with test.support.random. I've included screenshots for my cloned database integration:

  screenboard: AndrewMongoDB 
  screenshot: '/screenshots/level2_mongo_screenboard'
  public url: https://p.datadoghq.com/sb/bc9b95d7a-c54fd9b176

  timeboard:  Andrew's TimeBoard 15 Aug 2017 16:17
  screenshot: '/screenshots/level2_mongo_timeboard'

- Bonus: What is the difference between a timeboard and a screenboard? 

  Timeboards can not be shared publicly, while a screenboard can. A screenboard is customizable, with the ability to add free text, graphs, query values, and images. You can also resize graphs on screenboard, while a timeboard only shows graphs in a regimented size and are synced to the same time variable.

- Take a snapshot of your test.support.random graph and draw a box around a section that shows it going above 0.90. Make sure this snapshot is sent to your email by using the @notification

  I emailed a snapshot of test.support.random going above 0.90 to the email as04243n@pace.edu. 

  screenshot: '/screenshots/level2_snapshot_notification_email'


Level 3 - Alerting on your data

- Set up a monitor on this metric that alerts you when it goes above 0.90 at least once during the last 5 minutes. Give it a descriptive monitor name and message (it might be worth it to include the link to your previously created dashboard in the message). Make sure that the monitor will notify you via email.
Bonus points: Make it a multi-alert by host so that you won't have to recreate it if your infrastructure scales up.
  
  I have included a screenshot of the monitor I created for the test.support.random metric, 'test.support.random has hit over .9'. THe description included a link to the screenboard and a description. While creating the monitor, I selected multi-alert by host.

  screenshot: '/screenshots/level3_test_monitor'
  
- This monitor should alert you within 15 minutes. So when it does, take a screenshot of the email that it sends you.

  The monitor successfully sent an email to my account, providing the description, graph of the incident, and when the monitor was last triggered.

  screenshot: '/screenshots/level3_monitor_email_notification'


- Bonus: Since this monitor is going to alert pretty often, you don't want to be alerted when you are out of the office. Set up a scheduled downtime for this monitor that silences it from 7pm to 9am daily. Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

  I set up downtime and recieved email notification that the downtime was scheduled successfully.

  screenshot: '/screenshots/level3_downtime_setup'
  screenshot: '/screenshots/level3_downtime_email_notification'
