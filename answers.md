# The Challenger – Marc Ian Bucad

## Level 0 – Setting up an Ubuntu VM

### Installing and configuring the software and tools to set up an Ubuntu VM provisioned using Vagrant using Oracle VirtualBox as the hypervisor/provider.

- Operating System: Windows 10 Home x64


#### Oracle VM VirtualBox
  *  Source: https://www.virtualbox.org/
  <img hspace="20" src="https://dl.dropboxusercontent.com/s/euih82oyla8ze1h/001.png=0" />
  
  *  Downloaded an installed the VirtualBox platform for Windows Hosts.
  *  Downloaded and installed Oracle CM VirtualBox Exension Pack. Useful for private VLAN
  *  Version: 5.1.22
  <img hspace="20" src="https://dl.dropboxusercontent.com/s/8ft4733ehqltjon/002.png?dl=0" />
 

#### Vagrant
* Source: https://www.vagrantup.com/
 <img hspace="20" src="https://dl.dropboxusercontent.com/s/uxmugieq3rv4yfm/003.png?dl=0" />

* Downloaded an installed latest available version of Vagrant for Windows.
* Version: 1.9.4
 <img hspace="20" src="https://dl.dropboxusercontent.com/s/5sttcgvjj40txli/004.png?dl=0" />


#### MobaXterm
* Source: http://mobaxterm.mobatek.net
 <img hspace="20" src="https://dl.dropboxusercontent.com/s/e5qxvgjjewg34p4/005.png?dl=0" />

* Brings some common Linux command tools to windows. Acts as shell, SSH, SCP client.
* Version 10.2
 <img hspace="20" src="https://dl.dropboxusercontent.com/s/9w7v6yh6rrfs634/006.png?dl=0" />

* Additional configuration needed to make MobaXterm work with Vagrant.
  * Set environment variable “VAGRANT_HOME”
   <img hspace="20" src="https://dl.dropboxusercontent.com/s/s8betn46h6rnv30/007.png?dl=0" />

  * Configure MobaXterm to use Windows PATH variable. This will bring variables within the Windows space to be available in the Linux-like environment in MobaXterm
   <img hspace="20" src="https://dl.dropboxusercontent.com/s/5hhmppkxufqkn7q/008.png?dl=0" />

   <img hspace="20" src="https://dl.dropboxusercontent.com/s/qz8sauxoee5efzi/009.png?dl=0" />

 
 
#### Provisioning the VM
* Verify Vagrant setup.
  * Ran `vagrant -h` to check if vagrant binaries are accessible.
  * Error encountered below.
   <img hspace="20" src="https://dl.dropboxusercontent.com/s/lr564n0qvgjcvpt/010.png?dl=0" />

  * As per research, it is a known issue which can be resolved by upgrading vagrant-share plugin
  * Resolution: Upgrade vagrant-share plugin
  * Reference: https://github.com/mitchellh/vagrant/issues/8532
   <img hspace="20" src="https://dl.dropboxusercontent.com/s/i6t2zrwl148djet/011.png?dl=0" />

  * Ran the command to upgrade the plugin
   <img hspace="20" src="https://dl.dropboxusercontent.com/s/kvenlbj7324c5nn/012.png?dl=0" />

  * Verified if issue was resolved. Successfully ran `vagrant -h` 
   <img hspace="20" src="https://dl.dropboxusercontent.com/s/y5upe4jo25igzqs/013.png?dl=0" />


* Created VagrantFile to provision an Ubuntu 14.04 VM using virtualbox as provider.
   <img hspace="20" src="https://dl.dropboxusercontent.com/s/r5w8tmc23j0mnvg/014.png?dl=0" />

  * ../data on the host PC is shared to /vagrant_data on VM in case files needs to be transferred to and fro
  * IP address set explicitly but will actually still get a default IP from VirtualBox starting from .15

