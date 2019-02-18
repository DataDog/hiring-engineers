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
  
 [mysql conf file](https://user-images.githubusercontent.com/47703847/52919061-3bd45880-32cc-11e9-9129-c03a3ab658d5.png)
 
Output:

![user datadog in mysql](https://user-images.githubusercontent.com/47703847/52916498-323bf800-32ae-11e9-80ee-a78af8e42142.png)

![mysql installed](https://user-images.githubusercontent.com/47703847/52917191-6c10fc80-32b6-11e9-84f1-9b489e548c6a.png)

![mysql configured and datadog reporting mysql metrics](https://user-images.githubusercontent.com/47703847/52917219-e3df2700-32b6-11e9-9d77-9340b27031e7.png)
 
3. Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

Answer:  
step 1: Created custom_test.py file in /etc/datadog-agent/checks.d 

       [Python Script](https://github.com/srp84/hiring-engineers/blob/master/custom_test.py)
       
step 2:Created custom_test.yaml file in /etc/datadog-agent/conf.d

       ![custom agent check input in yaml file](https://user-images.githubusercontent.com/47703847/52919311-2280db80-32cf-11e9-91cd-2c8b08fb1e67.png)
       
step 3:Run Agent Check:
       sudo -u dd-agent -- datadog-agent check custom_test
       
       ![output of agent-check 1](https://user-images.githubusercontent.com/47703847/52919212-f9ac1680-32cd-11e9-811f-79d236d36411.png)
       
       ![output of agent check 2](https://user-images.githubusercontent.com/47703847/52919214-fdd83400-32cd-11e9-8810-8674bc1014e3.png)
       
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

![snapshot of graph and email you](https://user-images.githubusercontent.com/47703847/52928565-67783280-330e-11e9-8307-4a42b6f6637a.png)

![email of graph snapshot](https://user-images.githubusercontent.com/47703847/52928575-719a3100-330e-11e9-86c0-7e7acbb8d914.png)

Bonus Question: What is the Anomaly graph displaying?
Answer:





## MONITORING DATA:

1. Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

>> Warning threshold of 500
>> Alerting threshold of 800
>> And also ensure that it will notify you if there is No Data for this query over the past 10m.

Answer: Went to the Create Monitor section on datadog UI
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

ANSWERS: The host ip was determined by navigating datadog's UI Infrastructure list >> Inspect shruti-VirtualBox >> system info >> network as 10.0.2.5
As seen in the image my_metric was > 800.0

Input:

![alert message with host ip input](https://user-images.githubusercontent.com/47703847/52931384-20903a00-331a-11e9-8b5c-d48e36455163.png)

Output:

![alert message with host ip output](https://user-images.githubusercontent.com/47703847/52931400-2c7bfc00-331a-11e9-8182-1e3986612cd0.png)






        
 

