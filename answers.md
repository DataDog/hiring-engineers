Your answers to the questions go here.

# Steps I Took:

1. Set up an Ubuntu 16.04 Virtual Machine in VirtualBox on Mac OSX
2. Sign up for Datadog, using "Datadog Recruiting Candidate" in the "Company" field.

**Bonus Question: What is the agent?**
The DataDog Agent is a program that runs on one's host (can also run in Docker or a VM) that aggregates events and methods, and sends them to DataDog. It is composed of three parts, which are, in turn, controlled and coordinated by a supervisor process.
*The collector (a program that runs continously and checks on integrations, in addition to system stats such as CPU usage, disk latency, network traffic, etc) 
*Dogstatsd (a backend server that utilizes etsy's stats aggregation daemon (statsd) to receive custom metrics)
*Forwarder (a program that aggregates data from the collector and dogstatsd to present to DataDog) 

3.) Installed the DataDog agent for Ubuntu:
```root@zaps-VirtualBox:~# DD_API_KEY=d5ed33bc1830f93767bbc1a16056ca95 bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/dd-agent/master/packaging/datadog-agent/source/install_agent.sh)"

  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  9911  100  9911    0     0  17690      0 --:--:-- --:--:-- --:--:-- 17698

* Installing apt-transport-https

Get:1 http://security.ubuntu.com/ubuntu xenial-security InRelease [102 kB]
Hit:2 http://us.archive.ubuntu.com/ubuntu xenial InRelease
Get:3 http://us.archive.ubuntu.com/ubuntu xenial-updates InRelease [102 kB]
Get:4 http://us.archive.ubuntu.com/ubuntu xenial-backports InRelease [102 kB]
Fetched 306 kB in 0s (525 kB/s)
Reading package lists...
Reading package lists...
Building dependency tree...
Reading state information...
The following packages will be upgraded:
  apt-transport-https
1 upgraded, 0 newly installed, 0 to remove and 93 not upgraded.
                                                               Need to get 0 B/26.1 kB of archives.
                   After this operation, 1,024 B of additional disk space will be used.
(Reading database ... 207993 files and directories currently installed.)
Preparing to unpack .../apt-transport-https_1.2.20_amd64.deb ...
Unpacking apt-transport-https (1.2.20) over (1.2.19) ...
Setting up apt-transport-https (1.2.20) ...

* Installing APT package sources for Datadog

Executing: /tmp/tmp.1cE2dLojbX/gpg.1.sh --recv-keys
--keyserver
hkp://keyserver.ubuntu.com:80
C7A7DA52
gpg: requesting key C7A7DA52 from hkp server keyserver.ubuntu.com
gpg: key C7A7DA52: public key "Datadog Packages <package@datadoghq.com>" imported
gpg: Total number processed: 1
gpg:               imported: 1  (RSA: 1)
Executing: /tmp/tmp.Tch89GsVxN/gpg.1.sh --recv-keys
--keyserver
hkp://keyserver.ubuntu.com:80
382E94DE
gpg: requesting key 382E94DE from hkp server keyserver.ubuntu.com
gpg: key 382E94DE: public key "Datadog, Inc <package@datadoghq.com>" imported
gpg: Total number processed: 1
gpg:               imported: 1  (RSA: 1)

* Installing the Datadog Agent package

Ign:1 https://apt.datadoghq.com stable InRelease
Get:2 https://apt.datadoghq.com stable Release [2,367 B]
Get:3 https://apt.datadoghq.com stable Release.gpg [473 B]
Get:4 https://apt.datadoghq.com stable/main amd64 Packages [9,752 B]
Get:5 https://apt.datadoghq.com stable/main i386 Packages [8,382 B]
Fetched 21.0 kB in 0s (40.8 kB/s)
Reading package lists...
Reading package lists...
Building dependency tree...
Reading state information...
The following NEW packages will be installed:
  datadog-agent
0 upgraded, 1 newly installed, 0 to remove and 93 not upgraded.
Need to get 69.4 MB of archives.
After this operation, 223 MB of additional disk space will be used.
Get:1 https://apt.datadoghq.com stable/main amd64 datadog-agent amd64 1:5.13.2-1 [69.4 MB]
Fetched 69.4 MB in 21s (3,206 kB/s)
                                   Selecting previously unselected package datadog-agent.
(Reading database ... 207993 files and directories currently installed.)
Preparing to unpack .../datadog-agent_1%3a5.13.2-1_amd64.deb ...
Prepare Datadog Agent keys rotation
  Add the new 'Datadog, Inc <package@datadoghq.com>' key to the list of APT trusted keys.... key already installed
Unpacking datadog-agent (1:5.13.2-1) ...
Processing triggers for systemd (229-4ubuntu16) ...
Processing triggers for ureadahead (0.100.0-19) ...
Setting up datadog-agent (1:5.13.2-1) ...
Registering service datadog-agent
Enabling service datadog-agent
Creating dd-agent group
Creating dd-agent user
W: --force-yes is deprecated, use one of the options starting with --allow instead.

* Adding your API key to the Agent configuration: /etc/dd-agent/datadog.conf

* Starting the Agent...


Your Agent has started up for the first time. We're currently verifying that
data is being submitted. You should see your Agent show up in Datadog shortly
at:

    https://app.datadoghq.com/infrastructure

Waiting for metrics.....................................

Your Agent is running and functioning properly. It will continue to run in the
background and submit metrics to Datadog.

If you ever want to stop the Agent, run:

    sudo /etc/init.d/datadog-agent stop

And to run it again run:

    sudo /etc/init.d/datadog-agent start```

