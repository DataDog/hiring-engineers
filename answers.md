Your answers to the questions go here.


## Prerequisites - Setup the environment

I have started a linux VM via vagrant.
To do so, I have followed the tutorial in [this link]( 
https://www.vagrantup.com/intro/getting-started/via)

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

and then then restart agent.


To make the check run every 45s, I have updated the my_metric.yaml file as follows:

<!-- >>>>>> BEGIN INCLUDED FILE (code_block): SOURCE Scripts/my_metric.yaml -->
```
init_config:

instances:
 - min_collection_interval: 45
```
<!-- >>>>>> END INCLUDED FILE (code_block): SOURCE Scripts/my_metric.yaml -->

min_collection_interval: 45 was added to enable the check every 45s

# BONUS QUESTION:
The change of the check interval is done on the config file, thus, no need to modify the python script.


<img src="https://github.com/GafsiS/hiring-engineers/blob/master/Screenshots/my_metric_interval_45.png" />
<img src="https://github.com/GafsiS/hiring-engineers/blob/master/Screenshots/last_5_min.png" />


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


<img src="https://github.com/GafsiS/hiring-engineers/blob/master/Screenshots/MyMetricTimeboard"/>

Setting Timeboard's timeframe to the past 5 minutes: This is done by selecting the last 5min timeframe in the graph:

<img src="https://github.com/GafsiS/hiring-engineers/blob/master/Screenshots/MyCustomTimeboard.png"/>

Taking a snapshot of this graph and using the @ notation to send it to yourself:

- Taking a snapshot
<img src="https://github.com/GafsiS/hiring-engineers/blob/master/Screenshots/snapshot.png"/>

- Email received
<img src="https://github.com/GafsiS/hiring-engineers/blob/master/Screenshots/email_snapshot.png"/>

* BONUS QUESTION:
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
<img src="https://github.com/GafsiS/hiring-engineers/blob/master/Screenshots/Alert.png"/>



* BONUS QUESTION


I have created the Maintenance Periods through datadog front end, and have followed this [documentation](https://docs.datadoghq.com/monitors/downtimes/) in order to do so.

These are the scheduled downtimes I have created:


- A scheduled downtime that silences MyMetric from 7pm to 9am on weekdays

<img src="https://github.com/GafsiS/hiring-engineers/blob/master/Screenshots/MaintenancePeriod_weekdays.png"/>

<img src="https://github.com/GafsiS/hiring-engineers/blob/master/Screenshots/maintenance_weekdays2.png"/>

- A schedule downtime that that silences it all day during the weekend

<img src="https://github.com/GafsiS/hiring-engineers/blob/master/Screenshots/maintenance_weekend.png"/>

<img src="https://github.com/GafsiS/hiring-engineers/blob/master/Screenshots/maintenance_weekend2.png"/>

These are the notifications I have received:

- Scheduled downtime starting on weekdays

<img src="https://github.com/GafsiS/hiring-engineers/blob/master/Screenshots/maintenance_weekday_start.png"/>

- Scheduled downtime ending on weekdays

<img src="https://github.com/GafsiS/hiring-engineers/blob/master/Screenshots/maintenance_weekday_end.png"/>

- Scheduled downtime starting on weekend

<img src="https://github.com/GafsiS/hiring-engineers/blob/master/Screenshots/maintenance_weekend_start.png"/>

- Scheduled downtime ending on weekend

<img src="https://github.com/GafsiS/hiring-engineers/blob/master/Screenshots/maintenance_weekend_end.png"/>



** Adding maintenance periods:

Maintenance period link: https://app.datadoghq.com/monitors#downtime?id=358240967


Check attached screenshots 
(Screenshots/maintenance_weekend.png: https://github.com/GafsiS/hiring-engineers/blob/master/Screenshots/maintenance_weekend.png, 
Screenshots/MaintenancePeriod.png: https://github.com/GafsiS/hiring-engineers/blob/master/Screenshots/MaintenancePeriod.png, 
Screenshots/weekend_maintenance.png: https://github.com/GafsiS/hiring-engineers/blob/master/Screenshots/weekend_maintenance.png, 
Screenshots/weekday_maintenance.png: https://github.com/GafsiS/hiring-engineers/blob/master/Screenshots/weekday_maintenance.png)

5- Collecting APM Data

* Installing flask and ddtrace:

APM Services link: https://app.datadoghq.com/apm/service/flask/flask.request?start=1533591120928&end=1533677520928&env=prod&paused=false

--> Logs:
***************************
root@ubuntu-xenial:~# pip install flask
Collecting flask
  Downloading https://files.pythonhosted.org/packages/7f/e7/08578774ed4536d3242b14dacb4696386634607af824ea997202cd0edb4b/Flask-1.0.2-py2.py3-none-any.whl (91kB)
    100% |¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦| 92kB 2.1MB/s
Collecting Jinja2>=2.10 (from flask)
  Downloading https://files.pythonhosted.org/packages/7f/ff/ae64bacdfc95f27a016a7bed8e8686763ba4d277a78ca76f32659220a731/Jinja2-2.10-py2.py3-none-any.whl (126kB)
    100% |¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦| 133kB 2.2MB/s
Collecting itsdangerous>=0.24 (from flask)
  Downloading https://files.pythonhosted.org/packages/dc/b4/a60bcdba945c00f6d608d8975131ab3f25b22f2bcfe1dab221165194b2d4/itsdangerous-0.24.tar.gz (46kB)
    100% |¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦| 51kB 2.3MB/s
Collecting Werkzeug>=0.14 (from flask)
  Downloading https://files.pythonhosted.org/packages/20/c4/12e3e56473e52375aa29c4764e70d1b8f3efa6682bef8d0aae04fe335243/Werkzeug-0.14.1-py2.py3-none-any.whl (322kB)
    100% |¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦| 327kB 891kB/s
Collecting click>=5.1 (from flask)
  Downloading https://files.pythonhosted.org/packages/34/c1/8806f99713ddb993c5366c362b2f908f18269f8d792aff1abfd700775a77/click-6.7-py2.py3-none-any.whl (71kB)
    100% |¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦| 71kB 2.0MB/s
Collecting MarkupSafe>=0.23 (from Jinja2>=2.10->flask)
  Downloading https://files.pythonhosted.org/packages/4d/de/32d741db316d8fdb7680822dd37001ef7a448255de9699ab4bfcbdf4172b/MarkupSafe-1.0.tar.gz
Building wheels for collected packages: itsdangerous, MarkupSafe
  Running setup.py bdist_wheel for itsdangerous ... done
  Stored in directory: /root/.cache/pip/wheels/2c/4a/61/5599631c1554768c6290b08c02c72d7317910374ca602ff1e5
  Running setup.py bdist_wheel for MarkupSafe ... done
  Stored in directory: /root/.cache/pip/wheels/33/56/20/ebe49a5c612fffe1c5a632146b16596f9e64676768661e4e46
Successfully built itsdangerous MarkupSafe
Installing collected packages: MarkupSafe, Jinja2, itsdangerous, Werkzeug, click, flask
Successfully installed Jinja2-2.10 MarkupSafe-1.0 Werkzeug-0.14.1 click-6.7 flask-1.0.2 itsdangerous-0.24
You are using pip version 8.1.1, however version 18.0 is available.
You should consider upgrading via the 'pip install --upgrade pip' command.
root@ubuntu-xenial:~# cd /etc/datadog-agent/APM/
root@ubuntu-xenial:/etc/datadog-agent/APM#  ddtrace-run python my_app.py
ddtrace-run: command not found
root@ubuntu-xenial:/etc/datadog-agent/APM# pip install ddtrace
Collecting ddtrace
  Downloading https://files.pythonhosted.org/packages/9d/48/c59c5fb0df206bcb744ae9ed72d0fc5a523d52df18f879a92a24c236cfbb/ddtrace-0.12.1.tar.gz (93kB)
    100% |¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦| 102kB 1.6MB/s
Collecting wrapt (from ddtrace)
  Downloading https://files.pythonhosted.org/packages/a0/47/66897906448185fcb77fc3c2b1bc20ed0ecca81a0f2f88eda3fc5a34fc3d/wrapt-1.10.11.tar.gz
Collecting msgpack-python (from ddtrace)
  Downloading https://files.pythonhosted.org/packages/8a/20/6eca772d1a5830336f84aca1d8198e5a3f4715cd1c7fc36d3cc7f7185091/msgpack-python-0.5.6.tar.gz (138kB)
    100% |¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦| 143kB 2.0MB/s
Building wheels for collected packages: ddtrace, wrapt, msgpack-python
  Running setup.py bdist_wheel for ddtrace ... done
  Stored in directory: /root/.cache/pip/wheels/4b/38/40/1a7038e5586b14716aa16ad635c5eb7e49ca695f0ef2acea6e
  Running setup.py bdist_wheel for wrapt ... done
  Stored in directory: /root/.cache/pip/wheels/48/5d/04/22361a593e70d23b1f7746d932802efe1f0e523376a74f321e
  Running setup.py bdist_wheel for msgpack-python ... done
  Stored in directory: /root/.cache/pip/wheels/d5/de/86/7fa56fda12511be47ea0808f3502bc879df4e63ab168ec0406
Successfully built ddtrace wrapt msgpack-python
Installing collected packages: wrapt, msgpack-python, ddtrace
Successfully installed ddtrace-0.12.1 msgpack-python-0.5.6 wrapt-1.10.11
You are using pip version 8.1.1, however version 18.0 is available.
You should consider upgrading via the 'pip install --upgrade pip' command.
***************************

* Running the my_app.py

--> Logs:
***************************
root@ubuntu-xenial:/etc/datadog-agent/APM# ddtrace-run python my_app.py
DEBUG:ddtrace.contrib.flask.middleware:flask: initializing trace middleware
2018-08-06 22:26:03,036 - ddtrace.contrib.flask.middleware - DEBUG - flask: initializing trace middleware
DEBUG:ddtrace.writer:resetting queues. pids(old:None new:6181)
2018-08-06 22:26:03,039 - ddtrace.writer - DEBUG - resetting queues. pids(old:None new:6181)
DEBUG:ddtrace.writer:starting flush thread
2018-08-06 22:26:03,041 - ddtrace.writer - DEBUG - starting flush thread
DEBUG:ddtrace.contrib.flask.middleware:please install blinker to use flask signals. http://flask.pocoo.org/docs/0.11/signals/
2018-08-06 22:26:03,042 - ddtrace.contrib.flask.middleware - DEBUG - please install blinker to use flask signals. http://flask.pocoo.org/docs/0.11/signals/
 * Serving Flask app "my_app" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
INFO:werkzeug: * Running on http://0.0.0.0:5050/ (Press CTRL+C to quit)
2018-08-06 22:26:03,057 - werkzeug - INFO -  * Running on http://0.0.0.0:5050/ (Press CTRL+C to quit)
DEBUG:ddtrace.api:reported 1 services
2018-08-06 22:26:04,054 - ddtrace.api - DEBUG - reported 1 services
***************************

Please check the attached screenshots 
(Screenshots/apm_enabled.png: https://github.com/GafsiS/hiring-engineers/blob/master/Screenshots/apm_enabled.png, 
Screenshots/APMvsCPULoad.png: https://github.com/GafsiS/hiring-engineers/blob/master/Screenshots/APMvsCPULoad.png)

Timeboard System vs APM metrics: https://app.datadoghq.com/dash/880157/apm-vs-system-timeboard?live=true&page=0&is_auto=false&from_ts=1533673962051&to_ts=1533677562051&tile_size=m


BONUS QUESTION
Service: a process/set of processes that can provide a feature, these are being defined by the user.
Resource: A query to a service to return certain data, we can have multiple resources attached to a service, for multiple type of data requested.


6- Final Question:

It can be used to help blinded people cross streets by monitoring red/green lights in their way.



