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
Output:! 
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
Answer: Clicked on the camera button on each graph 
        
 

