## ENVIRONMENT SETUP

I have experience working with VirtualBox and hypervisor for academic-oriented and self-learning. Docker and Vagrant both are interesting and new to me, with no special reason I have chosen Vagrant.

Instead of manually creating and installing a virtual OS from scratch in VirtualBox. It is easy to use pre-built images ("boxes") provided by vagrant and a single command vagrant up/vagrant destroy, can create/shutdown a virtual environment.

Below are required to perform the task:
  - Vagrant - v2.2.3
  - VirtualBox - v6.0
  - Cmder - linux like console for windows

Downloaded vagrant and added ubuntu 16.04 image/box ("ubuntu/xenial")

![002](https://user-images.githubusercontent.com/33669341/53703513-2fdfaf00-3e13-11e9-964c-7546da8440c6.PNG)

Signed up into datadog and downloaded agent which suits to above vagrant.

The datadog-agent status after installing agent in the host ubuntu-xenial.

![001](https://user-images.githubusercontent.com/33669341/53703664-d1b3cb80-3e14-11e9-9a92-3b05a1d6f33f.PNG)

## COLLECTING METRICS

Once the environment setup is done well. Then datadog service start collecting data for further process. Before that we can see overview of current status with the command *"datadog-agent status"*

I have used below commands that seems shortcut to see required details of datadog services.
  > *datadog-agent --help* - display all options  
  > *datadog-agent status* - display status  
  > *datadog-agent config* - display necessary config info  
  > *datadog-agent check* - display info about check and more  

There are 3 important config file 
1) datadog.yaml - /etc/datadog-agent/**datadog.yaml** - responsible for all the application, host, trace, tags and more.
2) cust_app.yaml - /etc/datadog-agent/**conf.d**/cust_app.yaml - responsible for installed/custom created app's interval time.
3) cust_app.py - /etc/datadog-agent/**check.d**/cust_app.py - responsible for getting metric's of installed/custom app.

Edited the datadog.yaml to add the tag <first_tag> and ensure the tag is added, run *datadog-agent config* command.

