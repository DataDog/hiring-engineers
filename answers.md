# Collecting Metrics:

* Installing datadog agent

``` bash
DD_API_KEY=my_keyXXXXXX bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```
* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
``` bash
vi /etc/datadog-agent/datadog.yaml
## add tags
tags:
  - env:ubuntu:local
# restart agent
 service datadog-agent restart
```
Snapshot ![here](https://github.com/cmcornejocrespo/hiring-engineers/blob/solutions-engineer/images/images01-tags.jpg)

* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
``` bash
# install mysql
apt install mysql-server
# Create a datadog user with replication rights in your MySQL server
sudo mysql -e "CREATE USER 'datadog'@'localhost' IDENTIFIED BY 'haaaa';"
sudo mysql -e "GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'localhost' WITH MAX_USER_CONNECTIONS 5;"

#grant the following privileges to get the full metrics catalog
sudo mysql -e "GRANT PROCESS ON *.* TO 'datadog'@'localhost';"
sudo mysql -e "GRANT SELECT ON performance_schema.* TO 'datadog'@'localhost';"

# verify all ok
mysql -u datadog --password='NTQ1fMKAZNMSNji2z1r2g[Iq' -e "show status" | \
grep Uptime && echo -e "\033[0;32mMySQL user - OK\033[0m" || \
echo -e "\033[0;31mCannot connect to MySQL\033[0m"
mysql -u datadog --password='NTQ1fMKAZNMSNji2z1r2g[Iq' -e "show slave status" && \
echo -e "\033[0;32mMySQL grant - OK\033[0m" || \
echo -e "\033[0;31mMissing REPLICATION CLIENT grant\033[0m"

mysql -u datadog --password='NTQ1fMKAZNMSNji2z1r2g[Iq' -e "SELECT * FROM performance_schema.threads" && \
echo -e "\033[0;32mMySQL SELECT grant - OK\033[0m" || \
echo -e "\033[0;31mMissing SELECT grant\033[0m"
mysql -u datadog --password='NTQ1fMKAZNMSNji2z1r2g[Iq' -e "SELECT * FROM INFORMATION_SCHEMA.PROCESSLIST" && \
echo -e "\033[0;32mMySQL PROCESS grant - OK\033[0m" || \
echo -e "\033[0;31mMissing PROCESS grant\033[0m"

# Configure the Agent to connect to MySQL
vi /etc/datadog-agent/conf.d/mysql.yaml

init_config:

instances:
  - server: localhost
    user: datadog
    pass: NTQ1fMKAZNMSNji2z1r2g[Iq
    tags:
        - optional_tag1
        - optional_tag2
    options:
      replication: 0
      galera_cluster: 1
      
# restart the agent
service datadog-agent restart

# check agent status (mysql)
datadog-agent status
...

 mysql (1.5.0)
    -------------
      Instance ID: mysql:4ff4449a9ad6c6f1 [OK]   
...

```

* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

```bash
#add custom metrics
vi /etc/datadog-agent/conf.d/my_metric.yaml

instances: [{}]

#create check

vi /etc/datadog-agent/checks.d/my_metric.py

from random import randint
# the following try/except block will make the custom check compatible with any Agent version
try:
    # first, try to import the base class from old versions of the Agent...
    from checks import AgentCheck
except ImportError:
    # ...if the above failed, the check is running in Agent version 6 or later
    from datadog_checks.checks import AgentCheck

# content of the special variable __version__ will be shown in the Agent status page
__version__ = "1.0.0"


class RandomCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', randint(0,1000))

# restart agent
service datadog-agent restart

# check the check is ok
datadog-agent check my_metric

```

# Change your check's collection interval so that it only submits the metric once every 45 seconds

```bash
#add min_collection_interval
vi /etc/datadog-agent/conf.d/my_metric.yaml

init_config:

instances:
  - min_collection_interval: 45
  
# restart agent
service datadog-agent restart


```

# Bonus Question Can you change the collection interval without modifying the Python check file you created?
By changing the interval at the instance level in the yaml file.