* Provision the VM
  * Once VagrantFile is created, create/provision Vm using `vagrant up` command.
  * Downloaded the binaries for Ubuntu successfully.
  * Error encountered below when provisioning/starting up the VM using `vagrant up` command.
  <img hspace="20" src="https://dl.dropboxusercontent.com/s/t0h0ulky85uls14/015.png?dl=0" />

  * Resolution: Upgrade to Vagrant 1.9.5 (Not yet GA)
    * As per research, the error message is already a known issue 
  * Workaround: Replace certain YAML and Ruby files
    * Backed up original files and replaced with ones downloaded below.
    * Reference: https://github.com/mitchellh/vagrant/issues/8520
    <img hspace="20" src="https://dl.dropboxusercontent.com/s/cwn3ulotz260crr/016.png?dl=0" />

  * `vagrant up` command no longer resulted to errors and successfully provisioned the VM
  * Checked if VM is running.
  <img hspace="20" src="https://dl.dropboxusercontent.com/s/fq9efrev4igx37u/017.png?dl=0" />


* Verify access to VM
  * Issue when accessing VM via `vagrant ssh`.
  <img hspace="20" src="https://dl.dropboxusercontent.com/s/gu0yzkksdcvqv2q/018.png?dl=0" />

  * Workarounds
    - If private IP accessible from Host, SSH directly.
    <img hspace="25" src="https://dl.dropboxusercontent.com/s/21480zy8zh2c46v/019.png?dl=0" />
      
    - If Oracle VirtualBox Extensions installed, SSH via forwarded port.
    <img hspace="25" src="https://dl.dropboxusercontent.com/s/scs8vs7g32f2j2e/020.png?dl=0" />
      
    - Override `vagrant` command via .BASHRC
      - Reference: https://github.com/mitchellh/vagrant/issues/5559
    
    <img hspace="25" src="https://dl.dropboxusercontent.com/s/v718qds1l3sbacr/021.png?dl=0" />
    <img hspace="25" src="https://dl.dropboxusercontent.com/s/p0ottr0yg22vtmp/022.png?dl=0" />


* Used below modified script to allow running `vagrant ssh <name>`
  ```
  [mibucad.Bucad-Lenovo] → cat .bashrc

  vagrant() {
    if [[ $1 == "ssh" ]];
    then
      if [[ -z "$2" ]] ;
      then
        command vagrant ssh-config > vagrant-ssh-config && ssh -A -F vagrant-ssh-config $(cat vagrant-ssh-config  |cut -d" " -f2 | head -1 | xargs echo -n)
      else
        command vagrant ssh-config > vagrant-ssh-config && ssh -A -F vagrant-ssh-config "$2"
      fi

    else
      command vagrant "$@"
    fi
  }
  ```

  * Verified that “vagrant ssh” is able to access default VM.
   <img hspace="20" src="https://dl.dropboxusercontent.com/s/hj1ac1yh5rtbrpy/023.png?dl=0" />



## Level 1 – Collecting your Data
### Sign up with Datadog
* Accessed www.datadoghq.com via browser
 <img hspace="25" src="https://dl.dropboxusercontent.com/s/aghws3su8ffq38s/101.png?dl=0" />

### Installing the Datadog Agent
* After signup, went to next step installing the agent.
* Checked instructions for Ubuntu
 <img hspace="25" src="https://dl.dropboxusercontent.com/s/avncrotul0q749x/102.png?dl=0" />

