Here are my answers to the hiring exercise:


## Prerequisites - Setup the environment

I have started a linux VM via vagrant.
To do so, I have followed the tutorial in [this link]( 
https://www.vagrantup.com/intro/getting-started/)

However, to start a Ubuntu 16.04 VM, since this is the minimum required, I have used the following [link](https://gist.github.com/maxivak/c318fd085231b9ab934e631401c876b1)

This is the content of the vagrant file
<!-- >>>>>> BEGIN INCLUDED FILE (code_block): SOURCE Scripts/Vagrantfile -->
```
Vagrant.configure(2) do |config|

  config.vm.box = "ubuntu/xenial64"

  config.vm.provider "virtualbox" do |vb|
    #   # Display the VirtualBox GUI when booting the machine
    #   vb.gui = true
    #
    #   # Customize the amount of memory on the VM:
    vb.memory = "1524"
  end

end
```
<!-- <<<<<< END INCLUDED FILE (code_block): SOURCE Scripts/Vagrantfile  -->

I have used the following [link] (https://www.datadoghq.com/#) to get a free datadog account for 14 days.

To liaise the new environnement with Datadog, I have installed the agent on the VM, by following the steps related to Ubuntu in the Datadog GUI, Integrations > API > Ubuntu.

<img src="https://github.com/GafsiS/hiring-engineers/blob/master/Screenshots/setting_agent.png" />



## Collecting Metrics


# Adding tags in the agent file:

The tags were created by adding the following lines in /etc/datadog/datadog.yaml file:

<!-- >>>>>> BEGIN INCLUDED FILE (code_block): SOURCE Scripts/datadog.yaml -->

```
tags: env:test, host:ubuntu, name:xenial, region:france

```
<!-- <<<<<< END INCLUDED FILE (code_block): SOURCE Scripts/datadog.yaml  -->

A restart of the datadog agent is then done.

The documentation used can be found [here](https://docs.datadoghq.com/tagging/)

<img src="https://github.com/GafsiS/hiring-engineers/blob/master/Screenshots/adding_tags_xenial.png" />

## Installing a database

To install mysql on the VM, I have followed this [tutorial](https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-16-04)

# Setting the datadog-mysql integration:

I have followed the steps in this [link](https://docs.datadoghq.com/integrations/mysql/)

First step is to create a user 'datadog'

```
mysql> CREATE USER 'datadog'@'localhost' IDENTIFIED BY 'XXXXXXXX';
Query OK, 0 rows affected (0.00 sec)
```

```
vagrant@ubuntu-xenial:/etc/datadog-agent/conf.d/mysql.d$ mysql -u datadog --password="XXXXXXXX" -e "show status" | \
> grep Uptime && echo -e "\033[0;32mMySQL user - OK\033[0m" || \
> echo -e "\033[0;31mCannot connect to MySQL\033[0m";
mysql: [Warning] Using a password on the command line interface can be insecure.
Uptime  714
Uptime_since_flush_status       714
MySQL user - OK
```

```
mysql> GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'localhost' WITH MAX_USER_CONNECTIONS 5;
Query OK, 0 rows affected, 1 warning (0.00 sec)

mysql> GRANT PROCESS ON *.* TO 'datadog'@'localhost';
Query OK, 0 rows affected (0.00 sec)

mysql> show databases like 'performance_schema';
+-------------------------------+
| Database (performance_schema) |
+-------------------------------+
| performance_schema            |
+-------------------------------+
1 row in set (0.00 sec)

mysql> GRANT SELECT ON performance_schema.* TO 'datadog'@'localhost';
Query OK, 0 rows affected (0.00 sec)

mysql>
```

A restart of the agent is then neeeded. 


# Mysql files updates:

* Updating mysql init_config file:

This is how is written the conf.yaml file in /etc/datadog/check.d/mysql.d
<!-- >>>>>> BEGIN INCLUDED FILE (code_block): SOURCE Scripts/conf.yaml -->
```
instances:
    # NOTE: Even if the server name is "localhost", the agent will connect to MySQL using TCP/IP, unless you also
    # provide a value for the sock key (below).
  - server: 127.0.0.1
     user: datadog
     pass: XXXXXXXX
     port: 3306             # Optional
    # sock: /path/to/sock    # Connect via Unix Socket
    # defaults_file: my.cnf  # Alternate configuration mechanism
    # connect_timeout: None  # Optional integer seconds
    # tags:                  # Optional
    #   - optional_tag1
    #   - optional_tag2
     options:               # Optional
       replication: 0
    #   replication_channel: channel_1  # If using multiple sources, the channel name to monitor
    #   replication_non_blocking_status: false  # grab slave count in non-blocking manner (req. performance_schema)
       galera_cluster: 1
       extra_status_metrics: true
       extra_innodb_metrics: true
       extra_performance_metrics: true
       schema_size_metrics: false
       disable_innodb_metrics: false
```
<!-- >>>>>> END INCLUDED FILE (code_block): SOURCE Scripts/conf.yaml -->


* Updating my.cnf file
mysql logs were set and enabled on my.cnf

<!-- >>>>>> BEGIN INCLUDED FILE (code_block): SOURCE Scripts/my.cnf -->
```
!includedir /etc/mysql/conf.d/
!includedir /etc/mysql/mysql.conf.d/

[mysqld_safe]
log_error=/var/log/mysql/mysql_error.log
[mysqld]
general_log = on
general_log_file = /var/log/mysql/mysql.log
log_error=/var/log/mysql/mysql_error.log
slow_query_log = on
slow_query_log_file = /var/log/mysql/mysql-slow.log
long_query_time = 2
```
<!-- >>>>>> END INCLUDED FILE (code_block): SOURCE Scripts/my.cnf -->


* enabling mysql logs in datadog conf file:
The following lines were enabled in conf.d/mysql.d/conf.yaml

<!-- >>>>>> BEGIN INCLUDED FILE (code_block): SOURCE Scripts/conf.yaml -->
```
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
```
<!-- >>>>>> END INCLUDED FILE (code_block): SOURCE Scripts/conf.yaml -->

Agent restart was done after each change

# Creating custom metric


To set the custom metric, I have had to go through the documentation in this [link](https://docs.datadoghq.com/developers/agent_checks/) first.

In order to create a new metric, two files needs to be created:
- /etc/datadog-agent/conf.d/my_metric.yaml

<!-- >>>>>> BEGIN INCLUDED FILE (code_block): SOURCE Scripts/my_metric.yaml -->
```
init_config:
instances:
    [{}]
```
<!-- >>>>>> END INCLUDED FILE (code_block): SOURCE Scripts/my_metric.yaml -->


- /etc/datadog-agent/check.d/my_metric.py 

<!-- >>>>>> BEGIN INCLUDED FILE (code_block): SOURCE Scripts/my_metric.py -->

```
from checks import AgentCheck
import random

class my_check(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric',random.randint(0,1000))
```
<!-- >>>>>> END INCLUDED FILE (code_block): SOURCE Scripts/my_metric.py -->


To make the check run every 45s, I have updated the my_metric.yaml file as follows:

<!-- >>>>>> BEGIN INCLUDED FILE (code_block): SOURCE Scripts/my_metric.yaml -->
```
init_config:

instances:
 - min_collection_interval: 45
```
<!-- >>>>>> END INCLUDED FILE (code_block): SOURCE Scripts/my_metric.yaml -->

min_collection_interval: 45 was added to enable the check every 45s

<img src="https://github.com/GafsiS/hiring-engineers/blob/master/Screenshots/my_metric_interval_45.png" />

# BONUS QUESTION:
The change of the check interval is done on the config file, thus, no need to modify the python script.



## Visualizing data

To create timeboard using Datadog API, I have followed datadog documentation in this [link](https://docs.datadoghq.com/api/?lang=bash#timeboards)

First step was to create environement variables (api_key and app_key) with the datadog API keys values.
I got these keys values from Datadog GUI, Integrations > APIs > API Keys and Application Keys

<img src="https://github.com/GafsiS/hiring-engineers/blob/master/Screenshots/api_key.png" />

<img src="https://github.com/GafsiS/hiring-engineers/blob/master/Screenshots/app_key.png" />

```
vagrant@ubuntu-xenial:/etc/datadog-agent$ export app_key=bdfabec3f3baa57a44f6514d1d302fa3bed5e69a
vagrant@ubuntu-xenial:/etc/datadog-agent$ export api_key=e527bbb476b605db8ad1044e94ce2b3a
vagrant@ubuntu-xenial:/etc/datadog-agent$ echo $app_key
bdfabec3f3baa57a44f6514d1d302fa3bed5e69a
vagrant@ubuntu-xenial:/etc/datadog-agent$ echo $api_key
e527bbb476b605db8ad1044e94ce2b3a
```

To have an idea about the content of the script that I need to use, I have generated a timeboard with the three asked graphs and have checked the json script generated.

- My custom metric scoped over my host:
```
 "q": "avg:my_metric{*}",
      "type": "line",
      "style": {
        "palette": "dog_classic",
        "type": "solid",
        "width": "normal"
```

- A metric from the Integration with the Database with the anomaly function applied.
```
"q": "anomalies(avg:mysql.performance.cpu_time{*}, 'basic', 2)",
      "type": "line",
      "style": {
        "palette": "dog_classic",
        "type": "solid",
        "width": "normal"

```

- My custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
```
      "q": "avg:my_metric{*}.rollup(sum, 3600)",
      "type": "line",
      "style": {
        "palette": "dog_classic",
        "type": "solid",
        "width": "normal"
```

This is the content of the json script generated on the front end:

```
{
  "viz": "timeseries",
  "status": "done",
  "requests": [
    {
      "q": "avg:my_metric{*}",
      "type": "line",
      "style": {
        "palette": "dog_classic",
        "type": "solid",
        "width": "normal"
      },
      "conditional_formats": [],
      "aggregator": "avg"
    },
    {
      "q": "anomalies(avg:mysql.performance.cpu_time{*}, 'basic', 2)",
      "type": "line",
      "style": {
        "palette": "dog_classic",
        "type": "solid",
        "width": "normal"
      }
    },
    {
      "q": "avg:my_metric{*}.rollup(sum, 3600)",
      "type": "line",
      "style": {
        "palette": "dog_classic",
        "type": "solid",
        "width": "normal"
      }
    }
  ],
  "autoscale": true
}
```

This is the python script used to create the timeboard:
<!-- >>>>>> BEGIN INCLUDED FILE (code_block): SOURCE Scripts/my_app.py -->
```
from datadog import initialize, api

options = {
    'api_key': 'e527bbb476b605db8ad1044e94ce2b3a',
    'app_key': 'bdfabec3f3baa57a44f6514d1d302fa3bed5e69a'
}

initialize(**options)

title = "My Custom Timeboard"
description = "A dashboard created with API."
viz = "timeseries",
status = "done"
graphs = [{
           "title": "MyMetric Timeboard",
         "definition": {
         "events": [],
         "requests": [
         {
                "q": "avg:my_metric{host:ubuntu}",
                "type": "line",
                "style": {
                        "palette": "dog_classic",
                        "type": "solid",
                        "width": "normal"
                        },
                "conditional_formats": [],
                "aggregator": "avg"
        },
        {
        "q": "anomalies(avg:mysql.performance.cpu_time{host:ubuntu}, 'basic', 2)",
        "type": "line",
        "style": {
                "palette": "dog_classic",
                "type": "solid",
                "width": "normal"
                }
        },
        {
        "q": "avg:my_metric{host:ubuntu}.rollup(sum, 3600)",
        "type": "line",
        "style": {
                "palette": "dog_classic",
                "type": "solid",
                "width": "normal"
                }
        }
        ]
}
}]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:xenial"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)


```
<!-- >>>>>> END INCLUDED FILE (code_block): SOURCE Scripts/my_app.py -->

This is the Timeboard that was generated:

<img src="https://github.com/GafsiS/hiring-engineers/blob/master/Screenshots/MyCustomTimeboard.png"/>

Setting Timeboard's timeframe to the past 5 minutes: This is done by selecting the last 5min timeframe in the graph:

<img src="https://github.com/GafsiS/hiring-engineers/blob/master/Screenshots/my_metric_last_5min.png"/>

Taking a snapshot of this graph and using the @ notation to send it to yourself:

- Taking a snapshot
<img src="https://github.com/GafsiS/hiring-engineers/blob/master/Screenshots/snapshot.png"/>

- Email received
<img src="https://github.com/GafsiS/hiring-engineers/blob/master/Screenshots/email_snapshot.png"/>

## BONUS QUESTION:
--> The anomaly graph is displaying the expected behavior of the metric based on its past collected values.
In our case, the algorithm choosen is basic, it uses small amount of data to determine next value, but has a small range and can't determine long period behavior.


# Monitoring Data

In order to create the monitor, I have had to go through this [documentation](https://docs.datadoghq.com/monitors/).

The monitor was created through the front end

<img src="https://github.com/GafsiS/hiring-engineers/blob/master/Screenshots/notification_config.png"/>



and the following alerting template were used to create the notification emails, I wrote it after going through this [documentation](https://docs.datadoghq.com/monitors/notifications/).


Alerting message template:

***************************
```
Hello team,

{{#is_alert}}

Please be advised that the average of my_metric value is {{value}}, and is then beyond 800 on {{host.name}} ({{host.ip}}). This needs to be investigated as soon as possible.

{{/is_alert}}

{{#is_warning}}

Please be warned that the average of my_metric value is {{value}}, and is then beyond 500 on {{host.name}} ({{host.ip}}) . Please note that this needs to be investigated.

{{/is_warning}}

{{#is_no_data}}

Please be warned that no data was collected on {{host.name}} ({{host.ip}}), for my_metric the last 10min. Please note that this needs to be investigated.

{{/is_no_data}}

Regards, @safa.el.kafsi@gmail.com
```
***************************

These are the different emails that were received:

- Alert email
<img src="https://github.com/GafsiS/hiring-engineers/blob/master/Screenshots/Alert.png"/>

- Warning email:
<img src="https://github.com/GafsiS/hiring-engineers/blob/master/Screenshots/Warn.png"/>



## BONUS QUESTION


I have created the Maintenance Periods through datadog front end, and have followed this [documentation](https://docs.datadoghq.com/monitors/downtimes/) in order to do so.

These are the scheduled downtimes I have created:


- A scheduled downtime that silences MyMetric from 7pm to 9am on weekdays

<img src="https://github.com/GafsiS/hiring-engineers/blob/master/Screenshots/MaintenancePeriod_weekdays.png"/>

<img src="https://github.com/GafsiS/hiring-engineers/blob/master/Screenshots/maintenance_weekday2.png"/>

- A schedule downtime that that silences it all day during the weekend

<img src="https://github.com/GafsiS/hiring-engineers/blob/master/Screenshots/maintenance_weekend.png"/>

<img src="https://github.com/GafsiS/hiring-engineers/blob/master/Screenshots/maintenance_weekend2.png"/>

These are the notifications I have received:

- Scheduled downtime starting on weekdays

<img src="https://github.com/GafsiS/hiring-engineers/blob/master/Screenshots/maintenance_weekday_start.png"/>

- Scheduled downtime ending on weekdays

<img src="https://github.com/GafsiS/hiring-engineers/blob/master/Screenshots/weekday_downtime_end.png"/>

- Scheduled downtime starting on weekend

<img src="https://github.com/GafsiS/hiring-engineers/blob/master/Screenshots/maintenance_weekend_start.png"/>

- Scheduled downtime ending on weekend

<img src="https://github.com/GafsiS/hiring-engineers/blob/master/Screenshots/maintenance_weekend_end.png"/>



# Collecting APM Data

I have choosen to apply the APM monitoring to a flask application, to do so, I had to install flask and ddtrace.

* Installing flask and ddtrace:

For this section, I have followed the [APM](https://docs.datadoghq.com/tracing/setup/) documentation.

The APM enabling requires installing ddtrace.

I have chosen to monitor flask services by APM, and used the provided python script to launch APM.
I have followed these two links in order to do so:
- [link 1](https://docs.datadoghq.com/tracing/setup/python/#installation-and-getting-started) 
- [link 2](https://www.datadoghq.com/blog/monitoring-flask-apps-with-datadog/)


So I have started by installing flask on the VM by running 
```
pip install flask
```

Then I have installed ddtrace:
```
pip install ddtrace
```

And finally, I have created a script my_app.py (using the script provided in the exercise) in /etc/datadog/APM, and have started ddtrace against it.
```
ddtrace-run python my_app.py
```

Then I have added the my_app.py script in /etc/datadog/APM
```
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
```

Then APM was started:
```
ddtrace-run python my_app.py
```

- Run the app using curl commands:
```
curl http://0.0.0.0:5050
```

- Start the API trace
```
curl http://0.0.0.0:5050/api/trace
```

- Start the API APM
```
curl http://0.0.0.0:5050/api/trace
```

The services are then detected and the traces are being collected.

<img src="https://github.com/GafsiS/hiring-engineers/blob/master/Screenshots/apm_trace.png"/>

<img src="https://github.com/GafsiS/hiring-engineers/blob/master/Screenshots/apm_service.png"/>


## BONUS QUESTION
Service: a process/set of processes that can provide a feature, these are being defined by the user.
Resource: A query to a service to return certain data, we can have multiple resources attached to a service, for multiple type of data requested.

I have created a dashboard with timeboards of System metrics and APM metrics

<img src="https://github.com/GafsiS/hiring-engineers/blob/master/Screenshots/apm_enabled.png"/>

# Final Question:

In some Gym Centers, once there, you can assist to fitness courses only if there's an available spot.
It will be good if an online pre-inscription is required, and if datadog is then used to monitor availables spots and their numbers, and display this in colors (for example: Alert in red if no availables spots, warn in orange if less than 5 and green if there are more than 5 available spots), so you have the information before going to the Gym.

