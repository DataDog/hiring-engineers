Your answers to the questions go here.
________________________________________________________________________________________________________________
## Prerequisites - Setup the environment

- You can utilize any OS/host that you would like to complete this exercise. However, we recommend one of the following approaches:

- You can spin up a fresh linux VM via Vagrant or other tools so that you don’t run into any OS or dependency issues. Here are instructions for setting up a Vagrant Ubuntu VM. We strongly recommend using minimum v. 16.04 to avoid dependency issues.

- You can utilize a Containerized approach with Docker for Linux and our dockerized Datadog Agent image.
Then, sign up for Datadog (use “Datadog Recruiting Candidate” in the “Company” field), get the Agent reporting metrics from your local machine.

  >I set up a Vagrant Ubuntu VM of version 18.04
  
  >Showing the Vagrant host in the Datadog UI:
  
  >![VagrantHost1](https://github.com/GB-18/hiring-engineers/blob/GB-18-patch-1/Vagrant%20Host%201.png)
      
________________________________________________________________________________________________________________
## Collecting Metrics:

- Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

  >Showing the Vagrant Tags in the datadog.yaml:
  
  >![VagrantTags](https://github.com/GB-18/hiring-engineers/blob/GB-18-patch-1/Vagrant%20Tags.png)
     
  >Showing the Vagrant Tags in the Datadog UI:
  
  >![VagrantHost2](https://github.com/GB-18/hiring-engineers/blob/GB-18-patch-1/Vagrant%20Host%202.png)  

________________________________________________________________________________________________________________
- Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

  >I installed a MySQL database and put configured it to communicate with the datadog agent in the conf.yaml within the etc/datadog-agent/conf.d/mysql.d directory
  
  >![MySQLConfigFile](https://github.com/GB-18/hiring-engineers/blob/GB-18-patch-1/MySQL%20configuration%20file.png)
  
  >I configured a user, set the apporpriate permissions, and validated that the agent was collecting MySQL metrics:
  
  >![MySQLUser](https://github.com/GB-18/hiring-engineers/blob/GB-18-patch-1/MySQL%20Users.png)
  >![MySQLPermissions](https://github.com/GB-18/hiring-engineers/blob/GB-18-patch-1/MySQL%20Permissions.png)
  >![MySQLStatus](https://github.com/GB-18/hiring-engineers/blob/GB-18-patch-1/MySQL%20Status.png)
  >![MySQLCounters](https://github.com/GB-18/hiring-engineers/blob/GB-18-patch-1/MySQL%20Counters.png)
________________________________________________________________________________________________________________
- Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

  >I created a custom Agent check that submits a metric named custom_metric with a random value between 0 and 1000 and put it in the /etc/datadog-agent/checks.d/ directory


```

#the following try/except block will make the custom check compatible with any Agent version

try:

#first, try to import the base class from new versions of the Agent...
   from datadog_checks.base import AgentCheck
except ImportError:
#...if the above failed, the check is running in Agent version < 6.6.0
   from checks import AgentCheck

#content of the special variable __version__ will be shown in the Agent status page
___version__ = "1.0.0"

#import random integer function
from random import randint

#create a function that checks for the latest output value from the Datadog Agent of specified metric

class MetricCheck(AgentCheck):
   def check(self, instance):
      self.gauge('custom_metric',randint(0,1000))

```

  >I've included screenshots of the custom metric collection status from the Datadog Agent:
  
  >![CustomMetricStatus](https://github.com/GB-18/hiring-engineers/blob/GB-18-patch-1/Custom%20Metric%20Status.png)
  
________________________________________________________________________________________________________________


  >I put the custom_metric.yaml file in the /etc/datadog-agent/conf.d/ directory which creates the instances mapping:
  
```  
  
#creates a configuration file that changes the interval of collection of data

init_config:
instances:
    -   min_collection_interval: 45
 
``` 
________________________________________________________________________________________________________________    

- Change your check's collection interval so that it only submits the metric once every 45 seconds.

  >See above for code, below for screenshot of interval on dash:
  
  >![CustChange2](https://github.com/GB-18/hiring-engineers/blob/GB-18-patch-1/CustomMetric%20Interval%20Change%202.png)
  >![CustChange1](https://github.com/GB-18/hiring-engineers/blob/GB-18-patch-1/CustomMetric%20Interval%20Change%201.png)
________________________________________________________________________________________________________________   
**Bonus Question Can you change the collection interval without modifying the Python check file you created?**

  >Yes! In the conf.yaml file for the custom check (code above) you can change the interval
  
________________________________________________________________________________________________________________   
- Utilize the Datadog API to create a Timeboard that contains:

- Your custom metric scoped over your host.

  >![CustDash](https://github.com/GB-18/hiring-engineers/blob/GB-18-patch-1/CustomMetric%20Dash.png)

________________________________________________________________________________________________________________ 
- Any metric from the Integration on your Database with the anomaly function applied.
- Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

  >![CustMetGlobalDash](https://github.com/GB-18/hiring-engineers/blob/GB-18-patch-1/CustomMetricGlobalDash.png)

________________________________________________________________________________________________________________ 
- Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.

```

from datadog import initialize, api

options = {
         'api_key': '5339cb2233282c327d3450f5e9c48c41',
         'app_key': '0d38c97a515286c329dde6b903636590ed3cd6f6'
         }

initialize(**options)

title = "My Timeboard"
description = "Shows my custom metric over time"
graphs = [{
       "title": "Custom metric over time",
       "definition": {
          "events": [],
          "requests": [
             {"q": "avg:custom_metric{*}"}],
          "viz":"timeseries"}
          },
{
        "title": "Hourly Rollup of Custom Metric",
        "definition": {
           "events": [],
           "requests": [
             {"q": "avg:custom_metric{*}.rollup(sum, 3600)"}],
           "viz": "timeseries"}
          },
{
        "title": "MySQL CPU Time Anomaly",
        "definition": {
           "events": [],
           "requests": [
              {"q": "anomalies(mysql.performance.cpu_time{*}, 'basic' ,3)"}],
           "viz": "timeseries"}
}]

template_variables = [{
        "name": "vagrant",
        "prefix": "host",
        "default": "host:vagrant"
                }]
                
read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)
                     
```                     

________________________________________________________________________________________________________________ 

- Once this is created, access the Dashboard from your Dashboard List in the UI:

  >See above screenshots
  
________________________________________________________________________________________________________________ 

- Set the Timeboard's timeframe to the past 5 minutes

  >![Cust5MinDash](https://github.com/GB-18/hiring-engineers/blob/GB-18-patch-1/CustomMetric%20Dash%20over%205%20mins.png)

________________________________________________________________________________________________________________ 

- Take a snapshot of this graph and use the @ notation to send it to yourself.

  >I sent the 5 min interval graph to myself in an email via the @ notation:
  
  >![CustAtMet](https://github.com/GB-18/hiring-engineers/blob/GB-18-patch-1/CustomMetric%20Sent%20via%20at.png)
  
  
  >I also set up a slack integration to be able to send snapshots of these custom dashboards via slack. The example below provides a screenshot of the MySQL anomaly graph sent via Slack:
  
  >![CustDashSlack](https://github.com/GB-18/hiring-engineers/blob/GB-18-patch-1/CustomDash%20Sent%20via%20Slack.png)
  
________________________________________________________________________________________________________________   

**Bonus Question: What is the Anomaly graph displaying?**

>The Anomaly graph is displaying a measure of the amount of CPU time the MySQL database takes to execute a task against what has been historically considered "normal". Essentially, the anomaly measure within Datadog will figure out what a normal amount of CPU time to execute a task is based on historical data and project out what upper and lower bounds would be considered normal based on that. If there are CPU times that are outside of those bounds, it will highlight them in red as an anomaly or potential risk.

________________________________________________________________________________________________________________  

- Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.

- Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

- Warning threshold of 500
- Alerting threshold of 800
- And also ensure that it will notify you if there is No Data for this query over the past 10m.

>![MonitorDashThresh](https://github.com/GB-18/hiring-engineers/blob/GB-18-patch-1/Monitor%20Thresholds.png)

________________________________________________________________________________________________________________  

- Please configure the monitor’s message so that it will:

- Send you an email whenever the monitor triggers.

- Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.

- Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.

  >![MetAlertMessage](https://github.com/GB-18/hiring-engineers/blob/GB-18-patch-1/Metric%20Alert%20Message.png)
________________________________________________________________________________________________________________

- When this monitor sends you an email notification, take a screenshot of the email that it sends you.

  >Email notification for no data:
  
  >![NoDataAlert](https://github.com/GB-18/hiring-engineers/blob/GB-18-patch-1/No%20data%20alert.png)
  
  >Email notification for warning:
  
  >![WarningEmail](https://github.com/GB-18/hiring-engineers/blob/GB-18-patch-1/Warning%20Email%20Alert.png)
  
  >Email notification for alert:
  
  >![HighThresh](https://github.com/GB-18/hiring-engineers/blob/GB-18-patch-1/High%20threshold%20alert.png)

________________________________________________________________________________________________________________ 
**Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:**

- One that silences it from 7pm to 9am daily on M-F,

  >![WeekdayDowntimeAlert](https://github.com/GB-18/hiring-engineers/blob/GB-18-patch-1/Weekday%20Downtime%20Email%20Alert.png)
  >![WeekdayWindow](https://github.com/GB-18/hiring-engineers/blob/GB-18-patch-1/Weekday%20Window.png)

- And one that silences it all day on Sat-Sun.

  >![WeekendDowntimeAlert](https://github.com/GB-18/hiring-engineers/blob/GB-18-patch-1/Weekend%20Downtime%20Email%20Alert.png)
  >![WeekendWindow](https://github.com/GB-18/hiring-engineers/blob/GB-18-patch-1/Weekend%20Window.png)
  
  >I also sent out these notifications via slack:
  
  >![MetricDowntimeSlack](https://github.com/GB-18/hiring-engineers/blob/GB-18-patch-1/Metric%20Downtime%20Slack%20Alert.png)

- Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

  >See screenshots above
________________________________________________________________________________________________________________ 

## Collecting APM Data:



________________________________________________________________________________________________________________ 

**Bonus Question: What is the difference between a Service and a Resource?**

>A Service is 

Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

Please include your fully instrumented app in your submission, as well.
