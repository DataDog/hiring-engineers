I would like to start off by saying, this is the most interesting and intuitive techinal hiring exercise I have taken. Thanks much for give the opportunity.

Note: All the screenshots are in the Screenshots Folder. And the scripts are in the folder Code.

### Setup the environment

  I had setup two Ubuntu 16.04 enviroments just to see variations in the setup.
    - On Windows 10 using Virtual box.
    - On Mac OS with Vagrant(Virtual Box as provider for base env)
  
  
  The datadog config file used for this exercise.

  ```yaml
  dd_url: https://app.datadoghq.com

  api_key: b95c8e083ceec42accc4af841d80187d

  skip_ssl_validation: false

  hostname: AishVM-Vagrant

  tags:
    - env:Mac_Vagrant(VB)
    - os:Ubuntu_Xenial
    -


  procfs_path: /proc


  process_config:
    enabled: "true"

  apm_config:
    enabled: true
  ```

  
  
  
### Collecting Metrics

  - Installed Datadog agent on both the VM's
  - Created custom tags for both the agents  
  - Observed both the agents reporting on the Host Map page on Datadog website.
    
  - __`Both the hosts on the Host Map page`__
    
    <img src="https://github.com/aish241093/hiring-engineers/blob/AishwaryaG_Solutions_Engineer/Screenshots/HostMap.png">
    
  - __`Host with custom tags`__
  
    <img src="https://github.com/aish241093/hiring-engineers/blob/AishwaryaG_Solutions_Engineer/Screenshots/HostMap_with_tags.png">
  
  
  - Installed Postgres database and installed the respective integration from the Integrations page in Datadog.
  
  - __`Postgres agent reporting to the datadog`__
  
    <img src="https://github.com/aish241093/hiring-engineers/blob/AishwaryaG_Solutions_Engineer/Screenshots/Database%20inegration%20-postgres.png"> 
  
  - Created a custom agent check python file in the /datadog-agent/checks.d/ and its respective config file with the custom interval in the /datadog-agent/conf.d/
  - Verified that the agent config file is good by running "datadog-agent configcheck"
    
  - __`Screenshot for the config check`__ 
    
    <img src="https://github.com/aish241093/hiring-engineers/blob/AishwaryaG_Solutions_Engineer/Screenshots/Custom_metric%20with%20interval.png">
    
  - __`The python code for the check file`__ 
    ```python
    #!/usr/bin/env python
    __version__="1.0.0.1"

    from checks import AgentCheck
    from random import randint
    class MyMetricCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', randint(0, 1000))
    ```
    
  - __`The configuration yaml file for the same`__
    ```yaml
    init_config:

    instances:
      - min_collection_interval: 45
    ```
    
  - Verfied that the custom metric created reports the value to the datadog collection, on the datadog Host Map page.
    
  - __`Screenshot for the above from Datadog page`__
    
    <img src="https://github.com/aish241093/hiring-engineers/blob/AishwaryaG_Solutions_Engineer/Screenshots/Custom_metric.png">
    
    
  - *__Bonus Question:__ Can you change the collection interval without modifying the Python check file you created?*
      
      __`Yes, it possible to change the collection interval in the configuration file in the /datadog-agent/conf.d/`__
       
       
       
       
### Visualizing Data


  - Time board with name Aishwarya_TimeBoard with required content was created.
  
  - Screenshot for the Timeboard from the Datadog page
    
    <img src="https://github.com/aish241093/hiring-engineers/blob/AishwaryaG_Solutions_Engineer/Screenshots/Timeboard.png">
  
  - __`The python script for all three timeboards`__ 
    ```python
    #!/usr/bin/env python3.6

    from datadog import initialize, api

    options = {
        'api_key': 'b95c8e083ceec42accc4af841d80187d',
        'app_key': '0ee42a306f7a5aab45073e4a30587d5c0eb3408e'
    }

    initialize(**options)

    title = "Aishwarya_TimeBoard"
    description=""
    graphs = [{
      "viz": "timeseries",
      "status": "done",
      "requests": [
        {
          "q": "avg:my_metric{host:AishVM-Vagrant}",
          "type": "line",
          "style": {
            "palette": "dog_classic",
            "type": "solid",
            "width": "normal"
          },
          "conditional_formats": [],
          "aggregator": "avg"
        }
      ],
      "autoscale": true,
      "xaxis": {}
    },{
      "viz": "timeseries",
      "status": "done",
      "requests": [
        {
          "q": "anomalies(avg:postgresql.bgwriter.checkpoints_timed{host:AishVM-Vagrant}.as_count(), 'basic', 2)",
          "type": "line",
          "style": {
            "palette": "dog_classic",
            "type": "solid",
            "width": "normal"
          },
          "conditional_formats": [],
          "aggregator": "avg"
        }
      ],
      "autoscale": true,
      "xaxis": {}
    },{
      "viz": "timeseries",
      "status": "done",
      "requests": [
        {
          "q": "avg:my_metric{host:AishVM-Vagrant}.rollup(sum, 3600)",
          "type": "line",
          "style": {
            "palette": "dog_classic",
            "type": "solid",
            "width": "normal"
          },
          "conditional_formats": [],
          "aggregator": "avg"
        }
      ],
      "autoscale": true,
      "xaxis": {}
    }]

    template_variables = []

    read_only = True

    api.Timeboard.create(title=title,
                         description=description,
                         graphs=graphs,
                         template_variables=template_variables,
                         read_only=read_only)
    ```
        
  - Changed the timeboard's timeframe to the past 5 minutes and sent it to myself.
  
 
 - __`Screenshot of Timeboard with 5 mins timeframe`__ 
  
    <img src="https://github.com/aish241093/hiring-engineers/blob/AishwaryaG_Solutions_Engineer/Screenshots/Timeboard_5mins.png">
      
  
  - __`Screenshot with the Email to myself`__ 
  
    <img src="https://github.com/aish241093/hiring-engineers/blob/AishwaryaG_Solutions_Engineer/Screenshots/Snapshot_to_self.png">

  
  - *__Bonus Question:__ What is the Anomaly graph displaying?*
    
      __`The anamoly graph displays any deviation of metrics from the normal average. In my case, I used the Postgres checkpoint function as input, it perform a check between the data file and write ahead log every five minutes. So we got a graph that spikes every five minutes. And it is caught as a anomaly by the graph.`__

      