4. Added tags in the Agent config file (etc/dd-agent/datadog.conf)

```tags: env:vm, database:mysql```

https://app.datadoghq.com/infrastructure/map?fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=none&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=false&palette=green_to_orange&paletteflip=false&host=298892401

5. Restarted DataDog service in order for the tags to show up

```/etc/init.d/datadog-agent restart```

6. Installed MySQL on the VM

```apt-get install mysql-server```

8.) Installed DataDog integration for MySQL, and checked to make sure all was well

root@zaps-VirtualBox:/etc/dd-agent# mysql -u root -p
Enter password: 
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 8
Server version: 5.7.18-0ubuntu0.16.04.1 (Ubuntu)

Copyright (c) 2000, 2017, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> CREATE USER 'datadog'@'localhost' IDENTIFIED BY 'dogmysql';
Query OK, 0 rows affected (0.00 sec)

mysql> GRANT PROCESS ON *.* TO 'datadog'@'localhost';
Query OK, 0 rows affected (0.01 sec)

mysql> GRANT SELECT ON performance_schema.* TO 'datadog'@'localhost';
Query OK, 0 rows affected (0.00 sec)

root@zaps-VirtualBox:/etc/dd-agent/conf.d# mysql -u datadog --password=dogmysql -e "show status" | \
> grep Uptime && echo -e "\033[0;32mMySQL user - OK\033[0m" || \
> echo -e "\033[0;31mCannot connect to MySQL\033[0m"
mysql: [Warning] Using a password on the command line interface can be insecure.
Uptime	93014
Uptime_since_flush_status	93014
MySQL user – OK