* Executed installation steps
  ```
  vagrant@ddog:~$ sudo su
  root@ddog:/home/vagrant# DD_INSTALL_ONLY=true
  root@ddog:/home/vagrant# echo $DD_INSTALL_ONLY
  true
  ```

  ```
  root@ddog:/home/vagrant# DD_API_KEY=086a2e1cdd154712037058ebc4a52cf0 bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/dd-agent/master/packaging/datadog-agent/source/install_agent.sh)"
    % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                   Dload  Upload   Total   Spent    Left  Speed
  100  9911  100  9911    0     0   3496      0  0:00:02  0:00:02 --:--:--  3495

  * Installing apt-transport-https

  Get:1 http://security.ubuntu.com trusty-security InRelease [65.9 kB]
  Ign http://archive.ubuntu.com trusty InRelease

  ...<snipped>

  Ign http://archive.ubuntu.com trusty/multiverse Translation-en_US
  Ign http://archive.ubuntu.com trusty/restricted Translation-en_US
  Ign http://archive.ubuntu.com trusty/universe Translation-en_US
  Fetched 11.5 MB in 2min 51s (67.2 kB/s)
  Reading package lists...
  Reading package lists...
  Building dependency tree...
  Reading state information...
  apt-transport-https is already the newest version.
  The following packages were automatically installed and are no longer required:
    acl at-spi2-core colord dconf-gsettings-backend dconf-service fontconfig

  ...<snipped>

  Use 'apt-get autoremove' to remove them.
  0 upgraded, 0 newly installed, 0 to remove and 0 not upgraded.

  * Installing APT package sources for Datadog

  Executing: gpg --ignore-time-conflict --no-options --no-default-keyring --homedir /tmp/tmp.RPvVx38taA --no-auto-check-trustdb --trust-model always --keyring /etc/apt/trusted.gpg --primary-keyring /etc/apt/trusted.gpg --recv-keys --keyserver hkp://keyserver.ubuntu.com:80 C7A7DA52
  gpg: requesting key C7A7DA52 from hkp server keyserver.ubuntu.com
  gpg: key C7A7DA52: public key "Datadog Packages <package@datadoghq.com>" imported
  gpg: Total number processed: 1
  gpg:               imported: 1  (RSA: 1)
  Executing: gpg --ignore-time-conflict --no-options --no-default-keyring --homedir /tmp/tmp.frRjWbjdwa --no-auto-check-trustdb --trust-model always --keyring /etc/apt/trusted.gpg --primary-keyring /etc/apt/trusted.gpg --recv-keys --keyserver hkp://keyserver.ubuntu.com:80 382E94DE
  gpg: requesting key 382E94DE from hkp server keyserver.ubuntu.com
  gpg: key 382E94DE: public key "Datadog, Inc <package@datadoghq.com>" imported
  gpg: Total number processed: 1
  gpg:               imported: 1  (RSA: 1)

  * Installing the Datadog Agent package

  Get:1 https://apt.datadoghq.com stable InRelease
  Ign https://apt.datadoghq.com stable InRelease
  Get:2 https://apt.datadoghq.com stable Release
  Get:3 https://apt.datadoghq.com stable/main amd64 Packages
  Get:4 https://apt.datadoghq.com stable/main Translation-en_US
  Ign https://apt.datadoghq.com stable/main Translation-en_US
  Ign https://apt.datadoghq.com stable/main Translation-en
  Fetched 12.5 kB in 6s (1,881 B/s)
  Reading package lists...
  Reading package lists...
  Building dependency tree...
  Reading state information...
  The following packages were automatically installed and are no longer required:
    acl at-spi2-core colord dconf-gsettings-backend dconf-service fontconfig

  ...<snipped>

  Use 'apt-get autoremove' to remove them.
  The following NEW packages will be installed:
    datadog-agent
  0 upgraded, 1 newly installed, 0 to remove and 0 not upgraded.
  Need to get 69.4 MB of archives.
  After this operation, 223 MB of additional disk space will be used.
  Fetched 69.4 MB in 2min 7s (544 kB/s)
  Selecting previously unselected package datadog-agent.
  (Reading database ... 62855 files and directories currently installed.)
  Preparing to unpack .../datadog-agent_1%3a5.13.2-1_amd64.deb ...
  Prepare Datadog Agent keys rotation
    Add the new 'Datadog, Inc <package@datadoghq.com>' key to the list of APT trusted keys.... key already installed
  Unpacking datadog-agent (1:5.13.2-1) ...
  Processing triggers for ureadahead (0.100.0-16) ...
  Setting up datadog-agent (1:5.13.2-1) ...
  Registering service datadog-agent
   Adding system startup for /etc/init.d/datadog-agent ...
     /etc/rc0.d/K20datadog-agent -> ../init.d/datadog-agent
     /etc/rc1.d/K20datadog-agent -> ../init.d/datadog-agent
     /etc/rc6.d/K20datadog-agent -> ../init.d/datadog-agent
     /etc/rc2.d/S20datadog-agent -> ../init.d/datadog-agent
     /etc/rc3.d/S20datadog-agent -> ../init.d/datadog-agent
     /etc/rc4.d/S20datadog-agent -> ../init.d/datadog-agent
     /etc/rc5.d/S20datadog-agent -> ../init.d/datadog-agent
  Enabling service datadog-agent
  Creating dd-agent group
  Creating dd-agent user

  * Adding your API key to the Agent configuration: /etc/dd-agent/datadog.conf

  * Starting the Agent...

   * Stopping Datadog Agent (stopping supervisord) datadog-agent
     ...done.
   * Starting Datadog Agent (using supervisord) datadog-agent
     ...done.

  Your Agent has started up for the first time. We're currently verifying that
  data is being submitted. You should see your Agent show up in Datadog shortly
  at:

      https://app.datadoghq.com/infrastructure

  Waiting for metrics.......................................

  Your Agent is running and functioning properly. It will continue to run in the
  background and submit metrics to Datadog.

  If you ever want to stop the Agent, run:

      sudo /etc/init.d/datadog-agent stop

  And to run it again run:

      sudo /etc/init.d/datadog-agent start
  ```

