## Collecting Metrics:

* **Q1**

  To add tags, there are few methods to achieve it such as using the UI or API, though the UI and API only allow us to add tags at the host level. The recommended method is to rely on the integrations or via the configuration files. In this example, I am assigning a new tag "region:nsw" as an agent tag via configuring the datadog.yaml file. Please refer to the two screenshots below.
  
  - 1.Configuration - Create a database user for the Datadog Agent:
  
    Open the datadog.yaml file and define the tag by adding "tags: region:nsw" under the "#Set the host's tags" line.
  
    **Note:** There are two forms to define tags in the configuration files, but datadog.yaml init file only supports the "tags: key_first_tag:value_1, key_second_tag:value_2, ..." form.
  
    Screenshot 1: datadog.yaml

    ![](https://github.com/su27k-2003/hiring-engineers/blob/master/image/Collecting_datadog_yaml.PNG)

  - 2.Confirmation
  
    After a few seconds, confirmed the new tag appeared in the Host Map.
  
    Screenshot 2: Host Map (Added the "region:nsw" tag)

    ![](https://github.com/su27k-2003/hiring-engineers/blob/master/image/Collecting_HostMap.PNG)
  
  - References: [Datadog Docs - Assigning tags](https://docs.datadoghq.com/getting_started/tagging/assigning_tags/#how-to-assign-tags)
  
  
* **Q2**

  I installed MySQL on my Ubuntu (16.04.4) and I followed the MySQL integration page to configure MySQL and the agent. Please refer to the steps below.
  
  - 1.Configuration - Create a database user for the Datadog Agent
  
    Launch MySQL and input the command below:
  
    `mysql> CREATE USER 'datadog'@'192.168.1.5' IDENTIFIED BY 'Su27k2003';`
  
    Then verified the user was created successfully using the following commands.
   
    `mysql -u datadog --password=Su27k2003 -e "show status" | \`
    
    `grep Uptime && echo -e "\033[0;32mMySQL user - OK\033[0m" || \`
    
    `echo -e "\033[0;31mCannot connect to MySQL\033[0m"`
    
    `mysql -u datadog --password=Su27k2003 -e "show slave status" && \`
    
    `echo -e "\033[0;32mMySQL grant - OK\033[0m" || \`
    
    `echo -e "\033[0;31mMissing REPLICATION CLIENT grant\033[0m"`
   
    The Agent needs a few privileges in order to collect metrics. Grant the user the following limited privileges ONLY:
   
    `mysql> GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'192.168.1.5' WITH MAX_USER_CONNECTIONS 5;`
   
    `mysql> GRANT PROCESS ON *.* TO 'datadog'@'192.168.1.5';`
   
    If enabled, metrics can be collected from the performance_schema database by granting an additional privilege:
   
    `mysql> show databases like 'performance_schema';`
    
    `mysql> GRANT SELECT ON performance_schema.* TO 'datadog'@'192.168.1.5';`
   
  - 2.Configuration - Metric Collection
   
    Added the configuration block below to mysql.d/conf.yaml in order to start gathering the MySQL metrics:
   
    Screenshot 1: Configured /etc/datadog-agent/conf.d/mysql.d/conf.yaml

    ![](https://github.com/su27k-2003/hiring-engineers/blob/master/image/Collecting_mysql_conf.PNG)

  - 3.Configuration - Restart the agent
  
  - 4.Confirmation
  
    After configuration, I confirmed the dashboard was receiving data from MySQL. Please refer to the screenshot below.
  
    Screenshot 2: MySQL dashboard

    ![](https://github.com/su27k-2003/hiring-engineers/blob/master/image/Collecting_mysql.PNG)
  
  - References: [Datadog Docs - Mysql](https://docs.datadoghq.com/integrations/mysql/)


* **Q3**

  To create a custom Agent check, I created mycheck.yaml and mycheck.py then configured the two files accordingly. Please refer to the steps and screenshots below. 
  
  - 1.Configuration - Create mycheck.yaml in conf.d directory
 
    As the custom Agent check does nothing more than sending random values for the metric my_metric, mycheck.yaml is very simple, including no real information.
 
    Screenshot 1: Created and configured /etc/datadog-agent/conf.d/mycheck.yaml

    ![](https://github.com/su27k-2003/hiring-engineers/blob/master/image/Collecting_custom_check_1.PNG)

  - 2.Configuration - Create mycheck.yaml in checks.d directory
  
    The check itself inherits from AgentCheck and send a gauge of random value for my_metric on each call. This goes in checks.d/mycheck.py:
  
    Screenshot 2: Created and configured /etc/datadog-agent/checks.d/mycheck.py

    ![](https://github.com/su27k-2003/hiring-engineers/blob/master/image/Collecting_custom_check_2.PNG)
    
  - 3.Confirmation
  
    After configuration, confirmed 'my_metric' appeared in the Metric menu in the UI and was collecting data properly. Please refer to the screenshot below. 
    
    Screenshot: My_metric in the timeboard

    ![](https://github.com/su27k-2003/hiring-engineers/blob/master/image/Visualizing_2.PNG)
    
  
  - **Note:** 
    - The names of the configuration and check files must match. If the check file is called mycheck.py then the configuration file must be named mycheck.yaml.
    - Before running the custom Agent check, it's best to check for exceptions by running the command: `sudo /etc/init.d/datadog-agent info`. It should raise a meaningful exception if there were any improper configuration or programming error resulting in the check failing to collect metrics.
  - References: [Datadog Docs - Writing an Agent check](https://docs.datadoghq.com/developers/agent_checks/)

* **Q4**

  I used time.sleep function in mycheck.py to make the 45 seconds time delay to data collection interval. Please refer to the screenshot below.

  Screenshot: Added time delay function into the /etc/datadog-agent/checks.d/mycheck.py

  ![](https://github.com/su27k-2003/hiring-engineers/blob/master/image/Collecting_custom_check_3.PNG)

* **Bonus Question**

  We also could change the data collection interval by configuring min_collection_interval in mycheck.yaml file. Please refer to the screenshot below.

  Screenshot: Added min_collection_interval to the /etc/datadog-agent/conf.d/mycheck.yaml

  ![](https://github.com/su27k-2003/hiring-engineers/blob/master/image/Collecting_custom_check_4.PNG)
  

****


## Visualizing Data:

* **Q1**

  I created a timeboard which collected data of the custom metric: my_metric just created in the previous step by running Python code below. Please refer to the steps below for detailed information.

  - 1.Check authentication - API and APP keys
  
    As all requests to Datadog’s API must be authenticated, we should confirm the API and APP keys first. Requests that write data require reporting access and require an API key. Requests that read data require full access and also require an application key. The API and APP keys can be found at https://app.datadoghq.com/account/settings#api. 
    
  - 2.Create a Timeboard via Datadog API
  
    There are a few ways to submit Datadog API such as using Curl or Python/Ruby code. 
     
    The "How to" page in the Docs gave me lots of useful information about how to use the Datadog API and I just need to copy the source code from the Docs and modify it accordingly. In this case, I changed the title of the Timeboard to "Show my_metric" and the name of the graph to "My Metric (custom metric)". The most important thing is modifying the "requests" part in "graphs" to add the metric: "my_metric" to the Timeboard.

    Python code: /code/Create_timeboard.py

    ```python
    from datadog import initialize, api

    options = {
        'api_key': '5032023d686e6bd9b5e0b376a59bb27f',
        'app_key': '94846c5a071f7c2dc77381214fed18614987250a'
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

    try:
        api.Timeboard.create(title=title,
                                description=description,
                                graphs=graphs,
                                template_variables=template_variables,
                                read_only=read_only)
    except:
        print 'Error occurred!'
    else:
        print 'Sent API request successfully.'

    '''
    
    
  - 3.Confirmation
  
    - The Datadog API uses HTTP status codes to indicate the success or failure of a request. An error indicates that the service did not successfully handle user's request. The explanation of status codes can be found at https://docs.datadoghq.com/api/?lang=python#success-and-errors.
    
      **Note**: When using libraries, some errors may throw exceptions rather than returning JSON objects, so it's better to use exception in the code to handle errors.  
    
    - I confirmed the timeboard worked as expected. Please refer to the screenshot below.
    
      Screenshot: My_metric in the timeboard just created.

      ![](https://github.com/su27k-2003/hiring-engineers/blob/master/image/Visualizing_2.PNG)
     
  - References: [Datadog Docs - Create a Timeboard](https://docs.datadoghq.com/api/?lang=python#create-a-timeboard)


* **Q2**

  I randomly picked mysql.net.connections as the metric to apply anomaly function. I tried to add the anomalies function to the timeboard I just created in the last step as requested, unfortunately I couldn't find the way to add the mysql.net.connections metric to the timeboard. It seems the anomaly function only could apply to the monitor so I created a monitor instead of timeboard in this step. (If I missed something, please point me to the right direction and let me know. Thank you.) 
  
  To add the anomalies function to the monitor query, it should follows this formula in the API query:
  
  ```
  time_aggr(eval_window_length):anomalies(space_aggr:metric{tags}, 'basic/agile/robust', deviation_number, direction='both/above/below', alert_window='alert_window_length', interval=seconds, count_default_zero='true') >= threshold_value
  ```
  
  In this case, we created a monitor called 
"Anomaly Function (MySQL Net-connections)" with the anomaly function which for the metric: mysql.net.connections. I used "Basic" as the anomaly detection algorithms for test purpose as I don't know whether the metric has seasonal behavior or not. Please refer to the Python code and screenshot below. 
  
  - 1.Create a monitor with anomalies function applied via Datadog API
  
    Python code: /code/Create_monitor_with_anomaly_function.py

    ```python
    from datadog import initialize, api

    options = {
        'api_key': '5032023d686e6bd9b5e0b376a59bb27f',
        'app_key': '94846c5a071f7c2dc77381214fed18614987250a'
    }

    initialize(**options)

    # Create a new monitor with the anomaly function applied
    options = {
        "notify_no_data": True,
        "no_data_timeframe": 20
    }
    tags = ["anomaly"]

	try:
      api.Monitor.create(
          type="metric alert",
          query="avg(last_4h):anomalies(avg:mysql.net.connections{host:deep-learning-virtual-machine}, \
           'basic', 2, direction='both', alert_window='last_15m', interval=60, count_default_zero='true') >= 1",
          name="Anomaly Function (MySQL Net-connections)",
          message="Alert test",
          tags=tags,
          options=options
      )
    except:
    	print 'Error occurred!'
	else:
    	print 'Sent API request successfully.'
    ```
    
    
    **Note**: 
    - Anomaly detection monitors may only be used by enterprise-level customer subscriptions. If you have a pro-level customer subscription and would like to use the anomaly detection monitoring feature, you can reach out to your customer success representative or email Datadog's billing team to discuss that further. 
    - There are three different anomaly detection algorithms we can apply to the function:
      - Basic: Use this algorithm for metrics that have no repeating seasonal pattern.
      - Agile: Use this algorithm for seasonal metrics when you want the algorithm to quickly adjust to level shifts in the metric.
      - Robust: Use this algorithm for seasonal metrics where you expect the metric to be stable and want to consider slow level shifts as anomalies.
  
  - 2.Confirmation
    I confirmed the anomaly detection monitor worked as expected. Please refer to the screenshot below. 
    
    Screenshot 1: Anomaly function applied to the mysql.net.connections metric
    ![](https://github.com/su27k-2003/hiring-engineers/raw/master/image/Visualizing_4.PNG)
    
    Screenshot 2: Received alert from the anomaly detection monitor  
    ![](https://github.com/su27k-2003/hiring-engineers/raw/master/image/Visualizing_10.PNG)
  
  - References: [Datadog Docs - Anomaly Monitors via the API](https://docs.datadoghq.com/monitors/monitor_types/anomaly/#anomaly-monitors-via-the-api)


* **Q3**

  To sum up data and display it in the Timeboard, I applied rollup function to the custom metric (my_metric) for the test. The function takes two parameters, method and time: `.rollup(method,time)`. The method can be sum/min/max/count/avg and time is in seconds. 
  
  - 1.Create a rollup function applied via Datadog API and add it to the Timeboard "Show my_metric" I created in the previous step.  
  
    In this case, I used `.rollup(sum, 3600)` as it requested to sum up all the points for the past hour equal to 3600 seconds. Also, add the rollup function applied graph to the Timeboard "Show my_metric" I created in the previous step to combine the custom metric: my_metric and the new one in the same bucket by adding two "q"s in the API query. Please refer to the Python code and the screenshot below. 
  
    Python code: /code/Create_timeboard.py

    ```python
    from datadog import initialize, api

    options = {
        'api_key': '5032023d686e6bd9b5e0b376a59bb27f',
        'app_key': '94846c5a071f7c2dc77381214fed18614987250a'
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

	try:
      api.Timeboard.create(title=title,
                              description=description,
                              graphs=graphs,
                              template_variables=template_variables,
                              read_only=read_only)
    except:
    	print 'Error occurred!'
    else:
    	print 'Sent API request successfully.'
    ```
    
  - 2.Confirmation
    I confirmed the two Timeboard worked as expected. The original my_metric metric and the rollup function applied my_metric both are showing in the same graph: My Metric (custom metric). Please refer to the screenshot below. 

    Screenshot: rollup function applied to the my_metric

    ![](https://github.com/su27k-2003/hiring-engineers/blob/master/image/Visualizing_6.PNG)

  - References: [Datadog Docs - Graphing Functions](https://docs.datadoghq.com/graphing/miscellaneous/functions/#rollup-1)


* **Q4**

  - Screenshot 1: Graph of the timeboard

    ![](https://github.com/su27k-2003/hiring-engineers/blob/master/image/Visualizing_7.PNG)

  - Screenshot 2: @ notation 

    ![](https://github.com/su27k-2003/hiring-engineers/blob/master/image/Visualizing_9.PNG)


* **Bonus Question**

  We use Anomaly Detection to identify when a metric is behaving differently to it has in the past, taking into account trends, seasonal day-of-week and time-of-day patterns. It is well-suited for metrics with strong trends and recurring patterns that are hard or impossible to monitor with threshold-based alerting. From this point, the metric: mysql.net.connections I applied anomaly function is not a good example as the value of the metric is too stable in my environment but from the second screenshot I can understand that the system generated an alert because it identified anomalies that spike out of the normal range of values. From the first screenshot below we can see the algorithm is monitoring historical data to calculate the metric’s expected normal range of behaviour.

  - Screenshot 1: Anomaly graph

    ![](https://github.com/su27k-2003/hiring-engineers/blob/master/image/Visualizing_8.PNG)
    
  - Screenshot 2: Anomaly function's alert  

    ![](https://github.com/su27k-2003/hiring-engineers/blob/master/image/Visualizing_10.PNG)
 
  - References: [Datadog Docs - Anomaly monitor](https://docs.datadoghq.com/monitors/monitor_types/anomaly/)

****


## Monitoring Data

* **Q1**

  To create a metric monitor and meet the demand for the question, I followed the steps below.
  
  - 1.Created a metric monitor and configurated it in the UI
    - Step 1: As we have two specific values for the Warning threshold and Alerting threshold, I clicked on "New Monitor" in the "Monitors" menu in the top page of the UI then selected "Metric" as the monitor type. 
    - Step 2: In the New Monitor page, select the "Threshold Alert" as the detection method.
    - Step 3: Select "my_metric" in "Define the metric". As I only monitor a metric from a single host in my environment, I left the alert grouping as "Simple Alert".
      **Note**: A multi alert applies the alert to each source.
    - Step 4: in this step, I configurated the Monitor to watch the average of the custom metric (my_metric) and it will alert if it’s above the warning threshold value: 500 and the alerting threshold value: 800 over the past 5 minutes. There are 4 options for "Threshold value" and I used "on average" during the last "5 minutes" as requested. 
      **Note**: Details of each threshold value option:
          - on average: The series is averaged to produce a single value that is checked against the threshold. It adds the avg() functions at the beginning of your monitor query.
          - at least once: If any single value in the generated series crosses the threshold then an alert is triggered. It adds the max() functions at the beginning of your monitor query.
          - at all times: If every point in the generated series is outside the threshold then an alert is triggered. It adds the min() functions at the beginning of your monitor query.
          - in total: If the summation of every point in the series is outside the threshold then an alert is triggered. It adds the sum() functions at the beginning of your monitor query.
    - step 5: Confirm the data missing option has been selected as "Notify" for more than "10" minutes.
    - step 6: To send message include the metric value that caused the monitor to trigger and host IP when the monitor triggers, I used Conditional variables and Tag variables below in "Say what's happening" part.
    
       ```   
       {{#is_alert}} Attention: The value of my_metric ({{value}}) on {{host.name}} ({{host.ip}}) is {{comparator}} the threshold ({{threshold}}). {{/is_alert}}` 
       {{#is_warning}} Attention: The value of my_metric ({{value}}) on {{host.name}} ({{host.ip}}) is {{comparator}} the threshold ({{warn_threshold}}). {{/is_warning}}  

       Alert for my_metric @liuqi_jp@hotmail.com
       ```
     - step 7: Save the configuration for the monitor.
     
  - 2.Confirmation   
    I confirmed the monitor worked properly. Please refer to the two screenshots below or access to my account (liuqi_jp@hotmail.com) to check the metric monitor I created.

    Screenshot 1: Creating the monitor

    ![](https://github.com/su27k-2003/hiring-engineers/blob/master/image/Monitoring_2.PNG)

    Screenshot 2: Email notification

    ![](https://github.com/su27k-2003/hiring-engineers/blob/master/image/Monitoring_1.PNG)
  
  - References:
    - [Datadog Docs - Metric monitor](https://docs.datadoghq.com/monitors/monitor_types/metric/)
    - [Datadog Docs - Notifications](https://docs.datadoghq.com/monitors/notifications)

* **Bonus Question**

  To silence the monitor I created in the last step, I used the Downtime function. Please refer to the steps below to setup Downtime.
  
  - 1.Created and manage Downtime function in the UI
    Step 1: Navigate to the Manage Downtime page by highlighting the “Monitors” tab in the main menu and selecting the “Manage Downtime” link. To schedule downtime, click the “Schedule Downtime” button in the upper right.
    Step 2: Choose what to silence. In this case, we select "Monitor: Test: Notification for my_metric" and the host is "host:deep-learning-virtual-machine".
    Step 3: In te set a schedule step, I set up recurring schedule for the two Downtimes.
    Step 4: Add an optional message to notify the team. In this case, set up the message to send email to my email box. Please refer to the two screenshots below.
    
    Screenshot 1: Downtime setup 7pm-9am daily on M-F

    ![](https://github.com/su27k-2003/hiring-engineers/blob/master/image/Downtime_3.PNG)

    Screenshot 2: Downtime setup all day on Sat-Sun

    ![](https://github.com/su27k-2003/hiring-engineers/blob/master/image/Downtime_4.PNG)
    
  - 2.Confirmation  
    I confirmed the two Downtime functions worked properly. Please refer to the two screenshots below.

    Screenshot 3: Downtime email notification for 7pm-9am daily on M-F

    ![](https://github.com/su27k-2003/hiring-engineers/blob/master/image/Downtime_1.PNG)

    Screenshot 4: Downtime email notification all day on Sat-Sun

    ![](https://github.com/su27k-2003/hiring-engineers/blob/master/image/Downtime_2.PNG)

  - References:
    - [Datadog Docs - Downtimes](https://docs.datadoghq.com/monitors/downtimes/)
   
****


## Collecting APM Data:

* **Bonus Question**

  Service is a set of processes that do the same job. For instance, a simple web application may consist of two services: a single webapp service and a single database service.
  
  Resource is a particular action for a service. For a web application: some examples might be a canonical URL, such as /user/home or a handler function like web.user.home. For a SQL database: a resource is the query itself, such as SELECT * FROM users WHERE id = ?.

* **Q1**
  To use Datadog's APM solution, we should follow these steps below.
  - 1.APM Setup
    - step 1: Install the Datadog Agent
    - step 2: Install the Trace Agent. After installing the Datadog Agent to my Ubuntu, the trace agent is pre-packaged with the standard Datadog agent and no extra configuration is needed.
    - step 3: Configure your environment
    - step 4: Instrument your application. In my case, I'm using Python so I need to install the Datadog Tracing library using pip: `pip install ddtrace`.
    - step 5: Start monitoring the app’s performance. Just simply run the Flask app then the Flask services appear in the APM home page. 
    
  - 2.Confirmation
    Datadog APM provides deep insight into application's performance. In this case, it automatically generated dashboards monitoring key metrics for the Flask app, such as request volume and latency. Please refer to the link and the screenshot below.  
    
    APM page of the Flask app and infrastructure metrics: https://p.datadoghq.com/sb/1d199b067-1878f66f0cbee4b76c9a3de718a749bd?tv_mode=true
  
    Screenshot: APM and Infrastructure Metrics
    ![](https://github.com/su27k-2003/hiring-engineers/blob/master/image/Collecting_APM_1.PNG)
  
  - References:
    - [Datadog Docs - APM and Distributed Tracing](https://docs.datadoghq.com/tracing/)
    
* **Q2**

  I used the Python sample code (Flask app) to create the APM.  
 

****


## Final Question:

 I’m very interested in IoT and I have developed a few Raspberry Pi based home automation projects such as smart garage door (Demo: https://youtu.be/OaJwVSyagKI) and home security camera. I’m aiming to build a smart home as it could make life easier for my family and improve my technical skills.

 While developing these projects, I found a few pain points and I think Datadog could help me to resolve/improve it.

 * Analysing issues

 For example, in the smart garage door project sometimes I found the smart garage door system did not work properly for some reason. The issue could be a communication issue between my phone and the Raspberry Pi (HTTP sending/receiving) or bugs in the script I developed and even the Raspberry Pi itself. Usually it’s not easy to figure out the root cause so I spent a lot of time on troubleshooting and debugging and found a way to determine and fix issues by sending out notification from each function in the system to trace which part caused the issue.
 Now, I could create a dashboard in Datadog which includes Infrastructure Metrics of Raspberry Pi and APM for the Flask application I developed, those data could help me to understand the current system state easily also allow me to quickly determine which part of the system didn't function when issue occurred. For example, if I still could receive those infrastructure metrics data from the Raspberry Pi but the APM didn't show proper data I would check any potential communication issues such as mobile data function had been turned off on my phone. If it wasn't a communication issue then I would look into the Flask as the next step to find the root cause.  
               
 * Integrate separate data into a single smart home system monitor

 There are a few smart home projects I’m running at home and different project generates their own data in different UI. For example, I have to check room temperature by ssh to the Raspberry Pi remotely every time and use VNC to access the Raspberry Pi if I need to check the security camera video. 
I believe that I can send these data to Datadog and integrate them into a single smart home system dashboard which includes all data I need to improve system visibility and make my life easier.
Unfortunately, I cannot provide a demo and show the possibility of Datadog could bring to me as it needs some time to complete but I will find some time to achieve this and share it with you.
