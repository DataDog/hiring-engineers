******************************************************************************************************************************************
******************************************************************************************************************************************
I have copied/pasted my word document into the form below. As I was instructed to treat this as a "client-facing deliverable", I have created a PDF version of my deliverable available here: http://brendan-roche.com/DataDog%20Setup%20Documentation.pdf

I hope you will utilize the PDF to view my delivery as opposed to the answers below due to formatting.

Thank you for the opportunity and I look forward to the next steps.  

- Brendan Roche | bmroche@gmail.com | (720) 295-1745
************************************************************************************************************************************************************************************************************************************************************************************

Introduction
The purpose of this document is to walk through an introduction to DataDog and how to configure the agent on Ubuntu.  This document will provide instructions, examples, and screenshots of the process to guide you through the initial setup.  Please refer to this document and DataDogHq.com for additional information.

Ubuntu Virtual Instance Installation
First, we will need to install a virtual server operating system. For this example, we will use Ubuntu.  

Install Vagrant OS X Package via the installer: vagrantup.com/docs/installation. When trying to boot Vagrant for Ubuntu install, it requires dependencies from a VM provider.

Then install the virtual provider of your choice. We are using Oracle VM VirtualBox for this example, but other acceptable providers are VMware, Hyper-V or Docker.

After the VirtualBox install is complete, run the vagrant-up command to spin up virtualbox(v1.1.0) running Ubuntu 12.04 LTS 64-bit.  The setup process will require a few confirmations before finishing.

DataDog Agent Installation
The next step is to install the DataDog Agent on our newly provisioned Linux virtual server.

Bonus Question Answer: An Agent is an aggregator of data on the local host – which could be a local machine, or could be a cloud hosted server – and reports it back to DataDog or other collection service to make the information useful.  

First, we will SSH into our newly created Linux box by using the $ vagrant ssh command. When we connect successfully, we will see our OS version information.

The following terminal commands can be used to start, stop and log into our virtual server.
•	vagrant up:  This starts the VM. 
•	vagrant halt: Forcefully shuts down the VM.
•	vagrant suspend: Suspends the VM.
•	vagrant ssh: This logs you into your VM.

Now that we have SSH access, we will install our DataDog Agent. From the DataDog Agent selection page, https://app.DataDoghq.com/signup/agent, we can select the operating system on which we want to install the Agent. For this example, we will select Ubuntu.

Next, we will paste the curl command provided by the DataDog after selecting the Agent for your operating system.

Copy the entire string from the “easy one-step install”.  

Note: If curl is not installed at this point, we can install it by using the below command. This must be done before installing the DataDog Agent.
sudo apt-get install curl

Follow any additional prompts through the curl installation, then proceed to paste the copied “easy one-step install” command into the terminal window.

Record the location of the API Agent configuration:

Now the DataDog agent should be installed and running. Congratulations!

Note: If you do not see the success message, “Your Agent is running and functioning properly,” or you get an error message, please reach out to support@DataDoghq.com with the error message received.

Useful Commands
Stop the DataDog Agent
•	sudo /etc/init.d/DataDog-agent stop 
Start the DataDog Agent
•	sudo /etc/init.d/DataDog-agent stop
Restart the DataDog Agent
•	sudo /etc/init.d/DataDog-agent restart
View all information about the DataDog Agent
•	sudo /etc/init.d/DataDog-agent info

Custom Tags
Next, we will add custom tags to our configuration file, which can be found here: /etc/dd-agent/DataDog.conf. This file can be opened in any text editor; for this example, we will use the Linux built-in text editor: VI. 

We will have to open this file as an admin or superuser using the sudo command.
sudo vi /etc/dd-agent/DataDog.conf 

