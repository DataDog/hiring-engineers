## Collecting Metrics:
* My Environment:
  * Single RHEL 7 VM running on my laptop
  * Installed and started a MySQL instance on the VM
* Datadog Agent Install/Configuration
  * Installed the Agent via the very simple curl command
  * Created tags for the this host by editing the /etc/datadog-agent/datadog.yaml
  * restarted the Agent via systemctl
  * Below is a screen shot showing my new host tags via the Host Map Page:

  <img src=screenshots/screenshot1.png>
* MySQL Datadog Integration Configuration
  * Created the datadog user and set the DB permissions inside MySQL
  * Added the following stanza to the /etc/datadog-agent/conf.d/mysql.d/conf.yaml
  ```
    instances:
    - server: 127.0.0.1
      user: datadog
      pass: 'password' # from the CREATE USER step earlier
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
  * Restarted the agent via systemctl
  * Screenshot of the MySQL Integration in the Host Map page:

   <img src=screenshots/screenshot2.png>

* Created a custom metric called my_metric that provides a value between 0 and 1000.
  * Created the following script and put it under the /etc/datadog-agent/checks.d/mymetric.py

  ```
   import random

   try:
     from checks import AgentCheck
  except ImportError:
     from datadog_check.check import AgentCheck

  __version__ = "0.0.9"

  class MyMetric(AgentCheck):
     def check(self, instance):
        self.gauge('my_metric', random.randint(1,1001))
  ```
  * Configured the datadog agent to run that script, as well as changed the default collection interval, by creating the following yaml file in /etc/datadog-agent/conf.d/mymetric.d/mymetric.yaml

  ```
  init_config:

  instances:
  - min_collection_interval: 45
  ```
  * restarted the agent via systemctl to have it pick up the new configuration
  * Was able to confirm that the agent was doing this check by running both 'datadog-agent configcheck' and 'datadog-agent check mymetric'
* The Metrics Collection Outcome:
   * **Bonus Question:** The configuration of the interval is not done via the python script but in fact is done by the configuration mymetric.yaml file in /etc/datadog-agent/conf.d/.
   * Having agent management done this way is a great configuration for a customer.  The check as well as the configuration can maintained independently.
   * Having these configurations both be flat text files allows for them managed and maintained in a version control system such as git.   
   * The simplicity of creating new checks and/or integrations by just pushing configuration files makes adding functionality/reporting to the Datadog console a very easy process.
   * These configuration files can easily be put in place at the time of server provisioning as well as maintained via an automation system such as Ansible.

## Visualizing Data:
* Created the following python script to create a Timeboard called 'Ryan Great Timeboard' with the following graphs included:
   * Your custom metric scoped over your host.
   * Any metric from the Integration on your Database with the anomaly function applied.
   * Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket


```
#!/usr/bin/python
from datadog import initialize, api

options = {
   'api_key': '17370fa45ebc4a8184d3dde9f8189c38',
   'app_key': 'b0d652bbd1d861656723c1a93bc1a2f22d493d57'
}

initialize(**options)

title = "Ryan Great Timeboard"
description = "My Timeboard that is super awesome"
graphs = [
{
  "title": "My Metric over my host",
  "definition": {
  "requests": [
    {
      "q": "avg:my_metric{host:secondaryhost.hennvms.net}",
      "type": "line",
      "style": {
        "palette": "dog_classic",
        "type": "solid",
        "width": "normal"
      },
      "conditional_formats": [],
      "aggregator": "avg"
    }
  ],
  "autoscale": "true",
  "viz": "timeseries"
  }
},
{
  "title": "MySQL Anomaly Function Applied",
  "definition": {
  "viz": "timeseries",
  "requests": [
    {
      "q": "anomalies(avg:mysql.performance.user_time{*}, 'basic', 2)",
      "type": "line",
      "style": {
        "palette": "dog_classic",
        "type": "solid",
        "width": "normal"
      },
      "conditional_formats": [],
      "aggregator": "avg"
    }
  ],
  "autoscale": "true"
  }
},
{
  "title": "My Metric Rollup Function",
  "definition": {
  "viz": "query_value",
  "requests": [
    {
      "q": "avg:my_metric{*}.rollup(sum, 60)",
      "type": "line",
      "style": {
        "palette": "dog_classic",
        "type": "solid",
        "width": "normal"
      },
      "conditional_formats": [],
      "aggregator": "avg"
    }
  ],
  "autoscale": "true"
  }
}]

