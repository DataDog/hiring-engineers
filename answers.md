## Collecting Metrics:

* **Q1**

  To add tags, I found an article "Assigning tags using the configuration files" in the Docs page (https://docs.datadoghq.com/getting_started/tagging/assigning_tags/assigning-tags-using-the-configuration-files) and configured datadog.yaml to add the region: nsw tag. Please refer to the two screenshots below.

  Screenshot 1: datadog.yaml

  ![](https://github.com/su27k-2003/hiring-engineers/blob/master/image/Collecting_datadog_yaml.PNG)

  Screenshot 2: Host Map (Added the "region:nsw" tag)

  ![](https://github.com/su27k-2003/hiring-engineers/blob/master/image/Collecting_HostMap.PNG)

* **Q2**

  I installed MySQL on my Ubuntu (16.04.4) and I followed the MySQL integration page (https://docs.datadoghq.com/integrations/mysql/) to configure MySQL and the agent. After configuration, I confirmed the dashboard was receiving data from MySQL. Please refer to the two screenshots below.

  Screenshot 1: Configured /etc/datadog-agent/conf.d/mysql.d/conf.yaml

  ![](https://github.com/su27k-2003/hiring-engineers/blob/master/image/Collecting_mysql_conf.PNG)

  Screenshot 2: MySQL dashboard

  ![](https://github.com/su27k-2003/hiring-engineers/blob/master/image/Collecting_mysql.PNG)

* **Q3**

  To create a custom Agent check, I followed the Docs page (https://docs.datadoghq.com/developers/agent_checks/) and created mycheck.yaml and mycheck.py then configured the two files accordingly. Please refer to the two screenshots below. 

  Screenshot 1: Created and configured /etc/datadog-agent/conf.d/mycheck.yaml

  ![](https://github.com/su27k-2003/hiring-engineers/blob/master/image/Collecting_custom_check_1.PNG)

  Screenshot 2: Created and configured /etc/datadog-agent/checks.d/mycheck.py

  ![](https://github.com/su27k-2003/hiring-engineers/blob/master/image/Collecting_custom_check_2.PNG)

* **Q4**

  I used time.sleep function in mycheck.py to make the 45 seconds time delay to data collection interval. Please refer to the screenshot below.

  Screenshot: Added time delay function into the /etc/datadog-agent/checks.d/mycheck.py

  ![](https://github.com/su27k-2003/hiring-engineers/blob/master/image/Collecting_custom_check_3.PNG)

* **Bonus Question**

  We also could change the data collection interval by configuring min_collection_interval in the mycheck.yaml file. Please refer to the screenshot below.

  Screenshot: Added min_collection_interval to the /etc/datadog-agent/conf.d/mycheck.yaml

  ![](https://github.com/su27k-2003/hiring-engineers/blob/master/image/Collecting_custom_check_4.PNG)



## Visualizing Data:

* **Q1**

  I created a timeboard which collected data of the custom metric: my_metric we just created in the previous step by submitting the Python code below and confirmed the timeboard worked as expected. Please refer to the screenshot and the Python code below. This page (https://docs.datadoghq.com/api/?lang=python#create-a-timeboard) gave me lots of useful information about how to use the Datadog API.

  Screenshot: My_metric in the timeboard just created.

  ![](https://github.com/su27k-2003/hiring-engineers/blob/master/image/Visualizing_2.PNG)	

  Python code: /code/Create_timeboard.py

```
from datadog import initialize, api

options = {
    'api_key': '',
    'app_key': ''
}

initialize(**options)


# Create a new Timeboard
title = "Show my_metric"
description = "For the home challenge"
graphs = [{
    "definition": {
        "events": [],
        "viz": "timeseries",
        "requests": [
            {"q": "my_metric{host:deep-learning-virtual-machine}",
            "type": "line",
            "style": {
                "palette": "dog_classic",
                "type": "solid",
                "width": "normal"},
            "conditional_formats": [],
            "aggregator": "avg"
            },
        ],
    },
    "title": "My Metric (custom metric)"
}]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:my-host"
}]

read_only = True

api.Timeboard.create(title=title,
                        description=description,
                        graphs=graphs,
                        template_variables=template_variables,
                        read_only=read_only)
```


* **Q2**

  I randomly picked mysql.net.connections as the metric to apply anomaly function (https://docs.datadoghq.com/monitors/monitor_types/anomaly/). Unfortunately, I couldn't find the way to add the mysql.net.connections metric to the timeboard I just created in the last step. It seems the anomaly function only could apply to the monitor so I created a monitor instead of timeboard in this step. Please refer to the screenshot and the Python code below. If I missed something, please point me to the right direction and let me know. Thank you.
  
  Screenshot: Anomaly function applied to the mysql.net.connections metric

  ![](https://github.com/su27k-2003/hiring-engineers/blob/master/image/Visualizing_4.PNG)

  Python code: /code/Create_monitor_with_anomaly_function.py

```
from datadog import initialize, api

options = {
    'api_key': '',
    'app_key': ''
}

initialize(**options)

# Create a new monitor with the anomaly function applied
options = {
    "notify_no_data": True,
    "no_data_timeframe": 20
}
tags = ["anomaly"]

api.Monitor.create(
    type="metric alert",
    query="avg(last_4h):anomalies(avg:mysql.net.connections{host:deep-learning-virtual-machine}, \
     'basic', 2, direction='both', alert_window='last_15m', interval=60, count_default_zero='true') >= 1",
    name="Anomaly Function (MySQL Net-connections)",
    message="Alert test",
    tags=tags,
    options=options
)
```


* **Q3**

  This page (https://docs.datadoghq.com/graphing/miscellaneous/functions/#rollup-1) guided me on how to use rollup function to sum up data and I applied it to the custom metric (my_metric) from the host:deep-learning-virtual-machine. Please refer to the screenshot and the Python code below. 
  
  Screenshot: rollup function applied to the my_metric

  ![](https://github.com/su27k-2003/hiring-engineers/blob/master/image/Visualizing_6.PNG)

  Python code: /code/Create_timeboard.py

```
from datadog import initialize, api

options = {
    'api_key': '',
    'app_key': ''
}

initialize(**options)


# Create a new Timeboard
title = "Show my_metric"
description = "For the home challenge"
graphs = [{
    "definition": {
        "events": [],
        "viz": "timeseries",
        "requests": [
            {"q": "my_metric{host:deep-learning-virtual-machine}",
            "type": "line",
            "style": {
                "palette": "dog_classic",
                "type": "solid",
                "width": "normal"},
            "conditional_formats": [],
            "aggregator": "avg"
            },
            {"q": "sum:my_metric{host:deep-learning-virtual-machine}.rollup(sum, 3600)",
            "type": "line",
            "style": {
                "palette": "orange",
                "type": "solid",
                "width": "normal"}
            }
        ],
    },
    "title": "My Metric (custom metric)"
}]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:my-host"
}]

read_only = True

api.Timeboard.create(title=title,
                        description=description,
                        graphs=graphs,
                        template_variables=template_variables,
                        read_only=read_only)
```


* **Q4**

  Screenshot 1: Graph of the timeboard

  ![](https://github.com/su27k-2003/hiring-engineers/blob/master/image/Visualizing_7.PNG)

  Screenshot 2: @ notation 

  ![](https://github.com/su27k-2003/hiring-engineers/blob/master/image/Visualizing_9.PNG)

* **Bonus Question**

  We use Anomaly Detection to identify when a metric is behaving differently to it has in the past, taking into account trends, seasonal day-of-week and time-of-day patterns. From the graph below we can see the algorithm is monitoring historical data to calculate the metric’s expected normal range of behaviour.

  Screenshot: Anomaly graph

  ![](https://github.com/su27k-2003/hiring-engineers/blob/master/image/Visualizing_8.PNG)
 

## Monitoring Data

* **Q1**

  Please refer to the two screenshots below or my account (liuqi_jp@hotmail.com) to check the metric monitor I created. I followed this Docs page (https://docs.datadoghq.com/monitors/notifications/) to created the monitor.

  Screenshot 1: Creating the monitor

  ![](https://github.com/su27k-2003/hiring-engineers/blob/master/image/Monitoring_2.PNG)

  Screenshot 2: Email notification

  ![](https://github.com/su27k-2003/hiring-engineers/blob/master/image/Monitoring_1.PNG)

* **Bonus Question**

  I followed this page in Docs https://docs.datadoghq.com/monitors/downtimes/ and created the two downtimes. Please refer to the two screenshots below.

  Screenshot 1: Downtime from 7pm to 9am daily on M-F

  ![](https://github.com/su27k-2003/hiring-engineers/blob/master/image/Downtime_1.PNG)

  Screenshot 2: Downtime all day on Sat-Sun

  ![](https://github.com/su27k-2003/hiring-engineers/blob/master/image/Downtime_2.PNG)


## Collecting APM Data:

* **Bonus Question**

  Service is a set of processes that do the same job. For instance, a simple web application may consist of two services: a single webapp service and a single database service.
  
  Resource is a particular action for a service. For a web application: some examples might be a canonical URL, such as /user/home or a handler function like web.user.home. For a SQL database: a resource is the query itself, such as SELECT * FROM users WHERE id = ?.

* **Q1**

  Please refer to the link and the screenshot below:
  
  https://p.datadoghq.com/sb/1d199b067-1878f66f0cbee4b76c9a3de718a749bd?tv_mode=true
  
  Screenshot: APM and Infrastructure Metrics
  ![](https://github.com/su27k-2003/hiring-engineers/blob/master/image/Collecting_APM_1.PNG)
  

* **Q2**

  I used the Python sample code (Flask app) to create the APM.  
 
 
## Final Question:

 I’m very interested in IoT and I have developed a few Raspberry Pi based home automation projects such as smart garage door (Demo: https://youtu.be/OaJwVSyagKI) and home security camera. I’m aiming to build a smart home by myself as it could make life easier for my family and improve my technical skills.

 While developing these projects, I found a few pain points and I think Datadog could help me to resolve/improve it.

 * Analysing issues

 For example, on the smart garage door project sometimes I found the smart garage door system did not work properly for some reason. The issue could be a communication issue between my phone and the Raspberry Pi (HTTP sending/receiving) or bugs in the script I developed and even the Raspberry Pi itself. Usually it’s not easy to figure out the root cause so I spent a lot of time on troubleshooting and debugging and found a way to determine and fix issues by sending out notification from each function in the system to trace which part caused the issue.
 Now, I could create a dashboard in Datadog which include Infrastructure Metrics of Raspberry Pi and APM for the Flask application I developed, those data could help me to understand the current system state easily also allow me to quickly determine which part of the system didn't function when issue occurred. For example, if I still could receive those infrastructure metrics data from the Raspberry Pi but the APM didn't show the proper data I would check any potential communication issues such as the mobile data function had been turned off in my phone. If it wasn't a communication issue then I would look into the Flask as the next step to find the root cause.  
               
 * Integrate separate data into a single smart home system monitor

 There are a few smart home projects I’m running at home and different project generates their own data in different UI. For example, I have to check room temperature by ssh to the Raspberry Pi remotely every time and use VNC to access the Raspberry Pi if I need to check the security camera video. 
I believe that I can send these data to Datadog and integrate them into a single smart home system dashboard which includes all data I need to improve system visibility and make my life easier.
Unfortunately, I cannot provide a demo and show the possibility of Datadog could bring to me as it needs some time to complete but I will find some time to achieve this and share it with you.