![004](https://user-images.githubusercontent.com/33669341/53703973-d62db380-3e17-11e9-8097-268a970eff68.png)

Below screenshot shows the "Host Map" with *added tag*.

![img001](https://user-images.githubusercontent.com/33669341/53703892-180a2a00-3e17-11e9-931f-35832252c3af.PNG)

Installed mysql and corresponing Datadog integration. Below screenshot shows mysql datadog integration

![010](https://user-images.githubusercontent.com/33669341/53704502-60c4e180-3e1d-11e9-8a46-d787b055327b.PNG)

Below two file name should be same  
 > </etc/datadog-agent/checks.d/custom_firstCheck.py> - check file &  
 > </etc/datadog-agent/cong.d/custom_firstCheck.yaml> - config file. 

**check file** 
Creating a custom application <customCheck> in the path /etc/datadog-agent/checks.d/custom_firstCheck.py and collecting metrics <my_metrics> as a random value in the range 0 and 1000.

**config file**
The application's time interval in the path /etc/datadog-agent/cong.d/custom_firstCheck.yaml with default interval time 30 sec and it has been changed to 45 sec.

![005](https://user-images.githubusercontent.com/33669341/53704096-5c96c500-3e19-11e9-9fca-2ad3a00b3929.PNG)

The created custom check can be viewed in the 'datadog-agent status' as below,

![dtdg-check](https://user-images.githubusercontent.com/33669341/53704173-974d2d00-3e1a-11e9-89a5-fe17def7a647.PNG)

Initial interval time 5 sec for testing.

![custom_metrics](https://user-images.githubusercontent.com/33669341/53704131-f1012780-3e19-11e9-883c-3b7023021a63.PNG)

Then interval changed from 5 sec to 45 sec to have a clear view.

![collection interval from 5 to 45](https://user-images.githubusercontent.com/33669341/53704144-13934080-3e1a-11e9-8a16-a2bf71155a18.png)

## VISUALIZING DATA

After collecting the data into the datadog, next step is to visualize the data in UI or monitor tha data manually. Here, i have collected the metrics of above created custom app and installed mysql app in the hostmap are shown below.

![008](https://user-images.githubusercontent.com/33669341/53704495-5c98c400-3e1d-11e9-8fcd-bf4fc28cd234.PNG)

![009](https://user-images.githubusercontent.com/33669341/53704498-5efb1e00-3e1d-11e9-878c-937641649208.PNG)

Timeboard has been created by using datadog API. It helps to monitor data flow in live or past manually by giving query. 

                import requests, json, os, datetime, time
                from datadog import initialize
                from datadog import api as dog

                options = {
                        'api_key' : '<<API_KEY>>',
                        'app_key' : '<<APP_KEY>>'
                        }

                initialize(**options)

                def create_timeboard():
                    title = "MY TEST DASHBOARDx"
                    description = "created timeboard via api"
                    graph = {
                        "title": "Custom metric",
                        "definition":
                        {
                            "requests": [{"q": "customCheck.my_metric{host:ubuntu-xenial}"}],
                            "viz": "timeseries",
                        }
                    }
                    graph2 = {
                        "title": "Custom metric with roll up for past 1h",
                        "definition":
                        {
                            "requests": [{"q": "customCheck.my_metric{host:ubuntu-xenial}.rollup(sum, 3600)"}],
                            "viz": "timeseries",
                        }
                    }
                    x = dog.Timeboard.create(title=title, description=description, graphs=[graph, graph2])
                    return x


                create_timeboard()

Below is the JSON response of created timeboard using datadog api

![016](https://user-images.githubusercontent.com/33669341/53705231-23635280-3e23-11e9-8b13-3c3ad3ddcf9f.PNG)

Under dashboard tab, created custom dashboard < My Dashboard > and integrated mysql dashboard <Mysql - Overview> are in the dashboard list as below.

![011bckup](https://user-images.githubusercontent.com/33669341/54142953-13520100-4429-11e9-9d7e-edbdb089d777.PNG)

Timeboard *custom metric* link:

    https://app.datadoghq.com/graph/embed?token=6da76d3c78d5cfac83ed7ea70f9a6d6082d69a4709033946f3c06e56dcfa5700&height=300&width=600&legend=true

Created custom metrics timeboard with no function and with rollup sum function 

![012](https://user-images.githubusercontent.com/33669341/53704818-2e68b380-3e20-11e9-8855-ba102423ead8.PNG)


Timeboard *custom metric with roll up* link:

    https://app.datadoghq.com/graph/embed?token=1db5616b1be00fae1a268699d4cfc0cf4eda6c17d83f4aecca8c850097b7fd8c&height=300&width=600&legend=true

Selected past 5 mins in the timeboard

![013](https://user-images.githubusercontent.com/33669341/53704819-2e68b380-3e20-11e9-98cd-1faca7e1b01f.PNG)

The received snapshot with selected last 5 mins data

![015](https://user-images.githubusercontent.com/33669341/53704821-2f014a00-3e20-11e9-8c4c-0b0be965af13.PNG)

Mysql timeboard

![014](https://user-images.githubusercontent.com/33669341/53704820-2e68b380-3e20-11e9-898a-7902be016116.PNG)

## MONITORING DATA

By using above timeboard, I have created a moniotor that works automatically and repeated with given contrians. The contrains are thresholds.

Created new metric monitor named < My Monitor >

![0019](https://user-images.githubusercontent.com/33669341/53705899-e3eb3500-3e27-11e9-80da-d1ce44e1ce8b.PNG)

Can manage monitor after creating, below properties that include threshold for past 5 mins raise :  
  *alert* if range above 800,  
  *warning* if range above 500 &  
  *notify* if no data more than 10 mins

![017](https://user-images.githubusercontent.com/33669341/53705815-560f4a00-3e27-11e9-9c96-4b9094ac7f52.PNG)

Data live status & history, & evaluation graph with threshold

![018](https://user-images.githubusercontent.com/33669341/53705763-0892dd00-3e27-11e9-8e0f-eb54c7a0f36a.PNG)

Received below mail for all different alerts

* Alert value if above 800  
  Test alert with test name (Monitor Name)

![021](https://user-images.githubusercontent.com/33669341/53707044-6aeedc00-3e2d-11e9-8c94-8622e8f5e9b9.PNG)

* Warn value if above 500

![022](https://user-images.githubusercontent.com/33669341/53706288-d33bbe80-3e29-11e9-9c80-c7c5faceff3a.PNG)

* Notify if no data

![031](https://user-images.githubusercontent.com/33669341/53890720-026c4e80-4029-11e9-9483-aeda450116d3.PNG)

**Bonus Question** : Downtime from 7pm to 9am during weekdays and all day in weekend are scheduled as below
monitor in manage downtime tab

Set up two scheduled downtimes  
  > Weekday - downtime for 14h on each day (monday to thursday) from 7 pm to 9 am  
  > Weekend - downtime for 63h on every weekend from friday 7 pm to monday 9 am

![020](https://user-images.githubusercontent.com/33669341/53706050-a935cc80-3e28-11e9-90b1-dc08f44f6307.PNG)

The received mail of downtime details:

![023](https://user-images.githubusercontent.com/33669341/53706380-61b04000-3e2a-11e9-820e-eebeaf91a722.PNG)

## APM

The ddtrace-run works good and produce data in UI initially then later after adding analysed span and env tag, i'm not able to get any data. 
So I have done this APM with manual method, in manual method, it shows only default env tag even after adding env tag with right syntax in main config (datadog.yaml) file  

Given flask python script

![024](https://user-images.githubusercontent.com/33669341/53888045-d0a4b900-4023-11e9-8431-6ea8ce95a65c.PNG)

Sending request

![026](https://user-images.githubusercontent.com/33669341/53888913-caafd780-4025-11e9-8df2-7e61f1f3a334.PNG)

Received responses 

![025](https://user-images.githubusercontent.com/33669341/53888188-24170700-4024-11e9-8fc8-bad55d394cab.PNG)

![032](https://user-images.githubusercontent.com/33669341/53891687-2d57a200-402b-11e9-91cd-45ba6f6093ac.PNG)

Service and resources in UI

![027](https://user-images.githubusercontent.com/33669341/53889273-6f321980-4026-11e9-8b71-9cecc6f6e3bf.PNG)
![028](https://user-images.githubusercontent.com/33669341/53889616-fd0e0480-4026-11e9-9a64-5b385634445a.PNG)
![029](https://user-images.githubusercontent.com/33669341/53903520-36a13880-4044-11e9-964c-22ed86137919.PNG)
![033](https://user-images.githubusercontent.com/33669341/53891684-2d57a200-402b-11e9-81f2-9564ed17372d.PNG)

APM Dashboard link

    https://app.datadoghq.com/graph/embed?token=ecd449236d088c9bc91a97b96fba9516b1aabedd815e1bc016c5ff9f486a698d&height=300&width=600&legend=true

Configuration file

![034](https://user-images.githubusercontent.com/33669341/53891685-2d57a200-402b-11e9-84e6-84203281b9d4.PNG)

Infrastructure List

![030](https://user-images.githubusercontent.com/33669341/53890176-ff249300-4027-11e9-8979-1cd3c814bcf3.PNG)

**Bonus Question** : Difference between a Service & a Resources

An application runs sevaral services to carry out the intended job defined by the developper. A minimal application may require a webapp service and database service. As the complexity of the application increases, services can be added to perform each kind of work efficiently, such as admin service for management.

Every service will perform actions inorder to get some work done. Such actions are referred as resources. In the case of a web app. http requests are classified into resources based on the url it points out to and the type of the request. Another example would be queries in the database. 

## THE LAST BUT NOT LEAST

Now a days car parking in Mall, Cinema theater, Side street park, concert and more became crucial to everyone. In few places, implemented IOT for parking availability but that haven't became spread all over. 

Using datadog services, develop an application to track parking availability in crowded places and throw an status of parking availability for people so that they no need to waste their time for searching places for parking their vehicles. 