* Verified agent is running
  ```
  root@ddog:/home/vagrant#  ps -ef |grep datadog
  dd-agent  2516     1  0 00:21 ?        00:00:01 /opt/datadog-agent/embedded/bin/python /opt/datadog-agent/bin/supervisord -c /etc/dd-agent/supervisor.conf --pidfile /opt/datadog-agent/run/datadog-supervisord.pid
  dd-agent  2518  2516  0 00:21 ?        00:00:02 /opt/datadog-agent/bin/trace-agent
  dd-agent  2519  2516  0 00:21 ?        00:00:18 /opt/datadog-agent/embedded/bin/python /opt/datadog-agent/agent/ddagent.py
  dd-agent  2520  2516  0 00:21 ?        00:00:14 /opt/datadog-agent/embedded/bin/python /opt/datadog-agent/agent/dogstatsd.py --use-local-forwarder
  dd-agent  2523  2516  0 00:21 ?        00:00:13 /opt/datadog-agent/embedded/bin/python /opt/datadog-agent/agent/agent.py foreground --use-local-forwarder
  root      5781  2056  0 01:09 pts/0    00:00:00 grep --color=auto datadog
  ```

* Verified reporting data to Datadog. Found 1 host reporting to Datadog with correct hostname.
 <img hspace="25" src="https://dl.dropboxusercontent.com/s/pwq5l1xdb3utzl4/103.png?dl=0" />



### Bonus question: In your own words, what is the Agent?
* The agent is a small piece of software installed/deployed on target resources which are to be monitored and collect defined metrics from. It does so as often as configured, stores them then sends the data to a central location/server/service (Datadog in this case) to be collated, processed, and transformed to more meaningful information.



### Add tags and view in Host Map
* Modified datadog agent configuration file to add tags.
  ```
  root@ddog:/etc/dd-agent#  vim datadog.conf
  ```

  ```
  …
  #  Set the host's tags (optional)
  #  tags: mytag, env:prod, role:database
  tags: challenge, env:test, role:database
  …
  ```

