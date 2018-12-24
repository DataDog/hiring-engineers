Your answers to the questions go here.

## Prerequisites - Setup the environment
My environment for this exercise is below :
  Vagrant Ubuntu VM 16.04 (xenial)  
  Docker (Ubuntu 16.04), MySQL on the Vagrant
  
## Collecting Metrics:

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
![HostMap](HostMap_Karino.PNG)

* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

** Install MySQL
1) sudo apt-get update
2) sudo apt-get install mysql-server

** Create a datadog user
1) sudo mysql -e "CREATE USER 'datadog'@'localhost' IDENTIFIED BY 'nl7ZchKVbXCEHux(MXG5LbkF';"
2) sudo mysql -e "GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'localhost' WITH MAX_USER_CONNECTIONS 5;"
3) sudo mysql -e "GRANT PROCESS ON *.* TO 'datadog'@'localhost';"
4) sudo mysql -e "GRANT SELECT ON performance_schema.* TO 'datadog'@'localhost';"

** Verification
1) mysql -u datadog --password='nl7ZchKVbXCEHux(MXG5LbkF' -e "show status" | \
grep Uptime && echo -e "\033[0;32mMySQL user - OK\033[0m" || \
echo -e "\033[0;31mCannot connect to MySQL\033[0m"
mysql -u datadog --password='nl7ZchKVbXCEHux(MXG5LbkF' -e "show slave status" && \
echo -e "\033[0;32mMySQL grant - OK\033[0m" || \
echo -e "\033[0;31mMissing REPLICATION CLIENT grant\033[0m"

2) mysql -u datadog --password='nl7ZchKVbXCEHux(MXG5LbkF' -e "SELECT * FROM performance_schema.threads" && \
echo -e "\033[0;32mMySQL SELECT grant - OK\033[0m" || \
echo -e "\033[0;31mMissing SELECT grant\033[0m"
mysql -u datadog --password='nl7ZchKVbXCEHux(MXG5LbkF' -e "SELECT * FROM INFORMATION_SCHEMA.PROCESSLIST" && \
echo -e "\033[0;32mMySQL PROCESS grant - OK\033[0m" || \
echo -e "\033[0;31mMissing PROCESS grant\033[0m"

** Configure the Agent to connect to MySQL
1) create config file
 cd /etc/datadog-agent
 sudo vi conf.d/mysql.yaml
---------------------------------
init_config:

instances:
  - server: localhost
    user: datadog
    pass: nl7ZchKVbXCEHux(MXG5LbkF
    
    tags:
        - optional_tag1
        - optional_tag2
    options:
      replication: 0
      galera_cluster: 1
---------------------------------

2) Restart the Agent
   sudo systemctl stop datadog-agent
   sudo systemctl start datadog-agent

3) Confirm Agent status 
  sudo datadog-agent status | grep 'mysql'

* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

* Change your check's collection interval so that it only submits the metric once every 45 seconds.


* **Bonus Question** Can you change the collection interval without modifying the Python check file you created?