root@zaps-VirtualBox:/etc/dd-agent/conf.d# mysql -u root -p -e "GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'localhost' WITH MAX_USER_CONNECTIONS 5;"
Enter password: 
root@zaps-VirtualBox:/etc/dd-agent/conf.d# mysql -u datadog --password=dogmysql -e "show slave status" && echo -e "\033[0;32mMySQL grant - OK\033[0m" || echo -e "\033[0;31mMissing REPLICATION CLIENT grant\033[0m"
mysql: [Warning] Using a password on the command line interface can be insecure.
MySQL grant - OK
root@zaps-VirtualBox:/etc/dd-agent/conf.d# mysql -u datadog --password=dogmysql -e "SELECT * FROM performance_schema.threads" && \
> echo -e "\033[0;32mMySQL SELECT grant - OK\033[0m" || \
> echo -e "\033[0;31mMissing SELECT grant\033[0m"
mysql: [Warning] Using a password on the command line interface can be insecure.
+-----------+----------------------------------------+------------+----------------+------------------+------------------+----------------+---------------------+------------------+-------------------+------------------------------------------+------------------+------+--------------+---------+-----------------+--------------+
| THREAD_ID | NAME                                   | TYPE       | PROCESSLIST_ID | PROCESSLIST_USER | PROCESSLIST_HOST | PROCESSLIST_DB | PROCESSLIST_COMMAND | PROCESSLIST_TIME | PROCESSLIST_STATE | PROCESSLIST_INFO                         | PARENT_THREAD_ID | ROLE | INSTRUMENTED | HISTORY | CONNECTION_TYPE | THREAD_OS_ID |
+-----------+----------------------------------------+------------+----------------+------------------+------------------+----------------+---------------------+------------------+-------------------+------------------------------------------+------------------+------+--------------+---------+-----------------+--------------+
|         1 | thread/sql/main                        | BACKGROUND |           NULL | NULL             | NULL             | NULL           | NULL                |            93344 | NULL              | NULL                                     |             NULL | NULL | YES          | YES     | NULL            |         4657 |
|         2 | thread/sql/thread_timer_notifier       | BACKGROUND |           NULL | NULL             | NULL             | NULL           | NULL                |             NULL | NULL              | NULL                                     |                1 | NULL | YES          | YES     | NULL            |         4661 |
|         3 | thread/innodb/io_write_thread          | BACKGROUND |           NULL | NULL             | NULL             | NULL           | NULL                |             NULL | NULL              | NULL                                     |             NULL | NULL | YES          | YES     | NULL            |         4668 |
|         4 | thread/innodb/io_write_thread          | BACKGROUND |           NULL | NULL             | NULL             | NULL           | NULL                |             NULL | NULL              | NULL                                     |             NULL | NULL | YES          | YES     | NULL            |         4669 |
|         5 | thread/innodb/io_write_thread          | BACKGROUND |           NULL | NULL             | NULL             | NULL           | NULL                |             NULL | NULL              | NULL                                     |             NULL | NULL | YES          | YES     | NULL            |         4670 |
|         6 | thread/innodb/io_write_thread          | BACKGROUND |           NULL | NULL             | NULL             | NULL           | NULL                |             NULL | NULL              | NULL                                     |             NULL | NULL | YES          | YES     | NULL            |         4671 |
|         7 | thread/innodb/page_cleaner_thread      | BACKGROUND |           NULL | NULL             | NULL             | NULL           | NULL                |             NULL | NULL              | NULL                                     |             NULL | NULL | YES          | YES     | NULL            |         4672 |
|         8 | thread/innodb/io_read_thread           | BACKGROUND |           NULL | NULL             | NULL             | NULL           | NULL                |             NULL | NULL              | NULL                                     |             NULL | NULL | YES          | YES     | NULL            |         4667 |
|         9 | thread/innodb/io_read_thread           | BACKGROUND |           NULL | NULL             | NULL             | NULL           | NULL                |             NULL | NULL              | NULL                                     |             NULL | NULL | YES          | YES     | NULL            |         4666 |
|        10 | thread/innodb/io_read_thread           | BACKGROUND |           NULL | NULL             | NULL             | NULL           | NULL                |             NULL | NULL              | NULL                                     |             NULL | NULL | YES          | YES     | NULL            |         4665 |
|        11 | thread/innodb/io_read_thread           | BACKGROUND |           NULL | NULL             | NULL             | NULL           | NULL                |             NULL | NULL              | NULL                                     |             NULL | NULL | YES          | YES     | NULL            |         4664 |
|        12 | thread/innodb/io_log_thread            | BACKGROUND |           NULL | NULL             | NULL             | NULL           | NULL                |             NULL | NULL              | NULL                                     |             NULL | NULL | YES          | YES     | NULL            |         4663 |
|        13 | thread/innodb/io_ibuf_thread           | BACKGROUND |           NULL | NULL             | NULL             | NULL           | NULL                |             NULL | NULL              | NULL                                     |             NULL | NULL | YES          | YES     | NULL            |         4662 |
|        15 | thread/innodb/srv_purge_thread         | BACKGROUND |           NULL | NULL             | NULL             | NULL           | NULL                |             NULL | NULL              | NULL                                     |             NULL | NULL | YES          | YES     | NULL            |         4678 |
|        16 | thread/innodb/srv_master_thread        | BACKGROUND |           NULL | NULL             | NULL             | NULL           | NULL                |             NULL | NULL              | NULL                                     |             NULL | NULL | YES          | YES     | NULL            |         4677 |
|        17 | thread/innodb/srv_worker_thread        | BACKGROUND |           NULL | NULL             | NULL             | NULL           | NULL                |             NULL | NULL              | NULL                                     |             NULL | NULL | YES          | YES     | NULL            |         4680 |
|        18 | thread/innodb/srv_worker_thread        | BACKGROUND |           NULL | NULL             | NULL             | NULL           | NULL                |             NULL | NULL              | NULL                                     |             NULL | NULL | YES          | YES     | NULL            |         4681 |
|        19 | thread/innodb/srv_worker_thread        | BACKGROUND |           NULL | NULL             | NULL             | NULL           | NULL                |             NULL | NULL              | NULL                                     |             NULL | NULL | YES          | YES     | NULL            |         4679 |
|        20 | thread/innodb/srv_monitor_thread       | BACKGROUND |           NULL | NULL             | NULL             | NULL           | NULL                |             NULL | NULL              | NULL                                     |             NULL | NULL | YES          | YES     | NULL            |         4676 |
|        21 | thread/innodb/srv_error_monitor_thread | BACKGROUND |           NULL | NULL             | NULL             | NULL           | NULL                |             NULL | NULL              | NULL                                     |             NULL | NULL | YES          | YES     | NULL            |         4675 |
|        22 | thread/innodb/srv_lock_timeout_thread  | BACKGROUND |           NULL | NULL             | NULL             | NULL           | NULL                |             NULL | NULL              | NULL                                     |             NULL | NULL | YES          | YES     | NULL            |         4674 |
|        23 | thread/innodb/dict_stats_thread        | BACKGROUND |           NULL | NULL             | NULL             | NULL           | NULL                |             NULL | NULL              | NULL                                     |             NULL | NULL | YES          | YES     | NULL            |         4683 |
|        24 | thread/innodb/buf_dump_thread          | BACKGROUND |           NULL | NULL             | NULL             | NULL           | NULL                |             NULL | NULL              | NULL                                     |             NULL | NULL | YES          | YES     | NULL            |         4682 |
|        25 | thread/sql/signal_handler              | BACKGROUND |           NULL | NULL             | NULL             | NULL           | NULL                |             NULL | NULL              | NULL                                     |                1 | NULL | YES          | YES     | NULL            |         4686 |
|        27 | thread/sql/compress_gtid_table         | FOREGROUND |              1 | NULL             | NULL             | NULL           | Daemon              |            93344 | Suspending        | NULL                                     |                1 | NULL | YES          | YES     | NULL            |         4687 |
|        41 | thread/sql/one_connection              | FOREGROUND |             16 | datadog          | localhost        | NULL           | Query               |                0 | Sending data      | SELECT * FROM performance_schema.threads |             NULL | NULL | YES          | YES     | Socket          |         4690 |
+-----------+----------------------------------------+------------+----------------+------------------+------------------+----------------+---------------------+------------------+-------------------+------------------------------------------+------------------+------+--------------+---------+-----------------+--------------+
MySQL SELECT grant - OK
root@zaps-VirtualBox:/etc/dd-agent/conf.d# mysql -u datadog --password=dogmysql -e "SELECT * FROM INFORMATION_SCHEMA.PROCESSLIST" && \
> echo -e "\033[0;32mMySQL PROCESS grant - OK\033[0m" || \
> echo -e "\033[0;31mMissing PROCESS grant\033[0m"
mysql: [Warning] Using a password on the command line interface can be insecure.
+----+---------+-----------+------+---------+------+-----------+----------------------------------------------+
| ID | USER    | HOST      | DB   | COMMAND | TIME | STATE     | INFO                                         |
+----+---------+-----------+------+---------+------+-----------+----------------------------------------------+
| 17 | datadog | localhost | NULL | Query   |    0 | executing | SELECT * FROM INFORMATION_SCHEMA.PROCESSLIST |
+----+---------+-----------+------+---------+------+-----------+----------------------------------------------+
MySQL PROCESS grant - OK

