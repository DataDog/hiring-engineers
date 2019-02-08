## Collecting Metrics:
* My Environment:
  * RHEL 7u6 virtual machine
  * Installed Mariadb (Mysql) instance on the VM
  ```
  yum install mariahdb
  ```
  * Created test database and configured service to run
  ```
  systemctl enable mariadb
  systemctl start mariadb
  ```
  * Configured the Mariadb for the datadog-agent
  ```
  mysql -e "CREATE USER 'datadog'@'localhost' IDENTIFIED BY 'passworddb';"
  mysql -e "GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'localhost' WITH MAX_USER_CONNECTIONS 5;"
  mysql -u datadog --password='passworddb' -e "show status" | \ grep Uptime && echo -e "\033[0;32mMySQL user - OK\033[0m" || \ echo -e "\033[0;31mCannot connect to MySQL\033[0m"
  mysql -u datadog --password='passworddb' -e "show slave status" && \ echo -e "\033[0;32mMySQL grant - OK\033[0m" || \ echo -e "\033[0;31mMissing REPLICATION CLIENT grant\033[0m"
  mysql -u datadog --password='passworddb' -e "SELECT * FROM performance_schema.threads" && \ echo -e "\033[0;32mMySQL SELECT grant - OK\033[0m" || \ echo -e "\033[0;31mMissing SELECT grant\033[0m"
  mysql -u datadog --password='passworddb' -e "SELECT * FROM INFORMATION_SCHEMA.PROCESSLIST" && \ echo -e "\033[0;32mMySQL PROCESS grant - OK\033[0m" || \ echo -e "\033[0;31mMissing PROCESS grant\033[0m"
  ```
* Datadog Agent Install/Configuration
  * Installed the Agent via the very simple curl command
  ```
  DD_API_KEY=0f4ed1330465ec78f05d13b39c865135 bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
  ```
     * Had issues with the fact that I just let the default hostname be localhost.localdomain.  Once I changed the hostname it fixed the issue of the Host Map kept saying install agent when I clicked on the host. I changed the name in the /etc/hostname and rebooted the system.  During this time I used different tools to troubleshoot the issue.  I also modified the log_level to DEBUG to see if I could fine the issue causing the problem.  I found a syntax error in my datadog.yaml using the datadog-agent configcheck and was also able to correct it.
  * Editing the /etc/datadog-agent/datadog.yaml to create tags
  ```
      tags:
      - mytag
      - env:nonprod
      - role:whatthehell
      - pleaseworkansible
  ```
  
  * Used systemctl to restart the Agent
  ```
  systemctl restart datadog-agent.service
  ```
  * Here is a screen shot showing my new host tags via the Host Map Page:
