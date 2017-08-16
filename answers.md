

# Datadog Support Engineer - At Home Task
</br>
</br>

## Table of Contents

+ [Introduction](#introduction)
+ [Setting Up Your Application Stack](#setting-up-your-application-stack)
  - [Vagrant Ubuntu and VirtualBox Installation](#vagrant-ubuntu-and-virtualbox-installation)
  - [MYSQL Installation](#mysql-installation)
+ [Data Collection](#data-collection)
  - [Datadog Sign Up and Vagrant Integration](#datadog-sign-up-and-vagrant-integration)</br>
&ensp;&ensp;Bonus Question: [What is an Agent?](#what-is-an-agent)
  - [Host Tags](#host-tags)
  - [MySQL Integration](#mysql-integration)
  - [Custom Agent Check](#custom-agent-check)
  - [Database Integration Screenboard](#database-integration-screenboard)
+ [Visualizing Your Data](#visualizing-your-data)</br>
&ensp;&ensp;Bonus Question: [What is the Difference Between Timeboards and Screenboards?](#timeboard-and-screenboard)
  - [Dashboard Cloning](#dashboard-cloning)
  - [Custom Agent Check Timeboard](#custom-agent-check-timeboard)
+ [Alerting Your Data](#alerting-your-data)
  - [Dashboard Snapshot and Notification](#dashboard-snapshot-and-notification)
  - [Events Monitoring](#events-monitoring)
  - [Monitoring Downtime](#monitoring-downtime)
 
</br>
</br>
</br>
</br>

# Introduction

With Datadog entering the IT industry in Australia, it is essential to hire competent and passionate employees to be the foundation of the company as it builds it's local client base. This activity is part of the hiring process and is intended to be done at home.

This activity will primarily focus on walking you through the four aspects below:
  1. Application Suite Set-up
  2. Datadog Integration
  3. Dashboard Set-ups
  4. Monitoring and Alerts


# Setting Up Your Application Stack

To start with, you need to set-up the application stack in your Mac OS X. It will consist of a Vagrant-Ubuntu operating system hosted on a VirtualBox VM with MySQL as the database server.

## 	Vagrant Ubuntu and VirtualBox Installation

  1. To download the Vagrant installer, go to the [vagrant downloads site](https://www.vagrantup.com/downloads.html) and choose the installer for Mac OS X.
  2. Open the downloaded DMG file and double-click on vagrant.pkg.</br>
&ensp;&ensp;<img width="310" height="218" src="https://user-images.githubusercontent.com/30991348/29323613-ca91b130-8224-11e7-8ce1-32bf85ce4092.png">&ensp;
  3. The steps are straightforward, the only parameter that you may want to change is in the Destination Select step which is sometimes skipped while clicking next. When that happens, click on the Change Install Location during the Installation Type step:</br>
&ensp;&ensp;<img width="310" height="218" src="https://user-images.githubusercontent.com/30991348/29323032-009acfd4-8223-11e7-8ba1-9375f5cf3594.png">&ensp;
  4. You would see the message below if the installation is a success. If you encounter any issues, please check the amount of diskspace available on your computer or if your operating system’s compatibility.</br>
&ensp;&ensp;<img width="310" height="218" src="https://user-images.githubusercontent.com/30991348/29323613-ca91b130-8224-11e7-8ce1-32bf85ce4092.png">&ensp;
  5. We will also be using VirtualBox for VM provisioning. To install, go to https://www.virtualbox.org/wiki/Downloads  and click on the OS X hosts option.
  6. The installer works exactly the same as with Vagrant. Follow steps 2-3.
  7. You would see the message below once you installation successfully completes.</br>
&ensp;&ensp;<img width="310" height="218" src="https://user-images.githubusercontent.com/30991348/29323033-009e9c18-8223-11e7-93cf-c6f839236aa3.png">&ensp;
 The commands below are simple vagrants that you may use:
 ```
 vagrant up      #start/create a Vagrant instance
 vagrant ssh     #connect to Vagrant instance
 vagrant halt    #shutdown the Vagrant instance
 vagrant destroy #terminate/delete the Vagrant instance
 ```


## MYSQL Installation
&ensp;&ensp;Follow the steps below to install MySQL on the Vagrant OS.
  1. Open your MAC Terminal and create/start a vagrant virtual machine by executing the command:<br />
&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;`vagrant up`
  2. Your Vagrant VM is now up and running. Connect to it by executing the command:<br />
&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;`vagrant ssh`
  3. Before MySQL installation, make sure the system is updated using the commands:<br />
&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;`sudo apt-get update`<br />
&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;`sudo apt-get upgrade` <--_NOTE:this will take a few minutes to download and install_
  4. To install MySQL, run the command:<br />
&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;`sudo apt-get install mysql-server`
  5. The MySQL server should be automatically up and running after the installation. To verify, check the mysql background process and try logging in:<br />
&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;`ps –ef | grep mysql`<br />
&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;`mysql –u root -p` <--_NOTE:you will be prompted to use the MySQL root credentials that you created during its installation_
  ![mysql_hc](https://user-images.githubusercontent.com/30991348/29323014-ffb2cc20-8222-11e7-9455-3599748cfebc.png)


# Data Collection

Now that you have set-up your application suite, you can now proceed with your system's integration with Datadog. 

### Datadog Sign Up and Vagrant Integration
  1. Go to [datadog homepage](https://www.datadoghq.com) and click on __GET STARTED FOR FREE__.
  2. Fill-in the form that will pop-up with your details and __Sign up__:<br />
  ![signup_details](https://user-images.githubusercontent.com/30991348/29323021-0006497c-8223-11e7-8249-8b80d08cf9e9.png)
  3. In the next step, you can answer the surveys about the softwares and services that you are currently using. Answer the survey and click on __Next__.
  4. Lastly, you will be required to install a datadog agent in your host server. Select Ubuntu from the left side menu to get the instructions:
  ![agent_setup1](https://user-images.githubusercontent.com/30991348/29322992-fe90d684-8222-11e7-97fa-6af4662799fa.png)
  5. Install curl before executing the script from the Datadog instructions by running the command below in the vagrant terminal:<br />
&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;`sudo apt-get install curl`
  6. Copy the datadog installation command and run it in the terminal:
```
DD_API_KEY=c08db2089f1d3ea2ee9f6238c2e87d12 bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/dd-agent/master/packaging/datadog-agent/source/install_agent.sh)" DD_INSTALL_ONLY=true
```
_NOTE:Replace the DD_API_KEY with the key that will be generated for your account_
  Running this command would automatically start the datadog agent data collection for the Vagrant server.
  7. After a few seconds, Datadog will receive the data from your host and you can now click on the Finish button in the lower right to complete the sign-up.<br />
  ![agent_setup2](https://user-images.githubusercontent.com/30991348/29322996-fef816fa-8222-11e7-8f50-71c4e0397c47.png)
<br />

Below are basic datadog commands that you can enter in the terminal:
```
sudo /etc/init.d/datadog-agent start 	#start the datadog agent processes
sudo /etc/init.d/datadog-agent stop 	#stop the datadog agent processes
sudo /etc/init.d/datadog-agent restart 	#restart the datadog agent processes
sudo /etc/init.d/datadog-agent info 	#displays information on the data being collected by the agent
sudo /etc/init.d/datadog-agent info -v 	#displays a more detailed(verbose) information on the agent
```

## What is an Agent?

An agent is a program installed in the host server as part of a parent program to remotely connect and interact with the host. Datadog’s agent in the server will collect data and send it to the Datadog application for monitoring.

## Host Tags
This exercise will show you how to put tags on your host/s. It is useful to distinguish your hosts from each other especially when you are using multiple servers.
	
### Via Config file
  1. From your Vagrant terminal, go to the datadog configuration directory via command:</br>
	&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;`cd /etc/dd-agent`
  2. Open and edit the configuration file - datadog.conf</br>
	&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;`sudo vi datadog.conf`
  3. On line 30-31, you will find a comment and a template for adding host tags:</br>
	&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;`30 # Set the host's tags (optional)`</br>
	&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;`31 # tags: mytag, env:prod, role:database`
  4. Copy the sample line excluding the comment and update it with your tag, update and save the file.</br>
  ![config_tag1](https://user-images.githubusercontent.com/30991348/29322997-fef8c9a6-8222-11e7-8c19-e09bd5f8571c.png)
  5. Restart the datadog agent via command:</br>
	&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;`sudo /etc/init.d/datadog-agent restart`
  6. You can now find the tags in the UI:</br>
&ensp;&ensp;&ensp;&ensp;__Host Map__</br>
  ![hostmap_config](https://user-images.githubusercontent.com/30991348/29323004-ff3ec8ca-8222-11e7-92ca-c6129c3a024d.png)

### Via Website
  1. From the left side menu, mouse over on __Infrastructure__ and click on __Infrastructure List__.
  2. On the upper right corner, click on __Update Host Tags__.</br>
  ![ui_tag1](https://user-images.githubusercontent.com/30991348/29323029-00661d48-8223-11e7-8af5-613c5b0a7a84.png)
  3. Click on __Edit Tags__ and enter.</br>
  ![ui_tag2](https://user-images.githubusercontent.com/30991348/29323030-006e955e-8223-11e7-8228-a986af0ca3c1.png)</br>
  &ensp;&ensp;&ensp;&ensp;__Host Map__</br>
  ![hostmap_ui](https://user-images.githubusercontent.com/30991348/29323006-ff5a0bda-8222-11e7-826d-b3d5571e91ee.png)</br>
 
## MySQL Integration
Next, integrate your MySQL to send your database metrics to Datadog. Replace the __[datadog db password]__ with your own from the commands below whenever applicable.
  1. On the left side menu of the Datadog UI, mouse over on __Integrations__ and click on __Integrations__.
  2. Type in MySQL in the search box and click on __Available__.</br>
  ![mysql_available](https://user-images.githubusercontent.com/30991348/29323011-ff934d8c-8222-11e7-993a-5031a15bb7dd.png)
  3. Click on __Generate Password__ for convenience. This will update the command lines with the same password for your convenience.</br>
  ![mysql_genpassword](https://user-images.githubusercontent.com/30991348/29323013-ffac7366-8222-11e7-9851-01fcab8c9b7a.png)
  4. Copy the commands and execute in the vagrant terminal where you have installed the MySQL:<br />
```
sudo mysql -e "CREATE USER 'datadog'@'localhost' IDENTIFIED BY '[datadog db password]';"
sudo mysql -e "GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'localhost' WITH MAX_USER_CONNECTIONS 5;"
sudo mysql -e "GRANT PROCESS ON *.* TO 'datadog'@'localhost';"
sudo mysql -e "GRANT SELECT ON performance_schema.* TO 'datadog'@'localhost';"
```
_NOTE: You may encounter the error “ERROR 1045 (28000): Access denied for user 'root'@'localhost' (using password: NO)”, when you do, append the command lines with –u root –p. You will be prompted with the root password.<br />
Ex. `sudo mysql -e "CREATE USER 'datadog'@'localhost' IDENTIFIED BY '[datadog password]';" –u root –p`_<br /></br>
  5. Verify the changes using the commands:
  ```
  mysql -u datadog --password=<datadog db password> -e "show status" | \
  grep Uptime && echo -e "\033[0;32mMySQL user - OK\033[0m" || \
  echo -e "\033[0;31mCannot connect to MySQL\033[0m"
  mysql -u datadog --password=[datadog db password] -e "show slave status" && \
  echo -e "\033[0;32mMySQL grant - OK\033[0m" || \
  echo -e "\033[0;31mMissing REPLICATION CLIENT grant\033[0m"
  ```
  Result:<br />
  ![mysql_verif1](https://user-images.githubusercontent.com/30991348/29323015-ffb6d5fe-8222-11e7-8eab-af9a70d04f22.png)<br />
  ```
  mysql -u datadog --password=[datadog db password] -e "SELECT * FROM performance_schema.threads" && \
  echo -e "\033[0;32mMySQL SELECT grant - OK\033[0m" || \
  echo -e "\033[0;31mMissing SELECT grant\033[0m"
  mysql -u datadog --password=[datadog db password] -e "SELECT * FROM INFORMATION_SCHEMA.PROCESSLIST" && \
  echo -e "\033[0;32mMySQL PROCESS grant - OK\033[0m" || \
  echo -e "\033[0;31mMissing PROCESS grant\033[0m"
  ```
  Result:<br />
  ![mysql_verif2](https://user-images.githubusercontent.com/30991348/29323016-ffcd7e30-8222-11e7-9b88-6eb83193155b.png)<br />
 
  6. Now we just have to create the MySQL configuration file for the Agent.  Go to directory __/etc/dd-agent/conf.d__ and create a file named mysql.yaml.
  ```
  cd /etc/dd-agent/conf.d
  sudo vi mysql.yaml
  ```
  7. Copy the configuration from the UI and paste it in mysql.yaml.
  ```
  init_config:

  instances:
  - server: localhost
    user: datadog
    pass: [datadog db password]
    tags:
        - optional_tag1
        - optional_tag2
    options:
        replication: 0
        galera_cluster: 1
   ```
 
  8. Save the file and restart the datadog agent:<br />
   `sudo /etc/init.d/datadog-agent restart`
  9. Execute the info command below:<br />
   `sudo /etc/init.d/datadog-agent info`

You should be able to see this under Checks:<br />
  ![mysql_checks](https://user-images.githubusercontent.com/30991348/29323012-ffa7684e-8222-11e7-874a-7172a2cd2623.png)<br />
 
## Custom Agent Check

To create a custom check, you need to create two components:
  - Integration Config file - a config file in __/etc/dd-agent/conf.d__ directory with a .yaml extension.
  - Custom Check Script     – a python script in the __/etc/dd-agent/checks.d__ directory similarly named as the config file but with a .py extension. _Ex. myscript.yaml, myscript.py_
  
 Follow the steps below to create a custome check that generates a random number(from 0-1) metric and send it to Datadog named as "test.random.support".
  1. Create a file named cc_random.yaml into the __conf.d__ directory and type in:
  ```
  init_config:

  instances:
    [{}]
  ```
  2. Create a file named cc_random.py into the __checks.d__ directory and type in:
  ```
  import random

  from checks import AgentCheck

  class HelloCheck(AgentCheck):
    def check(self, instance):
        self.gauge('test.support.random', random.random())
  ```
  <br />
  ![cc_random_files](https://user-images.githubusercontent.com/30991348/29322995-fef783c0-8222-11e7-9bcd-49b3b9485d0a.png)
  3. Restart the datadog agent:
   `sudo /etc/init.d/datadog-agent restart`
  4. execute the Datadog info command and you should see that the custom check is now included under Checks:
   `sudo /etc/init.d/datadog-agent info`<br />
  ![cc_random_hc](https://user-images.githubusercontent.com/30991348/29322998-fefcc90c-8222-11e7-9ccb-96dda1db77a2.png)<br />
 
## Visualizing your Data
  
### Timeboard and Screenboard
In Datadog, you can create two kinds of dashboards - the Timeboard and the Screenboard. The difference of these boards are their main purpose.
  * The Timeboard is primarily for internal use like investigations and alerts. You can set-up monitoring based from these graphs. You can also share snapshots of a graph to internal teams via annotations. 
  * The Screenboard’s primary purpose is for public viewing. It has features solely for making viewing aesthetically pleasing and intuitive such as including widgets, images and Hostmap on the screen.

Both of these type of dashboard can be created by:
  1. From the left side menu of the Datadog UI, mouse over on __Dasboards__ and click on __New Dashboard__.
  2. Populate the dashboard name, pick the type of dashboard you need and click on __New Timeboard/New Screenboard__.<br />
  ![timeboard_screenboard](https://user-images.githubusercontent.com/30991348/29323028-00646674-8223-11e7-942b-1a1b86ef2eb4.png)<br />
   
### Custom Agent Check Timeboard
  1. After choosing timeboard, you will be prompted to set-up your newly created dashboard.
  2. You can choose any of the objects available but for now, drag __Time Series__ into the blank space on the lower part of the page:<br />
  ![timeboard_1](https://user-images.githubusercontent.com/30991348/29323025-002e791a-8223-11e7-9903-b4aa3dc2cc9e.png)
  3. the Graph Editor box will pop-up to configure the graph:
     1. Set visualization to __Timeseries__ and choose the __test.support.random metric__.<br />
     ![timeboard_2](https://user-images.githubusercontent.com/30991348/29323026-003d76a4-8223-11e7-802c-c17287037621.png)
     2. Set the graph title then click on Save and Finish Editing. Your graph will look like this:<br />
     ![timeboard_3](https://user-images.githubusercontent.com/30991348/29323027-005acfce-8223-11e7-8f11-dfc6baec0c47.png)<br />

### Database Integration Screenboard
  1. After choosing screenboard, you will be prompted to set-up your newly created dashboard.
  2. You can choose any of the objects available but for now, drag __Graph__ into the blank space on the lower part of the page.
  3. the __Graph Editor__ box will pop-up to configure the graph:
     1. Set visualization to __Time Series__.
     2. Choose the metrics from MySQL and also the test.support.random metric. You can also click on __Add Metric__ to include more.
 
     3. Set the display preferences and Widget Title and click Done.<br />
    ![screenboard_1](https://user-images.githubusercontent.com/30991348/29323018-ffea6662-8222-11e7-97a8-6fa751207ca3.png)
     4. Click on __Save Changes__ and you now have your database and custom metric screenboard:<br />
   ![screenboard_2](https://user-images.githubusercontent.com/30991348/29323020-fff49d26-8222-11e7-9a47-22d919ec4ca5.png)<br />
  
### Dashboard Cloning
You can also create copies of your dashboard by cloning it. To create a clone you just need to:
  1. Click on the gear icon on the upper right of the dashboard page and choose __Clone Dashboard__:<br />
  ![dash_clone1](https://user-images.githubusercontent.com/30991348/29322994-fef0ef74-8222-11e7-978d-73e3ae68cddb.png)
  2. A pop-up box will appear so you can set the name of the dashboard clone. Click on __Clone__.
  3. A new dashboard patterned after your existing dashboard is now created:<br />
  ![dash_clone2](https://user-images.githubusercontent.com/30991348/29322993-fec99f0a-8222-11e7-91cc-53507b979e9e.png)
 
## Alerting Your Data

### Dashboard Snapshot and Notification
You can send snapshots with annotations using the timeboard graphs.
  1. Hover you mouse over the graph and a camera icon will appear on the upper right corner of the graph. Click on this icon:<br />
  ![snapshot_1](https://user-images.githubusercontent.com/30991348/29323022-00203c1a-8223-11e7-88cc-39682effb03d.png)
  2. The mouse cursor will be changed to a pencil and you can use this to draw a box and emphasize certain areas in the graph.
  3. You can also type in your comment in the dialog box below and send an email via annotation:<br />

  ![snapshot_2](https://user-images.githubusercontent.com/30991348/29323023-00270324-8223-11e7-9563-2bcaf0852f5e.png)<br />
			
  ![snapshot_3](https://user-images.githubusercontent.com/30991348/29323024-0027ae6e-8223-11e7-8b7e-c692cd8fd213.png)<br />


### Events Monitoring
Setting up a Monitor for the Test.Support.Random Metric
  1. On the left side menu of the Datadog UI, mouse over on Monitors and select __New Monitor__.<br />
  ![monitor_1](https://user-images.githubusercontent.com/30991348/29323034-00a705ce-8223-11e7-9461-8faaed7052ae.png)
  2. Select __Metric__ as the __Monitor type__.
  3. Make sure the detection method is set at __Threshold Alert__ since we want to be alerted when the random number breaches the 0.90 mark.
  4. Next on Define the metric, make sure that you have selected __test.support.random__ from our host(vagrant_system) and select __Multi Alert__ for each host so the alert will be applied to all of your existing and to be created hosts.<br />
  ![monitor_3](https://user-images.githubusercontent.com/30991348/29323008-ff7598d2-8222-11e7-89a8-86fbdfd1d09a.png)
  5. Modify the email subject and body:<br />
  ![monitor_4](https://user-images.githubusercontent.com/30991348/29323010-ff7bff10-8222-11e7-9eac-646a714ffd0f.png)
  6. Finally, set the notifications and permissions and click __Save__.<br /><br />
Email received:<br />
  ![monitor_5](https://user-images.githubusercontent.com/30991348/29323009-ff7ac2d0-8222-11e7-9211-917328222179.png)
<br />

### Monitoring Downtime

You can schedule monitoring downtimes for when you have a planned outage or you just don’t want to receive any alerts during off-business hours.
To set it up, follow the instructions below:

  1. On the left side menu of the Datadog UI, mouse over __Monitors__, click on __Manage Downtime__, then click on __Schedule Downtime__.<br />
  ![downtime_1](https://user-images.githubusercontent.com/30991348/29322999-fefefe48-8222-11e7-9c27-1d722a239c86.png)
  2. Choose a monitor. Choose the random number threshold monitoring:
  3. Configure the schedule as seen below so the monitor will stop at 7pm and resume at 9am on a daily basis:<br />
  ![downtime_2](https://user-images.githubusercontent.com/30991348/29323000-ff261bea-8222-11e7-994d-afa5783372fa.png)
  4. Lastly, add a message to notify your team for the reason for the monitoring outage/downtime.<br />
  ![downtime_3](https://user-images.githubusercontent.com/30991348/29323001-ff34baa6-8222-11e7-8bc5-befca568cc7b.png)
  
&ensp;&ensp;&ensp;&ensp;Your monitoring downtime is now set-up! You'll be able to receive these emails notifications as configured:<br /><br />

Downtime Start:<br />
 ![downtime_start](https://user-images.githubusercontent.com/30991348/29323005-ff3fb820-8222-11e7-9787-7de10a7809ed.png)
  <br />
 Monitoring End:<br />
 ![downtime_end](https://user-images.githubusercontent.com/30991348/29323002-ff35fbbe-8222-11e7-9299-d261565c123d.png)