Using VI keyboard commands, navigate to the “host’s tags” section and remove the comment (#) out of the tags line and add the desired tags. Tags can be a single value, although we have had the most success with a key:value pair. Below are some example tags, using the key:value pair notation.

From within the DataDog Agent, we can slice and dice based on these tags to get more meaningful metrics. Below is an example Host Map with tags displayed.

Application Setup
The last step in our installation is to set up and connect to our database. For this example, we will use MySQL.

Install MySQL by running the installation command.
sudo apt-get install MySQL-server

Walk through the setup process and, although not mandatory, we highly recommend to set a password for the MySQL admin account.

Log into MySQL and create a database, following the steps below.
1.	MySQL –u root –p
2.	enter password
3.	CREATE DATABASE databaseNamehere;

Install DataDog Integration
Next, we will install the MySQL DataDog integration for this package. The Integrations link is located on the left navigation panel of the DataDog homepage. From the Available Integrations list, click on the icon for MySQL. Now we have 3 tabs: Overview, Configuration, and Metrics. Click on the Configuration tab to display installation instructions.

Internal DataDog Note: One thing I ran into with the canned installation instructions is that they assume the root user has not set a password, with is not a good security practice.  As I set the password for my root user, I had to append –p to all of the commands on the “configuration” tab in order to prompt for password.

Now that we have set up and verified the DataDog user on the MySQL database, we are ready to move on to the next step.

Configure the Agent to Connect to MySQL
Locate the /etc/dd-agent/conf.d/ folder and look for the MySQL.yaml.  

Note: This might be labeled as MySQL.yaml.example, which you can modify per the integration instructions and rename as MySQL.yaml, or start with a new MySQL.yaml using the following command.
sudo /etc/dd-agent/conf.d/MySQL.yaml

Once this is complete, save the VI file, exit VI and restart the DataDog Agent using the Agent restart command.
sudo /etc/init.d/DataDog-agent restart

We will now see data being collected by our MySQL instance on the DataDog host page.

Note: You can also validate it is collecting metrics via the DataDog info command.
sudo /etc/init.d/DataDog-agent info

Custom DataDog Agent Check
Locate the conf.d and checks.d folders using the info command. Next, create the .py and .yaml files, with matching names and our desired check logic. In this example, we are using a random number generator to set the metric test.support.random every time the check runs. By default the collector runs every 15-20 seconds.

After modifying both files, restart the DataDog Agent.
sudo /etc/init.d/DataDog-agent restart

Validate that the new metric is working by locating it in Metrics Explorer from the Metrics menu on the navigation bar.

DataDog Dashboards
View and Clone
Now that our installation is reporting metrics, we can go into the MySQL dashboard to view our data. Clone the dashboard by clicking on the gear icon in the top right and selecting Clone Dashboard.

The cloned dashboard “MySQL Clone” used for this example is located at https://app.datadoghq.com/dash/256412/mysql-clone.

Add Custom Metrics
Now we will add a new MySQL metric (MySQL.net.max_connections_available) and our customer Agent check metric (test.support.random), both sliced by operating system.  

Click on the pencil on the appropriate TimeBoard or Screen Board.

Once we have made the appropriate changes, click Save and view the new TimeBoard or Screen Board.

Bonus Question: In DataDog’s dashboards, there is the concept of a TimeBoard and a Screen Board.  

TimeBoards are always scoped to the same time and always appear in a grid-like fashion. 
Screen Boards are flexible, customizable and are great for getting a high-level look into a system. They are created with drag-and-drop widgets, which can each have a different time frame.

Data Alerts
Now we can visualize our data, identify issues and easily collaborate with the team. In this example, we set up a marker at 0.9, so there is a red line showing where 0.9 is on the graph. This is to highlight any potentially problematic values above 0.9.

Manual Alert Observation
To snapshot an issue, click on the camera icon and indicate the issue by putting a rectangle around the problematic area of the graph. Using simple DataDog markup language, we can easily share the information with our team or a specific contact.  

We shared the snapshot with Brendan Roche via the comment @bmroche@gmail.com notation to illustrate how collaborative the DataDog platform is. Users can share information and reply inline around the specific incident. See the below example of the offending (>.9) transactions, and the conversation that has been started to discuss the issue.

Send Alerts via Monitor
Although it is useful to see the data on the dashboard to determine if any transactions have gone above 0.9, we want to be notified immediately if specific criteria are met. With DataDog’s alerts we can set the metrics, thresholds and durations for which we want notifications, and have the appropriate parties contacted immediately without human intervention.

Set up an alert to monitor the test.support.random metric and alert the interested party – which could be an entire team, specific stakeholders, etc. – when it has gone above 0.9 at least once during the last 5 minutes.

To do this, click on the gear icon and then Create Monitor.

Set the criteria for this alert.

Note: To reduce redundancy when creating alerts, set up a Multi Alert, separated by host, for times of infrastructure scaling up or new servers provisioned.


Craft the subject and body of the notification, being sure to include pertinent information to quickly identify the issue, which servers are having the issue and a link to the full dashboard.

Also set the notification group or people in step four on this page.

Receiving Alerts
Below is an example of the automated email from our “test.random is above .9” alert.

Setting Downtime
We can also set downtime for times that we do not want to be notified of a specific alert. Within the Manage Monitors tab of DataDog, click on Manage Downtime, then click on Schedule Downtime to set up a new alert silence rule. From here, we can set the alerts to silence, the scope, the schedule (recurring or non-recurring), the message and the appropriate parties to notify of the downtime.

Bonus Question: Since this monitor is going to alert pretty often, you don't want to be alerted when you are out of the office. Set up a scheduled downtime for this monitor that silences it from 7pm to 9am daily. Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

Bonus Answer: Below is an example of a recurring rule for the 0.9 monitor that will not alert from 7:00 pm to 9:00 pm daily.

 
The scheduled downtime will not send alerts for the configured metrics during the interval specified. Ensure that the appropriate parties understand when the downtime takes effect. In the automated email below, the administrator is notified of the downtime.

Conclusion

We hope this DataDog document for Ubuntu/MySQL was informative and pertinent and helps to keep critical servers and processes online.  Please refer to further documentation at http://docs.datadoghq.com/ or visit our help portal for more information at https://help.datadoghq.com/hc/en-us.
