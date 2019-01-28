Collecting Metrics:

	•	Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
  
  Screenshot: 
  
  ![alt text](https://github.com/ivantirado/hiring-engineers/blob/master/Datadog%20-%20Tags.png "Host with Tags")

  
  Configuration: 
  
  ![alt text](https://github.com/ivantirado/hiring-engineers/blob/master/Datadog%20-%20Tagsconfig.png "Tag Configuration")
  
	•	Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
  
  Installed MongoDB and the integration works as expected. The documentation and examples were real easy to follow.
  
  	•	Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
    
  Created my own agent check based on documentation I found on Datadog. Very easy to follow, and adopted the try/check logic to increase compatibility on agent version.
  
  Code:
  
  ```python
try:
    from checks import AgentCheck
except ImportError:
    from datadog_checks.checks import AgentCheck

from random import randint

__version__ = "1.0.0"

class my_metric(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', randint(1, 1000))
```

Adapted from here: [Datadog Docs](https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6)

	•	Change your check's collection interval so that it only submits the metric once every 45 seconds.
  
  This is changed on the instance configuration of the YAML. 
  
  Code:
  
  ```python
init_config:

instances:
  - min_collection_interval: 45
```

	•	Bonus Question Can you change the collection interval without modifying the Python check file you created?
  
The collection interval is changed on the YAML config file, not on the python file itself, so yes, the collection interval can be changed without altering the python code.

Visualizing Data:
Utilize the Datadog API to create a Timeboard that contains:

	•	Your custom metric scoped over your host.
	•	Any metric from the Integration on your Database with the anomaly function applied.
	•	Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
  
The above task was performed with this script: [Dashboard API script](https://github.com/ivantirado/hiring-engineers/blob/master/dashboard.py "Script")

Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.

Script is included above (in repository root)

Once this is created, access the Dashboard from your Dashboard List in the UI:
	•	Set the Timeboard's timeframe to the past 5 minutes
  
  Screenshot:
  
  ![alt text](https://github.com/ivantirado/hiring-engineers/blob/master/Datadog%20-%205m%20custom%20dashboard.png "5m Dashboard")
  
	•	Take a snapshot of this graph and use the @ notation to send it to yourself.
  
  I didn't find a way to take a snapshot of the whole dashboard/timeboard, but I was able to use the @ notation to snapshot individual graphs and send them to myself.
  
  Screenshot:
  
  ![alt text](https://github.com/ivantirado/hiring-engineers/blob/master/Datadog%20-%20at%20notation%20email.png "at notation")
  
  
	•	Bonus Question: What is the Anomaly graph displaying?
  
Mine isn't displaying much. It's mirroring the value of the connections on MySQL, because I don't have active users nor enough data for anomalies to be calculated. If I had these things, it would display the values as well as the deviations from the configurable norm. (stdev)
  
  Screenshot:
  
  ![alt text](https://github.com/ivantirado/hiring-engineers/blob/master/Anomalies.png "Anomalies")
  
Monitoring Data
Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.
Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:
	•	Warning threshold of 500
	•	Alerting threshold of 800
	•	And also ensure that it will notify you if there is No Data for this query over the past 10m.
  
  Created the monitor, it's difficult to get a full screenshot of the entire page.

Screenshot:

![alt text](https://github.com/ivantirado/hiring-engineers/blob/master/Monitor%20Config.png "Monitor Config")


Please configure the monitor’s message so that it will:
	•	Send you an email whenever the monitor triggers.
	•	Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
	•	Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
	•	When this monitor sends you an email notification, take a screenshot of the email that it sends you.
  
  The monitor is configured per the above. This is the config on the SAY WHAT'S HAPPENING section.
  
  Code:
  
  ```
{{#is_alert}} My_Metric at IP: {{host.ip}} has been at {{value}} for the last 5 minutes. {{/is_alert}}
{{#is_warning}} My_Metric has been between 500 and 800 for the last 5 minutes {{/is_warning}}
{{#is_no_data}} No data for My_Metric for the last 10 minutes. {{/is_no_data}}

@ivanhoek@gmail.com
```

Screenshot:

![alt text](https://github.com/ivantirado/hiring-engineers/blob/master/Monitor%20custom%20email.png "Monitor Email")

	•	Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:
	◦	One that silences it from 7pm to 9am daily on M-F,
	◦	And one that silences it all day on Sat-Sun.
	◦	Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.
  
  The downtimes were configured per the above requests. 
  
  Weekend Downtime Screenshot:
  
  ![alt text](https://github.com/ivantirado/hiring-engineers/blob/master/Weekend%20Downtime.png "Weekend Downtime")
  
  Weekday Downtime Screenshot:
  
  ![alt text](https://github.com/ivantirado/hiring-engineers/blob/master/Weekday%20Downtime.png "Weekday Downtime")
  
	◦	Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.
  
  Notification Screenshots for Downtime:
  
  ![alt text](https://github.com/ivantirado/hiring-engineers/blob/master/Weekday%20Downtime%20Notification.png "Weekday Downtime Notification")
  
  ![alt text](https://github.com/ivantirado/hiring-engineers/blob/master/Weekend%20Downtime%20Notification.png "Weekend Downtime Notification")
  
Collecting APM Data:
Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:

	•	Bonus Question: What is the difference between a Service and a Resource?
  
  A Service is, for example a web application. It's the thing that performs a task using compute power. A resource, on the other hand, is a query to a service. An example of a resource would be a specific path or URL.
  
Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

Screenshot:

![alt text](https://github.com/ivantirado/hiring-engineers/blob/master/Datadog%20-%20APM%20Dashboard.png "APM/Infrastructure Dashboard")

Please include your fully instrumented app in your submission, as well.

The instrumented application is here: [Instrumented Application](https://github.com/ivantirado/hiring-engineers/blob/master/instrument.py)

Final Question:
Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!
Is there anything creative you would use Datadog for?

I'm already thinking of writing a replacement for my clunky HomeSeer home automation implementation. I think the flexibility that DataDog offers is such that accurate/quick resource status query can be combined with status set using other scripting. Also, it would be cool to use this to monitor stocks.



