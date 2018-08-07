Your answers to the questions go here.


Datadog link: 

1- Setting Up the environment:

* Create a Vagrantfile to start a VM machine with Ubuntu 16.0.4

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/xenial64"
end

(Check the file in the attached documents: Scripts/Vagrantfile)

* Start the machine 
vagrant up

* Access the machine
vagrant ssh 

--> Logs:
***********************
PS C:\Users\A\Documents\Documents\partage> vagrant status
Current machine states:

default                   poweroff (virtualbox)

The VM is powered off. To restart the VM, simply run `vagrant up`
PS C:\Users\A\Documents\Documents\partage> vagrant up
Bringing machine 'default' up with 'virtualbox' provider...
==> default: Checking if box 'ubuntu/xenial64' is up to date...
==> default: There was a problem while downloading the metadata for your box
==> default: to check for updates. This is not an error, since it is usually due
==> default: to temporary network problems. This is just a warning. The problem
==> default: encountered was:
==> default:
==> default: Could not resolve host: vagrantcloud.com
==> default:
==> default: If you want to check for box updates, verify your network connection
==> default: is valid and try again.
==> default: Clearing any previously set forwarded ports...
==> default: Clearing any previously set network interfaces...
==> default: Preparing network interfaces based on configuration...
    default: Adapter 1: nat
==> default: Forwarding ports...
    default: 22 (guest) => 2222 (host) (adapter 1)
==> default: Running 'pre-boot' VM customizations...
==> default: Booting VM...
==> default: Waiting for machine to boot. This may take a few minutes...
    default: SSH address: 127.0.0.1:2222
    default: SSH username: vagrant
    default: SSH auth method: private key
    default: Warning: Connection reset. Retrying...
    default: Warning: Connection aborted. Retrying...
    default: Warning: Connection reset. Retrying...
    default: Warning: Connection aborted. Retrying...
    default: Warning: Connection reset. Retrying...
    default: Warning: Connection aborted. Retrying...
    default: Warning: Connection reset. Retrying...
    default: Warning: Connection aborted. Retrying...
    default: Warning: Remote connection disconnect. Retrying...
    default: Warning: Connection aborted. Retrying...
    default: Warning: Connection reset. Retrying...
    default: Warning: Connection aborted. Retrying...
==> default: Machine booted and ready!
==> default: Checking for guest additions in VM...
    default: The guest additions on this VM do not match the installed version of
    default: VirtualBox! In most cases this is fine, but in rare cases it can
    default: prevent things such as shared folders from working properly. If you see
    default: shared folder errors, please make sure the guest additions within the
    default: virtual machine match the version of VirtualBox you have installed on
    default: your host and reload your VM.
    default:
    default: Guest Additions Version: 5.1.38
    default: VirtualBox Version: 5.2
==> default: Mounting shared folders...
    default: /vagrant => C:/Users/A/Documents/Documents/partage