### Monitoring Data

  - *The monitor has been created for the custom metric with the required configurations:
      Warning threshold of 500
      Alerting threshold of 800
      And also ensure that it will notify you if there is No Data for this query over the past 10m.*
      
  - __`Screenshot of the monitor config`__
   
   <img src="https://github.com/aish241093/hiring-engineers/blob/AishwaryaG_Solutions_Engineer/Screenshots/Metric_config.png">  
      
  - __`Screenshot for monitoring warning event notification sent to Email`__ 
      
    <img src="https://github.com/aish241093/hiring-engineers/blob/AishwaryaG_Solutions_Engineer/Screenshots/Metric_monitor_email_warn.png">  
      
      
  - __`Screenshot with the warning notification from the monitor in the Datadog events`__
      
    <img src="https://github.com/aish241093/hiring-engineers/blob/AishwaryaG_Solutions_Engineer/Screenshots/Metric_monitor_event_warn.png">  
      
  
  - *__Bonus Question:__ Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:*

       - *One that silences it from 7pm to 9am daily on M-F,
       - And one that silences it all day on Sat-Sun.
       - Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.*

      
  The above was achieved by creating the downtime schedule. Screenshots attached for the same.

  - __`Screenshot for downtime schedule for weekends and weekdays are`__ 
  
  <img src="https://github.com/aish241093/hiring-engineers/blob/AishwaryaG_Solutions_Engineer/Screenshots/Monitor_downtime_datadog.png">
  
  
  <img src="https://github.com/aish241093/hiring-engineers/blob/AishwaryaG_Solutions_Engineer/Screenshots/Monitor_downtime_datadog1.png">
  
  
  
  - __`Screenshot for email notification for the change of schedule and start of the schedule are`__ 
  
  <img src="https://github.com/aish241093/hiring-engineers/blob/AishwaryaG_Solutions_Engineer/Screenshots/Downtime_email_notification_weekdays.png">
  
  
  <img src="https://github.com/aish241093/hiring-engineers/blob/AishwaryaG_Solutions_Engineer/Screenshots/Downtime_email_notification_weekends.png">
       
       
       
### Collecting APM Data


  An app was created based on the framework given in the hiring exercise.
  
  - __`Screenshot for curl commands`__ 
  
  <img src="https://github.com/aish241093/hiring-engineers/blob/AishwaryaG_Solutions_Engineer/Screenshots/app_curl.png">
  
  
  - __`Screenshot of APP metrics in the APM page in Datadog`__ 

  <img src="https://github.com/aish241093/hiring-engineers/blob/AishwaryaG_Solutions_Engineer/Screenshots/app_apm_page.png">


  The code for the app in python
  
  ```python
  from flask import Flask
  import logging
  import sys
  from random import randint
  import datetime


  main_logger = logging.getLogger()
  main_logger.setLevel(logging.DEBUG)
  c = logging.StreamHandler(sys.stdout)
  formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
  c.setFormatter(formatter)
  main_logger.addHandler(c)

  app = Flask(__name__)

  @app.route('/')
  def api_entry():
      return 'Welcome to the Application\nFor date got to navigate to /date\nTo find your lucky number navigate to /lucky :P \n'

  @app.route('/date')
  def date():
      return "The time now is {}\n".format(datetime.datetime.now())

  @app.route('/lucky')
  def lucky():
      return "Your lucky number is {} :-)\n".format(randint(1,9))

  if __name__ == '__main__':
      app.run(host='0.0.0.0', port='8500')
  ```
  
  - __`Screenshot of the Dashboard with both APM and infrastructure metrics`__
  
  <img src="https://github.com/aish241093/hiring-engineers/blob/AishwaryaG_Solutions_Engineer/Screenshots/Dashboard_with_APM.png">
  
  
  - *__Bonus Question:__ What is the difference between a Service and a Resource?*
      
      __`Service is a process that is run to accomplish a particular objective. A service is dependant on resources.
        Resource are elements required for a service to run. Like memory, cpu and or even a config file.`__



### Final Question


Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?

   __`- Use it to visualize JIRA's, to see bug reports and areas of most bugs. Would be really nice to have.`__
   __`- I would like to use the street parking data to create an information map on what is available.'__
     
