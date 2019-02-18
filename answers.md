# ANSWERS

## COLLECTING METRICS:

1. Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

Answer: Input: Added tags as input in agent config file that is datadog.yaml file. 

![assisgning tags input](https://user-images.githubusercontent.com/47703847/52916135-e8511300-32a9-11e9-85a5-7937532162bb.png)

Output: I have created User tags to play with datadog UI

![host tags and user tags output](https://user-images.githubusercontent.com/47703847/52916383-bab99900-32ac-11e9-8e6f-a722298dbd73.png)

2. Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

Answer: 

Input: Installed mysql on ubuntu by following commands:
               - sudo apt-get update
               - sudo apt-get install mysql-server
               
Installed respective datadog integration for that database and configured it
               - sudo mysql -e "CREATE USER 'datadog'@'localhost' IDENTIFIED BY '<UNIQUE PASSWORD>';"
               - sudo mysql -e "GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'127.0.0.1' WITH MAX_USER_CONNECTIONS 10;"
               - sudo mysql -e "GRANT PROCESS ON *.* TO 'datadog'@'127.0.0.1';"
               - sudo mysql -e "GRANT SELECT ON performance_schema.* TO 'datadog'@'127.0.0.1';"
  
/etc/datadog-agent/conf.d/mysql.d file:
  
![mysql conf file](https://user-images.githubusercontent.com/47703847/52919061-3bd45880-32cc-11e9-9129-c03a3ab658d5.png)
 
Output:

datadog user included in all mysql users

![user datadog in mysql](https://user-images.githubusercontent.com/47703847/52916498-323bf800-32ae-11e9-80ee-a78af8e42142.png)

mysql installed shown on UI

![mysql installed](https://user-images.githubusercontent.com/47703847/52917191-6c10fc80-32b6-11e9-84f1-9b489e548c6a.png)

mysql metrics reported in summary 

![mysql configured and datadog reporting mysql metrics](https://user-images.githubusercontent.com/47703847/52917219-e3df2700-32b6-11e9-9d77-9340b27031e7.png)
 
3. Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

Answer:  
step 1: Created custom_test.py file in /etc/datadog-agent/checks.d 

[Python Script](https://github.com/srp84/hiring-engineers/blob/master/custom_test.py)
       
step 2:Created custom_test.yaml file in /etc/datadog-agent/conf.d

[Python Script](https://github.com/srp84/hiring-engineers/blob/master/custom_test.yaml)
       
step 3:Run Agent Check:
       sudo -u dd-agent -- datadog-agent check custom_test
       
![output of agent-check 1](https://user-images.githubusercontent.com/47703847/52939745-e5e6cb80-3332-11e9-8ee2-be353b22cce2.png)
       
![output of agent check 2](https://user-images.githubusercontent.com/47703847/52939760-ec754300-3332-11e9-88e1-72f177e986cf.png)
       
step 4:It was successfully implemented and available in metrics summary

![my_metric image](https://user-images.githubusercontent.com/47703847/52919267-86ef6b00-32ce-11e9-9b42-f235a956c488.png)
       
4. Change your check's collection interval so that it only submits the metric once every 45 seconds.

Answer:This answers the BONUS QUESTION too.
Changes made in /etc/datadog-agent/conf.d/custom_test.yaml file

[Python Script](https://github.com/srp84/hiring-engineers/blob/master/custom_test.yaml)

## VISUALIZING DATA:

1. Utilize the Datadog API to create a Timeboard that contains:

>> Your custom metric scoped over your host.
>> Any metric from the Integration on your Database with the anomaly function applied.
>> Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

Answer: Created a new python file in /etc/datadog-agent named as new_timeboard.py
        Reffered to API section under DOCS of datadog website.
        Created three different graphs by listing them in graphs: section of python code.
        
Input:  [Python Script](https://github.com/srp84/hiring-engineers/blob/master/new_timeboard.py)

Output: ![three graphs on a timeboard](https://user-images.githubusercontent.com/47703847/52919498-0d0cb100-32d1-11e9-8bd7-a72816122f2c.png)

2. Once this is created, access the Dashboard from your Dashboard List in the UI:

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

Answer: Went to Create Monitor section on datadog UI
Input:

![create monitor input 1](https://user-images.githubusercontent.com/47703847/52928908-0e110300-3310-11e9-8b2b-6b78397363b8.png)

![create monitor input 2](https://user-images.githubusercontent.com/47703847/52928917-15381100-3310-11e9-8231-74ff67ca6e91.png)

![create monitor input 3](https://user-images.githubusercontent.com/47703847/52928920-18cb9800-3310-11e9-83bb-fe50a1afee6a.png)

Please configure the monitor’s message so that it will:

>> Send you an email whenever the monitor triggers.

Answers:

Email Notification i/p:

![email notification input](https://user-images.githubusercontent.com/47703847/52929399-4580af00-3312-11e9-8cc3-f25e2902a514.png)

Triggered Monitor: 

![triggered monitor](https://user-images.githubusercontent.com/47703847/52929427-60532380-3312-11e9-959f-957be231d213.png)

Email of triggered monitor:

![email of triggered monitor](https://user-images.githubusercontent.com/47703847/52929435-6812c800-3312-11e9-931b-546267d90831.png)

>> Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.

Answers: ALERT input 

![alert message input](https://user-images.githubusercontent.com/47703847/52930685-63044780-3317-11e9-8646-a1ff1e6d1523.png)

ALERT output

![alert message email output](https://user-images.githubusercontent.com/47703847/52930687-68619200-3317-11e9-8db4-7914178bc373.png)

WARN input

![warn input](https://user-images.githubusercontent.com/47703847/52930690-6f88a000-3317-11e9-9088-4d88ae3bdacb.png)

WARN output

![warn message output](https://user-images.githubusercontent.com/47703847/52930694-72839080-3317-11e9-9c15-29e359f70853.png)

NO DATA input

![no data input](https://user-images.githubusercontent.com/47703847/52930703-79120800-3317-11e9-9089-7f6dfb3d07b8.png)

NO DATA output

![no data message output](https://user-images.githubusercontent.com/47703847/52930704-7b746200-3317-11e9-985f-8905779d3290.png)

>> Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
>> When this monitor sends you an email notification, take a screenshot of the email that it sends you.

Answers: The host ip was determined by navigating datadog's UI Infrastructure list >> Inspect shruti-VirtualBox >> system info >> network as 10.0.2.5
As seen in the image my_metric was > 800.0

Input:

![alert message with host ip input](https://user-images.githubusercontent.com/47703847/52931384-20903a00-331a-11e9-8b5c-d48e36455163.png)

Output:

![alert message with host ip output](https://user-images.githubusercontent.com/47703847/52931400-2c7bfc00-331a-11e9-8182-1e3986612cd0.png)

>> Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

One that silences it from 7pm to 9am daily on M-F,
And one that silences it all day on Sat-Sun.
Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

Answers:

Schedule M-F 7 pm - 9 am. I tried changing time-zone multiple times but it would just stay America-New_york

Input:

![schedule downtime m-f input 1](https://user-images.githubusercontent.com/47703847/52932673-867ec080-331e-11e9-99c0-02cbe3f2fb59.png)

![schedule downtime m-f input 2](https://user-images.githubusercontent.com/47703847/52932698-a3b38f00-331e-11e9-86bd-5e0bd057f243.png)

Email notification:

![schedule downtime email notification m-f](https://user-images.githubusercontent.com/47703847/52932663-7a92fe80-331e-11e9-961b-0b8c91d0677c.png)

Schedule saturday sunday entire day

Input:

![schedule downtime saturday sunday input](https://user-images.githubusercontent.com/47703847/52932704-ab733380-331e-11e9-9b92-71a67964ed88.png)

Email notification:

![schedule downtime email notification sat-sun](https://user-images.githubusercontent.com/47703847/52932669-82eb3980-331e-11e9-8a1e-5c675b2cde6a.png)

## COLLECTING APM DATA:

>> Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

>> Please include your fully instrumented app in your submission, as well

Answers:

Started collecting traces by running the command
1. pip install ddtrace
2. ddtrace-run python my_app.py

Python script for my_app

[Python Script](https://github.com/srp84/hiring-engineers/blob/master/my_app.py)

Flask App on UI

![flask app](https://user-images.githubusercontent.com/47703847/52937458-23e0f100-332d-11e9-88bc-fb37caac24db.png)

Dashboard with APM and Infrastructure Metrics

![infrastructure and apm graph](https://user-images.githubusercontent.com/47703847/52937469-2d6a5900-332d-11e9-85cd-974fc3ee9f2e.png)

Trace

![apm trace](https://user-images.githubusercontent.com/47703847/52937501-4246ec80-332d-11e9-9d00-1c9026e41049.png)

## FINAL QUESTION:

>> Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!
Is there anything creative you would use Datadog for?

Answer: I think datadog is an interesting tool that provides communication between data in all ways possible. 
According to me, Datadog can be used effectively for analysing human behaviour for Fitbit and keep a track of data about the amount of sleep, the rate of heartbeat, walking data, running data and so on.



        
 

