Your answers to the questions go here.

Install Datadog Agent to virtual machine:
[Install of DDAgent](screenshots/agentInstall/installddagent)
[Agent is running](screenshots/agentInstall/agentinstallcomplete)



COLLECTING METRICS:
  Adding Tags:
  #Adding the tags on individual lines did not work for me for some reason. After the tags were added and datadog.yaml saved, I would receive an error that the the config file could not be loaded due to an error on the datadog.yaml. Adding the tags on a single line worked for me.
  [Opening the datadog.yaml file for edit](screenshots/collectingMetrics/opendatadogyaml)
  [My tags added to datadog.yaml](screenshots/collectingMetrics/tags)
  [View of my Host Map with new created tags](screenshots/collectingMetrics/hostmapwithtags)

  Installing MySQL database:
  Following the instructions on ubuntu.com, I installed MySQL on my virtual machine by running: 'sudo apt install mysql-server' from the command line

[Installing MySQL](screenshots/collectingMetrics/mysqlinstall)
  [Confirming MySQL server is running](screenshots/collectingMetrics/confirmmysql)
  [Confirming datadog as user, grants and privileges](screenshots/collectingMetrics/mysqlconfirmuser)
  [Grant datadog grants to ddtestdb and performance schema](screenshots/collectingMetrics/mysqlgrants)


#Had issues with the mysql.yaml file, so created new with only one instance  
[Config block added to .yaml file located in config.d/mysql.d](screenshots/collectingMetrics/mysqlyaml)
[Status check of MySQL(not sure about the warning)](screenshots/collectingMetrics/mysqlstatuscheck)



  Create a custom Agent Check:
[Creating a custom Agent Check py file with random value](screenshots/collectingMetrics/mymetricconf)
[Creating a custom Agent Check yaml file with collection interval](screenshots/collectingMetrics/mincollectioninterval45)
[Confirm status of custom metric](screenshots/collectingMetrics/mymetriccheck)

  Bonus:Question Can you change the collection interval without modifying the Python check file you created?
    The collection interval can also be modified via the Datadog UI by:
      filtering the metric summary by your custom metric name, double clicking the metric once it appears,
      clicking the metadata editing icon and entering the desired interval
[Changing the mymetric collection interval via the UI](screenshots/collectingMetrics/metricviaUI)




VISUALIZING DATA:
[Datadog Install for Dogshell wrapper for API](screenshots/visualizingData/datadoginstall)
**Showing that I do understand how the Dogshell wrapper works although I could not figure out the correct JSON syntax to create my Timeboard via the API. Below screenshots confirm Metric created via the API so the configuration is correct.
[Test Metric using API](screenshots/visualizingData/testmetric)
[Test Metric in shown in UI](screenshots/visualizingData/testmetricUI)
[1 of 700 attempts to create a Timeboard via API](screenshots/visualizingData/timeboardviaAPI)
[My_Metric over Host](screenshots/visualizingData/mymetricoverhost)
[Integration Metric with Anomoly](screenshots/visualizingData/anomaly)
[My_Metric with Rollup](screenshots/visualizingData/rollup)
[Timeboard via UI to complete exercise - shows 5min timeframe](screenshots/visualizingData/timeboard)
[Notification](screenshots/visualizingData/notification)

Bonus Question:What is the Anomaly graph displaying?
I used the MySQL.peformance.user-time metric with the Anomaly graph. The Anomaly graph shows when activity is well out of normal bounds and not just flucuations in use. In the case of my graph, the red lines which show really pronounced drops in activity are most likely when I've logged out of the MySQL server for some time.



MONITORING DATA:
[Monitoring Metric and conditions for alerts](screenshots/monitoringData/monitoringmetric)
[Monitoring Metric alerts config](screenshots/monitoringData/monitoringalerts)
[Monitoring Metric email notification](screenshots/monitoringData/emailmonitortrigger)


Bonus:Schedule downtime for Monitor:
[Monitoring downtime Mon-Fri](screenshots/monitoringData/downtimeweekday)
[Monitoring downtime Mon-Fri email notification](screenshots/monitoringData/emaildowntimeweekday)
[Monitoring downtime weekend](screenshots/monitoringData/downtimeweekend)
[Monitoring downtime weekend email notification](screenshots/monitoringData/emaildowntimeweekend)



COLLECTING APM DATA:
  #To complete this section of the the exercise, I used the Flask app provided. For this I needed to install Flask. I used Virtualenv to create a virtual environment and installed Python.
[Flask installed in virtualenv](screenshots/collectingAPMData/flaskinstall)
[Added datadog Flask code to appfile](screenshots/collectingAPMData/flaskapp)
[Installed ddtrace and instrumented Flask app](screenshots/collectingAPMData/ddtraceinstall)
[Flask app served](screenshots/collectingAPMData/flaskapprunning)

***Unforunately, I was never able to see any APM data in the Service window. I could not figure out the issue with my instrumentation. I will include the entire app/instrumentation folder nontheless. I did, at one point see 2 host for each of the virtual environments I created, but the virtual environ for the Flask install no longer shows as a host. Perhaps that's why APM is not working for me.

Bonus:What is the difference between a Service and a Resource?
A service is a set of processes that do the same job. An example would be a simple web application with webapp and databases services.
A resource is a particular action related to a service. An exampe of a resource would be a SQL database query (SELECT * FROM users WHERE id = Dawn). 


FINAL QUESTION:
Every year I make a resolution to spend more time out and about in the city, taking in the wide array of Arts related activities available. I get busy and often miss exhibits and events that I really want to see, or there are fantastic arts events happening that I don't know about until they've ended (for exampe, The Museum of Ice Cream last year). I could use Datadog to monitor the NYC Art Beat API to alert me to upcoming and current Arts events of interest to me. Also, when friends come to town, I could easily have at hand events of interest.




NOTES:
In support of the above work, I am including copies of my mysql.yaml, datadog.yaml, mymetric.yaml, mymetric.py


**Thank you for giving me the opportunity to complete the hiring exercise. I learned a lot and really enjoyed it!