* Restarted service for changes to take effect.
  ```
  root@ddog:/etc/dd-agent#  service datadog-agent restart
   * Stopping Datadog Agent (stopping supervisord) datadog-agent                   [ OK ]
   * Starting Datadog Agent (using supervisord) datadog-agent                      [ OK ]
  ```

  ```
  root@ddog:/etc/dd-agent#  tail /var/log/datadog/collector.log
  2017-05-14 01:30:03 UTC | INFO | dd.collector | checks.collector(collector.py:403) | Running check ntp
  2017-05-14 01:30:04 UTC | INFO | dd.collector | checks.collector(collector.py:403) | Running check disk
  2017-05-14 01:30:04 UTC | INFO | dd.collector | checks.collector(collector.py:403) | Running check network
  2017-05-14 01:30:04 UTC | INFO | dd.collector | checks.collector(collector.py:685) | Hostnames: {'socket-hostname': 'ddog', 'timezones': ('UTC', 'UTC'), 'hostname': 'ddog', 'socket-fqdn': 'ddog'}, tags: {'system': [u'challenge', u'env:test', u'role:database']}
  2017-05-14 01:30:04 UTC | INFO | dd.collector | checks.collector(collector.py:530) | Finished run # 1. Collection time: 4.71s. Emit time: 0.09s
  ```

* Verified tags on Host Map page in Datadog.
  <img hspace="25" src="https://dl.dropboxusercontent.com/s/rvwxou8ktxx1vuo/104.png?dl=0" />
 
  <img hspace="25" src="https://dl.dropboxusercontent.com/s/cjestc5futryvjt/105.png?dl=0" />

 

### Installing database and respective Datadog integration
* Installing MySQL database
  * Checked for mysql-version in repository
    ```
    root@ddog:~#  apt search mysql-server
    Sorting... Done
    Full Text Search... Done
    auth2db/trusty 0.2.5-2+dfsg-4 all
      Powerful and eye-candy IDS logger, log viewer and alert generator

    mysql-server/trusty-updates,trusty-security 5.5.55-0ubuntu0.14.04.1 all
      MySQL database server (metapackage depending on the latest version)
    ```

  * Downloaded and installed mysql-server
    ```
    root@ddog:~#  apt-get install mysql-server
    Reading package lists... Done
    Building dependency tree
    Reading state information... Done

    ...<snipped

    The following NEW packages will be installed:
      libaio1 libdbd-mysql-perl libdbi-perl libhtml-template-perl libmysqlclient18
      libterm-readkey-perl mysql-client-5.5 mysql-client-core-5.5 mysql-common
      mysql-server mysql-server-5.5 mysql-server-core-5.5
    0 upgraded, 12 newly installed, 0 to remove and 0 not upgraded.
    Need to get 9,714 kB of archives.
    After this operation, 97.2 MB of additional disk space will be used.
    Do you want to continue? [Y/n] Y

    ...<snipped

    170514  1:55:51 [Note] /usr/sbin/mysqld (mysqld 5.5.55-0ubuntu0.14.04.1) starting as process 12870 ...
    mysql start/running, process 13019
    Setting up libhtml-template-perl (2.95-1) ...
    Processing triggers for ureadahead (0.100.0-16) ...
    Setting up mysql-server (5.5.55-0ubuntu0.14.04.1) ...
    Processing triggers for libc-bin (2.19-0ubuntu6.11) ...

    root@ddog:~#  mysql --version
    mysql  Ver 14.14 Distrib 5.5.55, for debian-linux-gnu (x86_64) using readline 6.3
    ```

* Installing Datadog integration for MySQL. Integrations > Integrations > search “mysql”
 <img hspace="25" src="https://dl.dropboxusercontent.com/s/fhy55gpso91ry50/106.png?dl=0" />

 <img hspace="25" src="https://dl.dropboxusercontent.com/s/tt2hl6ljtmb0nky/107.png?dl=0" />


  * Checked for instructions under Configuration tab
   <img hspace="25" src="https://dl.dropboxusercontent.com/s/aqfl3zjf9p8a329/108.png?dl=0" />


  * Clicked “Generate Password” and ran commands after logging in to mysql as root.
    ```
    root@ddog:~#  mysql -u root -p
    Enter password:
    Welcome to the MySQL monitor.  Commands end with ; or \g.
    Your MySQL connection id is 171
    Server version: 5.5.55-0ubuntu0.14.04.1 (Ubuntu)

    mysql> CREATE USER 'datadog'@'localhost' IDENTIFIED BY ' A6VLkdC58RgBGTbLJicT39q8';
    Query OK, 0 rows affected (0.00 sec)

    mysql> GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'localhost' WITH MAX_USER_CONNECTIONS 5;
    Query OK, 0 rows affected (0.00 sec)

    mysql> GRANT PROCESS ON *.* TO 'datadog'@'localhost';
    Query OK, 0 rows affected (0.00 sec)

    mysql> GRANT SELECT ON performance_schema.* TO 'datadog'@'localhost';
    Query OK, 0 rows affected (0.00 sec)
    ```

