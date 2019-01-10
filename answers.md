## Collecting Metrics:  
  
Q) Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.  
  
A) I added some tags to the agent.  #datadog:yuhki, #env:test, #gcp:compute, #os:centos7.    
Please see the screenshot [./CollectingMetrics/appeared_tags_on_Host_Map_page.png](./CollectingMetrics/appeared_tags_on_Host_Map_page.png)    
 
Q)Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.  
Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.  
Change your check's collection interval so that it only submits the metric once every 45 seconds.  
  
A) I created mycheck.yaml and mycheck.py for the custom agent check.  Please see the following files.    
 [./CollectingMetrics/mycheck.yaml  ](/CollectingMetrics/mycheck.yaml)     
 [./CollectingMetrics/mycheck.py  ](./CollectingMetrics/mycheck.py)    
I named the metric my_metric.randomint.

For DB integration, I used MySQL. Please see the below screen shot.   
 [./CollectingMetrics/MySQLOverview.png](./CollectingMetrics/MySQLOverview.png)  

Q) Bonus Question Can you change the collection interval without modifying the Python check file you created?  
  
A) Yes. The interval can be changed in the mycheck.yaml file with min_collection_interval

## Visualizing Data:    
  
Q) Utilize the Datadog API to create a Timeboard that contains:  
-Your custom metric scoped over your host. 
-Any metric from the Integration on your Database with the anomaly function applied.  
-Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket. 
Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.   
Once this is created, access the Dashboard from your Dashboard List in the UI: Set the Timeboard's timeframe to the past 5 minutes.Take a snapshot of this graph and use the @ notation to send it to yourself.  

A) I created CreateTimebaord.py to create the timeboard.  
[./VisualizingData/CreateTimeboard.py](./VisualizingData/CreateTimeboard.py)  
and its screenshot
[./VisualizingData/TimeBoardCreatedByAPI.png](./VisualizingData/TimeBoardCreatedByAPI.png)

For the past 5 min dashboard graph snapshot and how to send the graph to myself, please see the following file.
[./VisualizingData/Snapshot_of_graph_and_use_@notation_to_send_to_myself.png](./VisualizingData/Snapshot_of_graph_and_use_@notation_to_send_to_myself.png)  
  
Q) Bonus Question: What is the Anomaly graph displaying?  
A) The gray band shows the range of expected values computed by an anomaly detection algorithm. If a metric crosses the boundaries of the gray band, it means that the metirc is behaving differently than it has in the past,  

## Monitoring Data  
  
Q) Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:  
Warning threshold of 500  
Alerting threshold of 800  
And also ensure that it will notify you if there is No Data for this query over the past 10m.  
  
Please configure the monitor’s message so that it will send you an email whenever the monitor triggers. Create different messages based on whether the monitor is in an Alert, Warning, or No Data state. Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.  
  
A) Please see the following screenshot and a json file for the monitor setting.   
[./MonitoringData/Monitor_Setting.png](./MonitoringData/Monitor_Setting.png)    
[./MonitoringData/monitor.json](./MonitoringData/monitor.json)  
  
Q) When this monitor sends you an email notification, take a screenshot of the email that it sends you.  
  
A) Please see the following screenshot.   
[./MonitoringData/Monitor_Alert_Email.png](./MonitoringData/Monitor_Alert_Email.png)  
  
Q) Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:One that silences it from 7pm to 9am daily on M-F,And one that silences it all day on Sat-Sun.Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.
  
A)Please see the following screenshot for notification emails.  
[./MonitoringData/DowntimeSetting_NotifyEmail1.png](./MonitoringData/DowntimeSetting_NotifyEmail1.png)      
[./MonitoringData/DowntimeSetting_NotifyEmail2.png](./MonitoringData/DowntimeSetting_NotifyEmail2.png)      

I also took the screen shots for each setting.   
[./MonitoringData/DowntimeSetting1.png](./MonitoringData/DowntimeSetting1.png)      
[./MonitoringData/DowntimeSetting2.png](./MonitoringData/DowntimeSetting2.png)        
  
Please note that UTC+9 hours is my local time(JST).  
So, 10:00pm - 12:00 pm UTC equals 7:00am - 9pm JST,  3:00pm UTC equals 12:00am JST.  
  
## Collecting APM Data:  
 
Q)Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution: 
Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics. Please include your fully instrumented app in your submission, as well.  
 
A)  Please see "Infra-APM-Dashboard.png"  for the Dashbaord screenshot.  
[./CollectingAPMData/Infra-APM-Dashboard.png](./CollectingAPMData/Infra-APM-Dashboard.png)  
  
The dashboard public URL is below.  
https://p.datadoghq.com/sb/c6c89ec8f-dcee1084690f6f76ec4df099926b9516  

I  used  a sample flask app (manage.py) and executed  "ddtrace-run python manage.py".   
I put the whole application file in the following link.  
https://github.com/yuhkih/flask-sqlight-sample   

Q) Bonus Question: What is the difference between a Service and a Resource?  
A) Service is a set of process working together to provide a feature like a WebServer, a DB Server.  Resource is a particular query to a service. 
For example, if there is a "DB Server" service, the resource would be a SQL query to the "DB Server" service.

## Final Question:  
  
Q) Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability! Is there anything creative you would use Datadog for?   
  
A) Monitoring a remaining amount of ink and papers in copy machines. Rental cars, taxies monitoring via a LTE network to monitor battery level, fuel level, overall health status and latest GPS location.  
