# Alex Sands Technical Assessment

## Setting up environment  

I set up my virtual environment via Vagrant (vagrantup.com/docs/installation), an open-source software that makes it easy to spin up containers such as VirtualBox and Docker.  It is preferred to set up an Ubuntu workspace, to avoid dependency issues.  

Once my Vagrant environment was up and running, I went over to the Datadog website and went through the process of creating an account.  The registration was very simple, I just needed simple login information and my organization name to get started.  To link up your environment to the Datadog UI, the API and application keys are required, which are in the Organization settings of the Datadog UI.  

With the keys collected, enter the following command to install the Datadog Agent.  Be sure to replace <DATADOG_API_KEY>  with the keys obtained from the previous step.  

> DD_API_KEY=<DATADOG_API_KEY> DD_SITE="datadoghq.com" bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_script.sh)"

After running:

> $ sudo datadog-agent status

I was able to receive this output

Figure 1
<img width="1428" alt="datadog-agent-status" src="https://user-images.githubusercontent.com/32316958/146984515-491a69dd-2a55-4348-b0a2-c57941f35305.png">

## Collecting Metrics

The directions from Datadog (https://docs.datadoghq.com/getting_started/agent/) made it very easy to navigate vagrant and install the correct libraries for Datadog.

I used the following nano command to edit my configuration file: 

> $ sudo nano /etc/datadog-agnet/datadog.yaml

This allowed me to edit my host tags, as seen in the image below.  These tags allow me to better organize my metrics.  The tags were reflected in the Datadog UI, under the “Host Map” section after a few minutes. Restart the agent to resolve potential issues with the following comand: 

> $ sudo service datadog-agent restart

Figure 2

<img width="1273" alt="hostmap" src="https://user-images.githubusercontent.com/32316958/146995288-5e1ab17e-8810-4b97-87d0-8c9ba8412c6d.png">

I then installed MySQL in Vagrant environment using the following command: 

> $ sudo apt install mysql-server
  
Verify the service is running correctly by inputting the following in the command line:

> $ sudo service mysql status

By utilizing the documentation provided (https://docs.datadoghq.com/integrations/mysql/?tab=host), the MySql check was conveniently included in the Datadog-agent package.  

To prepare MySql, it is necessary to create a database user on each server by inputting: 

> mysql> CREATE USER 'datadog'@'localhost' IDENTIFIED BY ‘<UNIQUEPASSWORD>';
Replace ‘<UNIQUEPASSWORD>’; with the password created during installation.  To reset the password, follow this guide to troubleshoot issue: https://dev.mysql.com/doc/refman/8.0/en/resetting-permissions.html

Then verify that the user was created by entering the following in a separate command line: 

> mysql -u datadog --password=<UNIQUEPASSWORD> -e "show status" | \
> grep Uptime && echo -e "\033[0;32mMySQL user - OK\033[0m" || \
> echo -e "\033[0;31mCannot connect to MySQL\033[0m”

> mysql -u datadog --password=<UNIQUEPASSWORD> -e "show slave status" && \
> echo -e "\033[0;32mMySQL grant - OK\033[0m" || \
> echo -e "\033[0;31mMissing REPLICATION CLIENT grant\033[0m”

Afterwards grant the user limited priviledges: 

> mysql> GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'localhost' WITH MAX_USER_CONNECTIONS 5;

View the metrics collected from the performa_schema database using the following to grand privileges.  

> mysql> show databases like ‘performance_schema’;

 Figure 3
  
<img width="599" alt="mysqlperformaschema" src="https://user-images.githubusercontent.com/32316958/146952646-a601d780-04fd-41d4-953e-2bfc0cfb738c.png">

To edit the configuration by using the following command: 

> $ sudo nano /etc/datadog-agent/conf.d/mysql.d/conf.example.yaml

From the mysql.d folder (/etc/datadog-agent/conf.d/mysql.d/) I copied the contents over to a new file named conf.yaml in the mysql.d folder, which is demonstrated in the figure below:
  
 Figure 4
  
<img width="1434" alt="mysqlconfig" src="https://user-images.githubusercontent.com/32316958/146984566-69dee752-199c-463b-bf4c-310a23174ac9.png">

Once I had the mysql database running, I created a metric check called my_metric and used it to submit a random value between 0-1000.  

In order to submit a check, I had to create two files; one in the /conf.d/ that initiates the instance show in figure #, and a file in /checks.d/ that generates the random value as shown below.

In the yaml file created below, I created a sequence which calls an instance with an empty mapping.  
  
  *instances: [{}]*
  
In the /checks.d/ file we create a python file which initiates and submits the random value generated as a metric.  
  
 Figure 6
  
 <img width="714" alt="my_metric" src="https://user-images.githubusercontent.com/32316958/146953545-131a05e3-2df8-4cc5-82f5-cfe976fb6ad3.png">
  
Verified status of check:
  
 Figure 7
  
<img width="1436" alt="my_metric_check" src="https://user-images.githubusercontent.com/32316958/146984925-65d1c93b-549e-40ef-91d6-f366ddcd7839.png">

It is possible to change the collection interval to submit metrics every 45 seconds back in the yaml file I created in /conf.d/ file.
  
 Figure 8

<img width="659" alt="my_metricinstance" src="https://user-images.githubusercontent.com/32316958/146986894-12278c3e-4984-49e1-88de-3a6ba6ee988f.png">

### Bonus question:

Yes it is possible to edit the interval by adding min_collection_interval to the yaml in the conf.d/ file.  Add the min_collection_interval variable to the mapping within the stance, and input the number 45 as seen in figure 8 above.  The collector may not run the checker if there is another check running as well, for then the check will skip until the following interval.  

## Visualizing Data

Created board using PostMan API editor and sent POST API to Datadog using API token.  Included screen shot of API editor with JSON body.  

https://app.datadoghq.com/dashboard/gek-bgr-27h/mymetric?from_ts=1639782997319&to_ts=1639786597319&live=true

Datadog makes it easy to import their collection to Postman by offering a quick button to get set up in Postman which can be found here: https://docs.datadoghq.com/getting_started/api/.
  
 Figure 9
  
 <img width="780" alt="postmanimport" src="https://user-images.githubusercontent.com/32316958/146961193-cbd5c1a7-b59b-433a-bcc1-775a6a66f15e.png">

Once I am directed to the Postman UI, the available Datadog API’s are shown in the left pane of the window. The Collection that was just imported also contains an environment called Datadog authentication which can be utilized to add API and application keys to link to our application.
  
 Figure 10
  
<img width="1349" alt="postmanbody" src="https://user-images.githubusercontent.com/32316958/146961133-330e0a5a-39c4-49cf-906b-a3a76a03e07c.png">
 
 I implemented the following code into a file called <app.py src=https://github.com/asands24/hiring-engineers/blob/master/app.py> 

  
 Reference for JSON body: https://zero2datadog.readthedocs.io/en/latest/visualize.html

View the dashboards within the Dashboard list in the Datadog user interface.  The sum of my_metric to show within a 5 minute time span.  Snapshot of the graph with hourly anomalies dashboard included. 

https://app.datadoghq.com/dashboard/5aa-992-hs3/postman-test?from_ts=1639786334482&to_ts=1639786634482&live=true

 Figure 11
  
<img width="1277" alt="Timeboard" src="https://user-images.githubusercontent.com/32316958/146616807-8f607ea6-6d7e-49bd-9067-9142a818e05d.png">

 Figure 12
  
<img width="1267" alt="postmantimeboard" src="https://user-images.githubusercontent.com/32316958/146623324-a7d8c465-ca4f-4f8d-85f7-b7c8ca39ed10.png">
  

**Bonus:** 
  
In observation of the anomaly graph, the function distringuishes normal and abnormal trends within the gray area.  It is able to analyze a metric's behaviour and show a prediction of what may be too abnormal for the graph. 
  
  <img width="1117" alt="anomalyfunction" src="https://user-images.githubusercontent.com/32316958/146997162-bc1dfb87-b103-4d6f-bece-1fcadc58057a.png">


## Monitoring Data

To create a new Metric Monitor, navigate to the create a metric section in the left-hand panel.  The options to create a new custom metric can be observed.  The ability to use recommended metrics are also provided. 

 Figure 13
  
<img width="1281" alt="metricmonitor1" src="https://user-images.githubusercontent.com/32316958/146999868-f97f871d-2d69-472d-9df7-c8c494c66bbe.png">

Select “new monitor” and configure it to watch the average of my_metric and set the alert limits to reveal the following values over the past 5 minutes.  Below that, edit the monitor to set an alert threshold of 800, a warning threshold of 500, and a no data if the query does not receive data for 10 minutes. 
                                                                                                                                                  
  Figure 14 
                                                                                                                                                  
<img width="1243" alt="metricmonitor2" src="https://user-images.githubusercontent.com/32316958/146616752-1761074b-a082-49e7-a453-302ce942abf1.png">

Configure the message and the users it gets sent to in the set-up menu in section 4 & 5.  Configured the monitor’s messages in the cog menu to send an email whenever the monitor gets triggered. Configure the settings to send specific messages according to the variables set with reference to the template forms.  

  Figure 15   
                                                                                                                                                  
<img width="1271" alt="metricmonitor3" src="https://user-images.githubusercontent.com/32316958/146954449-3013a47f-4cd9-4616-b501-8de81b952979.png">  
                                                                                                                                                  
  The emails were able to successfully alert me depending on the which threshold was met: 
                                                                                                                                                  
<img width="697" alt="email5" src="https://user-images.githubusercontent.com/32316958/146999420-b43b8e6b-2a87-41e2-9d2d-f80e50c839fe.png">
                                                                                                                                           
<img width="708" alt="email6" src="https://user-images.githubusercontent.com/32316958/146999426-9e2fc884-cab5-4371-9531-43e1fa0a5025.png">
                                                                                                                                      
**Bonus Question:**
To set downtime for specific days, edit configuration through Manage Downtime within the Monitors menu.  There will be an option to schedule downtime. Use RRule Generator to set more specific options. 
                                                                                                                                                  
  Figure 16
                                                                                                                                                  
 <img width="719" alt="downtime_weekdays" src="https://user-images.githubusercontent.com/32316958/146616821-217268f7-90ad-422d-8254-027677ed590e.png">

          
  Figure 17 
                                                                                                                                         
  <img width="720" alt="downtime_weekends" src="https://user-images.githubusercontent.com/32316958/146616832-eee833e4-c5dc-4ddc-a462-6726b8e00a0b.png">

  Figure 18
                                                                                                                                         
  <img width="710" alt="email1" src="https://user-images.githubusercontent.com/32316958/146616776-7f3b524c-b776-4644-801f-e2a0b6d7a5e4.png">

  Figure 19
                                                                                                                                                     
  <img width="710" alt="email2" src="https://user-images.githubusercontent.com/32316958/146616778-c829e927-70f4-4ca5-8f34-20b2d117bc49.png">


## Collection APM Data

I was able to set up tracers using the information provided by Datadog here: https://docs.datadoghq.com/tracing/setup_overview/setup/python/?tab=containers.  

It is first recommend to set up the environment, which Datadog provides a step-by-step instruction to ensure a smooth deployment configuration here: https://app.datadoghq.com/apm/docs?architecture=host-based&language=python


Before getting started, the correct python libraries must be installed via the following commands:

> $ sudo apt-get install python-pip
> pip install flask
> pip install ddtrace

Issues became present with python 2 installation.  Tried with pip3 (using the command: $ sudo apt-get -y install python3-pip) to download flask and ddtrace and issues were resolved.  

Utilize the flask app by following the quick start guide provided by flask https://flask.palletsprojects.com/en/2.0.x/quickstart/ 

  Figure 20   
                                                                                                                                                     
<img width="714" alt="ddtrace_app" src="https://user-images.githubusercontent.com/32316958/146622489-f6b7c8ad-a3d9-4e02-83f2-4d896a7a766c.png">

  Figure 21                                                                                                                                            
<img width="519" alt="ddtrace-output" src="https://user-images.githubusercontent.com/32316958/146985646-f71f9fce-d8af-43c7-b343-2b7b98026fb3.png">

Created an application call app.py by using the touch command and then editing it with nano to create application using Python.

> $ sudo touch app.py
> $ sudo nano app.py

I entered the provided code to create a flask app as seen on figure # 

Once this is created it, instrument it into Datadog’s APM by calling it with the following command:

DD_SERVICE="flask-app" DD_ENV="dev" DD_LOGS_INJECTION=true ddtrace-run python app.py

A service running summary can be observed if all steps were completed.
  
  Figure 22  
                                   
<img width="714" alt="ddtrace_app" src="https://user-images.githubusercontent.com/32316958/146954279-4be12264-b061-4fe7-a7a4-7f0b69bea12f.png">

I then sent requests to the three routes in the app (/, api/apm, api/trace) 

Although I was receiving a message that the service was running.  I ran into issues where the metrics would not display in the APM section of the Datadog UI. I believe the issue relates to the metrics I am sending.  

### Bonus Question:
Services act as “building blocks” that utilize microservice architectures.  A service can group together endpoints, and is usually named after a specific business action.  A resource is an action given to a service (e.g. query to a database or an endpoint.  

### Final Question 
Datadog can be used in many different ways.  For example, it can be utilized to organize IoT devices within businesses such as a local bar.  The devices can collect metrics such as inventory, capacity, and even other metrics such as sales.  It is even possible to integrate AWS services such as Amazon SageMaker to utilize machine learning and predict future events such as peak sales.  
                                                                                                                                              
Datadog can also be used to monitor hardware usage for devices such as CPU and memory.  This would be useful for organizations that rely on devices that need to run constantly.  For example, a company that makes predictions on weather patterns may rely on devices that are outdoors and record specific data.  Datadog can help visualize the system's levels and alert if it goes above/below a specific threshold.  