* Verified user and replication rights
  ```
  root@ddog:~#  mysql -u datadog --password=A6VLkdC58RgBGTbLJicT39q8 -e "show status" | \
  > grep Uptime && echo -e "\033[0;32mMySQL user - OK\033[0m" || \
  > echo -e "\033[0;31mCannot connect to MySQL\033[0m"
  Uptime  3145
  Uptime_since_flush_status       3145
  MySQL user - OK
  root@ddog:~#  mysql -u datadog --password=A6VLkdC58RgBGTbLJicT39q8 -e "show slave status" && \
  > echo -e "\033[0;32mMySQL grant - OK\033[0m" || \
  > echo -e "\033[0;31mMissing REPLICATION CLIENT grant\033[0m"
  MySQL grant - OK
  ```

* Verified privileges for full metric catalogs
  ```
  root@ddog:~#  mysql -u datadog --password=A6VLkdC58RgBGTbLJicT39q8 -e "SELECT * FROM performance_schema.threads" && \
  > echo -e "\033[0;32mMySQL SELECT grant - OK\033[0m" || \
  > echo -e "\033[0;31mMissing SELECT grant\033[0m"
  MySQL SELECT grant - OK
  root@ddog:~#  mysql -u datadog --password=A6VLkdC58RgBGTbLJicT39q8 -e "SELECT * FROM INFORMATION_SCHEMA.PROCESSLIST" && \
  > echo -e "\033[0;32mMySQL PROCESS grant - OK\033[0m" || \
  > echo -e "\033[0;31mMissing PROCESS grant\033[0m"
  +-----+---------+-----------+------+---------+------+-----------+----------------------------------------------+
  | ID  | USER    | HOST      | DB   | COMMAND | TIME | STATE     | INFO                                         |
  +-----+---------+-----------+------+---------+------+-----------+----------------------------------------------+
  | 206 | datadog | localhost | NULL | Query   |    0 | executing | SELECT * FROM INFORMATION_SCHEMA.PROCESSLIST |
  +-----+---------+-----------+------+---------+------+-----------+----------------------------------------------+
  MySQL PROCESS grant - OK
  ```

* Configure the Agent with mysql credentials
  ```
  root@ddog:~#  cat > /etc/dd-agent/conf.d/mysql.yaml
  init_config:

  instances:
    - server: localhost
      user: datadog
      pass: A6VLkdC58RgBGTbLJicT39q8
      tags:
          - optional_tag1
          - optional_tag2
      options:
          replication: 0
          galera_cluster: 1
  ```

* Restarted the Agent for changes to take effect
  ```
  root@ddog:~#  service datadog-agent restart
   * Stopping Datadog Agent (stopping supervisord) datadog-agent           [ OK ]
   * Starting Datadog Agent (using supervisord) datadog-agent              [ OK ]
  ```

* Verified MySQL integration by checking info
  ```
  root@ddog:~#  dd-agent info
  ====================
  Collector (v 5.13.2)
  ====================

  ...<snipped>

    Checks
    ======

      mysql (5.13.2)
      --------------
        - instance # 0 [OK]
        - Collected 64 metrics, 0 events & 1 service check
        - Dependencies:
            - pymysql: 0.6.6.None

  ```


### Writing a Custom Check
- Metric name: test.support.random
- Check script: zz_Random.py
- Reference: http://docs.datadoghq.com/guides/agent_checks/

* Created configuration file
  ```
  root@ddog:~#  cat /etc/dd-agent/conf.d/zz_Random.yaml

  init_config:

  instances:
      [{}]

  ```

