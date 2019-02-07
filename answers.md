### Here are my answers to the technical exercise

## Setup:
* My Environment:
  * Ubuntu VM - Vagrant setup / VirtualBox
  * Installed the Agent via the curl command per instructions
  * Installed and started MySQL Server on the VM
  
## Collecting Metrics:
* Created tags for the this host by editing the /etc/datadog-agent/datadog.yaml
  <img src=screenshots/datadog.yaml.jpg>
 
* Restarted the Agent: <B>sudo service datadog-agent restart</B>
* Verified new tag shows in Host Map view
  <img src=screenshots/hostmap.jpg>

* MySql Integration Setup
  * Instructions on configuration @ https://app.datadoghq.com/account/settings#integrations/mysql
  * datadog-agent status - error result on mysql config:
    <img src=screenshots/mysql_error.png>
  * Fixed issue with formating of conf.yaml file (space indentation):
    <img src=screenshots/conf.yaml.jpg>
  * datadog-agent status - warning result on mysql config:
    <img src=screenshots/mysql_warning.png>
    * Researched warning message:  <I>Warning: Privilege error or engine unavailable accessing the INNODB status</I>
    * Found: https://github.com/DataDog/dd-agent/issues/2376
    * Re-executed following and fixed the warning (thought I already did, but tried again :-)
       * sudo mysql -e "GRANT PROCESS ON *.* TO 'datadog'@'localhost';"
       * sudo mysql -e "GRANT SELECT ON performance_schema.* TO 'datadog'@'localhost';"
       
  * datadog-agent status - now OK  (woo hoo!)
    
    <img src=screenshots/mysql_good.png>
    
  * Custom Agent Check:
    * Custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
    * Created conf.d/my_metric.yaml and checks.d/my_metric.py
      ```
      init_config:

      instances:
        - min_collection_interval: 45
      ```
      ```
      import random
      try:
         from checks import AgentCheck
      except ImportError:
         from datadog_check.check import AgentCheck

      __version__ = "1.0.0"

      class MyMetric(AgentCheck):
         def check(self, instance):
            self.gauge('my_metric', random.randint(1,1000))
      ```
    * Check Agent Check configuration: <I>datadog-agent configcheck</I>
      <img src=screenshots/my_metric_configcheck.png>
    * Verified Agent Check: <I>dd-agent check my_metric</I>
      <img src=screenshots/my_metric_check.png>
    * Confirmed in Host Map UI:
      <img src=screenshots/my_metric.png>
  
* <B>Bonus Question</B> Can you change the collection interval without modifying the Python check file you created?
    * Yes, since the interval is defined in the .yaml config file, no change the python code is required
* Commentary:
    * Adding custom agent checks is very simple and having config and check python code separate makes it easier to maintain
    * configcheck and agent check commands make it easy to verify the custom agent check is setup and running correctly
   
## Visualizing Data
* Timeboard:
  * Your custom metric scoped over your host.
  * Any metric from the Integration on your Database with the anomaly function applied.
  * Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
    
* API python code to generate the Timeboard:
  ```
  ```
  
* My Timeboard showed up on Dashboard list:
  <img src=screenshots/timeboard.png>
    
  * Focused on the "MySQL Anomaly" graph for the last 5 minutes
  * Created a snapshot of that interval and used the @ mention notation to send it to myself:
    <img src=screenshots/snapshot.png>
      
* <B>Bonus Question:</B> What is the Anomaly graph displaying?
  * The Anomaly graph is identifying when a metric is behaving differently than it has in the past.  In my example, whether the MySQL instance CPU time was 3 std. deviations above or below the value over the the last 5 minutes.

* Commentary:
  * API documentation provided details and examples to easily be able to write the code to create the timeboard
  * Nice to have examples provided for Python, Ruby and Curl
  * Found that creating a graph and clicking on the JSON tab provided the correct syntax and content to be used with the API
  * One confusion I had was when instructed to take snapshot. The graph has camera icon, but if you hover over the icon sometimes it shows "Camera" and other times it shows "Annotate this graph". Was not clear at first that this was the snapshot.

