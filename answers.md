# Introduction

## Agent Install
I have deployed the agent on my Intel Nuc running Ubuntu 18.04. Deployment is done easily by running the following command:

`DD_API_KEY=792aad7f4bd921fba0e91560d2382275 DD_SITE="datadoghq.eu" bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"`

For step-by-step instructions, or other architectures, check out: https://app.datadoghq.eu/account/settings#agent/ubuntu

## Tags
Tags are a convenient way of adding dimensions to metrics. They can be filtered, aggregated and compared in visualizations. Tags are a key:value pair with some restrictions for the key. 

In complex cloud and container deployments, it's a good idea to look at service level in a collection of hosts apposed to looking at a single host due to the dynamic nature.

For more information on tags, take a look at: https://docs.datadoghq.com/tagging/. Using tags in visualisations is described in https://docs.datadoghq.com/tagging/using_tags/?tab=assignment

## Applying tags to Ubuntu
To apply tags to an Ubuntu host, edit /etc/datadog-agent/datadog.yaml. Under **&#64;param tags** you can define your tags.

Here is an example:
```yaml
tags:
  - environment:dev
  - data:dog

```
For a full copy of the yaml, check out agent/datadog.yaml


## MySQL deployment
I have installed MySQL Server version: 5.7.27-0 on my Ubuntu host.

## Monitoring MySQL
It takes a few steps to monitor MySQL databases with Datadog. First we need to configure some configuration files in the Datadog conf directory (/etc/datadog-agent/conf.d/mysql.d). Then, we create a Datadog user for MySQL.

Step-by-step instructions can be found at: https://docs.datadoghq.com/integrations/mysql/

### Generate some load on MySQL and show some pretty graphs

We can use Sysbench to generate some load on the MySQL database.

### Install sysbench:
```shell
sudo apt-get install sysbench
```

###Create database for Sysbench
Then we create a database and assign privileges to user sysbench:
```sql
    mysql> CREATE DATABASE sysbench;
    mysql> CREATE USER 'sysbench'@'localhost' IDENTIFIED BY 'password';
    mysql> GRANT ALL PRIVILEGES ON sysbench. * TO 'sysbench'@'localhost';
    mysql> FLUSH PRIVILEGES;
```

### Setup MySQL integration in Datadog
Now we are going to setup MySQL integration in the Datadog GUI:
* Go to Integrations - Integrations 
* Type mysql in the search bar
* Click Install


### Show the MySQL dashboard
In the Datadog GUI:
* Click Dashboards
* Click MySQL - Overview

### Run Sysbench

Now we can go to the directory with Sysbench config files (/usr/share/sysbench) and run the command:

```shell
sysbench oltp_read_only.lua --threads=4 --mysql-host=localhost --mysql-user=sysbench --mysql-password=password --mysql-port=3306 --tables=10 --table-size=1000000 prepare --db-driver=mysql```

Output should be similar to:
    sysbench 1.0.11 (using system LuaJIT 2.1.0-beta3)

    Initializing worker threads...
    Creating table 'sbtest2'...
    Creating table 'sbtest1'...
    Creating table 'sbtest4'...
    Creating table 'sbtest3'...
    Inserting 1000000 records into 'sbtest2'
    Inserting 1000000 records into 'sbtest1'
    Inserting 1000000 records into 'sbtest4'
    Inserting 1000000 records into 'sbtest3'
```
    
### Note
For an extensive guide into Sysbench, take a look at: https://severalnines.com/database-blog/how-benchmark-performance-mysql-mariadb-using-sysbench