* Created script to send a random number for metric.
  ```
  root@ddog:~#  vim /opt/datadog-agent/agent/checks.d/zz_Random.py

  import random
  from checks import AgentCheck

  class zz_Random(AgentCheck):
      def check(self, instance):
          self.gauge('test.support.random', random.random())

  ```

* Tested custom metric
  ```
  root@ddog:/opt/datadog-agent/agent#  sudo -u dd-agent dd-agent check zz_Random
  2017-05-14 10:42:46,408 | INFO | dd.collector | config(config.py:1139) | initialized checks.d checks: ['zz_Random', 'network', 'mysql', 'ntp', 'disk']
  2017-05-14 10:42:46,412 | INFO | dd.collector | config(config.py:1140) | initialization failed checks.d checks: []
  2017-05-14 10:42:46,415 | INFO | dd.collector | checks.collector(collector.py:542) | Running check zz_Random
  Metrics:
  [('test.support.random',
    1494758566,
    0.5482504386063396,
    {'hostname': 'ddog', 'type': 'gauge'})]
  Events:
  []
  Service Checks:
  []
  Service Metadata:
  [{}]
      zz_Random (5.13.2)
      ------------------
        - instance # 0 [OK]
        - Collected 1 metric, 0 events & 0 service checks
  ```

*  Verified in Datadog if metric was received from the agent
  <img hspace="25" src="https://dl.dropboxusercontent.com/s/x8x8a9yzv1jca0m/109.png?dl=0" />


  
## Level 2 – Visualizing your Data
Clone database integration
* Opened the Dashboard List
 <img hspace="25" src="https://dl.dropboxusercontent.com/s/zf4egfclikdb88g/201.png?dl=0" />
 
* Launched the default “MySQL – Overview” Dashboard
 <img hspace="25" src="https://dl.dropboxusercontent.com/s/7sy27wdc9hxxjnd/202.png?dl=0" />

* Clicked on the gear icon and chose “Clone Dashboard”
 <img hspace="25" src="https://dl.dropboxusercontent.com/s/o81dmpk08ejzd9j/203.png?dl=0" />

* Named the cloned dashboard as “MySQL – Clone”
 <img hspace="25" src="https://dl.dropboxusercontent.com/s/hk7lgzbuzn5y6fr/204.png?dl=0" />

 
### Add additional metric (Custom Check)
* Drag and drop Timeseries widget to the cloned dashboard
 <img hspace="25" src="https://dl.dropboxusercontent.com/s/w0nxbfwzi65kfq6/205.png?dl=0" />

* Configure the widget
  * Search for the Metric and provide a title for the graph
  <img hspace="25" src="https://dl.dropboxusercontent.com/s/a009vv497dfs3tm/206.png?dl=0" />

* Verified widget added with Random Check metric.
 <img hspace="25" src="https://dl.dropboxusercontent.com/s/szz1mip80ksn9pm/207.png?dl=0" />
 

### Bonus question: What is the difference between a timeboard and a screenboard?

* TimeBoard
  * General purpose: troubleshooting and correlating metric data.
  * Time scope: All graphs share the same configure time range to display.
  * Customizability: Graphs will always show in grid-like fashion but can be rearranged.
  * Shareability: Each graph can be shared individually
  
* Screenboard
  * General purpose: status boards and data sharing
  * Time scope: Each graph can be configured with different time spans.
  * Customizability: Graphs are more flexible and are more customizable. Graphs can be of different dimensions.
  * Shareablility: Graphs are shared as a whole but as a read-only entity
  
  - Reference: https://p.datadoghq.com/sb/5a8ad3031-18d4027fe9

  
### Take snapshot of `test.support.random` graph
* Highlight to zoom graph containing values of above 0.90
 <img hspace="25" src="https://dl.dropboxusercontent.com/s/9hcalx1aas8e4e8/208.png?dl=0" />
 <img hspace="25" src="https://dl.dropboxusercontent.com/s/71uem1jcpq1be3d/209.png?dl=0" />
 