## Monitoring Data
* New Metric Monitor my_metric that will alert if it’s above the following values over the past 5 minutes:
  * Warning threshold of 500
  * Alerting threshold of 800
  * And also ensure that it will notify you if there is No Data for this query over the past 10m
  * Monitor Notification:
    * Send you an email whenever the monitor triggers.
    * Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
    * Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
* Added new Metric Monitor using https://app.datadoghq.com/monitors#create/metric
* Exported Monitor configuration:
  ```
  {
	  "name": "My Metric Monitor",
	  "type": "metric alert",
	  "query": "max(last_5m):avg:my_metric{host:precise64} > 800",
	  "message": "{{#is_alert}} ERROR: 800 Threshold exceeded! Value is {{value}} on {{host.ip}} {{/is_alert}}\n{{#is_warning}} WARNING: 500 Threshold exceeded! {{/is_warning}} \n{{#is_no_data}} No data received in last 10 minutes {{/is_no_data}}\n\n@arlenh@comcast.net ",
	  "tags": [],
	  "options": {
		   "notify_audit": false,
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
* Alert Email (with trigger and host ip values):
  <img src=screenshots/alert_email.png>
* Warning Email:
  <img src=screenshots/warning_email.png>

* <B>Bonus Question:</B> Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:
  * One that silences it from 7pm to 9am daily on M-F,
  * One that silences it all day on Sat-Sun.
    
  * Email downtime scheduled:
    <img src=screenshots/downtime_email.png>

* Commentary:
  * UI "wizard" makes it very easy to create/edit/manage monitors
  * Downtime and Mute is nice feature to easily setup notification and silence windows
  * Export of configuration to JSON very nice so that can use that with API
    * Would be nice to have an import so that configs can be shared
  * Downtime email notification shows time range in UTC, even though selected time zone
    * Could not figure out how to set this in email template to show in time zone specified?
      
## Collecting APM Data
* Flask app instrumentation using Datadog’s APM solution:
  * pip install ddtrace
  * Run <I> ddtrace-run python myFlaskApp.py</I>
    
  * Alternatively, also instrumented script (found instructions @ http://pypi.datadoghq.com/trace/docs/web_integrations.html#flask) and called <I>python myFlaskApp.py</I> directly
    ```
    from ddtrace import patch_all
    patch_all()
      
    from flask import Flask
    import logging
    import sys

    # Have flask use stdout as the logger
    main_logger = logging.getLogger()
    ...
    ```
  * Used curl to access the different endpoints (e.g. curl localhost:5050/api/apm)
  * APM immediately shows data (e.g. trace list):
    <img src=screenshots/apm.png>
  * Created dashboard with APM and System metrics:
    https://app.datadoghq.com/dashboard/wxr-bs3-x6i/arlen?tile_size=m&page=0&is_auto=false&from_ts=1549494960000&to_ts=1549498560000&live=true
    <img src=screenshots/dashboard.png>
      
* <B>Bonus Question:</B> What is the difference between a Service and a Resource?
  * A service is a set of processes that do the same job - for example a web framework or database
  * A resource is a particular action for a given service (typically an individual endpoint or query)
    * For a web application: some examples might be a canonical URL, such as /user/home
    * For a SQL database: a resource is the query itself, such as SELECT * FROM users WHERE id = ?
  * So for the Flask example:
    * flask would be the service
    * /, /api/apm & /api/trace would be the resources
    <img src=screenshots/flask.png>

* Commentary:
  * APM collection setup is very simple
    * ddtrace-run seems like a prefered solution since it does not require changing/instrumenting the code
  * Data collection tracing was almost immediate.
  * Demonstrates real value to a customer/prospect that they can get APM up and running very quickly
  * Creating a dashboard was also very simple.  Drag-and-drop to select widget, select metric and data shows up immediately.  Nice!
  * Also nice feature of "Export to Timeboard" from APM services to easily add widget to Dashboard
    
## Final Question
* Is there anything creative you would use Datadog for?
  * Datadog could be used by grocery stores to monitor their stores.  With IOT being so prevelent, sensors could be put on refrigerators and freezers and Datadog could monitor temperature thresholds to assure that the units did not malfunction, thus saving money by getting notified of any issues immediately and preventing product loss.