==> default: Machine already provisioned. Run `vagrant provision` or use the `--provision`
==> default: flag to force provisioning. Provisioners marked to run always will still run.
PS C:\Users\A\Documents\Documents\partage> vagrant ssh
Welcome to Ubuntu 16.04.5 LTS (GNU/Linux 4.4.0-131-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  Get cloud support with Ubuntu Advantage Cloud Guest:
    http://www.ubuntu.com/business/services/cloud

2 packages can be updated.
0 updates are security updates.


Last login: Sun Aug  5 21:23:33 2018 from 10.0.2.2
vagrant@ubuntu-xenial:
**********************


* Installing agent 

--> Logs
***************************
vagrant@ubuntu-xenial:/etc/datadog-agent/APM$ DD_API_KEY=e527bbb476b605db8ad1044e94ce2b3a bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 10323  100 10323    0     0  10364      0 --:--:-- --:--:-- --:--:-- 10364
tee: ddagent-install.log: Permission denied
***************************

* Installing apt-transport-https

--> Logs
***************************
Hit:1 http://archive.ubuntu.com/ubuntu xenial InRelease
Get:2 http://security.ubuntu.com/ubuntu xenial-security InRelease [107 kB]
Get:3 http://archive.ubuntu.com/ubuntu xenial-updates InRelease [109 kB]
Get:4 http://archive.ubuntu.com/ubuntu xenial-backports InRelease [107 kB]
Ign:5 https://apt.datadoghq.com stable InRelease
Hit:6 https://apt.datadoghq.com stable Release
Get:7 http://archive.ubuntu.com/ubuntu xenial-updates/main Sources [318 kB]
Get:8 http://security.ubuntu.com/ubuntu xenial-security/main Sources [131 kB]
Get:9 http://archive.ubuntu.com/ubuntu xenial-updates/universe Sources [217 kB]
Get:10 http://security.ubuntu.com/ubuntu xenial-security/universe Sources [69.5 kB]
Get:12 http://security.ubuntu.com/ubuntu xenial-security/main amd64 Packages [533 kB]
Get:13 http://archive.ubuntu.com/ubuntu xenial-updates/main amd64 Packages [824 kB]
Get:14 http://security.ubuntu.com/ubuntu xenial-security/main Translation-en [228 kB]
Get:15 http://archive.ubuntu.com/ubuntu xenial-updates/main Translation-en [339 kB]
Get:16 http://archive.ubuntu.com/ubuntu xenial-updates/universe amd64 Packages [676 kB]
Get:17 http://archive.ubuntu.com/ubuntu xenial-updates/universe Translation-en [273 kB]
Get:18 http://archive.ubuntu.com/ubuntu xenial-backports/main Sources [4,488 B]
Get:19 http://archive.ubuntu.com/ubuntu xenial-backports/main amd64 Packages [6,756 B]
Get:20 http://security.ubuntu.com/ubuntu xenial-security/universe amd64 Packages [363 kB]
Get:21 http://security.ubuntu.com/ubuntu xenial-security/universe Translation-en [136 kB]
Fetched 4,442 kB in 3s (1,307 kB/s)
Reading package lists...
Reading package lists...
Building dependency tree...
Reading state information...
apt-transport-https is already the newest version (1.2.27).
0 upgraded, 0 newly installed, 0 to remove and 2 not upgraded.
Reading package lists...
Building dependency tree...
Reading state information...
dirmngr is already the newest version (2.1.11-6ubuntu2.1).
0 upgraded, 0 newly installed, 0 to remove and 2 not upgraded.
***************************

* Installing APT package sources for Datadog

--> Logs:
***************************
Executing: /tmp/tmp.knDSx8oyI0/gpg.1.sh --recv-keys
--keyserver
hkp://keyserver.ubuntu.com:80
382E94DE
gpg: requesting key 382E94DE from hkp server keyserver.ubuntu.com
gpg: key 382E94DE: "Datadog, Inc <package@datadoghq.com>" not changed
gpg: Total number processed: 1
gpg:              unchanged: 1

* Installing the Datadog Agent package

Ign:1 https://apt.datadoghq.com stable InRelease
Hit:2 https://apt.datadoghq.com stable Release
Reading package lists...
Reading package lists...
Building dependency tree...
Reading state information...
datadog-agent is already the newest version (1:6.4.1-1).
0 upgraded, 0 newly installed, 0 to remove and 2 not upgraded.

* Keeping old datadog.yaml configuration file

* Starting the Agent...



Your Agent is running and functioning properly. It will continue to run in the
background and submit metrics to Datadog.

If you ever want to stop the Agent, run:

    sudo systemctl stop datadog-agent

And to run it again run:

    sudo systemctl start datadog-agent

vagrant@ubuntu-xenial:/etc/datadog-agent/APM$
***************************

Hosts MAP Link: https://app.datadoghq.com/infrastructure/map?fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=availability-zone&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=true&palette=green_to_orange&paletteflip=false&node_type=host


2- Collecting Metrics


* Adding tags in the agent file:

in /etc/datadog/datadog.yaml, add the follwing lines:

tags:
   - env:prod
   - host:ubuntu
   - name:precise64

(check the config file in the attached documents Scripts/datadogyaml)

Check screenshot of the added tags on Host monitor (Screenshots/adding_tags.png, Screenshots/hostmap_tags.png).

Host Map tags link: https://app.datadoghq.com/infrastructure/map?host=543861600&fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=availability-zone&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=true&palette=green_to_orange&paletteflip=false&node_type=host

* Installing a database:

Mysql is included in the datadog package as per the documentation
https://docs.datadoghq.com/integrations/mysql/

** Setting mysql:

--> Logs:
***************************
vagrant@ubuntu-xenial:/etc/datadog-agent/conf.d/mysql.d$ vi conf.yaml.example
vagrant@ubuntu-xenial:/etc/datadog-agent/conf.d/mysql.d$ ll
total 16
drwxr-xr-x  2 dd-agent dd-agent 4096 Aug  6 21:06 ./
drwxr-xr-x 97 dd-agent dd-agent 4096 Aug  5 21:31 ../
-rw-r--r--  1 dd-agent dd-agent 5000 Aug  1 20:29 conf.yaml.example
vagrant@ubuntu-xenial:/etc/datadog-agent/conf.d/mysql.d$ sudo cp conf.yaml.example  conf.yaml
vagrant@ubuntu-xenial:/etc/datadog-agent/conf.d/mysql.d$ chmod 755 conf.yaml
chmod: changing permissions of 'conf.yaml': Operation not permitted
vagrant@ubuntu-xenial:/etc/datadog-agent/conf.d/mysql.d$ sudo chmod 755 conf.yaml
vagrant@ubuntu-xenial:/etc/datadog-agent/conf.d/mysql.d$ sudo vi conf.yaml
***************************


** Installing mysql server on the same machine 

--> Logs:
***************************
vagrant@ubuntu-xenial:/etc/datadog-agent/conf.d/mysql.d$ sudo apt-get update
Hit:1 http://security.ubuntu.com/ubuntu xenial-security InRelease
Hit:2 http://archive.ubuntu.com/ubuntu xenial InRelease
Hit:3 http://archive.ubuntu.com/ubuntu xenial-updates InRelease
Hit:4 http://archive.ubuntu.com/ubuntu xenial-backports InRelease
Ign:5 https://apt.datadoghq.com stable InRelease
Hit:6 https://apt.datadoghq.com stable Release
Reading package lists... Done
vagrant@ubuntu-xenial:/etc/datadog-agent/conf.d/mysql.d$ sudo apt-get install mysql-server
Reading package lists... Done
Building dependency tree
Reading state information... Done
The following additional packages will be installed:
  libaio1 libcgi-fast-perl libcgi-pm-perl libencode-locale-perl libevent-core-2.0-5 libfcgi-perl libhtml-parser-perl libhtml-tagset-perl libhtml-template-perl libhttp-date-perl libhttp-message-perl libio-html-perl
  liblwp-mediatypes-perl libtimedate-perl liburi-perl mysql-client-5.7 mysql-client-core-5.7 mysql-common mysql-server-5.7 mysql-server-core-5.7
Suggested packages:
  libdata-dump-perl libipc-sharedcache-perl libwww-perl mailx tinyca
The following NEW packages will be installed:
  libaio1 libcgi-fast-perl libcgi-pm-perl libencode-locale-perl libevent-core-2.0-5 libfcgi-perl libhtml-parser-perl libhtml-tagset-perl libhtml-template-perl libhttp-date-perl libhttp-message-perl libio-html-perl
  liblwp-mediatypes-perl libtimedate-perl liburi-perl mysql-client-5.7 mysql-client-core-5.7 mysql-common mysql-server mysql-server-5.7 mysql-server-core-5.7
0 upgraded, 21 newly installed, 0 to remove and 2 not upgraded.
Need to get 19.4 MB of archives.
After this operation, 162 MB of additional disk space will be used.
Do you want to continue? [Y/n] Y
***************************

** Setting the datadog-Mysql integration

--> Logs:
***************************
vagrant@ubuntu-xenial:/etc/datadog-agent/conf.d/mysql.d$ sudo mysql -u root --password=Kenza1608
mysql: [Warning] Using a password on the command line interface can be insecure.
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 8
Server version: 5.7.23-0ubuntu0.16.04.1 (Ubuntu)

Copyright (c) 2000, 2018, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> CREATE USER 'datadog'@'localhost' IDENTIFIED BY 'Hello00';
ERROR 1819 (HY000): Your password does not satisfy the current policy requirements
mysql> CREATE USER 'datadog'@'localhost' IDENTIFIED BY 'Hello1234';
Query OK, 0 rows affected (0.00 sec)

vagrant@ubuntu-xenial:/etc/datadog-agent/conf.d/mysql.d$ mysql -u datadog --password="Hello1234" -e "show status" | \
> grep Uptime && echo -e "\033[0;32mMySQL user - OK\033[0m" || \
> echo -e "\033[0;31mCannot connect to MySQL\033[0m";
mysql: [Warning] Using a password on the command line interface can be insecure.
Uptime  714
Uptime_since_flush_status       714
MySQL user - OK
vagrant@ubuntu-xenial:/etc/datadog-agent/conf.d/mysql.d$ mysql -u datadog --password="Hello1234" -e "show slave status" && \
> echo -e "\033[0;32mMySQL grant - OK\033[0m" || \
> echo -e "\033[0;31mMissing REPLICATION CLIENT grant\033[0m"
mysql: [Warning] Using a password on the command line interface can be insecure.
ERROR 1227 (42000) at line 1: Access denied; you need (at least one of) the SUPER, REPLICATION CLIENT privilege(s) for this operation
Missing REPLICATION CLIENT grant
vagrant@ubuntu-xenial:/etc/datadog-agent/conf.d/mysql.d$ sudo mysql -u datadog --password="Hello1234" -e "show slave status" && echo -e "\033[0;32mMySQL grant - OK\033[0m" || echo -e "\033[0;31mMissing REPLICATION CLIENT grant\033[0m"
mysql: [Warning] Using a password on the command line interface can be insecure.
ERROR 1227 (42000) at line 1: Access denied; you need (at least one of) the SUPER, REPLICATION CLIENT privilege(s) for this operation
Missing REPLICATION CLIENT grant
vagrant@ubuntu-xenial:/etc/datadog-agent/conf.d/mysql.d$ sudo mysql -u root --password=Kenza1608
mysql: [Warning] Using a password on the command line interface can be insecure.
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 13
Server version: 5.7.23-0ubuntu0.16.04.1 (Ubuntu)

Copyright (c) 2000, 2018, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

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

** Updating mysql config file:

init_config:

This is how is written the conf.yaml file in /etc/datadog/check.d/mysql.d

instances:
    # NOTE: Even if the server name is "localhost", the agent will connect to MySQL using TCP/IP, unless you also
    # provide a value for the sock key (below).
  - server: 127.0.0.1
     user: dataidog
     pass: Hello1234
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
***************************


The file can be found within the attached documents (Scripts/conf.yaml).


** Mettre à jour le fichier my.cnf

--> Logs:
***************************
vagrant@ubuntu-xenial:/etc/datadog-agent/conf.d/mysql.d$ cat /etc/mysql/my.cnf
#
# The MySQL database server configuration file.
#
# You can copy this to one of:
# - "/etc/mysql/my.cnf" to set global options,
# - "~/.my.cnf" to set user-specific options.
#
# One can use all long options that the program supports.
# Run program with --help to get a list of available options and with
# --print-defaults to see which it would actually understand and use.
#
# For explanations see
# http://dev.mysql.com/doc/mysql/en/server-system-variables.html

#
# * IMPORTANT: Additional settings that can override those from this file!
#   The files must end with '.cnf', otherwise they'll be ignored.
#

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
vagrant@ubuntu-xenial:/etc/datadog-agent/conf.d/mysql.d$
***************************


The file can be found within the attached documents. (Scripts/my.cnf)


** enabling mysql logs in datadog conf file:


--> Logs:
***************************
    # - type : (mandatory) type of log input source (tcp / udp / file)
    #   port / path : (mandatory) Set port if type is tcp or udp. Set path if type is file
    #   service : (mandatory) name of the service owning the log
    #   source : (mandatory) attribute that defines which integration is sending the logs
    #   sourcecategory : (optional) Multiple value attribute. Can be used to refine the source attribtue
    #   tags: (optional) add tags to each logs collected


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
***************************

Agent restart was done after each change

* Creating custom metric

In order to create a new metric, two files needs to be created:
- /etc/datadog-agent/conf.d/my_metric.yaml (Scripts/my_metric.yaml)

***************************
vagrant@ubuntu-xenial:/etc/datadog-agent/conf.d$ cat my_metric.yaml
init_config:

instances:
 - min_collection_interval: 45
vagrant@ubuntu-xenial:/etc/datadog-agent/conf.d$
***************************

min_collection_interval: 45 was added to enable the check every 45s


- /etc/datadog-agent/check.d/my_metric.py (Scripts/my_metric.py)

***************************
vagrant@ubuntu-xenial:/etc/datadog-agent/checks.d$ cat my_metric.py
from checks import AgentCheck
import random

class my_check(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric',random.randint(0,1000))
vagrant@ubuntu-xenial:/etc/datadog-agent/checks.d$
***************************

and then then restart agent.

BONUS QUESTION:
The change of the check interval is done on the config file, thus, no need to modify the python script.

Check the attached screenshot for the my_metric graph. (Screenshots/my_metric_interval_45.png, Screenshots/last_5_min.png)


3- Visualizing data


- Script used to create the timeboard:

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

(script under Scripts/MyTimeboard.json)

Please check also the attached screenshots (Screenshots/MyDashboard.png, Screenshots/MyTimeboard.png, Screenshots/anomalie.png).


Timeboard link: https://app.datadoghq.com/dash/878535/mytimeboard?live=true&page=0&is_auto=false&from_ts=1533662828984&to_ts=1533677228984&tile_size=m

BONUS QUESTION:
--> The anomaly graph is displaying the expected behavior of the metric based on its past collected values.


4- Monitoring Data

Please check attached screenshots (Screenshots/notification_config.png).
Notification annotation (Screenshots/email_notification.png)

Monitor link: https://app.datadoghq.com/monitors/5825551


Alerting message template:

***************************
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
***************************

Mails received (Screenshots/notification_warn)


** Adding maintenance periods:

Maintenance period link: https://app.datadoghq.com/monitors#downtime?id=358240967


Check attached screenshots (Screenshots/maintenance_weekend.png, Screenshots/MaintenancePeriod.png, Screenshots/weekend_maintenance.png, Screenshots/weekday_maintenance.png)

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

Please check the attached screenshots (Screenshots/apm_enabled.png, Screenshots/APMvsCPULoad.png)

Timeboard System vs APM metrics: https://app.datadoghq.com/dash/880157/apm-vs-system-timeboard?live=true&page=0&is_auto=false&from_ts=1533673962051&to_ts=1533677562051&tile_size=m


BONUS QUESTION
Service: a process/set of processes that can provide a feature, these are being defined by the user.
Resource: A query to a service to return certain data, we can have multiple resources attached to a service, for multiple type of data requested.


6- Final Question:

It can be used to help blinded people cross streets by monitoring red/green lights in their way.



