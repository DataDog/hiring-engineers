
## *Amrith's answers to the exercise*

*Please find below answers to the excercise*


# Setting up the environment

## Installing Vagrant and VirtualBox on a local machine

### Install Vagrant:


Download the proper package for your operating system and architecture from [Vagrant Download page](https://www.vagrantup.com/downloads). Additional instructions on installation if needed are available [here](https://www.vagrantup.com/docs/installation)


### Install VirtualBox:

VirtualBox is a free and open source virtualisation software. We will use VirtualBox to run Ubuntu 18.04 The latest version is available in the [VirtualBox Download page](https://www.virtualbox.org/wiki/Downloads)


## Configuring Vagrant and verifying the OS

The following command initialises Vagrant on your local machine and downloads the image of Ubuntu 18.04 also known as Bionic Beaver.
````
vagrant init hashicorp/bionic64
````


![Init vagrant](screenshots/1.1-init-vagrant.png)

### Launching the server

The following command would bring the server up. If this is the first time the command is run and if Vagrant cannot find the image it will attempt to find and install the OS on VirtualBox

````
vagrant up
````
![vagrant up](screenshots/1.2-bringing-vagrant-up.png)

### Connecting to the server

Once Vagrant has brought up the server you will need to connect to it by performing a Vagrant ssh. This simulates connecting to the server through Secure Socket Shell (SSH). The following command connects to the Ubuntu Bionic server that we just spun up:
````
vagrant ssh
````
![vagrant ssh](screenshots/1.3.vagrant-ssh-ubuntu.png)

### Verify the OS version by running the command
````
lsb_release -a
````
![verify-os](screenshots/1.4.verify-os-version.png)

### Change the hostname for better identification

The below screenshot confirms that the hostname has been changed.

![hostname](screenshots/1.5.change-hostname-vagrant.png)

### Create a new Datadog account.

* Use your browser and open https://www.datadoghq.com/ and create a new account
* After siging up, your new Datadog home page may appear like below:

![new-dd-account](screenshots/1.6.new.dd.account.png)

## Installing Datadog agent

### Agent Installation Instructions

Agent installations instructions are available in the following path:

Integrations ⇨ Agent ⇨ Ubuntu(choose based on the OS)  ⇨ Copy the instruction that matches the most suitable option. In our case, we will be performing a new installation.

The command would look similar to below.
Note: The API key will be associated to your account only and should not be shared.

````
DD_AGENT_MAJOR_VERSION=7 DD_API_KEY=███████████████████████████ DD_SITE="datadoghq.com" bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_script.sh)"
````

Copy and paste the command on the server and run it. You may have to enter your password if prompted.

### Verify the installation

The installation can be verified by checking the status of the Datadog service.

### Checking the status of the agent

````
sudo systemctl status datadog-agent
````
![datadog-agent-status](screenshots/1.7.datadog-agent-status.png)

Please note the following commands which will be used to stop, start or restart the agent.

The agents will need to be restarted whenever there is a change to the any configuration.

### Stopping the agent
````
sudo systemctl stop datadog-agent
````

### Starting the agent
````
sudo systemctl start datadog-agent
````

### Restarting the agent
````
sudo systemctl restart datadog-agent
````

## Confirming that the agent is reporting metrics:

Login to your Datadog account to verify that the agent is reporting metrics. This can be verified by any of the following options:

* Datadog event stream would indicate that the agent on the new host has been started. Datadog  ⇨ Events
![datadog-event](screenshots/1.8.datadoghq-event-stream.png)
* Datadog Infrastructure section would start reporting a new host. Datadog  ⇨ Infrastructure
![datadog-infra-host](screenshots/1.9.datadoghq-infra-host.png)
* Checking the home page as well where you would notice a new host has started to report
* Further, the default dashboard would start reporting metrics in graphs as well.

# Collecting Metrics

## Updating tags

Change the tags in the datadog_conf.yaml as per your requirement.

The datadog_conf.yaml is located in /etc/datadog for Ubuntu 18.04. The file location may vary depending on the platform. You can refer [this page](https://docs.datadoghq.com/agent/guide/agent-configuration-files/?tab=agentv6v7) for additional details
````
~
tags:
   - env:test
   - app:vagrant
   - owner:amrith
~
````


Verify that the tags are reporting in Datadog by navigating to
Infrastructure  ⇨ Host maps

![hostmap](screenshots/2.2.datadoghq-infra-hostmap-tags.png)

## Installing a Database

We will be installing MySQL as an example. Follow the below instructions to install MySQL on Ubuntu

Updating the OS
````
sudo apt update
````

Installing MySQL
````
sudo apt install mysql-server
````
![installing-mysql](screenshots/2.3.installing-mysql.png)

Enter the following commands and accept the defaults to configure the security settings of MySQL:
````
sudo mysql_secure_installation
````
![mysql-secure-installation](screenshots/2.4.mysql-secure-installation.png)

Verify that the installation is successful by entering the mysql command followed by performing a SELECT statement:
````
$ sudo mysql

mysql> SELECT user,authentication_strig,plugin,host FROM mysql.user;

````
If you see a table listed as shown in the screenshot below, you can be assured that the installation was successful.
![](screenshots/2.5.mysql-check-user.png)

### Create a datadog user and providing privilges to collect metrics

Enter the following command in mysql to create a new user named 'datadog' with a password
````
CREATE user 'datadog'@'localhost' IDENTIFIED BY '████████';
````

Verify that the user was created by running the previously run SELECT user command.
![verify-mysql-datadog-user](screenshots/2.6.mysql-verify-datadog-user.png)

The datadog agent needs a few privileges to collect metrics. Run the following commands to grant limited privileges only
````
mysql> GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'localhost' WITH MAX_USER_CONNECTIONS 5;
Query OK, 0 rows affected, 1 warning (0.01 sec)

mysql>
mysql>
mysql> GRANT PROCESS ON *.* TO 'datadog'@'localhost';
Query OK, 0 rows affected (0.00 sec)

mysql>
mysql>
mysql> ALTER USER 'datadog'@'localhost' WITH MAX_USER_CONNECTIONS 5;
Query OK, 0 rows affected (0.00 sec)

````
Verify that metrics can be collected from the performance_schema database and grant additional privilege by running the GRANT command

````
mysql>
mysql> show databases like 'performance_schema';
+-------------------------------+
| Database (performance_schema) |
+-------------------------------+
| performance_schema            |
+-------------------------------+
1 row in set (0.00 sec)

mysql>
mysql>


mysql> GRANT SELECT ON performance_schema.* TO 'datadog'@'localhost';
Query OK, 0 rows affected (0.02 sec)

````

### Configuration to collect MySQL metrics

Edit the mysql.d/conf.yaml file, in the conf.d/ folder at the root of your Agent’s configuration directory to start collecting your MySQL metrics and logs.

MySQL configuration for Datadog in our example is located in the following directory:
````
/etc/datadog-agent/conf.d/mysql.d
````
Modify the config file at these sections with the datadog username, password and other settings as shown below:
````
~
instances:
  - host: localhost
    user: datadog
    pass: ███████
    port: 3306
~
.
~

    options:
      replication: false
      galera_cluster: true
      extra_status_metrics: true
      extra_innodb_metrics: true
      extra_performance_metrics: true
      schema_size_metrics: false
      disable_innodb_metrics: false
````
Note: localhost may be replaced with 127.0.0.1 if needed. Also if you need to extract the database performance from a remote DB server

Additional details can be refered from the [MySQL Integration page](https://docs.datadoghq.com/integrations/mysql/?tab=host)

Save the conf.yaml in the mysql.d directory and restart the datadog agent.

### Verifying the integration check

Confirm that the mysql check is running correctly by running this specific agent subcommand:
````
sudo datadog-agent check mysql
````
Notice there are no warnings when you run this command:

![MySQL-agent-check](screenshots/2.8.datadog-agent-check-mysql-output.png)


### Verifying the metrics in Datadog
Navigate to Datadog  ⇨ Dashboards  ⇨ All Dashboards  ⇨ MySQL - Overview which is a preset dashboard for MySQL. Verify if you can see MySQL metrics as shown below:
![mysql-dashboard](screenshots/2.7.mysql-verify-metrics.png)
