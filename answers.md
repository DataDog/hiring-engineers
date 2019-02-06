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
   
   The min_collection_interval allows you to modify the timelimit for collection of the metric without having to change the python code at all.
   
Visualizing Data:
Utilize the Datadog API to create a Timeboard that contains:

Your custom metric scoped over your host.
Any metric from the Integration on your Database with the anomaly function applied.
Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.

Once this is created, access the Dashboard from your Dashboard List in the UI:

Set the Timeboard's timeframe to the past 5 minutes
Take a snapshot of this graph and use the @ notation to send it to yourself.
Bonus Question: What is the Anomaly graph displaying?
Monitoring Data
Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

Warning threshold of 500
Alerting threshold of 800
And also ensure that it will notify you if there is No Data for this query over the past 10m.
Please configure the monitor’s message so that it will:

Send you an email whenever the monitor triggers.

Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.

Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.

When this monitor sends you an email notification, take a screenshot of the email that it sends you.

Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

One that silences it from 7pm to 9am daily on M-F,
And one that silences it all day on Sat-Sun.
Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.
Collecting APM Data:
Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:

from flask import Flask
import logging
import sys

# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

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
Note: Using both ddtrace-run and manually inserting the Middleware has been known to cause issues. Please only use one or the other.

Bonus Question: What is the difference between a Service and a Resource?

Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

Please include your fully instrumented app in your submission, as well.

Final Question:
Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?


