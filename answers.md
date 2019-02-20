# ANSWERS

Vagrant allows users to create and destroy virtual machines and transfer the vagrant file to another user who can generate the same environment on which you are working. It helps you transfer development environment from one machine to another.I Installed Vagrant for Windows 64-bit on my laptop. To install Vagrant you need to do two things:  
Step-1. Install virtual machine from this website:
        https://www.virtualbox.org/  
        Once you install virtual box, it would look like this:
   
   ![virtual box installed](https://user-images.githubusercontent.com/47703847/53057366-336f4f80-347d-11e9-90a1-94fabc4bc0da.png)

Step-2. Install Vagrant for Windows 64-bitfrom this website:  
        https://www.vagrantup.com/downloads.html  
After installing vagrant, go to command prompt of desktop and enter following command to check for successful installation:    
vagrant -v

![vagrant has succesfully installed](https://user-images.githubusercontent.com/47703847/53057803-ca88d700-347e-11e9-80bc-25a7a22d3678.png)

Go to https://app.vagrantup.com/boxes/search. You'll see different boxes. I selected ubuntu/trusty64
Go to Command prompt : Write following commands:  
1. vagrant box add ubuntu/trusty64  
2. vagrant init ubuntu/trusty64  
3. vagrant up  
After these commands, the box is installed.  
Now give ssh command : vagrant ssh

Now go to VirtualBox, 

Select the user, type in your password

![virtual box user](https://user-images.githubusercontent.com/47703847/53105189-a7057100-34fe-11e9-8f8a-d2d1443876b4.png)

![vm desktop](https://user-images.githubusercontent.com/47703847/53105201-ac62bb80-34fe-11e9-90fa-789530d0a876.png)

Open Applications>Terminal  
In Terminal, put command:  
sudo -i  
put your password.

![starting terminal on vm](https://user-images.githubusercontent.com/47703847/53058462-218fab80-3481-11e9-80ad-69448ce083e5.png)

SETTING UP dd-agent:

Go to https://app.datadoghq.com/account/settings#agent/ubuntu (You can select any OS that you are working on, I selected ubuntu).Directed to page that looks like this:

![dd-agent install](https://user-images.githubusercontent.com/47703847/53064622-7a1d7380-3496-11e9-971b-e60c97aba95f.png)

I am going to copy "use our easy one-step install" command and paste it on my VM terminal.

![dd-agent install command on vm terminal](https://user-images.githubusercontent.com/47703847/53064848-442cbf00-3497-11e9-9213-07b9ab2bedac.png)

After installing dd-agent, I am going to start this agent as a service by putting following command on my VM Terminal:  

sudo service datadog-agent start

On your terminal open following path: /etc/datadog-agent in which you will find following files:

![datadog-agent path](https://user-images.githubusercontent.com/47703847/53065148-738ffb80-3498-11e9-9bee-5ce849c81ffb.png)

The configuration files and folders for the Agent are located in:  
/etc/datadog-agent/datadog.yaml
Configuration files for Integrations:  
/etc/datadog-agent/conf.d/

## COLLECTING METRICS:

1. Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

Answer:
Input: To Add host tags as input in agent config file that is datadog.yaml file, first put following command to open that file and edit it.  
vi datadog.yaml
The entire file has comments. While reading comments I came across tags in comment section as shown below:

![tags before editing file](https://user-images.githubusercontent.com/47703847/53066032-126a2700-349c-11e9-95d5-432dad241ac7.png)

The format for assigning tags is   
tags: <KEY_1>:<VALUE_1>, <KEY_2>:<VALUE_2> or  
tags:  
    - <KEY_1>:<VALUE_1>  
    - <KEY_2>:<VALUE_2>  
I assigned two host tags as input as shown below. I saved and exited the file by pressing esc and then writing :wq.

![assisgning tags input](https://user-images.githubusercontent.com/47703847/52916135-e8511300-32a9-11e9-85a5-7937532162bb.png)

Output: Now to see the output on my UI, I logged into my datadog account with username and password. Go to Hostmap.

![click on hostmap](https://user-images.githubusercontent.com/47703847/53066340-5873ba80-349d-11e9-9e5f-f6fc468b12bb.png)

![directed to shruti-virtualbox host](https://user-images.githubusercontent.com/47703847/53066399-b0aabc80-349d-11e9-8980-5f661083d98b.png)

Click on shruti-VirtualBox host, The host tags assigned are displayed under Tags > datadog section
I have created User tags to play with datadog UI by clicking on edit tags. Writting tags like:  
instance:comments,instance:follows,instance:likes,name:instademo and saved them.

![host tags and user tags output](https://user-images.githubusercontent.com/47703847/52916383-bab99900-32ac-11e9-8e6f-a722298dbd73.png)

2. Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

Answer: 

Input: Installed mysql on VM terminal by following commands:  
               - sudo apt-get update  
               - sudo apt-get install mysql-server  
               - sudo apt install mysql-workbench (To get the workbench of mysql on my VM Desktop)  
               
Open datadog UI and click on integrations as show below:

![click on integrations](https://user-images.githubusercontent.com/47703847/53067060-8b6b7d80-34a0-11e9-93fe-3b7403e70029.png)

![mysql installed](https://user-images.githubusercontent.com/47703847/52917191-6c10fc80-32b6-11e9-84f1-9b489e548c6a.png)
               
Installed respective datadog integration for that database and configured it by following commands on VM Terminal:  
               - sudo mysql -e "CREATE USER 'datadog'@'localhost' IDENTIFIED BY '<UNIQUE PASSWORD>';"  
               - sudo mysql -e "GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'127.0.0.1' WITH MAX_USER_CONNECTIONS 10;"  
               - sudo mysql -e "GRANT PROCESS ON *.* TO 'datadog'@'127.0.0.1';"  
               - sudo mysql -e "GRANT SELECT ON performance_schema.* TO 'datadog'@'127.0.0.1';"  
  
Output: datadog user included in all mysql users can be checked by putting command:  
SELECT User, Host FROM mysql.user;

![user datadog in mysql](https://user-images.githubusercontent.com/47703847/52916498-323bf800-32ae-11e9-80ee-a78af8e42142.png)

Edit configuration file for mysql as follows : /etc/datadog-agent/conf.d/mysql.d. Open and edit conf.yaml by:  
vi conf.yaml
  
![mysql conf file](https://user-images.githubusercontent.com/47703847/52919061-3bd45880-32cc-11e9-9129-c03a3ab658d5.png)
 
Output:

To check for metrics reported by mysql go to Metrics > Summary on Datadog UI > Type "mysql" in Filter Metrics by name search and all the metrics for mysql will appear in the list.

![mysql configured and datadog reporting mysql metrics](https://user-images.githubusercontent.com/47703847/52917219-e3df2700-32b6-11e9-9d77-9340b27031e7.png)
 
3. Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

Answer:  
step 1: Created a new custom_test.py file in following path: /etc/datadog-agent/checks.d by following command:  
vi custom_test.py

[Python Script](https://github.com/srp84/hiring-engineers/blob/master/custom_test.py)

After writing python script, checked for successful execustion of file by following command:  
python custom_test.py
       
step 2:Created custom_test.yaml file in following path: /etc/datadog-agent/conf.d by following command:  
vi custom_test.yaml

[Python Script](https://github.com/srp84/hiring-engineers/blob/master/custom_test.yaml)
       
step 3:Run Agent Check:  
       sudo -u dd-agent -- datadog-agent check custom_test  
       
![output of agent-check 1](https://user-images.githubusercontent.com/47703847/52939745-e5e6cb80-3332-11e9-8ee2-be353b22cce2.png)
       
![output of agent check 2](https://user-images.githubusercontent.com/47703847/52939760-ec754300-3332-11e9-88e1-72f177e986cf.png)
       
step 4:It was successfully implemented and available in metrics summary

![my_metric image](https://user-images.githubusercontent.com/47703847/52919267-86ef6b00-32ce-11e9-9b42-f235a956c488.png)
       
4. Change your check's collection interval so that it only submits the metric once every 45 seconds.

Answer:This answers the BONUS QUESTION too.
Changes made in /etc/datadog-agent/conf.d/custom_test.yaml file. Defined minimum interval as 45 seconds.

[Python Script](https://github.com/srp84/hiring-engineers/blob/master/custom_test.yaml)

## VISUALIZING DATA:

1. Utilize the Datadog API to create a Timeboard that contains:

>> Your custom metric scoped over your host.
>> Any metric from the Integration on your Database with the anomaly function applied.
>> Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

Answer: Created a new python file in following path: /etc/datadog-agent and named it as new_timeboard.py
Arguments -  
title [required]: The name of the dashboard.  
description [required]: A description of the dashboard’s content.  
graphs [optional, default=None]: A list of graph definitions. Graph definitions follow this form:  
  title [required]: The name of the graph.  
  definition [optional, default=None]:  
  events [optional, default=None]: The query for event overlay.    
  requests [optional, default=None]: The metric query, line type, style, conditional formats, and aggregator.    
  viz [optional, default=timeseries]: The type of visualization.   
  template_variables [optional, default=None]:    

![created new_timeboard python file](https://user-images.githubusercontent.com/47703847/53067606-f918a900-34a2-11e9-8d9c-41379e676594.png)
        
Reffered to API section under DOCS of datadog website.Created three different graphs by listing them in graphs: section of python code.
The requests in python script followed the following rule:  
"q": "function(space aggregation:metric{scope}.Time-aggregation)"  
The function and Time-aggregation part is optional.
        
Input:  [Python Script](https://github.com/srp84/hiring-engineers/blob/master/new_timeboard.py)

Output: ![three graphs on a timeboard](https://user-images.githubusercontent.com/47703847/52919498-0d0cb100-32d1-11e9-8bd7-a72816122f2c.png)

2. Once this is created, access the Dashboard from your Dashboard List in the UI:

Answer:Go to datadog UI and click on Dashboard List as shown below:

![click on dashboard list](https://user-images.githubusercontent.com/47703847/53068067-0040b680-34a5-11e9-8cd4-68b303e06cd7.png)

![custom timeboard in dashboard list](https://user-images.githubusercontent.com/47703847/53068075-06cf2e00-34a5-11e9-8a72-f738aaf61aa2.png)

![three graphs on a timeboard](https://user-images.githubusercontent.com/47703847/52919498-0d0cb100-32d1-11e9-8bd7-a72816122f2c.png)

>> Set the Timeboard's timeframe to the past 5 minutes

Answer: For timeboard, if the timeframe is selected for one graph, it sets the same timeframe for all the graphs on the timeboard. Dragged the time on one graph to make it for 5 minutes.

Output: ![timeboard 5 min graphs](https://user-images.githubusercontent.com/47703847/52919602-00d52380-32d2-11e9-90e0-8e69bb8d8232.png)

>> Take a snapshot of this graph and use the @ notation to send it to yourself

Answer: Clicked on the camera button on each graph and mentioned email id with @ sign.

Output : 

Camera

![snapshot of graph and email you](https://user-images.githubusercontent.com/47703847/52928565-67783280-330e-11e9-8307-4a42b6f6637a.png)

Email notification

![email of graph snapshot](https://user-images.githubusercontent.com/47703847/52928575-719a3100-330e-11e9-86c0-7e7acbb8d914.png)

Bonus Question: What is the Anomaly graph displaying?

Answer:
It is used for dynamic infrastructure and metrics. By applying anomaly function on a dynamic graph, it displays reults based on historical trends. It shows that even though a metric fluctuate constantly, it is still in the range of past trends. When actual traffic doesn't match the prediction then that is called anomaly. Datadog uses three algorithms for anamoly
1. Basic: lagging rolling quantile algo
2. Agile: SARIMA
3. Robust: Seasonal-trend Decomposition Algorithm
All the algorithms are robust so past anomalies don't blow off future broadcasts, adapt to changes at metric base-line, adapt to missing data

## MONITORING DATA:

1. Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

>> Warning threshold of 500
>> Alerting threshold of 800
>> And also ensure that it will notify you if there is No Data for this query over the past 10m.

Answer: Go to Datadog UI and Create Monitor as shown below:

![click on new monitor](https://user-images.githubusercontent.com/47703847/53068194-9a086380-34a5-11e9-8e8d-ec4ebd31a024.png)

Select Metric Monitor:

![select metric monitor](https://user-images.githubusercontent.com/47703847/53068287-f3709280-34a5-11e9-9cbf-d32f2c501437.png)

Input:

![create monitor input 1](https://user-images.githubusercontent.com/47703847/52928908-0e110300-3310-11e9-8b2b-6b78397363b8.png)

![create monitor input 2](https://user-images.githubusercontent.com/47703847/52928917-15381100-3310-11e9-8231-74ff67ca6e91.png)

![create monitor input 3](https://user-images.githubusercontent.com/47703847/52928920-18cb9800-3310-11e9-83bb-fe50a1afee6a.png)

Please configure the monitor’s message so that it will:

>> Send you an email whenever the monitor triggers.

Answers:

Email Notification i/p:

The message before notify your team was:  
ALERT{host: shruti-VirtualBox}  
Monitor Message: Threshold is breached.

![email notification input](https://user-images.githubusercontent.com/47703847/52929399-4580af00-3312-11e9-8cc3-f25e2902a514.png)

Triggered Monitor: 

![triggered monitor](https://user-images.githubusercontent.com/47703847/52929427-60532380-3312-11e9-959f-957be231d213.png)

Email of triggered monitor:

![email of triggered monitor](https://user-images.githubusercontent.com/47703847/52929435-6812c800-3312-11e9-931b-546267d90831.png)

>> Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.

Various template variables are found by clicking use message template vaiables.

![template variables](https://user-images.githubusercontent.com/47703847/53068901-1603ab00-34a8-11e9-86e5-28461f0aeb7d.png)

Answers: ALERT input in message box :  
Used {{#is_alert}}{{/is_alert}} 

![alert message input](https://user-images.githubusercontent.com/47703847/52930685-63044780-3317-11e9-8646-a1ff1e6d1523.png)

ALERT output

![alert message email output](https://user-images.githubusercontent.com/47703847/52930687-68619200-3317-11e9-8db4-7914178bc373.png)

WARN input in message box :  
Used {{#is_warning}}{{/is_warning}}

![warn input](https://user-images.githubusercontent.com/47703847/52930690-6f88a000-3317-11e9-9088-4d88ae3bdacb.png)

WARN output

![warn message output](https://user-images.githubusercontent.com/47703847/52930694-72839080-3317-11e9-9c15-29e359f70853.png)

NO DATA input in message box :
Used {{#is_no_data}}{{/is_no_data}}

![no data input](https://user-images.githubusercontent.com/47703847/52930703-79120800-3317-11e9-9089-7f6dfb3d07b8.png)

NO DATA output 

![no data message output](https://user-images.githubusercontent.com/47703847/52930704-7b746200-3317-11e9-985f-8905779d3290.png)

>> Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
>> When this monitor sends you an email notification, take a screenshot of the email that it sends you.

Answers: The host ip was determined by navigating datadog's UI Infrastructure list >> Inspect shruti-VirtualBox >> system info >> network as 10.0.2.5 to check if its displaying correct in e-mail notification.

![verification of ip address](https://user-images.githubusercontent.com/47703847/53068437-7c87c980-34a6-11e9-9ed3-0fa76d2ae675.png
)

Input:  
{{host.shruti-VirtualBox}} with IP {{host.ip}} is down @srp84@njit.edu

![alert message with host ip input](https://user-images.githubusercontent.com/47703847/52931384-20903a00-331a-11e9-8b5c-d48e36455163.png)

Output:

![alert message with host ip output](https://user-images.githubusercontent.com/47703847/52931400-2c7bfc00-331a-11e9-8182-1e3986612cd0.png)

As seen in the image my_metric was > 800.0 and host ip displayed as 10.0.2.5

>> Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

One that silences it from 7pm to 9am daily on M-F,
And one that silences it all day on Sat-Sun.
Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

Answers:

Schedule M-F 7 pm - 9 am. I tried changing time-zone multiple times but it would just stay America-New_york

Input:Go to Datadog UI, click on Manage Downtime under Monitors as shown below:

![click on manage downtime](https://user-images.githubusercontent.com/47703847/53069087-c07bce00-34a8-11e9-9142-b9d0a31d17b6.png)

![click on schedule downtime](https://user-images.githubusercontent.com/47703847/53069139-e7d29b00-34a8-11e9-964c-eaca2b604f14.png)

Choose Monitor name to silence:

![choose monitor name to silence](https://user-images.githubusercontent.com/47703847/53069248-397b2580-34a9-11e9-83c1-2069526fb0dc.png)

Schedule Downtime:

![schedule downtime m-f input 1](https://user-images.githubusercontent.com/47703847/52932673-867ec080-331e-11e9-99c0-02cbe3f2fb59.png)

![schedule downtime m-f input 2](https://user-images.githubusercontent.com/47703847/52932698-a3b38f00-331e-11e9-86bd-5e0bd057f243.png)

Email notification:

![schedule downtime email notification m-f](https://user-images.githubusercontent.com/47703847/52932663-7a92fe80-331e-11e9-961b-0b8c91d0677c.png)

Schedule saturday sunday entire day

Input:Go to Datadog UI, click on Manage Downtime under Monitors as shown below:

![click on manage downtime](https://user-images.githubusercontent.com/47703847/53069087-c07bce00-34a8-11e9-9142-b9d0a31d17b6.png)

![click on schedule downtime](https://user-images.githubusercontent.com/47703847/53069139-e7d29b00-34a8-11e9-964c-eaca2b604f14.png)

Choose Monitor name to silence:

![choose monitor name to silence](https://user-images.githubusercontent.com/47703847/53069248-397b2580-34a9-11e9-83c1-2069526fb0dc.png)

![schedule downtime saturday sunday input](https://user-images.githubusercontent.com/47703847/52932704-ab733380-331e-11e9-9b92-71a67964ed88.png)

Email notification:

![schedule downtime email notification sat-sun](https://user-images.githubusercontent.com/47703847/52932669-82eb3980-331e-11e9-8a1e-5c675b2cde6a.png)

## COLLECTING APM DATA:

>> Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

>> Please include your fully instrumented app in your submission, as well

Answers:

Created Python file my_app.py in /etc/datadog-agent

[Python Script](https://github.com/srp84/hiring-engineers/blob/master/my_app.py)

Then went to /etc/datadog-agent to edit datadog.yaml file to enable apm config as true

![apm config enabled true](https://user-images.githubusercontent.com/47703847/53070319-bcea4600-34ac-11e9-9824-8d38a2554059.png)

Set up APM first by following different commands for different OS by following steps given on https://app.datadoghq.com/apm/install# Started collecting traces by running the command on VM:  
1. pip install ddtrace  
2. ddtrace-run python my_app.py  

![output of ddtrace](https://user-images.githubusercontent.com/47703847/53070245-83b1d600-34ac-11e9-8720-128cf520718d.png)

To view the app on UI, click service-map on UI

![click on service-map](https://user-images.githubusercontent.com/47703847/53069515-451b1c00-34aa-11e9-91cc-015fa8dac612.png)

Flask App on UI

![flask app](https://user-images.githubusercontent.com/47703847/52937458-23e0f100-332d-11e9-88bc-fb37caac24db.png)

trace.flask metrics in Summary

![trace flask metrics](https://user-images.githubusercontent.com/47703847/53070642-dcce3980-34ad-11e9-927c-e6f7aa35688d.png)

![apm trace](https://user-images.githubusercontent.com/47703847/52937501-4246ec80-332d-11e9-9d00-1c9026e41049.png)

Created a new graph on Custom Timeboard from Datadog UI

![apm graph via ui](https://user-images.githubusercontent.com/47703847/53070527-72b59480-34ad-11e9-9325-c1f86fe4e43a.png)

Dashboard with APM and Infrastructure Metrics

![infrastructure and apm graph](https://user-images.githubusercontent.com/47703847/52937469-2d6a5900-332d-11e9-85cd-974fc3ee9f2e.png)

>> Bonus Question: What is the difference between a Service and a Resource?

A service is a set of processes that do the same job.
The service list from UI for flask is shown below:

![flask shown in services list](https://user-images.githubusercontent.com/47703847/53106888-f600d580-3501-11e9-95bf-0da9008dd7c2.png)

A Resource is a particular action for a service. When i clicked flask from service list, I got directed to resources of that particular service

![flask resources](https://user-images.githubusercontent.com/47703847/53107063-424c1580-3502-11e9-81ce-479c4ed8f831.png)

## FINAL QUESTION:

>> Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!
Is there anything creative you would use Datadog for?

Answer: I think datadog is an interesting tool that provides communication between data in all ways possible. 

According to me, Datadog can be used effectively for analysing human behaviour for Fitbit and keep a track of data about the amount of sleep, the rate of heartbeat, walking data, running data everything at one place on a dashboard.

Datadog can also be used in a stock management system. Customers can easily view the prices of thier purchased stocks at one place. They can also view the historical trends of every stock to predict the price range for future.



        
 

