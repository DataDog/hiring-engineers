# The following will discuss the steps necessary in order to complete the Datadog Sales Engineering Lab.

## Prerequisites - Setup the environment
In order to properly complete the Datadog Sales Engineering Lab I first had to complete the environment setup. I chose to spin up a fresh new linux VM using Vagrant. In order to download and install a VM with Vagrant I followed the instructions provided in the reference section of the Datadog Sales Engineering lab by first downloading VirtualBox, and then downloading the latest version of Vagrant(2.2.7). 

From here I ran the following two commands in order to have a fully running virtual machine in Virtual box:

![upcommands](https://github.com/donp123/donp123/blob/master/vagrantup.png)

I then ran the command in order to ssh into the VM from my terminal:

$ Vagrant ssh 

From here I then signed up for a trial with Datadog using  “Datadog Recruiting Candidate” in the “Company” field, and proceeded to download the appropriate Agent for linux. I used the following command for the Datadog 7 installation onto my VM:

DD_AGENT_MAJOR_VERSION=7 DD_API_KEY=f622b4c53cca8fc2fd7e0f74c02e302b bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"

Once I ran the above command, I then went into Datadog to see my agent properly connected  by looking at my system dashboard:

![System Dash](https://github.com/donp123/donp123/blob/master/pic1_aftersetup.png)

Dashboard link: https://app.datadoghq.com/dash/integration/2/system---disk-io?from_ts=1585583453054&to_ts=1585587053054&live=true&tile_size=m

Now that my agent has been installed correctly, I was able to move on to the following 'Collecting Metrics' section.


## Collecting Metrics 

The following were the tasks given for completion of the Collecting Metrics section of the lab:

### 1.) Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

In order to complete this task, I first had to edit the datadog.yaml by running the following command:
  
  - $ sudo vi /etc/datadog-agent/datadog.yaml

Once inside the file file I was able to add in tags for my agent:
  
 ![tags](https://github.com/donp123/donp123/blob/master/datadogyaml.png)
  
I started off by adding one tag "env:dev" for my agent to make sure it would work. I then saved the yaml file and restarted the
agent: 

  - $ sudo service datadog-agent restart
  
Once restarted, I went back into Datadog to check my Host Map:

![Hostmap](https://github.com/donp123/donp123/blob/master/hostmap.png)

Hostmap Link: https://app.datadoghq.com/infrastructure/map?fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=availability-zone&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=true&palette=green_to_orange&paletteflip=false&node_type=host

I then saw that my tag has been succesfully added. At this point I went back and added a second tag "tier:webserver".
  
### 2.) Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

In order to complete this step I first chose to install MySQL onto my VM by running the following commands:
   - $ sudo apt update
   - $ sudo apt install mysql-server
   - $ sudo mysql_secure_installation
    
    
 I then had to install the Datadog integration for the MySQL database, which I found here:    https://docs.datadoghq.com/integrations/mysql/
  
The first step given for the Datadog integration was to create a new database user called datadog:

mysql> CREATE USER 'datadog'@'localhost' IDENTIFIED BY 'password';
  
I then granted the user proper permissions:
  
  mysql> GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'localhost' WITH MAX_USER_CONNECTIONS 5;
  
  Query OK, 0 rows affected, 1 warning (0.00 sec)

  mysql> GRANT PROCESS ON *.* TO 'datadog'@'localhost';
  
  Query OK, 0 rows affected (0.00 sec)
  
  
I then had to add the proper configuration block to my conf.yaml file to collect the MySQL metrics:
 
  - $ vi /etc/datadog-agent/conf.d/mysql.d/conf.yaml
 
From here I added the following code to the file:
  
  ![yaml](https://github.com/donp123/donp123/blob/master/confyam.png)
  
I then restarted the Datadog agent:
  
  - $ systemct1 restart datadog-agent
  
  
I now went into the Datadog UI and saw that a new dashboard was added called "MySQL Overview":
  
  ![mysqldash](https://github.com/donp123/donp123/blob/master/mysql.png)
  
  MySQL Dashboard Link: https://app.datadoghq.com/dash/integration/12/mysql---overview?from_ts=1585583599518&to_ts=1585587199518&live=true&tile_size=m
  
This dashbaord is showing that my agent is correctly setup and is now collecting from the MySQL databse I installed.
  
### 3.) Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

In order to complete this task, I first had to create a metric check python file. I called this file
my-metric-check.py:
  
  - $ sudo vi /etc/datadog-agent/checks.d/my-metric-check.py
   
I then added the following code into the python file:
  
  ![metriccheck](https://github.com/donp123/donp123/blob/master/pythonrand.png)
  
  
I then had to create a check Yaml file that also had the same name has my check Python file:
  
  - $ sudo vi /etc/datadog-agent/conf.d/my-metric-check.yaml
  
I then added the following to this file as directed by the Datadog doc file (https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7) :
  
    instances: [{}]
    
   
From here I restarted my Datadog-agent and tested to see if my custom metric check was working properly with the following command:
  
  ![mymetriccheck](https://github.com/donp123/donp123/blob/master/metriccheck.png)
  
  
### 4.) Change your check's collection interval so that it only submits the metric once every 45 seconds

In order to change my checks collection interval, I first went into the configuration yaml file I created in the above step and changed the min collection interval to 45. The below figure is taken from  (https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7), where I changed the interval from 30 to 45.

  
![intervalchange](https://github.com/donp123/donp123/blob/master/collectionintchangedoc.png)

![intervalchange2](https://github.com/donp123/donp123/blob/master/collectionchangecode.png)

From here I restarted the Datadog agent, and after went into Datadog to find my custome metric on the "Metric  Explorer":

![mymetricdash](https://github.com/donp123/donp123/blob/master/metricsexplorerinterval.png)

Metric Explorer Link: https://app.datadoghq.com/metric/explorer?from_ts=1585583750533&to_ts=1585587350533&live=true&page=0&is_auto=false&tile_size=m&exp_metric=my_metric&exp_agg=avg&exp_row_type=metric

The dashboard confirmed that the colection interval for my metric has been changed to 45 seconds.

### Bonus Question:  Can you change the collection interval without modifying the Python check file you created?

Yes you would just need to go into the configuration file and change the minimum collection interval as we just did to be 45 seconds from 15. There was no change needed to my check python file.

## Visualizing Data

The following were the tasks given for completion of the Visualizing Data section of the lab:

### 1.) Utilize the Datadog API to create a Timeboard that contains:
  - Your custom metric scoped over your host.
  - Any metric from the Integration on your Database with the anomaly function applied.
  - Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

I used the Datadog API using curl in order to create a Timeboard called "DPs first Dashboard" with three graphs. The first graph "My_Metric" displays the custom metric I created scoped over my vagrant host. The second graph created displays "MySQL Anomaly performance (CPU)" to show any anomalies in performance for the MySQL database I installed. The third graph being created by the API is to show my metric rolled up and summed over the last hour. The following is the code used to create my timeboard:

![timeboardapi](https://github.com/donp123/donp123/blob/master/timeboardcode.png)

The following is the Timeboard created by the API:

![timeboardapi](https://github.com/donp123/donp123/blob/master/timeboarddash.png)

Link to Timeboard: https://app.datadoghq.com/dashboard/df6-mrj-ffh/dps-first-dashboard?from_ts=1585248711534&to_ts=1585252311534&live=true&tile_size=m

### 2.) Once this is created, access the Dashboard from your Dashboard List in the UI:
  - Set the Timeboard's timeframe to the past 5 minutes
  - Take a snapshot of this graph and use the @ notation to send it to yourself.

I was able to change the timeframe of my Timeboard by using the shortcut "ALT +]" until it was five minutes:

![timeboardcut](https://github.com/donp123/donp123/blob/master/timeboardshortcuts.png)

From this new timeframe I took a snapshot of the "MySQL Anomaly performance (CPU)" graph and sent an email to myself:

![timeboardsnap](https://github.com/donp123/donp123/blob/master/snapshottime.png)

The following is the email I recieved from Datadog:

![timeboardemail](https://github.com/donp123/donp123/blob/master/emailtimeboard.png)

The following is the second email I sent myself:

![timeboardemail2](https://github.com/donp123/donp123/blob/master/secondtimeboardemail.png)


### Bonus Question: What is the Anomaly graph displaying?

The Anomaly graph shows any performance outside of normal behavior in red, and normal expected performance behavior in a grey shaded area. This uses Datadog algorithms to predict and determine what is considered normal behavior based on historical data , and allows a user to see what is 3 points above the standard deviation.


## Monitoring Data

The following were the tasks given for completion of the Monitoring Data section of the lab:

### 1.) Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:
  - Warning threshold of 500
  - Alerting threshold of 800
  - And also ensure that it will notify you if there is No Data for this query over the past 10m.
  
From the left hand navigation I created a new Metric Monitor:

Monitors -> New Monitor -> Metric 

Below is the configuration I added to monitor the metric "my_metric" based on the criteria assigned above:

![definemetric](https://github.com/donp123/donp123/blob/master/metricmonitorthres1.png)

### 2.) Please configure the monitor’s message so that it will:
  - Send you an email whenever the monitor triggers.
  - Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
  - Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
  - When this monitor sends you an email notification, take a screenshot of the email that it sends you.

In order to create an email notification based off a monitor trigger, I first had to create a monitor message:

![definemetricmessage](https://github.com/donp123/donp123/blob/master/warningmessage.png)

Below is the full monitor message:

![definemetricmessagefull](https://github.com/donp123/donp123/blob/master/messagecode.PNG)

Once the Metric Monitor has been fully filled out, I then ran a test to see what the alert would look like for an alert notification:

![definemetricmessagefull](https://github.com/donp123/donp123/blob/master/testmonitor.png)

Below is the test email alert notification I recieved:

![metricalerttest](https://github.com/donp123/donp123/blob/master/testresultemail.png)

After I was satisifed with the test result, I clicked "save" and my Metric Monitor was live. Below is the first live email warning notifcation when "my_metric" was greater than 500 on average during the last 5 minutes:

![metricalertlive](https://github.com/donp123/donp123/blob/master/liveemailtest.png)

### Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:
  - One that silences it from 7pm to 9am daily on M-F,
  - And one that silences it all day on Sat-Sun.
  - Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.


In order to Schedule Downtime for a monitor:

Monitors->Manage Downtime->Schedule Downtime

Below is the Schedueld Downtime configuration I used for my monitor during Monday-Friday 7pm to 9am:

![shutdownconf](https://github.com/donp123/donp123/blob/master/shutdown1.PNG)


And below is the configuration for Downtime on Saturday and Sunday:

![shutdownconfweekend](https://github.com/donp123/donp123/blob/master/weekendshutdown.png)


Once I Schedueled the Downtime in Datadog, I recieved an email notification informing me of the schuedeld downtime:

![shutdownconfirmationemail](https://github.com/donp123/donp123/blob/master/emailshutdown.png)



## Collecting APM Data
Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:

![APM](https://github.com/donp123/donp123/blob/master/apmflaskgiven.png)


In order to complete this section of the lab I first had to install python pip, and then install "ddtrace" using pip:

![pip](https://github.com/donp123/donp123/blob/master/installpipandddtrace.png)

I also installed flask using pip:

 -  $ sudo pip install flask
  
After installing pip, ddtrace, and flask I then created a flask.py file with the given APM code above to run my flask application. After creating my dpflask.py file I ran the following command to launch the application using Datadog tracing:

![ddtrace](https://github.com/donp123/donp123/blob/master/flasky.png)

I then ran the curl command below to test the application: 

![pip1](https://github.com/donp123/donp123/blob/master/testcurlapm.png)


After running the curl command above, a new service is present in my APM section of Datadog and the following dashboard for my flask application is visable:

![flaskdashboard](https://github.com/donp123/donp123/blob/master/flaskapmdashboard.png)

Dashboard link: https://app.datadoghq.com/apm/service/flask/flask.request?end=1585342678914&env=dev&maxPercentile=100&paused=false&start=1585339078914


### Bonus Question: What is the difference between a Service and a Resource?

After reading: https://docs.datadoghq.com/tracing/visualization/#services

Services act as building blocks for microservice architectures, such as a MySQL database or a group of URL endpoints, while Resources are the actions that take place within a service such as a background job or query of the application.

## Final Question
Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?

I believe an interesting way that I could use Datadog is to monitor the consumption of pre-made food I ingest on a weekly basis. I try prepare my meals on Sunday in big batches so I do not have to cook throughout the week for lunch and dinner. I have noticed that some weeks I run out of food, while other weeks I have excess(I am fairly consistent on how much food I buy each week and I hate wasting food!) The goal here would be able to create a correlatation with my workouts/daily behavior and food consumtion, in order to optomize my food preperation process. This would allow me to predict how much food I need for an upcoming week based on planned workout/daily activities. I figured this could be achieveable by monitoring the weight of my refrigerator shelf using a scale, raspberry Pi, and Python code to import the data into Datadog for monitoring, as well as cross referencing this data with my workouts/daily activities. I could create thresholds and alerts to let me know if my food is running low. I also read up on forecast monitors and thought this could be useful and incorporated to notify me before my food is gone so I can know exactly when to go shopping again.