9.) Copied MySQL YAML file into its own file, and altered it (mysql.yaml)

init_config:

instances:
  - server: localhost
    user: datadog
    pass: dogmysql

10.) Reset the DataDog service to allow the change to take place, then checked info to make sure everything was working

root@zaps-VirtualBox:/etc/dd-agent/conf.d# /etc/init.d/datadog-agent restart
[ ok ] Restarting datadog-agent (via systemctl): datadog-agent.service.
root@zaps-VirtualBox:/etc/dd-agent/conf.d# /etc/init.d/datadog-agent info

====================
Collector (v 5.13.2)
====================

  Status date: 2017-05-25 15:51:30 (10s ago)
  Pid: 26370
  Platform: Linux-4.8.0-36-generic-x86_64-with-Ubuntu-16.04-xenial
  Python Version: 2.7.13, 64bit
  Logs: <stderr>, /var/log/datadog/collector.log, syslog:/dev/log

  Clocks
  ======
  
    NTP offset: Unknown (No response received from 2.datadog.pool.ntp.org.)
    System UTC time: 2017-05-25 19:51:42.428868
  
  Paths
  =====
  
    conf.d: /etc/dd-agent/conf.d
    checks.d: /opt/datadog-agent/agent/checks.d
  
  Hostnames
  =========
  
    socket-hostname: zaps-VirtualBox
    hostname: zaps-VirtualBox
    socket-fqdn: zaps-VirtualBox
  
  Checks
  ======
  
    ntp (5.13.2)
    ------------
      - instance #0 [OK]
      - Collected 1 metric, 0 events & 1 service check
  
    disk (5.13.2)
    -------------
      - instance #0 [OK]
      - Collected 24 metrics, 0 events & 0 service checks
  
    network (5.13.2)
    ----------------
      - instance #0 [OK]
      - Collected 0 metrics, 0 events & 0 service checks
  
    mysql (5.13.2)
    --------------
      - instance #0 [OK]
      - Collected 21 metrics, 0 events & 1 service check
  
  
  Emitters
  ========
  
    - http_emitter [OK]