api.Timeboard.create(title=title, description=description, graphs=graphs)
```   

* From there I was able to login into the dashboard and see that the Timeboard was created.
  * I focused on the 'mymetric' graph and zoomed into the a 5 minute collection interval.
  * Created a snapshot of that graph with the 5 minute interval and sent it to myself via the @ mention.
  * The snapshot of the graph was then sent to the 'Events' feed in my account.  This is a great feature for quickly sharing graphs and information with users that might not be as familiar with the platform.   A more educated user can login and create/share information so quickly and with out having to do crazy stuff such as screen snapshots or data reformatting in an excel sheet.  
* Examples:
   * Data on Timeboard functionality

   <img src=screenshots/timeboarddata.png>
   * The snapshot that showed up my the Event feed:

   <img src=screenshots/last5minutes.png>
* The Visualizing Data Outcome:
  * **Bonus Question:**  The graph highlights the times where the metric (in this case the MySQL instance user time CPU cycles) was more or less than the average consumption.   Having this data sitting along side system/OS metrics can really assist with troubleshooting issues such as: "It was running OK yesterday, but not today"
  * Creating the Timeboard data was really quick and simple. The configuration of the charts are easy to search and implement via the Dashboard.
  * I was able to create the script quick and easy from the API documentation provided.  
  * Creating the graphs via the API was easy after I understood the information that was needed.  This was quickly gathered by creating the graph in the dashboard and the clicking on JSON tab after the graph was formatted.   Making the learning curve for a customer to use and manage the platform, via the API, very short.

## Monitoring Data
* Created a new monitor for the my_metric value with the following configuration:
  * Warning threshold of 500
  * Alerting threshold of 800
  * And also ensure that it will notify you if there is No Data for this query over the past 10m.
  * Send you an email whenever the monitor triggers.
  * Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
  * Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
  * When this monitor sends you an email notification, take a screenshot of the email that it sends you.
* The exported configuration for that monitor is below:
```
{
"name": "My Metric Alert",
"type": "metric alert",
"query": "avg(last_5m):avg:my_metric{*} > 800",
"message": "{{#is_alert}}Alert: The My Metric value is {{my_metric}} on {{host.ip}} {{/is_alert}} \n{{#is_warning}}Warning the My Metric Value is getting high on {{host.name}} {{/is_warning}} \n{{#is_no_data}}There has been not data for the My Metric value on host {{host.name}} {{/is_no_data}} \n\n @henndawg80@gmail.com",
"tags": [],
"options": {
  "notify_audit": true,
  "locked": false,
  "timeout_h": 0,
  "new_host_delay": 300,
  "require_full_window": true,
  "notify_no_data": true,
  "renotify_interval": "0",
  "escalation_message": "",
  "no_data_timeframe": 10,
  "include_tags": true,
  "thresholds": {
    "critical": 800,
    "warning": 500
  }
}
}
```

* Also included a screenshot of the email alert that was sent after the monitor was set up.

<img src=screenshots/emailalert.png>

* The Monitoring Data Outcome:
  * **Bonus Question**: Downtime created and the screen shot of the email notifications:

<img src=screenshots/emailnotification.png>
  * The ease of creating a monitor allows for the most novice user to create a new monitors.
  * It is great to see that you can export the monitor configuration for  use later with the API.  A user can use/tweak this JSON for creating a group of similar monitors.
  * The fact that the monitor content data can be specific to a level of alert is really great to provide actual real world fixes/troubleshooting steps in the alert notification.
  * Also was very excited to see that the alert itself (in the Event feed and the email notification) shows the alert graph information.  This makes the late night troubleshooting a whole lot easier.  Operations team members have a lot of the alert data right in the email (monitoring trending and potential troubleshooting information). It helps not having to login to a lot of tools to get all the information that you need to start troubleshooting.

## Collecting APM Data:
* Used the Flask app provided.  Just needed to modify it a bit to import the dd-trace python module.
  * installed the dd-trace module via pip
  * Modified the script so that import and patch_all() function was called right at the beginning of execution.
  * The updated script:

```
from ddtrace import patch_all
patch_all()

from flask import Flask
import logging
import sys

# Have flask use stdout as the logger
#main_logger = logging.getLogger()
#main_logger.setLevel(logging.DEBUG)
#c = logging.StreamHandler(sys.stdout)
#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#c.setFormatter(formatter)
#main_logger.addHandler(c)

app = Flask(__name__)

@app.route('/')
def api_entry():
    return 'Entrypoint to the Application'

@app.route('/api/apm')
def apm_endpoint():
    return 'Getting APM Started'

@app.route('/api/trace')
def trace_endpoint():
    return 'Posting Traces'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
```

 * After starting up the example Flask app, I ran a couple simple Bash for loops to curl the different endpoints defined in the Flask app.
 * Checking in the Dashboard it seemed that the APM data started following almost immediately.
 * Was able to create a Timeboard that included graphs with both APM data (in this case the request duration for each of the endpoints) as well as system/OS metrics (Memory and CPU consumption)
    * Timeboard URL:  https://app.datadoghq.com/dash/1020451/apm-dashboard?tile_size=m&page=0&is_auto=false&from_ts=1544796420000&to_ts=1544800020000&live=true
    * Screenshots of the graphs as I was running the for loops against the different endpoints

    <img src=screenshots/apm.png>

* Collecting APM Outcome:
   * **Bonus Question:**
      * In the case of the example provided the service is a fully implemented web application.  The resources are each of the different endpoints in that service.   
      * So a service is a super set grouping of resources.
      * Resources are different types of function that make up an full service  (Such as Databases, Application, and Web tiers).
      * Group in this manner allows for easy identification of the actual resource.  As in many large organizations, resource types will be repeated over and over.  By have a unique service name to each of them, it makes it easier to identity which resource you are actually looking at.
  * The actual implementation of the APM collection is very easy.
     * Either prepending the dd-trace in front of the application invocation.
     * Or including the library in the actual code.
  * Also like that you call out to exclude certain resources from the collection when you start the service.  In some cases the customer/developer will not want/need that data.
  * It is great to see that you can start collecting data right away.   Making use of the agent and showing value to the customer.
  * Great to be able map the full stack together in a Timeboard.
    * troubleshooting issues where it is unclear if it is the application and/or the infrastructure is the cause of an issue.
    * Get a full snapshot of a healthy application so you have baseline to compare against.

## Final Question:
For my own personal use I could see using this for collecting and monitoring the number of events on my different home automation devices.  I current gather metrics from these devices but have no real visibility beyond log data.  I could create a new metric gathering item and gather those events in real time.  I could also set alerts on certain thresholds to know things like when the kids leave the garage door open :-)