![alt text](https://github.com/bluey64/hiring-engineers/blob/solutions-engineer/DD-Tags-screenshot.png "Host with Tags")

* Custom Agent Check metric Named my_metric with random value between 0 and 1000

/etc/datadog-agent/checks.d/my_metric.py
```
   from random import randint

   try:
     from checks import AgentCheck
   except ImportError:
     from datadog_check.check import AgentCheck
  
   _version_ = "0.0.8"

   class my_metric(AgentCheck):
      def check(self, instance):
         self.gauge('my_metric' , randinit(1,1000))
```
* Set the interval to every 45 seconds

/etc/datadog-agent/conf.d/my_metric.d/my_metric.yaml
   ```
   init_config:

   instances:
     - min_collection_interval: 45
   ```
   * Bonus:
   
   The min_collection_interval allows you to modify the timelimit for collection of the metric without having to change the python code at all.  This allows admins to change without knowing how to read the code.
   
Visualizing Data:
* Utilize the Datadog API to create a Timeboard that contains:
 * Intalled pip on my mac
 ```
 sudo easy_install pip
 ```
 * Used pip to install datadog python module
```
pip install datadog
```
 * Looked at the documentation for API integration.
 * Also created a timeboard via the GUI to get a better idea of how to code it.
 * Below is the python code for my API call to create the timeboards. filename:dd-api.py
```
#!/usr/bin/python
from datadog import initialize, api

options = {'api_key': '0f4ed1330465ec78f05d13b39c865135',
           'app_key': '02aa01821ed3826e6ae0837649f256df3dea11aa'
          }

initialize(**options)

# Call Embed API function
api.Embed.get_all()

title = "My Special Timeboard"
description = "My SA sample timeboard for testvm.localdomain!"
graphs = [
{
  "title": "My_metric Timeboard",
  "definition": {
      "events": [],
      "requests": [
        {
           "q": "avg:my_metric{*}",
           "type": "line",
           "style": {
               "palette": "dog_warm",
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
  "title": "MySQL anonmalies Applied",
  "definition": {
  "viz": "timeseries",
      "events": [],
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
      "autoscale": "true",
    }
  },
{
  "title": "My_metric Rollup Timeboard",
  "definition": {
  "viz": "timeseries",
  "requests": [
    {
      "q": "avg:my_metric{*}.rollup(sum, 60)",
      "type": "line",
      "style": {
        "palette": "dog_classic",
        "type": "solid",
        "width": "normal"
      },
      "conditional_formats": []
    }
  ],
  "autoscale": "true"
 }
}
]

api.Timeboard.create(title=title, description=description, graphs=graphs)
```
* Below is the screen shot of my_metric from my custom Timeboard
![alt text](https://github.com/bluey64/hiring-engineers/blob/solutions-engineer/My-metric-timeboard.png "My metric timeboard")

Bonus Question: What is the Anomaly graph displaying?
* The anomalies of the mysql metric against the systems averages.


* Monitoring Data
  * Created the monitor for my_metric.
  * Warning at 500.
  * Alert at 800.
  * Notify if no data for 10 minutes.
  * All warnings, Alerts and notifications are sent to my email address with a different message linux64@gmail.com.
  * Below is the code used for my API call.
```
{
	"name": "Monitor Name: My Metric alarm",
	"type": "metric alert",
	"query": "avg(last_5m):avg:my_metric{host:testvm.localdomain} > 800",
	"message": "{{#is_alert}}Alert: My Metric is {{my_metric}} is high on {{host.ip}} {{/is_alert}}\n{{#is_warning}}Warning the My Metric Value is getting high on {{host.name}}{{/is_warning}}\n{{#is_no_data}}No data has been received My Metric value on host {{host.name}} {{/is_no_data}} \n@linux64@gmail.com",
	"tags": [],
	"options": {
		"notify_audit": false,
		"locked": false,
		"timeout_h": 0,
		"new_host_delay": 300,
		"require_full_window": false,
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

  * Screen Shot of a warning message sent to my email.

  ![alt text](https://github.com/bluey64/hiring-engineers/blob/solutions-engineer/Email-warning.png "Email warning")

  Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

  * Below is a screenshot of my scheduled downtime and the configuration of each.

  ![alt text](https://github.com/bluey64/hiring-engineers/blob/solutions-engineer/Manage-downtime-dd.png "Scheduled Downtime")

  * One that silences it from 7pm to 9am daily on M-F.

  ![alt text](https://github.com/bluey64/hiring-engineers/blob/solutions-engineer/M-F-Downtime.png "Monday-Friday scheduled downtime")

  * And one that silences it all day on Sat-Sun.

  ![alt text](https://github.com/bluey64/hiring-engineers/blob/solutions-engineer/Weekend-Downtime.png "Weekend scheduled downtime")

* Collecting APM Data:
  * Install pip from the Fedora EPEL repo
  ```
  yum install python-pip
  ```
  * Install ddtrace using pip
  ```
  pip install ddtrace
  ```
  * Executed the flask app on the host.
  * Started a script to curl to port 5050 to access an entry port with a while loop
  ```
  while true
   do 
   curl http://0.0.0.0:5050
   sleep 3
   done
  ```
  * Added the recommend configuration for APM data to the /etc/datadog-agent/datadog.yaml
  ```
  apm_config:
    analyzed_spans:
       flask|flask_span: 1
  ```
  
Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:
```
from ddtrace import check_all
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
    app.run(host='0.0.0.0', port='5050')
```    

Bonus Question: What is the difference between a Service and a Resource?
* Service is a grouping of resources
* In the example it is a webservice with multipule access points
* It was so easy to collect loads of data real quickly.  I was really impressed at how easy it was to setup and start collecting data.

Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.
   * Timeboard URL: https://app.datadoghq.com/dashboard/hwi-eac-fij/my-special-timeboard?tile_size=m&page=0&is_auto=false&from_ts=1549588380000&to_ts=1549591980000&live=true&tv_mode=false
   * Screenshot of my timeboard
 
  ![alt text](https://github.com/bluey64/hiring-engineers/blob/solutions-engineer/APM-dashboard.png "APM dashboard")

Final Question:
Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?
* There are many different applications that this could be used for.  Integration with the home automation or for monitoring small devices on pipelines or in oil fields to tell when one unit in the field changes production rates and is anonomaly.  This way you can see a divergant system quickly.  So in a really large environment you can know which system is having a problem quickly.  For me I would like to use it with my PI's some are doing home automation for items that I have upgraded to be automated. I could also use it to monitor the usage on my kids retropi to see how much time they spend playing on it.

