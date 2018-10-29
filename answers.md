# DataDog Technical Exercise Answers

### Environment Setup 
I used the latest Xenial64 Vagrant box running on my windows machine.  I quickly found out that Vagrant and Powershell don’t work all that well together which was a nice little surprise but didn’t hamper efforts too much. 

### Collecting Metrics
#### Adding Tags
I kept this simple and added some tags for “env” and “role” in the datadog.yaml file.  It took a few minutes for them to pick up in the Datadog app but it worked like a charm.  I can imagine that for some clients with a smaller number of hosts they may use the UI to assign tags instead of editing the configuration files directly. 

##### Host Map Screenshot
![alt text](https://github.com/cbtx/hiring-engineers/blob/master/tagscreencaps.png "Host Map")

#### MySQL Integration
I installed MySQL 5.7 on my Ubuntu box for this part of the exercise.  From there it took me less time to get the Datadog integration up and running that it did installing the database itself which is a pretty simple task.  Here is my yaml file for the MySQL integration:
```yaml
  init_config:
  instances:
    - server: 127.0.0.1
      user: datadog
      pass: 'datadog' 
      port: 3306
      options:
          replication: 0
          galera_cluster: 1
          extra_status_metrics: true
          extra_innodb_metrics: true
          extra_performance_metrics: true
          schema_size_metrics: false
          disable_innodb_metrics: false
```

#### Random Number Agent Check
For this step I created ame agent check that imports the random module using the following code: 
```python
from random import *
from checks import AgentCheck
class RandoCheck(AgentCheck):
        def check(self, instance):
                x = randint(0, 1000)
                self.gauge('my_metric',x)
```
#### Changing Collection Interval to 45 Seconds
To do this I changed the yaml file and set the min_collection_interval at the instance level for this agent check since I’m running Agent V6. This appears to also be the answer to the bonus qustions: Here is the yaml file:
```yaml
init_config:

instances:
        - min_collection_interval: 45
```
![alt text](https://github.com/cbtx/hiring-engineers/blob/master/randomnumbercheck.png "Rando Check")


### Visualizing Data
Here is the link to the shell script I used with cURL to create the Timeboard [SE Test Script](https://github.com/cbtx/hiring-engineers/blob/master/setest.sh).  I kept receiving an error when trying to create the anomaly graph - I did quite a bit of research and ensured that the JSON I was using matched the JSON you can view through the editor on the Timeboard GUI but it never would take.  I ended up creating the anomaly graph via the GUI.  

Here's a screenshot of the Timeboard where I'm using the snapshot features with notation to send it to myself:
![alt text](https://github.com/cbtx/hiring-engineers/blob/master/timeboard2.png "Timeboard")

And here's the email that came from this notation:
![alt text](https://github.com/cbtx/hiring-engineers/blob/master/timeemail2.png "Timeboard Email")

#### Bonus Questions
In this instance the anomaly graph uses the Basic function which is using a rolling window of time to compare existing values to historical values.  Compared to the two other anomaly algorithms it's not great for values that show seasonality of any kind. 

### Monitoring Data
#### Creating and Configuring the Monitor
Here is a screenshot of the Metric Monitor Setup:
![alt text](https://github.com/cbtx/hiring-engineers/blob/master/alert1.png "Monitor Setup")

This screenshot shows the message sent with the various messages based on the monitor state:
![alt text](https://github.com/cbtx/hiring-engineers/blob/master/alert2.png "Monitor Setup")

This is the email I received when the monitor hit the warning threshold:
![alt text](https://github.com/cbtx/hiring-engineers/blob/master/alertemail.png "Monitor Email")


#### Bonus Question
Scheduling downtime was easy through the web interface - here are some screenshots:

Here are the two downtimes I scheduled:
![alt text](https://github.com/cbtx/hiring-engineers/blob/master/downtimesnap.png "Downtimes")

This is the detail of the recurring nightly downtime:
![alt text](https://github.com/cbtx/hiring-engineers/blob/master/downtimenight.png "Detail")

Here's the email I got letting me know I set up the downtime:
![alt text](https://github.com/cbtx/hiring-engineers/blob/master/downtimeemail.png "Downtime Email")

### Collecting APM Data
I used the Flask app provided to set up the APM via ddtrace-run: [Flask App](https://github.com/cbtx/hiring-engineers/blob/master/apmtest.py)

Here is a link to the public dashboard: https://p.datadoghq.com/sb/c87ecf0a7-29923e96e9514d03f89b28ce3d24bc15

And here is a screenshot of the dashboard I created with graphs I've added:
![alt text](https://github.com/cbtx/hiring-engineers/blob/master/apmscreenboard.png "APM Screenboard")

#### Bonus Question
A service is a group of processes that do the same job - like all of the components that make up a web app which you'd want to monitor together to understand the overall behavior of that service for an end users.  Resources are components of a service that do a specific function or action like a query to a database or url. 

### Final Question
I come from an analytics background and often see databases get thrashed by open ended queries from end users that typically don't get caught until they either bring down a system or they never get caught at all.  I would love to see DataDog be used to keep tabs on these databases and provide insight into when action needs to be taken so that DBA's can kill queries or better yet understand how end users are using their database to improve performance.  Many of the tools that databases provide to do this type of analysis don't allow someone to take into account the OS level metrics that DataDog could allow a DBA to see side by side in a single dashboard. 
