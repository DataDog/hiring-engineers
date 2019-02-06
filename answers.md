### Here are my answers to the technical exercise

## Setup:
* My Environment:
  * Ubuntu VM - Vagrant setup / VirtualBox
  * Installed the Agent via the curl command per instructions
    * Error: The program 'curl' is currently not installed.
    * Installed curl: <b>sudo apt-get install curl</b>
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
  * datadog-agent status - now OK   Woo Hoo!
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

## Monitoring Data
  * New Metric Monitor my_metric that will alert if it’s above the following values over the past 5 minutes:
    * Warning threshold of 500
    * Alerting threshold of 800
    * And also ensure that it will notify you if there is No Data for this query over the past 10m
    * Monitor Notification:
      * Send you an email whenever the monitor triggers.
      * Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
      * Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
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
      
        
      


