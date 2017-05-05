Your answers to the questions go here.
# Level 0 Answer "setup an ubuntu VM"

I have used my Mac, and I already have a CentOS VM which I think is running a database.

# Level 1 

## Sign up for DataDog

I signed up for DataDog a week ago (mark@jeffery.com), and I have changed the company name to Datadog Recruiting Candidate

## Bonus Question: What is an agent

The datadog agent is some software that runs in the background on a computer, and measures metrics and events, sending them up the DataDog SaaS servers. The agent collects standard Infrastructure metrics (CPU utilisation etc), but it is also able to collect metrics from Cloud providers (AWS, Azure etc), Databases (MySQL, MongoDB etc), Web Servers (IIS, Apache etc) and container technologies (Docker, Kubernetes etc)

## Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

Edited /etc/dd-agent/datadog.conf

Added some tags to define the server

![definition of tags](https://github.com/markjeffery/hiring-engineers/blob/master/screen%20shot%20-%20tag%20definition.png)

Restarted agent (not sure if I needed to)

Checked out the infrastructure menu, selected my new server in the host map, and clicked on system. It shows the tags.

![tags shown in datadog](https://github.com/markjeffery/hiring-engineers/blob/master/screen%20shot%20-%20tag%20results.png)

## Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

## I gave the Vagrant thing a go - here is the vagrant file

```yaml
# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/trusty64"

  config.vm.provider "virtualbox" do |vb|
    vb.memory = "1024"
  end
  config.vm.provision :shell, path: "bootstrap.sh"
end

```
## and here is the bootstrap.sh
```
#!/usr/bin/env bash

apt-get update
apt-get install -y apache2
export DEBIAN_FRONTEND="noninteractive"

debconf-set-selections <<< "mysql-server mysql-server/root_password password password"
debconf-set-selections <<< "mysql-server mysql-server/root_password_again password password"
apt-get install -y mysql-server-5.6 mysql-client-core-5.6

DD_API_KEY=aa14a1463b8ac4fdbd27dc02bd5a50e2 bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/dd-agent/master/packaging/datadog-agent/source/install_agent.sh)"

echo tags: mj, type:vagrant, role:db, env:qa >> /etc/dd-agent/datadog.conf

service datadog-agent restart
```

after that, I configured mysql with the performance stuff taken from the blog: (url later)

### executed the following in mysql, as per mysql tile:

```
mysql> CREATE USER 'datadog'@'localhost' IDENTIFIED BY 'password';
Query OK, 0 rows affected (0.01 sec)

mysql> GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'localhost' WITH MAX_USER_CONNECTIONS 5;
Query OK, 0 rows affected (0.01 sec)

mysql> GRANT PROCESS ON *.* TO 'datadog'@'localhost';
Query OK, 0 rows affected (0.00 sec)

mysql> GRANT SELECT ON performance_schema.* TO 'datadog'@'localhost';
Query OK, 0 rows affected (0.00 sec)
```
### executed the verification

```
vagrant@vagrant-ubuntu-trusty-64:/vagrant/mysql-sys$ mysql -u datadog --password=password -e "show status" | \
> grep Uptime && echo -e "\033[0;32mMySQL user - OK\033[0m" || \
> echo -e "\033[0;31mCannot connect to MySQL\033[0m"
Warning: Using a password on the command line interface can be insecure.
Uptime	2815
Uptime_since_flush_status	2815
MySQL user - OK
vagrant@vagrant-ubuntu-trusty-64:/vagrant/mysql-sys$ mysql -u datadog --password=password -e "show slave status" && \
> echo -e "\033[0;32mMySQL grant - OK\033[0m" || \
> echo -e "\033[0;31mMissing REPLICATION CLIENT grant\033[0m"
Warning: Using a password on the command line interface can be insecure.
MySQL grant - OK

vagrant@vagrant-ubuntu-trusty-64:/vagrant/mysql-sys$ mysql -u datadog --password=password -e "SELECT * FROM performance_schema.threads" && \
> echo -e "\033[0;32mMySQL SELECT grant - OK\033[0m" || \
> echo -e "\033[0;31mMissing SELECT grant\033[0m"
...
MySQL SELECT grant - OK
vagrant@vagrant-ubuntu-trusty-64:/vagrant/mysql-sys$ mysql -u datadog --password=password -e "SELECT * FROM INFORMATION_SCHEMA.PROCESSLIST" && \
> echo -e "\033[0;32mMySQL PROCESS grant - OK\033[0m" || \
> echo -e "\033[0;31mMissing PROCESS grant\033[0m"
...
MySQL PROCESS grant - OK

### now configure mysql.yaml

vagrant@vagrant-ubuntu-trusty-64:/etc/dd-agent/conf.d$ sudo cp mysql.yaml.example mysql.yaml
```

### executed info command to check out mysql:

```
vagrant@vagrant-ubuntu-trusty-64:/etc/dd-agent/conf.d$ sudo /etc/init.d/datadog-agent info
====================
Collector (v 5.13.0)
====================
... 
    mysql (5.13.0)
    --------------
      - instance #0 [OK]
      - Collected 64 metrics, 0 events & 1 service check
      - Dependencies:
          - pymysql: 0.6.6.None
```

### Loaded up a sample database

```
vagrant@vagrant-ubuntu-trusty-64:/vagrant/test_db$ mysql -u root -p -t < employees.sql
vagrant@vagrant-ubuntu-trusty-64:/vagrant/test_db$ while (true) do mysql -u root --password=password -t < test_employees_md5.sql ; done
Warning: Using a password on the command line interface can be insecure.

![mysql dashboard](https://github.com/markjeffery/hiring-engineers/blob/master/screen%20shot%20-%20mysql%20screenshot.png)
```

## Write a custom Agent check that samples a random value. Call this new metric: test.support.random

random.yaml in /etc/dd-agent/conf.d/
```yaml
init_config:

instances:
    [{}]
```
random.py in /etc/dd-agent/checks.d
```py
import random
from checks import AgentCheck
class RandomCheck(AgentCheck):
    def check(self, instance):
        self.gauge('test.support.random', random.random())
```

Check status:
```
/etc/init.d/datadog-agent info
====================
Collector (v 5.13.0)
====================
...
  Checks
  ======
  
    random (5.13.0)
    ---------------
      - instance #0 [OK]
      - Collected 1 metric, 0 events & 0 service checks
  
...
```
# Level 2 - Visualizing your Data

Database dashboard here: https://app.datadoghq.com/dash/integration/mysql?live=true&tpl_var_scope=host%3Avagrant-ubuntu-trusty-64&page=0&is_auto=false&from_ts=1494015509696&to_ts=1494019109696&tile_size=m

![db dashboard](https://github.com/markjeffery/hiring-engineers/blob/master/screen%20shot%20-%20standard%20db%20dashboard.png)

Cloned and added random

https://app.datadoghq.com/dash/285369/mysql---overview-cloned?live=true&page=0&is_auto=false&from_ts=1494015710972&to_ts=1494019310972&tile_size=m

![db dashboard with random](https://github.com/markjeffery/hiring-engineers/blob/master/screen%20shot%20-%20db%20dashboard%20with%20random.png)

## Bonus question: What is the difference between a timeboard and a screenboard?

A timeboard shows a *grid* of dashboard elements that share a same time period. The time period can be chosen, and all the dashboard elements will be in sync, allowing the user to check different metrics for correlation.

https://app.datadoghq.com/dash/285372/marks-timeboard-5-may-2017-2225?live=true&page=0&is_auto=false&from_ts=1494016194790&to_ts=1494019794790&tile_size=m

![timeboard example](https://github.com/markjeffery/hiring-engineers/blob/master/Screen%20Shot%20-%20timeboard%20example.png)

A screenboard shows a more flexible layout of differently sized dashboard elements that have independent time periods.

https://app.datadoghq.com/screen/181381/marks-screenboard-5-may-2017-2225

![screenboard example](https://github.com/markjeffery/hiring-engineers/blob/master/Screen%20Shot%20-%20screenboard%20example.png)

## Take a snapshot of your test.support.random graph and draw a box around a section that shows it going above 0.90. Make sure this snapshot is sent to your email by using the @notification

Not sure I understand this yet: https://app.datadoghq.com/screen/181381/marks-screenboard-5-may-2017-2225

It has a line at 0.9 (dashed)

![marker at 0.9](https://github.com/markjeffery/hiring-engineers/blob/master/Screen%20Shot%20marker%20at%200.9.png)

I've setup a monitor - I really like the colour coding of the chart to show where the monitors will trigger - it makes it much easier to set thresholds correctly.

![setting up monitor](https://github.com/markjeffery/hiring-engineers/blob/master/Screen%20Shot%20setting%20up%20monitor.png)

https://app.datadoghq.com/monitors#2001094?group=all&live=4h

