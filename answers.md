I would like to start off my saying, this is the more interesting and intuitive techinal hiring exercise I have taken. Thanks much for give the opportunity.

Note: All the screenshots are in the Screenshots Folder. And the scripts are in the folder Code.

### Setup the environment

I had setup two Ubuntu 16.04 enviroments just to see variations in the setup.
  - On Windows 10 using Virtual box.
  - On Mac OS with Vagrant(Virtual Box as provider for base env)
  
  
  
### Collecting Metrics

  - Installed Datadog agent on both the VM's
  - Created custom tags for both the agents 
  - Observed both the agents reporting on the Host Map page on Datadog website.
  - Screenshot 1 - Both hosts on the HostMap (hiring-engineers/Screenshots/HostMap.png)
  - Screenshot 2 - Host with custom tags created in the datadog.yaml file (hiring-engineers/Screenshots/HostMap_with_tags.png)
      
  
  - Installed Postgres database and installed the respective integration from the Integrations page in Datadog.
  - Screenshot 3 - postgres agent reporting to the datadog (hiring-engineers/Screenshots/Database inegration -postgres.png)
      
  
  - Created a custom agent check python file in the /datadog-agent/checks.d/ and its respective config file with the custom interval in the /datadog-agent/conf.d/
  - Verified that the agent config file is good by running "datadog-agent configcheck"
    Screenshot for the above is in the file (hiring-engineers/Screenshots/Custom_metric with interval.png)
    The python code and the configuration yaml file is in (hiring-engineers/Code/my_metric.py) and (hiring-engineers/Code/my_metric.yaml)
  - Verfied that the custom metric created reports the value to the datadog collection, on the datadog Host Map page.
    Screenshot for the above is in the file (hiring-engineers/Screenshots/Custom_metric.png)
    
    
    Bonus Question: Can you change the collection interval without modifying the Python check file you created?
      - Yes, it possible to change the collection interval in the configuration file in the /datadog-agent/conf.d/
       
       
       
       
### Visualizing Data


  - Time board with name Aishwarya_TimeBoard with required content was created.
    Screenshot with the above is in the file (hiring-engineers/Screenshots/Timeboard.png)
  
  - The python script and json(for timeboard) used for all three timeboards are in files in the folder hiring-engineers/Code
        - Timeboard_script.py
        - Custom_metric_TB.json
        - Custom_metric_Rollup_TB.json
        - Database_metric_anamoly_TB.json
        
  - Changed the timeboard's timeframe to the past 5 minutes and sent it to myself.
      - Screenshot with 5 mins timeframe (hiring-engineers/Screenshots/Timeboard_5mins.png)
      - Screenshot with the snapshot to myself (hiring-engineers/Screenshots/Snapshot_to_self.png)

    Bonus Question: What is the Anomaly graph displaying?
      - The anamoly graph displays any deviation of metrics from the normal average. In my case, I used the Postgres checkpoint function as input, it perform a check between the data file and write ahead log every five minutes. So we got a graph that spikes every five minutes. And it is caught as a anomaly by the graph.
      
      

### Monitoring Data

  - The monitor has been created for the custom metric with the required configurations:
      Warning threshold of 500
      Alerting threshold of 800
      And also ensure that it will notify you if there is No Data for this query over the past 10m.
      
      Screenshot for the above is in the file (hiring-engineers/Screenshots/Metric_config.png)
      Screenshot for monitoring warning event notification to Email (hiring-engineers/Screenshots/Metric_monitor_email_warn.png)
      Screenshot with the notification from the monitor is in file (hiring-engineers/Screenshots/Metric_monitor_event_warn.png)
      
    Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the   office. Set up two scheduled downtimes for this monitor:

           - One that silences it from 7pm to 9am daily on M-F,
           - And one that silences it all day on Sat-Sun.
           - Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

      
     The above was achieved by creating the downtime schedule. Screenshots attached for the same.
     
       Screenshot for downtime schedule for weekends and weekdays are in (hiring-engineers/Screenshots/Monitor_downtime_datadog.png) and (hiring-engineers/Screenshots/Monitor_downtime_datadog1.png)
       Screenshot for email notification of the schedule change and start of the schedule are in files (hiring-engineers/Screenshots/Downtime_email_notification_weekdays.png) and (hiring-engineers/Screenshots/Downtime_email_notification_weekends.png)
       
       
       
       
### Collecting APM Data


  An app was created using the basic framework given hiring exercise.
  Attached the screenshot for curl commands is in file (hiring-engineers/Screenshots/app_curl.png)
  Screenshot of APP metrics in the APM page in Datadog is in (hiring-engineers/Screenshots/app_apm_page.png)

  The code for the app is included in the Code folder here (hiring-engineers/Code/apm_app.py)

  Bonus Question: What is the difference between a Service and a Resource?
    - Service is a process that is run to accomplish a particular objective. A service is dependant on resources.
      Resource are elements required for a service to run. Like memory, cpu and or even a config file.


  
