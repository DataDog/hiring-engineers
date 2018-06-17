# Hiring-Engineers(Solution Engineer)


## Environment:

 I used **Google Cloud** to create two virtual machines. One has **windows Server 2016** operating system and other has **Ubuntu 16.04 LTS**




## 1.Collecting Metrics:


### Question 1:  Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.



I have used two VM's.

For the windows machine, i have done the following : 

 Updated the *datadog.yaml* file in *C:\ProgramData\Datadog* folder with the following tags
 1. ddWindowsMachine
 2. env:GoogleCloudVM

 > ![gui of agent](images/1.Q1-datadog-gui-screenshot-tags.PNG)

 For the Ubuntu machine, i have done the following :
updated the *datadog.yaml* file in */etc/datadog-agent* with the following tags
1. ddUbuntuMachine
 2. env:GoogleCloudVM
> ![Ubuntu Tags](images/ubuntu_datadog_yaml_tag.PNG)



**In the browser under Host map, the tags were reflecting after i restarted agent.**

> ![Browser windows tag](images/2.Q1-datadog-dashboard-screenshot-tags.PNG)



Note: i created two VM's so that i can actually see the use of tag's. 

So, i tried to group hosts on google cloud and it was really helpful. below is the screenshot of the same

![Group by tag](images/Q1-Hosts-filtered-by-tag.PNG)


## Question 2 : Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

I have  installed mongoDB on windows and postgresql on Ubuntu and integrated both.

**MongoDB:**

Result of *agent status* for mongoDB : 

![mongoDB status](images/3.Q2-datadog-status-screenshot-mongo.PNG)

Success message on Integration of mongoDB in browser:

![mongoDB browser](images/4.Q2-datadog-dashboard-screenshot-mongo.PNG)


**Postgresql**

Result of *agent status* for postgresql

![Postgresql status](images/3.Q2-datadog-status-screenshot-postgres.PNG)

Success message on integration of postgresql in browser

![Postgresql browser](images/4.Q2-datadog-dashboard-screenshot-postgres.PNG)



## Question 3 : Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

I used ubuntu machine to do this.
I created a *my_metric.yaml* file in */etc/datadog-agent/conf.d* with text as shown in  below image

![my_metric_conf_yaml](images/yaml_conf_mymetric.PNG)

created a *my_metric.py* file in */etc/datadog-agent/checks.d* with code as shown in below image

![my_metric_code](images/my_metric_code.PNG)

When i ran `sudo -u dd-agent -- datadog-agent check my_metric`  i got the following output

![my_metric output](images/7.Q3-datadog-my_metric_check-screenshot.PNG)

I checked the same in my dashboard and its as shown below

![my_metric dashboard](images/7.Q3-datadog-my_metric_dashboard.PNG)

So, custom metric is being recorded.

## Question 4: Change your check's collection interval so that it only submits the metric once every 45 seconds.

I updated my_metrics.py file  as shown below 

![my_metrics 45 delay](images/8.Q4-datadog-my_metric_code_45sec_delay.png)

The following was the output when i ran `sudo -u dd-agent -- datadog-agent check my_metric`

![my_metric 45 delay status](images/9.Q4-datadog-my_metric_check_45sec_delay.PNG)

As seen in the above image, it took 45 seconds pause. so, Success!


## Bonus Question : Can you change the collection interval without modifying the Python check file you created?

Yes, by modifying my_metrics.yaml file to as shown below, i was able to add interval without modifying python check file

![my_metric 45 delay conf](images/yaml_conf_45_delay.PNG)



# Visualizing Data:


## Question : Utilize the Datadog API to create a Timeboard that contains:

* Your custom metric scoped over your host.
 * Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
![timeboard code my metric](images/timeboard_my_metric_code.PNG)

Timeboard of my_metric in the browser

![timeboard graph](images/custom_metric_dashboard.PNG)

* Any metric from the Integration on your Database with the anomaly function applied.
* ![Timeboard code for mongo](images/timeboard_api_mongo_code.PNG)

Timeboard of mongoDB in browser:
![Timeboard mongo graph](images/mongodb.PNG)












## Question : Once this is created, access the Dashboard from your Dashboard List in the UI:

* Set the Timeboard's timeframe to the past 5 minutes
For Custom timeboard
![5 min timeframe](images/CustomMetric - 5 min timeframe.PNG)

For mongoDB timeboard:
![5 min mongo](images/MongoDB-5 min timeframe.PNG)

* Take a snapshot of this graph and use the @ notation to send it to yourself.

For custom metric:
![mail custom metric](images/CustomMetric - 5 min timeframe - mail.PNG)

for mongo metric:
![mail mongo metric](images/MongoDB-5 min timeframe - mail.PNG)




* **Bonus Question**: What is the Anomaly graph displaying?

I have refered [THIS](https://docs.datadoghq.com/monitors/monitor_types/anomaly/) to understand the concept. According to the documentation, the data that do not fit the norm based on different algorithms are marked as anomaly. 



## Monitoring Data

### Question : Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

* Warning threshold of 500
* Alerting threshold of 800
* And also ensure that it will notify you if there is No Data for this query over the past 10m.

The following image shows above three settings
![Monitoring thresholds](images/Monitoring-1-setting_thresholds.PNG)



### Question : Please configure the monitor’s message so that it will:

* Send you an email whenever the monitor triggers.
* Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
* Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.

The following image shows above three settings:
![Monitoring-2](images/monitoring-2.PNG)


* Monitoring email notification Screenshots:

Warning mail:

![Monitoring-email-1](images/warning_monitoring.PNG)

Recovered from warning-  Email: 
![Monitoring-recovered-mail-1](images/recovered_monitoring_mail.PNG)




### Bonus Qustion: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

* One that silences it from 7pm to 9am daily on M-F,
* Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.
![M-F downtime](images/Downtime-7to9.PNG)

Mail- Screenshot
![M-F downtime Mail](images/Downtime-7to9 - Mail.PNG)

* And one that silences it all day on Sat-Sun.
* Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

![Weekend-downtime](images/Downtime-Weekend.PNG)

Mail- Screenshot

![Weekend-downtime mail](images/Downtime-Weekend - Mail.PNG)



# Collecting APM Data:

I used provided Flask App. The dashboard generated for this section has number of requests and the durations.

flask_code.py
![apm_code](images/apm_flask.PNG)


**Dashboard of APM**

![apm_flash dashboard](images/apm_python_flask.PNG)

link to dashboard: https://app.datadoghq.com/apm/service/flask/flask.request?start=1529263046666&end=1529277446666&env=none&paused=false

### Bonus Question: What is the difference between a Service and a Resource?

A service is a set of processes that caries out a functionality. where as resource is the point of action for a service. for example, rest service could be a flask application running and this is a service. A JSON response is the resource.


# Final Question: Is there anything creative you would use Datadog for?

I think datadog will be extremely helpful where everything needs to be tracked. i think, this can be extremely useful, if its paired with AI,computer vision. Lets say, we have a AI system that does object detection. So, the dashboard will be showings number of objects detected(Could be used to monitor traffic). Number of Human's or animals. Number of trucks, and so on. 