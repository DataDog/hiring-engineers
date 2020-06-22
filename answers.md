# COLLECTING METRICS:
## TASK 1: 
Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

**TASK 1 RESULTS:**

Screenshot of Host Map showing tags via /etc/datadog-agent/datadog.yaml
![Tags via config file](https://user-images.githubusercontent.com/4591443/85254270-76e91d80-b425-11ea-978e-86b71ca350b2.png)
In this host called `<vagrant>` the tag keys and values were added to the `</etc/datadog-agent/datadog.yaml>` config file.

Here is the `<tags:>` section of the config.
```
    tags:
      - environment:dev
      - owner:robertl
      - os:linux
      - distro:ubuntu
```

## TASK 2: 

Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

**TASK 2 RESULTS:**

MySQL was installed and a sample database called [classicmodels](https://www.mysqltutorial.org/mysql-sample-database.aspx) was downloaded and setup.

The following config was entered / uncommented in `</etc/datadog-agent/conf.d/mysql.d/conf.yaml>`.  NOTE:  In the actual conf.yaml file, the port parameter was left commented out since the integration would default to the standard mysql port of 3306.  
```
init_config:

instances:
  - server: 127.0.0.1
    user: vagrant
    pass: "<YOUR_CHOSEN_PASSWORD>" # from the CREATE USER step earlier
    port: "<YOUR_MYSQL_PORT>" # e.g. 3306
    options:
      replication: false
      galera_cluster: true
      extra_status_metrics: true
      extra_innodb_metrics: true
      extra_performance_metrics: true
      schema_size_metrics: false
      disable_innodb_metrics: false
```

Here is a screenshot of the MySQL integration overview dashboard:
![MySQL Dashboard](https://user-images.githubusercontent.com/4591443/85257125-ee6d7b80-b42a-11ea-9b37-17c672b9df27.png)

## TASK 3: 
Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

**TASK 3 RESULTS:**

Using the Datadog documentation a [Custom Agent Check](https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7) was created using the following files:

The config file - `</etc/datadog-agent/conf.d/custom_agent_ck.yaml>`
```
init_config:

instances: [{}]
```

The python script - `</etc/datadog-agent/checks.d/custom_agent_ck.py>`   NOTE:  It was discovered that the 
```
from datadog_checks.base import AgentCheck

# random float from 1 to 1000
import random

int_num = random.choice(range(5, 5000))
x = round(int_num/5, 3)

# content of the special variable __version__ will be shown in the Agent status page
__version__ = "7.20.2"

class HelloCheck(AgentCheck):
    def check(self, instance):
        self.gauge(
                'my_metric.gage',
                x,
                tags=['custom_metric_type:gage'],
        )
```
The randomizer above was one of 3 or 4 ways to generate a random float between 1 and 1000.

## TASK 4: 
Change your check's collection interval so that it only submits the metric once every 45 seconds.

**TASK 4 RESULTS:**

The way to change the collection interval is to edit the `</etc/datadog-agent/conf.d/custom_agent_ck.yaml>` from `<instances: [{}]>` to `<instances:  - min_collection_interval: 45>`.
```
init_config:

# instances: [{}]

instances:  - min_collection_interval: 45
```

## BONUS QUESTION: 
Can you change the collection interval without modifying the Python check file you created?  

**BONUS QUESTION RESULTS:**

I could not find a way to change the collection interval without editing the `</etc/datadog-agent/conf.d/custom_agent_ck.yaml>` file as shown above in the **TASK 4 RESULTS**.  If there is another way, it is most likely by leveraging the Datadog API, but I did not find anything in my search.


# VISUALIZING DATA:
## TASK 1: 
Utilize the Datadog API to create a Timeboard that contains **Part A, Part B** and **Part C**.

**TASK 1 RESULTS:**

Screenshot of Timeboard with all three visualizations.
![LINDEN_Timeboard_via_API](https://user-images.githubusercontent.com/4591443/85265076-54600000-b437-11ea-8a79-f5fef67c1911.png)

  **Part A -** Your custom metric scoped over your host.
  ![Part_A_screenshot](https://user-images.githubusercontent.com/4591443/85263919-84a69f00-b435-11ea-8338-f27855a7fb05.png)
  
  **Part B -** Any metric from the Integration on your Database with the anomaly function applied.
  ![Part_B_screenshot](https://user-images.githubusercontent.com/4591443/85263932-88d2bc80-b435-11ea-88ce-64a4da1ee373.png)
  
  **Part C -** Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket.
  ![Part_C_screenshot](https://user-images.githubusercontent.com/4591443/85263947-8f613400-b435-11ea-8021-4000a8918612.png)
  

## TASK 2:
Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.

**TASK 2 RESULTS:**

  **LINDEN Timeboard via API curl creation script**
  ```
  # Curl command
DD_CLIENT_API_KEY="d45dfd289e48797f9eea3773f57731fa"
DD_CLIENT_APP_KEY="8419a09897b9b536ec27133518a9b71d59cbc277"

curl -X POST https://api.datadoghq.com/api/v1/dashboard \
-H "Content-Type: application/json" \
-H "DD-API-KEY: ${DD_CLIENT_API_KEY}" \
-H "DD-APPLICATION-KEY: ${DD_CLIENT_APP_KEY}" \
-d @- << EOF
{
   "title":"LINDEN Timeboard via API-03",
   "description":"Timeboard for project",
   "widgets":[
      {
         "id":5668139629690266,
         "definition":{
            "type":"timeseries",
            "requests":[
               {
                  "q":"avg:my_metric.gage{host:vagrant}",
                  "display_type":"line",
                  "style":{
                     "palette":"dog_classic",
                     "line_type":"solid",
                     "line_width":"normal"
                  }
               }
            ],
            "yaxis":{
               "label":"",
               "scale":"linear",
               "min":"auto",
               "max":"auto",
               "include_zero":true
            },
            "title":"my_metric_Over_Host",
            "show_legend":false,
            "legend_size":"0"
         }
      },
      {
         "id":1020804297811358,
         "definition":{
            "type":"timeseries",
            "requests":[
               {
                  "q":"anomalies(avg:mysql.performance.cpu_time{host:vagrant}, 'basic', 1)",
                  "display_type":"line",
                  "style":{
                     "palette":"dog_classic",
                     "line_type":"solid",
                     "line_width":"normal"
                  }
               }
            ],
            "yaxis":{
               "label":"",
               "scale":"linear",
               "min":"auto",
               "max":"auto",
               "include_zero":true
            },
            "title":"MySQL_Perf_CPU_Anomalies",
            "show_legend":false,
            "legend_size":"0"
         }
      },
      {
         "id":8516672511044502,
         "definition":{
            "type":"timeseries",
            "requests":[
               {
                  "q":"avg:my_metric.gage{host:vagrant}.rollup(sum, 3600)",
                  "display_type":"line",
                  "style":{
                     "palette":"dog_classic",
                     "line_type":"solid",
                     "line_width":"normal"
                  }
               }
            ],
            "yaxis":{
               "label":"",
               "scale":"linear",
               "min":"auto",
               "max":"auto",
               "include_zero":true
            },
            "title":"Rollup_Sum_my_metric.gage_Past_hour",
            "time":{

            },
            "show_legend":false,
            "legend_size":"0"
         }
      }
   ],
   "template_variables":[

   ],
   "layout_type":"ordered",
   "is_read_only":false,
   "notify_list":[

   ],
   "id":"t3c-bja-pfd"
}
EOF
```

## TASK 3:
Once this is created, access the Dashboard from your Dashboard List in the UI and complete **Part A & B** below:

**TASK 3 RESULTS:**

  **Part A -** Set the Timeboard's timeframe to the past 5 minutes.
  ![Timeframe_Past_5_Minutes](https://user-images.githubusercontent.com/4591443/85266987-3cd64680-b43a-11ea-9148-479dc749164e.png)
  
  **Part B -** Take a snapshot of this graph and use the @ notation to send it to yourself.
  ![Send_snapshot_graph](https://user-images.githubusercontent.com/4591443/85267335-c1c16000-b43a-11ea-906f-362c520fa0b3.png)
  
  Snapshot of message using @ annotation.
  ![dd_graph_sending_from_dashboard_snapshot](https://user-images.githubusercontent.com/4591443/85267467-ec131d80-b43a-11ea-81ab-a4b37d1aa979.png)
  
  Snapshot of graph received via email.
  ![dd_graph_received_via_at_annotation](https://user-images.githubusercontent.com/4591443/85267556-0947ec00-b43b-11ea-8c45-15bd2c367400.png)
  
## BONUS QUESTION: 
What is the Anomaly graph displaying?

**BONUS QUESTION RESULTS:**

The anomaly graph represents a methodology used to detect when metrics fall above or below an expected range.  There are two parameters for this function, the Algorithm and Bounds.  This function overlays a gray band on the metric showing the expected behavior of a series based on the past and will show if the metric value is falling outside the expected behavior.  The bounds parameter can be interpreted as the standard deviations for the specific algorithm being used.



# MONITORING DATA:
## TASK 1:
Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

  Warning threshold of 500
  Alerting threshold of 800
  And also ensure that it will notify you if there is No Data for this query over the past 10m.

**TASK 1 RESULTS:**

Screenshot of Monitor summary for ALERT, WARNING and NO_DATA notifications according to the instructions above.
![Monitor_summary](https://user-images.githubusercontent.com/4591443/85270140-79a43c80-b43e-11ea-8bcb-f8452e114dab.png)


Screenshot of thresholds and No_Data configuration according to the instructions above.
![Monitor_threshold_config](https://user-images.githubusercontent.com/4591443/85270583-1e267e80-b43f-11ea-91e8-a527d1c71683.png)

## TASK 2:
Please configure the monitor’s message so that it will:

  Send you an email whenever the monitor triggers.
  Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
  Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
  
**TASK 2 RESULTS:**

Screenshot of message configuration for ALERT, WARNING and NO_DATA according to the instructions above (1 of 2).
![Monitor_message_config](https://user-images.githubusercontent.com/4591443/85270605-2979aa00-b43f-11ea-9aa6-f9dc2a8c6e0f.png)


Screenshot of message configuration for ALERT, WARNING and NO_DATA according to the instructions above (2 of 2).
![Monitor_message_config_2_of_2](https://user-images.githubusercontent.com/4591443/85271013-cc322880-b43f-11ea-922f-087e21665912.png)

Detailed messages based on ALERT, WARNING and NO_DATA:

ALERT
```
{{#is_alert}}
  ALERT:  my_metric threshold is above 800 on host {{host.name}} with {{host.ip}}!
 1.  Contact Linden immediately via email.
 2.  If no reply within 1 hour, call cell at 555-555-5432. 
      @robert@lindtex.com 
{{/is_alert}}
```

WARNING
```
{{#is_warning}}
  WARNING:  my_metric threshold is between 500 and 800.
  No action needed. 
  @robert@lindtex.com 
{{/is_warning}}
```

NO_DATA
```
{{#is_no_data}}
NO DATA for my_metric in the last 10 minutes.
1.  Check datadog-agent status
2.  If there are errors contact Linden
@robert@lindtex.com 
{{/is_no_data}}
```


When this monitor sends you an email notification, take a screenshot of the email that it sends you.

ALERT Notification email.
![ALERT_Monitor_email](https://user-images.githubusercontent.com/4591443/85274832-1a95f600-b445-11ea-8184-b57ff3274797.png)


WARNING Notification email.
![WARNING_Monitor_email](https://user-images.githubusercontent.com/4591443/85273856-c50d1980-b443-11ea-903c-7c02e6722663.png)


NO_DATA Notification email.
![NO_DATA_Monitor_email](https://user-images.githubusercontent.com/4591443/85273890-cfc7ae80-b443-11ea-9b3d-3fbfce961818.png)

## BONUS QUESTION:
Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

  One that silences it from 7pm to 9am daily on M-F,
  And one that silences it all day on Sat-Sun.
  Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.
  
**BONUS QUESTION RESULTS:**

Two DOWNTIME Schedules were created, one for the weekdays down 7pm to 9am the following moring, the second for weekends all day until 9am Monday morning.  Email was notified when changes were made to the Monitor (see below).

Screenshot of the Weekday Downtime Schedule.
![DOWNTIME_Weekday_Monitor_schedule](https://user-images.githubusercontent.com/4591443/85275420-eec74000-b445-11ea-99be-bd22019cdea8.png)


Screenshot of the Weekend Downtime Schedule.
![DOWNTIME_Weekend_Monitor_schedule](https://user-images.githubusercontent.com/4591443/85275428-f2f35d80-b445-11ea-901b-7a130847093a.png)


Screenshot of Monitor change notification for Weekday Schedule creation.
![DOWNTIME_Weekday_Monitor_email](https://user-images.githubusercontent.com/4591443/85275652-3fd73400-b446-11ea-88da-309ea14bcf24.png)


Screenshot of Monitor change notification for Weekend Schedule creation.
![DOWNTIME_Weekend_Monitor_email](https://user-images.githubusercontent.com/4591443/85275683-46fe4200-b446-11ea-967f-e2631cb4465b.png)


# COLLECTING APM DATA:

## TASK 1:
Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:

**TASK 1 RESULTS:**


# BONUS QUESTION:
What is the difference between a Service and a Resource?

## BONUS QUESTION RESULTS:
Services are the building blocks of microservice architectures - broadly a service groups together endpoints, queries or jobs for the purposes of building your application.
Resources represent a particular domain of a customer application - they are typically an instrumented web endpoint, database query, or background job.







