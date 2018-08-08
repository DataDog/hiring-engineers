Hello, please allow me to take you through this exercise.

Getting started.

I needed to enable VT-x options in the bios of the laptop first. Available inventory, a laptop with some free drive space, and [virtualbox](https://www.virtualbox.org/wiki/Downloads)
Next up was to install vagrant. This resulted in a running virtual machine vm, with just an ssh terminal. This worked, until laptop went to sleep, woken up and the vm was corrupt. The rest of the exercise was performed inside a normal vm inside virtualbox. Please see this [guide to installing ubuntu as a vm inside virtualbox](https://askubuntu.com/questions/142549/how-to-install-ubuntu-on-virtualbox)
last prep step was to sign up for DataDog trial. This process asks a few questions and results with an api key that associates your company with the DataDog servers.   

Then inside the vm ssh terminal, run the command provided, substituting in your own key :
`DD_API_KEY=149af9318091dbc92d4e4e2ec60f32f1 bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"`

# H1 Collecting Metrics:
--Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
Please see these pages as reference material.
https://docs.datadoghq.com/getting_started/tagging/assigning_tags/
https://docs.datadoghq.com/agent/basic_agent_usage/ubuntu/

Inside the vm ssh terminal, run the commands:
cd /etc/datadog-agent
sudo cp datadog.yaml datadog.yaml.bak
sudo nano datadog.yaml

Side note : the second line above is a safety measue, to enable “rollback” should something go wrong. Not strictly needed, just a safety precaution.
This opens an editor, please scroll down til you see the section #tags”, uncomment tags: by removing the # in front, 
and follow by adding in the rest seen below, change tags ass desired.
tags:
 - region:east
 - region:south
 - application:database
 - database:primary
 - role:testing

Press control + O to save, control + x to exit when finished. This drops you back to the terminal prompt. 
Type :
sudo service datadog-agent restart
sudo datadog-agent status
Please see file : etc.datadog-agent.datadog.yaml
Now wait. Go make a cup of coffee, watch the weather channel in the breakroom. You deserve it.


--Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
Please see these pages as reference material.
https://docs.datadoghq.com/agent/faq/agent-configuration-files/#agent-configuration-directory
https://docs.datadoghq.com/integrations/mysql/
https://stackoverflow.com/questions/39281594/error-1698-28000-access-denied-for-user-rootlocalhost

I started with a fresh ubuntu vm. Anything needed would have to be installed/added.
Inside the vm ssh terminal, run the commands:
sudo apt-get update
sudo apt-get install mysql-server
cd /etc/datadog-agent/conf.d/mysql.d
sudo cp conf.yaml.example conf.yaml
mysql -u root 
CREATE USER 'datadog'@'localhost' IDENTIFIED BY 'PASSWORD';
exit

This drops you back to the terminal prompt.
Run this from unix commandline, not mysql commandline (where we are now) :
mysql -u datadog --password=PASSWORD -e "show status" | \
grep Uptime && echo -e "\033[0;32mMySQL user - OK\033[0m" || \
echo -e "\033[0;31mCannot connect to MySQL\033[0m"

mysql -u datadog --password=PASSWORD -e "show slave status" && \
echo -e "\033[0;32mMySQL grant - OK\033[0m" || \
echo -e "\033[0;31mMissing REPLICATION CLIENT grant\033[0m"

now we need to go back in mysql, add permissions. Type :
mysql -u root
GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'localhost' WITH MAX_USER_CONNECTIONS 5;
GRANT PROCESS ON *.* TO 'datadog'@'localhost';
show databases like 'performance_schema';
GRANT SELECT ON performance_schema.* TO 'datadog'@'localhost';
exit
This all gives the DataDog client access to the mysql db.

Type these commands:
cd /etc/datadog-agent/conf.d/mysql.d
sudo nano conf.yaml

This opens an editor, please scroll down til you see the section “#instances:” , uncomment instances:, add in this below.
Be careful, the spacing is important. Can either uncomment appropriate lines, or leave the whole comment block in and just add this in in addition to preserve the original as examples.

 - server: 127.0.0.1
   user: datadog
   pass: 'Rm117Onleave'
   port: 3306
   options:
       replication: 0
       galera_cluster: 1
       extra_status_metrics: true
       extra_innodb_metrics: true
       extra_performance_metrics: true
       schema_size_metrics: false
       disable_innodb_metrics: false

Press control + O to save, control + x to exit when finished. This drops you back to the terminal prompt. 
Please see file etc.datadog-agent.conf.d.mysql.d.conf.yaml
Type these commands:
sudo service datadog-agent restart
sudo datadog-agent status
sudo nano /etc/mysql/my.cnf

Add in this to the end of the file :

[mysqld_safe]
log_error=/var/log/mysql/mysql_error.log
[mysqld]
general_log = on
general_log_file = /var/log/mysql/mysql.log
log_error=/var/log/mysql/mysql_error.log
slow_query_log = on
slow_query_log_file = /var/log/mysql/mysql-slow.log
long_query_time = 2

Press control + O to save, control + x to exit when finished. This drops you back to the terminal prompt. 
Please see file etc.mysql.my.cnf
Type these commands:
service mysql restart

This section is needed to grant the DataDog agent access to the logrotate folder, mysql log files.
Please see this page as a guide :
https://help.datadoghq.com/hc/en-us/articles/360001001211-Setting-file-permissions-for-rotating-logs-linux-
Type these commands:
sudo setfacl -m u:dd-agent:rx /var/log/mysql
getfacl /var/log/mysql
sudo touch /etc/logrotate.d/dd-agent_ACLs
sudo nano /etc/logrotate.d/dd-agent_ACLs

This opens an editor, which was blank, add in below :
{
 postrotate
 /usr/bin/setfacl -m g:dd-agent:rx /var/log/mysql
 endscript
}

Press control + O to save, control + x to exit when finished. This drops you back to the terminal prompt. 
Please see file etc.logrotate.d.dd-agent_ACLs
Type these commands:
sudo nano /etc/logrotate.d/mysql-server
edit first line to look like: /var/log/mysql.log /var/log/mysql/*log /var/log/mysql/mysql.log /var/log/mysql/mysql-slow.log {
edit create line to look like:  create 644 mysql adm

Press control + O to save, control + x to exit when finished. This drops you back to the terminal prompt. 
please see file etc.logrotate.d.mysql-server
Type these commands:
sudo nano /etc/datadog-agent/datadog.yaml

by default, the line looks like : #logs_enabled: false
use control + w to find line, change to :
logs_enabled: true

Press control + O to save, control + x to exit when finished. This drops you back to the terminal prompt. 
Please see file etc.datadog-agent.datadog.yaml
Type these commands:
cd /etc/datadog-agent/conf.d/mysql.d
sudo cp conf.yaml conf.yaml.bak
sudo nano conf.yaml

This opens an editor, please scroll down til you see the section “#logs:” , uncomment logs:, add in this below.
Be careful, the spacing is important. Can either uncomment appropriate lines, or leave the whole comment block in and just add this in in addition to preserve the original as examples.

logs:
 - type: file
   path: /var/log/mysql/mysql_error.log
   source: mysql
   sourcecategory: database
   service: myapplication

 - type: file
   path: /var/log/mysql/mysql-slow.log
   source: mysql
   sourcecategory: database
   service: myapplication

 - type: file
   path: /var/log/mysql/mysql.log
   source: mysql
   sourcecategory: database
   service: myapplication
   # For multiline logs, if they start by the date with the format yyyy-mm-dd uncomment the following processing rule
   # log_processing_rules:
   #   - type: multi_line
   #     name: new_log_start_with_date
   #     pattern: \d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])

Press control + O to save, control + x to exit when finished. This drops you back to the terminal prompt. 
Please see file etc.datadog-agent.conf.d.mysql.d.conf.yaml
Type these commands:
sudo service datadog-agent restart
sudo datadog-agent status


--Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
Please see these pages as reference :
https://docs.datadoghq.com/developers/agent_checks/
https://datadog.github.io/summit-training-session/handson/customagentcheck/
https://docs.python.org/2/library/random.html
https://help.datadoghq.com/hc/en-us/articles/115002137506-Where-can-I-visualize-my-service-check-in-the-Datadog-UI-

Type these commands:
cd /etc/datadog-agent/conf.d/
sudo nano my_check.yaml

This opens an editor, which is blank, add in below :

init_config:

instances:
  - min_collection_interval: 45 #Change your check's collection interval so that it only submits the metric once every 45 seconds.

Press control + O to save, control + x to exit when finished. This drops you back to the terminal prompt. 
Please see file etc.datadog-agent.conf.d.my_check.yaml
Type these commands:
cd /etc/datadog-agent/checks.d
sudo nano my_check.py
This opens an editor, which is blank, add in below :

import random
from checks import AgentCheck
class my_metricCheck(AgentCheck):
  def check(self, instance):

    data=random.randrange(0, 1000, 1)

    self.gauge('my_check.update.value', data)


Press control + O to save, control + x to exit when finished. This drops you back to the terminal prompt. 
please see file etc.datadog-agent.checks.d.my_check.py
Type these commands:
sudo -u dd-agent -- datadog-agent check my_check
sudo service datadog-agent restart

--Bonus Question Can you change the collection interval without modifying the Python check file you created?
This page answers how to fo this : https://help.datadoghq.com/hc/en-us/articles/204590189-Is-there-an-alternative-to-dogstatsd-and-the-api-to-submit-metrics-Threadstats-

--Utilize the Datadog API to create a Timeboard that contains:
--Your custom metric scoped over your host.
https://app.datadoghq.com/dash/879620/mycheck?live=true&page=0&is_auto=false&from_ts=1533669047061&to_ts=1533683447061&tile_size=m

--Any metric from the Integration on your Database with the anomaly function applied.
Please see this page as reference: 
https://www.datadoghq.com/blog/introducing-anomaly-detection-datadog/
https://app.datadoghq.com/monitors/5814287

--Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
https://app.datadoghq.com/dash/879620/mycheck?live=true&page=0&is_auto=false&from_ts=1533669300761&to_ts=1533683700761&tile_size=m
please see dd-04


--Take a snapshot of this graph and use the @ notation to send it to yourself.
shows up in events, also see dd-02

--Bonus Question: What is the Anomaly graph displaying?
By analyzing a metric’s historical behavior, anomaly detection distinguishes between normal and abnormal metric trends. Anomaly detection can separate the trend component from the seasonal component of a timeseries, so it can track metrics that are trending steadily upward or downward. its not just a high or a low, it is using statistical models to detect something outside of normal. for example traffic, might be slow on a sunday morning, but to hit that same lower number on a Tuesday afternoon would not trigger a normal alert, it needs to correlate historical trends. 


Monitoring Data
Please see these pages as reference : 
https://docs.datadoghq.com/monitors/monitor_types/metric/
https://docs.datadoghq.com/monitors/notifications/#message-template-variables

here is the logic to send the alert
{{#is_alert}} value over 800, actual value of {{value}} and with IP {{host.ip}}  {{/is_alert}}
{{#is_warning}} value over 500 {{/is_warning}}
{{#is_no_data}} there is No Data for this query over the past 10m {{/is_no_data}} @hayesjonathand@gmail.com

please see picture dd-02


Collecting APM Data:
Please see these pages for reference :
https://docs.datadoghq.com/tracing/visualization/
https://stackoverflow.com/questions/31252791/flask-importerror-no-module-named-flask

Type these commands:
cd /etc/datadog-agent/checks.d
sudo apt-get install virtualenv python-virtualenv
sudo pip install flask
sudo virtualenv venv
. venv/bin/activate
sudo pip install blinker
sudo nano my_app.py

This opens an editor, which is blank, add in below :

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
Press control + O to save, control + x to exit when finished. This drops you back to the terminal prompt. 
Type these commands:
ddtrace-run python my_app.py
now visit vm_ip_address:5050, this triggers an event
now visit DataDog dashboard, should be a new lisitng under APM.
please see file etc.datadog-agent.checks.d.my_app.py
https://app.datadoghq.com/dash/879620?live=true&page=0&is_auto=false&from_ts=1533659542700&to_ts=1533673942700&tile_size=m

please see picture dd-03

-- Bonus Question: What is the difference between a Service and a Resource?
- a service is the job/action that performs the task. on linux these are typically daemons, on windows they are "services". some examples include ntp for time, iis as webserver.
- a resource is an action on or using a service. an example is an end to end dns request fulfilled, here the dns service is asked to perform its task and return information. the request and answer is the resource 

--final question. I am currently on the lookout for server gear to fillout my homelab. write up a a webpage that does a pricelookup for the specific item, returns dollar amount. use alert thresholds to send email when price gets below certian point.