====================
Dogstatsd (v 5.13.2)
====================

  Status date: 2017-05-25 15:51:35 (7s ago)
  Pid: 26367
  Platform: Linux-4.8.0-36-generic-x86_64-with-Ubuntu-16.04-xenial
  Python Version: 2.7.13, 64bit
  Logs: <stderr>, /var/log/datadog/dogstatsd.log, syslog:/dev/log

  Flush count: 1
  Packet Count: 17
  Packets per second: 1.7
  Metric count: 1
  Event count: 0
  Service check count: 0

====================
Forwarder (v 5.13.2)
====================

  Status date: 2017-05-25 15:51:40 (2s ago)
  Pid: 26366
  Platform: Linux-4.8.0-36-generic-x86_64-with-Ubuntu-16.04-xenial
  Python Version: 2.7.13, 64bit
  Logs: <stderr>, /var/log/datadog/forwarder.log, syslog:/dev/log

  Queue Size: 0 bytes
  Queue Length: 0
  Flush Count: 5
  Transactions received: 3
  Transactions flushed: 3
  Transactions rejected: 0
  API Key Status: API Key is valid
  

======================
Trace Agent (v 5.13.2)
======================

  Pid: 26365
  Uptime: 19 seconds
  Mem alloc: 1040288 bytes

  Hostname: zaps-VirtualBox
  Receiver: localhost:8126
  API Endpoints: https://trace.agent.datadoghq.com

  Bytes received (1 min): 0
  Traces received (1 min): 0
  Spans received (1 min): 0

  Bytes sent (1 min): 0
  Traces sent (1 min): 0
  Stats sent (1 min): 0
  
  Link: https://app.datadoghq.com/dash/integration/mysql?live=true&page=0&is_auto=false&from_ts=1495766092386&to_ts=1495769692386&tile_size=s
  
  Working Agent with tags
  
  ![Alt text](https://github.com/szaporta/Sarah_Zaporta_Support_Engineer/blob/master/Agent%20Tag%20Host%20View.png)
  
    
  MySQL Dashboard View
  
  ![Alt text](https://github.com/szaporta/Sarah_Zaporta_Support_Engineer/blob/master/MySQL%20Dashboard%20View.png)
  
  11.) Wrote custom agent to sample a random value (randomval.py, in check.d directory and randomval.yaml in conf.d directory)
  
  12.) Cloned MySQL integration dashboard 
  
  ![Alt text](https://github.com/szaporta/Sarah_Zaporta_Support_Engineer/blob/master/MySQL%20Cloned%20Dashboard.png)
  
  and added another metric 
  
  ![Alt text](https://github.com/szaporta/Sarah_Zaporta_Support_Engineer/blob/master/MySQL%20Performance%20Open%20Tables%20Added%20Metric.png)
  
  as well as the custom test.support.random metric from the custom Agent Check 
  
  ![Alt text](https://github.com/szaporta/Sarah_Zaporta_Support_Engineer/blob/master/test.support.random%20metric.png)
  
 Link: https://app.datadoghq.com/dash/294541/mysql---overview-cloned?live=true&page=0&is_auto=false&from_ts=1495764683206&to_ts=1495768283206&tile_size=m
  
  13.) Bonus question: What is the difference between a timeboard and a screenboard?
  A timeboard gives you metrics and event graphs and can be shared individually, whereas a screenboard has drag and drop widgets, are customizable, and allow a higher-level look into a host.
  
  14.) Took a snapshot of the test.support.random graph and drew a box around the section that showed it going above 0.90, and had the snapshot sent to my email using the @notification 
  
  ![Alt text](https://github.com/szaporta/Sarah_Zaporta_Support_Engineer/blob/master/snapshot%20over%200.90.png)

  15.) Set up monitor on the test.support.random metric that alerts when it goes above 0.90 at least once during the last 5 minutes, and have monitor email notifications:
 
Trigger:

  ![Alt text](https://github.com/szaporta/Sarah_Zaporta_Support_Engineer/blob/master/Monitor%20Alert%20-%20Trigger.png)

Recovery:

  ![Alt text](https://github.com/szaporta/Sarah_Zaporta_Support_Engineer/blob/master/Monitor%20Alert%20-%20Recovery.png)
 
