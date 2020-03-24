# Setup the environment 
## **Download VM and download Vagrant

 (https://github.com/sararidder/hiring-engineers/blob/master/Downloading_VM.png) 
 (https://github.com/sararidder/hiring-engineers/blob/master/VM.png)
 (https://github.com/sararidder/hiring-engineers/blob/master/Vagrant_Download.png)


## **Install Datadog Agent Ubuntu and use API Key
```
DD_AGENT_MAJOR_VERSION=7 
DD_API_KEY=21f04e5395da3b006b4dc9c1ad2802b4 bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
  ```
  
# **Collecting Metrics
## Add tags in the agent config file 
### Copy  datadog.yaml file and you only need to edit api_key, hostname, and tags within the datadog.yaml file. 

```
  sudo vi datadog.yaml
  cat datadog.yaml.example
  sudo vi datadog.yaml
  ```
  ### See datadog.yamal.2 for full example file 
(https://github.com/sararidder/hiring-engineers/blob/master/datadog.yaml.2)
  ```
  api_key: 21f04e5395da3b006b4dc9c1ad2802b4
hostname: vagrant
tags:
  - environment:dev
  - hosttype:vagrant
  ```

### Restart the agent to send updated tags to Datadog UI
  ```
  sudo service datadog-agent restart
  sudo service datadog-agent status
  sudo apt-get update
  ```
### See screenshot of tags
### (https://github.com/sararidder/hiring-engineers/blob/master/Host%20.png "host") 
### (https://github.com/sararidder/hiring-engineers/blob/master/Host%20Map.png "host map") 

## **Instal MySql Database (aka mariadb)
```
  sudo apt-get install -y mariadb-server
  sudo service mariadb status
  ```

## Install Datadog Ingeration for MySQL Database
```
vagrant@vagrant:/etc/datadog-agent/conf.d/mysql.d$ sudo mysql

MariaDB [(none)]>  CREATE USER 'datadogB'@'localhost' IDENTIFIED BY '<Data1234>';
Query OK, 0 rows affected (0.00 sec)

MariaDB [(none)]> GRANT REPLICATION CLIENT ON *.* TO 'datadogB'@'localhost' WITH MAX_USER_CONNECTIONS 5;
Query OK, 0 rows affected (0.01 sec)

MariaDB [(none)]> GRANT PROCESS ON *.* TO 'datadogB'@'localhost';
Query OK, 0 rows affected (0.00 sec)

MariaDB [(none)]> show databases like 'performance_schema';
+-------------------------------+
| Database (performance_schema) |
+-------------------------------+
| performance_schema            |
+-------------------------------+
1 row in set (0.00 sec)

MariaDB [(none)]> GRANT SELECT ON performance_schema.* TO 'datadogB'@'localhost';
Query OK, 0 rows affected (0.00 sec)

exit
```

### Insert updated MySQL Datadog user and password into the mysql.d/conf.yaml.example
```
vagrant@vagrant:cd /etc/datadog-agent/conf.d/mysql.d
ls conf.yaml.example

sudo vi conf.yaml.example

init_config:

instances:
  - server: 127.0.0.1
    user: datadogB
    pass: 'Data1234'
    port: 3306
    options:
     replication: false
     galera_cluster: false
     extra_status_metrics: true
     extra_innodb_metrics: true
     extra_performance_metrics: true
     schema_size_metrics: false
     disable_innodb_metrics: false


## Log Section (Available for Agent >=6.0)
##
## type - mandatory - Type of log input source (tcp / udp / file / windows_event)
## port / path / channel_path - mandatory - Set port if type is tcp or udp. Set path if type is file. Set channel_path if type is windows_event
## service - mandatory - Name of the service that generated the log
## source  - mandatory - Attribute that defines which Integration sent the logs
## sourcecategory - optional - Multiple value attribute. Used to refine the source attribute
## tags: - optional - Add tags to the collected logs
##
## Discover Datadog log collection: https://docs.datadoghq.com/logs/log_collection/
#
# logs:
#   - type: file
#     path: "<ERROR_LOG_FILE_PATH>"
#     source: mysql
#     sourcecategory: database
#     service: "<SERVICE_NAME>"
#
#   - type: file
#     path: "<SLOW_QUERY_LOG_FILE_PATH>"
#     source: mysql
#     sourcecategory: database
#     service: "<SERVICE_NAME>"
#     log_processing_rules:
#       - type: multi_line
#         name: new_slow_query_log_entry
#         pattern: "# Time:"
#         # If mysqld was started with `--log-short-format`, use:
#         # pattern: "# Query_time:"
#
#   - type: file
#     path: "<GENERAL_LOG_FILE_PATH>"
#     source: mysql
#     sourcecategory: database
#     service: "<SERVICE_NAME>"
## For multiline logs, if they start by the date with the format yyyy-mm-dd uncomment the following processing rule
#     log_processing_rules:
#       - type: multi_line
#         name: new_log_start_with_date
#         pattern: \d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])

sudo service datadog-agent restart
sudo service datadog-agent status
```

## Create Custom Agent "my_metric"
### Create python file (see mymetric.py) and a yaml file (mymetric.yaml)
cd  /etc/datadog-agent/checks.d
sudo vi /etc/datadog-agent/checks.d/mymetric.py

#paste in code from mymetric.py
cd /etc/datadog-agent/conf.d
sudo vi /etc/datadog-agent/conf.d/mymetric.yaml

#paste in code from mymetric.yaml
sudo service datadog-agent restart
sudo service datadog-agent status

#Change collection interval to 45 seconds
#Edit config file
sudo vi /etc/datadog-agent/conf.d/mymetric.yaml
#change min_collection_interval: 45
sudo service datadog-agent restart
sudo service datadog-agent status

#Go into Datadog UI > Metrics > Explorer > In graph type "my_metric"
  See screenshot 'My_Metric'


#Bonus Question
#Can you change the collection interval without modifying the Python check file you created?
  Answer: Yas you only need to change the yaml file.

##Visualizing Data##
  Create Timeboard
  https://app.datadoghq.com/dashboard/6j3-cgq-8h3/datadog-dashboard-v4?from_ts=1584649021785&live=true&tile_size=m&to_ts=1584652621785
  Mymetric Scoped by Host
  https://app.datadoghq.com/graph/embed?token=adb9a4ba5c3b0902f429d1f7d63da44fa93290b046ad8fe3e8c4227eba028788&height=300&width=600&legend=true
  MyMetric RollUp by Hour
  https://app.datadoghq.com/graph/embed?token=0feeefd97e3f19c6567b0473fa62b53c2d8fbb3aefc53ad4544fb2c16b4a7264&height=300&width=600&legend=true
  Anomalies MySql Max System CPU
  https://app.datadoghq.com/graph/embed?token=916d1baa31164655cbbab3458967a3279cbc8470e2acdc82df40bf477be0d528&height=300&width=600&legend=true


#Create New Dashboard with 3 widgets and See screenshot 'API_Timeboard'


api_key="21f04e5395da3b006b4dc9c1ad2802b4"
app_key="5e36d12e1847e5192eb7f7c358e6c5042f8e6b6e"

curl  -X POST \
-H "Content-type: application/json" \
-H "DD-API-KEY: ${api_key}" \
-H "DD-APPLICATION-KEY: ${app_key}" \
-d '{
  "title": "Datadog Dashboard",
  "widgets": [
    {
      "definition": {
        "type": "timeseries",
        "requests": [{"q": "avg:my_metric{host:vagrant}"}],
        "title": "Mymetric Scoped by Host"
      }
    },
    {
      "definition": {
        "type": "timeseries",
        "requests": [{"q": "avg:my_metric{host:vagrant}.rollup(sum, 3600)"}],
        "title": "Mymetric RollUp by Hour"
      }
    },
    {
      "definition": {
        "type": "timeseries",
        "requests": [{"q": "anomalies(max:system.cpu.system{host:vagrant}, \"basic\", 2)"}],
        "title": "Anomalies MySql Max System CPU"
      }
    }
  ],
  "layout_type": "ordered",
  "description": "A dashboard with mymetrics info.",
  "is_read_only": true,
  "notify_list": ["user@domain.com"],
  "template_variables": [
    {"name": "host", "prefix": "host", "default": "<HOSTNAME_1>"}
  ],
  "template_variable_presets": [
    {
      "name": "Saved views for hostname 2",
      "template_variables": [
        {"name": "host", "value": "<HOSTNAME_2>"}
      ]
    }
  ]
}' \
"https://api.datadoghq.com/api/v1/dashboard"

#Set Timeboard's timeframe to the past 5 mins
  See screenshot 'Timeframe_5_min'

#Snapshot and Annotation
  See screenshot 'Snapshot_Annotation'

#Bonus Question - What is the Anomaly graph displaying?
  Answer: The gray band shows us what is expected behavior on previous trends. If the traffic goes outside the gray bands then the trend goes outside of the expected behavior and can be considered an anomaly.

##Monitoring Data##

#Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

#Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.

{{#is_alert}}
  Mymetric is greater than 800
{{/is_alert}}

{{#is_warning}}
  Mymetric is above 500. Check on it
{{/is_warning}}

{{#is_no_data}}
  No data from Mymetric past 10 minutes
{{/is_no_data}}

Notify @sara.ridder77@gmail.com

#When this monitor sends you an email notification, take a screenshot of the email that it sends you.
  See screenshots: 'Is_Warning_500' , 'No_Data_Alert', 'Alert_Threshold_800'


#Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:
  See screenshots 'Weekend_Downtime', 'Email_Downtime', 'Daily_Downtime', and 'Email_Downtime_Daily'

##Collecting APM Data##
#Create file for the Flask App see app.py and create an API
#Within the app.py I added a hashbang to the script #!/usr/bin/env python this allowed me to execute the script like "./app.py"
vagrant@vagrant: sudo apt-get install python-pip
vagrant@vagrant: sudo pip install flask
vagrant@vagrant: cd /vagrant
vagrant@vagrant: ifconfig
vagrant@vagrant: sudo chmod +x ./app.py
vagrant@vagrant: ./app.py

#Enable APM and  set to non-localhost apm_non_local_traffic: true
vagrant@vagrant:/etc/datadog-agent/conf.d$ cd /etc/datadog-agent
vagrant@vagrant:/etc/datadog-agent$ ls
auth_token  checks.d  conf.d  datadog.yaml  datadog.yaml.example  selinux  system-probe.yaml.example
vagrant@vagrant:/etc/datadog-agent$ sudo vi datadog.yaml
#type "i" for insert mode
#set apm_non_local_traffic: true and then hit escape to get out of insert mode
#type ":wq" to save
vagrant@vagrant:/etc/datadog-agent$ sudo service datadog-agent restart

#Configure Your Environment through datadog.yaml file
vagrant@vagrant:/etc/datadog-agent$ sudo vi datadog.yaml
#type "i" for insert mode
api_key: 21f04e5395da3b006b4dc9c1ad2802b4
hostname: vagrant
tags:
  - environment:dev
  - hosttype:vagrant
apm_config:
  enabled: true
  env: vagrant
  receiver_port: 8126
  apm_non_local_traffic: true
#then hit escape to get out of insert mode
#type ":wq" to save
vagrant@vagrant:/etc/datadog-agent$ sudo service datadog-agent restart

#Import Trace
#Add the following commands to app.py  
import ddtrace

ddtrace.config.analytics_enabled = True

#Install Datadog Tracing Python
 sudo pip install ddtrace
 sudo ddtrace-run python /vagrant/app.py

  See screenshot 'APM_Infrastructure_Metrics'
 https://app.datadoghq.com/apm/service/flask/flask.request?end=1584744734988&env=vagrant&paused=false&start=1584741134988


#Bonus Question: What is the difference between a Service and a Resource?
An example of service would be a group of MariaDB queries whereas resource is a specific database query on MariaDB.


##Final Question##
COVID-19 is on everyone's minds so I think it could be beneficial to show wait times/load in the ER, number of available beds by each hospital, overall number of COVD-19 tests by each state.

A happier idea would be to monitor the number of times my dog goes outside. I would need to put a tracker on our doggie door but definitely think it could work.  It would be interesting to see if seasonality impacts (I assume it does) how much she goes outside or perhaps day of the week or time of day.
