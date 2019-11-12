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
* Click Dashboard List
* Click MySQL - Overview

<img src="https://github.com/arnizzle/hiring-engineers/blob/master/screenshots/MySQL%20Sysbench.png">

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

## Running and monitoring MySQL on Docker

* In the Datadog GUI Click Integrations, and search for Docker.
* Install the Docker Integration, and click Configuration.
* Follow the steps to add dd-agent to the Docker group and allow the agent to connect to docker
* Restart the agent on your host

### Pull MySQL image
Next we are going to pull the MySQL image.

```shell
arne@nuc:~$ docker pull mysql/mysql-server:5.7
5.7: Pulling from mysql/mysql-server
a316717fc6ee: Pull complete 
b64762744f75: Pull complete 
a1f742e3aa43: Pull complete 
f71a5f0dcc26: Pull complete 
Digest: sha256:5396bc60a6c08abb6b7e8350b255324a91ee9f3ea11f009aea3e4b61ead38bf6
Status: Downloaded newer image for mysql/mysql-server:5.7
docker.io/mysql/mysql-server:5.7
```

### Run container
and run the container, using a different port (optional if there is no MySQL running locally)

```shell
arne@nuc:~$ docker run --name=mysql1 -d mysql/mysql-server:5.7 -p 33060:3306
0ad5b981857a43a828ae60c729257c4a3aa9b9ef0282046fd35c34247d42f330

```

### Get password
We have to find out the auto-generated password:

```shell
arne@nuc:~$ docker logs mysql1 2>&1 | grep GENERATED
[Entrypoint] GENERATED ROOT PASSWORD: 3M2EkVaNiqIK@hYLBIhedYpG3L0N

```

### Login MySQL
and log in to the container using the generated password

```shell
arne@nuc:~$ docker exec -it mysql1 mysql -uroot -p
Enter password: 
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 5
Server version: 5.7.28

```
### Create MySQL database for Sysbench
We are going to generate some load using Sysbench. First we need to create a database and user for Sysbench
**Note: The Commands Used For The Docker Container Are Slighly Different From The Local Mysql Deployment since we are going to connect over TCP versus local socket. With the GRANT PRIVILEGES command we allow access from ANY host. **

```shell
mysql> CREATE DATABASE sysbench;
mysql> CREATE USER 'sysbench'@'localhost' IDENTIFIED BY 'password';
mysql> GRANT ALL PRIVILEGES ON sysbench. * TO 'sysbench'@''%;
mysql> FLUSH PRIVILEGES;
```

### Install sysbench:
```shell
sudo apt-get install sysbench
```
### Run some load
Finally we can run the Sysbench command. Note that the host is NOT localhost since that would connect to a socket. Instead an IP address is used to force a TCP connection. Also, we are using a different port to match that of the container.

```shell
sysbench oltp_read_only.lua --threads=4 --mysql-host=127.0.0.1 --mysql-user=sbtest --mysql-password=password --mysql-port=33060 --tables=10 --table-size=1000000 prepare --db-driver=mysql
```

### Custom Agent Check

In this example we are going to deploy a custom agent check. Custom agent checks run at a regular interval which defaults to every 15 seconds and are recommended to collect metrics for custom applications or unique systems. Alternatively you can write a full fledged integration if you want to share your application (commercially or open soruce).

For more information on customer agent checks check out: https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6 and the full fledged integration can be found here: https://docs.datadoghq.com/developers/integrations/new_check_howto/

### Deploying the custom agent check

First we are going to create a hello.yaml in the *conf.d/ *directory of the agent. This needs to cointain a sequence called *Instances*  that has a mapping, but that can be empty.

     
	 conf.d/hello.yaml
	     instances: [{}]
		 

Next we are going to deploy the code in *checks.d *.

```python
# the following try/except block will make the custom check compatible with any Agent version
try:
    # first, try to import the base class from old versions of the Agent...
	from checks import AgentCheck
except ImportError:
    # ...if the above failed, the check is running in Agent version 6 or later
    from datadog_checks.checks import AgentCheck

# content of the special variable __version__ will be shown in the Agent status page
__version__ = "1.0.1"


class HelloCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', 1, tags=['data:dawg'])


```

### Modifying interval and data
To modify the interval of the checks, you can simply modify the conf.d/hello.yaml with the following code:

    init_config:
    
    instances:
      - min_collection_interval: 45
	  

To make the ouput of the check a little more interesting, we modify the code to generate a random number.

    # the following try/except block will make the custom check compatible with any Agent version
    import random
    
    try:
        # first, try to import the base class from old versions of the Agent...
        from checks import AgentCheck
    except ImportError:
        # ...if the above failed, the check is running in Agent version 6 or later
    from datadog_checks.checks import AgentCheck
    
    # content of the special variable __version__ will be shown in the Agent status page
    __version__ = "1.0.2"
    
    
    class HelloCheck(AgentCheck):
        def check(self, instance):
            self.gauge('my_metric', random.randint(1,1000), tags=['data:dawg'])
    
    

