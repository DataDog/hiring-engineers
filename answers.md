Your answers to the questions go here.

## Prerequisites - Setup the environment

> You can utilize any OS/host that you would like to complete this exercise. However, we recommend one of the following approaches:
>
> * You can spin up a fresh linux VM via Vagrant or other tools so that you don’t run into any OS or dependency issues. [Here are instructions](https://github.com/DataDog/hiring-engineers/blob/solutions-engineer/README.md#vagrant) for setting up a Vagrant Ubuntu VM. We strongly recommend using minimum `v. 16.04` to avoid dependency issues.
> * You can utilize a Containerized approach with Docker for Linux and our dockerized Datadog Agent image.

As my host OS is Windows 10 x64, I opted for VMware Workstation 15 to set up my guest VM (Ubuntu 18.04).

> Then, sign up for Datadog (use “Datadog Recruiting Candidate” in the “Company” field), get the Agent reporting metrics from your local machine.

This was a very straightforward process. It was simply a matter of signing up for Datadog and executing the provided installation script for Ubuntu:
```bash
$ DD_API_KEY=********* bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```
Immediately after installation, incoming metrics could be seen in the “System – Metrics” dashboard:

![Alt text](img/1-System-Metrics-Datadog.png?raw=true "Datadog System Metrics Dashboard")

## Collecting Metrics:

> * Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

```bash
sudo vi /etc/datadog-agent/datadog.yaml
```

Set arbitrary tags: 
```bash
# Set the host's tags (optional)
tags:
   - env:dev
   - tier:webserver 
```

Restart agent:
```bash
$ sudo systemctl restart datadog-agent
```

View of Host Map page:
![Alt text](img/2-Host-Map_Datadog.png?raw=true "Datadog Host Map page")

>
> * Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

Install MySQL:
```bash
$ sudo apt update
$ sudo apt install mysql-server
$ sudo mysql_secure_installation
$ sudo mysql

mysql> ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '*******';
mysql> FLUSH PRIVILEGES;
mysql> exit;
```

Follow integration setup instructions here:
https://docs.datadoghq.com/integrations/mysql/
```bash
$ mysql -u root -p

mysql> CREATE USER 'datadog'@'localhost' IDENTIFIED WITH mysql_native_password by '********';

```

Grant privileges to Agent to collect DB metrics:
```bash
mysql> GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'localhost' WITH MAX_USER_CONNECTIONS 5;
mysql> GRANT PROCESS ON *.* TO 'datadog'@'localhost';
mysql> GRANT SELECT ON performance_schema.* TO 'datadog'@'localhost';
```

Create and populate Agent MySQL config as follows:
```bash
$ sudo vi /etc/datadog-agent/conf.d/mysql.d/conf.yaml

  init_config:

  instances:
    - server: 127.0.0.1
      user: datadog
      pass: '**********'
      port: 3306
      options:
          replication: 0
          galera_cluster: true
          extra_status_metrics: true
          extra_innodb_metrics: true
          extra_performance_metrics: true
          schema_size_metrics: false
          disable_innodb_metrics: false

$ sudo systemctl restart datadog-agent
```

Note MySQL app listed on Infrstructure List page:
![Alt text](img/3a-Infrastructure_List_Datadog.png?raw=true "Infrastructure List")


View of newly created "MySql Overview" dashboard:
![Alt text](img/3b-MySQL-Overview_Datadog.png?raw=true "MySql Overview")


> * Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.


> * Change your check's collection interval so that it only submits the metric once every 45 seconds.

> * **Bonus Question** Can you change the collection interval without modifying the Python check file you created?
