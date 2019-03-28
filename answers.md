# Prerequisites - Setup the environment
[x] You can spin up a fresh linux VM via Vagrant Ubuntu VM 

![vagrant](./screenshots/1-vagrantversion.png)

# 1. Collecting Metrics

### Tasks

    [x] Installed MySQL and integrated with Datadog
    [x] Create custom Agent Check (my_metric) with random value between 0 - 1000
    [x] Submit metric once every 45 seconds (Bonus: change w/o modifying Python check file)


### Screenshots
Host Map and Configuration

![host_map](./screenshots/1-host_map.png)
### Host Map

![Host_map1](./screenshots/1-host_map1.png)
### Host Map 2

![Host_map1](./screenshots/hostnametags.png)

### MySQL Integration

![Host_map2](./screenshots/1_mysql.png)

### MySQL Integration MySql agent check

![agent_check](./screenshots/1_mysql_agentcheck.png)


### Agent Check my_metric

![agent_check](./screenshots/1_Agent_Check.png)

### my_metric yaml

![agent_check](./screenshots/1_Agent_Checkconf.png)


### Questions
Can you change the collection interval without modifying the Python check file you created?
**Answer: Yes. It is configured the min_collection_interval setting to 45 on configuration file /etc/datadog-agent/conf.d/my_metric.yaml.**

# 2. Visualizing Data
### Tasks
    [x] With the Datadog API, create a Timeboard that contains:
    [x] Custom metric (my_metric)
    [x] Database metric w/ anomaly function
    [x] Custom metric w/ rollup function applied to sum up all points for past hour into 1 bucket
    [x] Access Dashboard from Dashboard List in UI:
    [x] Set Timeboard's timeframe to past 5 mins

[Datadog API Script creating Timeboard](scripts/timeboard.py)

  ### Screenshots
  
  #### Timeboard
  ![Timeboard](screenshots/2_timeboard2.png)
 
  #### Graph w/ @ notation to send self  
  ![Graph Snapshot](screenshots/Anomaly_5min_MySQL.png)
  
  ### Questions
   What is the anomaly graph displaying?  
   Answer: **Anomaly detection is designed to assist with visualizing and monitoring metrics that have predictable patterns.The Anomaly graph reveals the anomalies that happens when MySQL database makes commits and show that it is above the trends.**

   # 3. Monitoring Data
  ### Tasks
    [x] Create a new Metric Monitor that watched my_metric and will alert if it's above the following values for the past 5 mins   
    [x] Warning threshold of 500  
    [x] Alerting threshold of 800  
    [x] Notify if there is No Data for the past 10m  
    [x] Configure monitor's message so that it will:   
    [x] Send an email whenever a monitor triggers  
    [x] Create different messages based on warning, alert, no data  
    [x] Include metric value and host IP on Alert  
    [x] Bonus: Schedule 2 downtimes     
            - 7pm - 9am (M - F)   
            - All day Sat and Sun  
  
  ### Screenshots

  #### Monitoring Data
  ![Monitoring Data](screenshots/3_Notification_Entire_infra.png)
  
  #### Monitor Alert
  ![Monitor Alert](screenshots/3_Alert.png)
  
  #### No Data Alert
  ![No Data](screenshots/3_No_Data.png)
  
  #### Downtime (Bonus)
  ![Downtime](screenshots/3_Downtime.png) 

  # 4. Collecting APM Data   
Given an app use Datadog’s APM solution   
Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

[Dashboard Link](https://p.datadoghq.com/sb/ov0483fsnj4ruvv8-bbe1d97bcb9454657c24cb9a41719c1d)

![APM and Infrasctructure](screenshots/4_APM_timeboard_Public_URL.png)

![APM and Infrasctructure](screenshots/4_Public_URL_access.png)
  
### Question: What is the difference between a Service and a Resource? 
A service is a set of processes that do the same job. For instance, a simple web application may consist of two services:

A single webapp service and a single database service.
A Resource is a particular action for a service.

For a web application: some examples might be a canonical URL, such as /user/home or a handler function like web.user.home (often referred to as “routes” in MVC frameworks).
For a SQL database: a resource is the query itself, such as SELECT * FROM users WHERE id = ?.

# 5. Final Question
Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?  

### Amyotrophic Lateral Sclerosis patient to be able to communicate free of human intervention, thus returning the high esteem and making it more independent. 
### Using only eye movements they can access all computer resources and turn on light and TV change channels open doors and so on.
### The solution : Using tobii 4C + Optikey connected to a notebook and DataDog monitoring will help with dashboards to prevent system outage and remote support for this patient.
### Connect Datadog with Mobile Health apps :
        - Track heart beats
        - brain activity
### Connect Datadog Using Behavioral Health Apps in Clinical Practice Using apps in clinical practice can act as a valuable adjunct to psychotherapy. behavioral health apps are beneficial for helping psychologists maintain a better connection with their patients, and improve tracking of :
        - Track patients mood
        - symptoms
### With a system like this is possible to monitor not just computer but health status of patients behavioral health and on the same platform 

Your answers to the questions go here.
