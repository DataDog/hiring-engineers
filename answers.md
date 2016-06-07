##Level 1 - Collecting your Data

###Sign up for Datadog (use "Datadog Recruiting Candidate" in the "Company" field), get the Agent reporting metrics from your local machine.

I ran the datadog installation prompts through the command line to get the Agent properly running on my machine.

###Bonus question: In your own words, what is the Agent?

 The Agent is software, written in python, that can be installed on the user's hosts to help monitor them. It is what allows the user to easily configure and customize what metrics they need to monitor. The agent is made up of four moving parts, three of which the user mostly interacts with directly. The four parts are the:
 1.The Collector - Responsible for capturing system metrics.
 2. DogStatsD - A backend server to which the user can send custom metrics from an application
 3.The Forwarder - Grabs the metrics from the DogStasD and the Collector to be sent up to Datadog.
 4. The Supervisord - Monitors the first three processes like a controller.

###Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

I have added a copy of the config file to this github repo, indicating the tags I attached to the local host and a screenshot of the hostmap.

![Host map](/Hostmap.png)


###Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
 I have attached a PostgreSQL YAML configuration file, templated from the example YAML file provided by the documentation, adjusting for the desired username and password to give datadog access to PostgreSQL.


###Write a custom Agent check that samples a random value. Call this new metric: test.support.random

I have attached both the YAML file and the python script that runs the check for the random test.
  I utilized the documentation to use the count method from the AgentCheck and tested out multiple methods provided from the AgentCheck class.
  In the random_check.py file :
```python
from checks import AgentCheck
import random
class RandomCheck(AgentCheck):
    def check(self, instance):
        self.count('test.support.random', random.random())
```
  In the random_check.yaml file

```python
init_config:

instances:
    [{}]
```

##Level 2 - Visualizing your Data

###Since your database integration is reporting now, clone your database intergration dashboard and add additional database metrics to it as well as your test.support.random metric from the custom Agent check.

Link to cloned dashboard:
https://app.datadoghq.com/dash/143486/custom-metrics---postgresql-support-engineer?live=true&page=0&is_auto=false&from_ts=1465334570023&to_ts=1465338170023&tile_size=xl

###Bonus question: What is the difference between a timeboard and a screenboard?

Screenboards are more visually friendly in that it is created through a drag and drop interface, which allows different graphs that are not necessarily being compared or correlated to be viewed and can be seen as read only dashboards. Timeboards, however, have all the graphs scaled to the same timeframe and are laid out in a fixed format that allows for effective comparison and correlation.

###Take a snapshot of your test.support.random graph and draw a box around a section that shows it going above 0.90. Make sure this snapshot is sent to your email by using the @notification

![Random Test snapshot](/random_test.png)


##Level 3 - Alerting on your Data

###Set up a monitor on this metric that alerts you when it goes above 0.90 at least once during the last 5 minutes
###Bonus points: Make it a multi-alert by host so that you won't have to recreate it if your infrastructure scales up.
###Give it a descriptive monitor name and message (it might be worth it to include the link to your previously created dashboard in the message). Make sure that the monitor will notify you via email.
###This monitor should alert you within 15 minutes. So when it does, take a screenshot of the email that it sends you.

![Email alert](/email_alert.png)

###Bonus: Since this monitor is going to alert pretty often, you don't want to be alerted when you are out of the office. Set up a scheduled downtime for this monitor that silences it from 7pm to 9am daily. Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

![Downtime settings](/downtime.png)