* Annotated graph to send an event. Can draw a box before posting.
 <img hspace="25" src="https://dl.dropboxusercontent.com/s/nuqt15g9hiupa37/210.png?dl=0" />
 <img hspace="25" src="https://dl.dropboxusercontent.com/s/1n2zjp2bear8mrg/211.png?dl=0" />
 <img hspace="25" src="https://dl.dropboxusercontent.com/s/cbmgexg1ed4qvx6/212.png?dl=0" />
  
* Check Events and found the annotated graph. Clicked on the graph to take a snapshot.
 <img hspace="25" src="https://dl.dropboxusercontent.com/s/kl5e6i9urbpsanr/213.png?dl=0" />
 <img hspace="25" src="https://dl.dropboxusercontent.com/s/atlt9xz739ew3tl/214.png?dl=0" />
 
* Draw and snapshot the graph
 <img hspace="25" src="https://dl.dropboxusercontent.com/s/v5iix9ed1wl5p1r/215.png?dl=0" />
 <img hspace="25" src="https://dl.dropboxusercontent.com/s/88mkfa5z150f96z/216.png?dl=0" />

* Email verification. Checked if notification received via email.
 <img hspace="25" src="https://dl.dropboxusercontent.com/s/8hzg8x2v757wzrj/217.png?dl=0" />

* Issues encountered
  * Some Email notifications were not being received
  * Nothing found  in Spam/Junk folder
  * Notified Outlook.com email instead of Gmaill.com – Received successfully
  * _Conclusion_: Gmail servers have blocked incoming mail from "noreply=datadoghq.com@dtdg.co"
 
 
 
## Level 3 – Alerting on your Data

### Setup Monitor
* Threshold: 0.90
* Clicked on the gear icon for a specific graph to base the Monitor.
 <img hspace="25" src="https://dl.dropboxusercontent.com/s/rpu2kly6j9kyhgg/301.png?dl=0" />

* Bonus points: Make it a multi-alert by host so that you won't have to recreate it if your infrastructure scales up.
 <img hspace="25" src="https://dl.dropboxusercontent.com/s/gj1k34t9qg1vhyy/302.png?dl=0" />
 
* Set conditions to alert if threshold crossed once during last 5 minutes.
 <img hspace="25" src="https://dl.dropboxusercontent.com/s/pj8p4g8b65gjzp5/303.png?dl=0" />

* Set the description/message for the alert and set to Notify intended recipients.
 <img hspace="25" src="https://dl.dropboxusercontent.com/s/a913z03hpw8dnoi/304.png?dl=0" />

* Check if Monitor has been triggered
 <img hspace="25" src="https://dl.dropboxusercontent.com/s/od4zxn8vymwttkg/305.png?dl=0" />

* Verify Email alert
*Note: Email alert received in both Gmail and Outlook. Likely because sender is not no-reply=datadoghq.com@dtdg.co*

  * Gmail
    <img hspace="25" src="https://dl.dropboxusercontent.com/s/9kelofpvps9f3m5/306.png?dl=0" />
    <img hspace="25" src="https://dl.dropboxusercontent.com/s/g7eya8bppo6vgkd/307.png?dl=0" />

  * Outlook
    <img hspace="25" src="https://dl.dropboxusercontent.com/s/29hdynqk1jyon6n/308.png?dl=0" />

 
### Bonus: Set up a scheduled downtime
* Defined a downtime schedule by going to Monitors > “Manage Downtime”
 <img hspace="25" src="https://dl.dropboxusercontent.com/s/syv2eivuge1cz2x/309.png?dl=0" />

* Set the Schedule and message
 <img hspace="25" src="https://dl.dropboxusercontent.com/s/zczmafwdot5ug9r/310.png?dl=0" />

* Verified created scheduled downtime
 <img hspace="25" src="https://dl.dropboxusercontent.com/s/9hdyjh3a1d9zj6z/311.png?dl=0" />

* Verified that Email notification is received
 <img hspace="25" src="https://dl.dropboxusercontent.com/s/gcminfv7iyeui6h/312.png?dl=0" />
 

# END
