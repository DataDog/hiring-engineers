Your answers to the questions go here.  
ENVIRONMENT:  
    •	vagrant  
    •	ubuntu-xenial 16.04  
    •	python3  
    •	mysql  
      
Install the datadog agent 
![installagent](screenshots/installagent.png)  
  
Datadog welcome page  
![welcome](screenshots/welcome.PNG)  
  
COLLECTING METRICS:  
  
Creating a new metric called "my_metric"    
![checkvalue_py](screenshots/checkvalue_py.png)  

Config file for the new metric (Change your check's collection interval so that it only submits the metric once every 45 seconds.)   
![checkvalue_config](screenshots/checkvalue_config.png)  
  

Bonus Question Can you change the collection interval without modifying the Python check file you created?  
Yes, you can change the collection interval changing the config file instead  of the python file.  

VISUALIZING DATA:  
  
Script to create a timeboard via the datadog API  
![timeboard_create](screenshots/timeboard_create.PNG)  
  
Monitor created via the API.  
![my_metric_dashboard](screenshots/my_metric_dashboard.PNG)  
  
Bonus Question: What is the Anomaly graph displaying?  
Nothing.  
  
MONITORING DATA:  
  
Monitor the my_metric creating alarms and warnings  
![my_metric_monitor](screenshots/my_metric_monitor.PNG)  
  
Email1  
![email1](screenshots/email1.png)  
  
Email2  
![email2](screenshots/email2.png)  
  
Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor.  
Adding two schedule downtime rules:  
1.- rule for the week  
![schedule2](screenshots/schedule2.png)  
  
2.- rule for the weekend  
![schedule1](screenshots/schedule1.png)  
  
COLLECTING DATA APM:  
Run the phthon as "ddtrace-run python3 apm.py"  
  
Dashboard with the apm traces and infrastructure  
![apm1](screenshots/apm1.png)  
  
Service "flask"  
![apm2](screenshots/apm2.png)  
  
Bonus Question: What is the difference between a Service and a Resource?  
•	Service: A service is a set of processes that do the same job. For instance, a simple web application may consist of two services: A single webapp service and a single database service.  
•	Resource: A resource is a particular action for a service.   
For a web application: some examples might be a canonical URL, such as /user/home or a handler function like web.user.home (often referred to as “routes” in MVC frameworks).  
For a SQL database: a resource is the query itself, such as SELECT * FROM users WHERE id = ?  
