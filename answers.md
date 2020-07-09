# 1:Setup the environment:
  I used a vagrant VM running ubuntu
  [VM](./Vagrant_VM.png)

# 2:Collecting Metrics:
  Tags is the datadog.yaml file [Tags](./tags_datadog_yaml.png)
  
  Host Map Screenshot: see file -> [1-hostmap_screenshot](./1-hostmap_screenshot.png)

  MYSQL installation: [MYSQL](./mysql.png)
  
  MYSQL config: [MYSQL conf.yaml](./mysql_conf.yaml)
  
  Custom Check Agent My_metric.py: see file -> [2-my_metric_py](./2-my_metric_py.png)
  
  Custome check agent My_metric.yaml: see file -> [3-my_metric_yaml](./3-my_metric_yaml.png)

  ### Bonus Question Can you change the collection interval without modifying the Python check file you created ?
  DD: Yes through the metric’s config file …/conf.d/my_metric.d/my_metric.yaml

# 3:Visualizing Data:
  Dashboard creation API Script: See file -> [my_dashboard.py](./my_dashboard.py)
  
  Resulting dashboard Screenshot: see file -> [4-My_dashboard_screenshot](./4-My_dashboard_screenshot.png)

  Dashboard with a 5 min timeframe: see file -> [5-my_dashboard_5min_screenshot](./5-my_dashboard_5min_screenshot.png)

  Dashboard Snapshot and @notation email: see file-> [6-snapshot_notation_email](./6-snapshot_notation_email.png)

  ### Bonus Question: What is the Anomaly graph displaying? 
  DD: The anomaly graph is highlighting abnormal variations in data value as compared to the majority of values in the given interval. In my case it highlights spikes in cpu   utilization for the given timeframe.

# 4:Monitoring Data:
  Create a metric monitor : see file -> [7-metric_monitor](./7-metric_monitor.png)

  Triggered alert email notification: see file -> [8-Triggered_alert_email](./8-Triggered_alert_email.png)

  ### Bonus Question: 
  Downtime email notif : see file -> [9-Downtime_schedule_emails](./9-Downtime_schedule_emails.png)
  
  Downtime schedules: see file -> [10-Downtime_schedule_screenshot](./10-Downtime_schedule_screenshot.png)

 # 5:Collecting APM data
  Instrumented app: see file -> [./trial_app](trial_app.py)
  
  Dashboard Screenshot with Infrastructure and APM metrics: see file -> [11-Dasboard_with_APM_screenshot](./11-Dasboard_with_APM_screenshot.png)
  
  Dashboard link: https://p.datadoghq.com/sb/pplgzjts4v4gyxk3-4a2301f4a537fdf031350b2b0cb55419
  
  ### Bonus Question: What is the difference between a Service and a Resource?
  DD: 
  -A *service* is a group of processes \(queries, jobs, endpoints) that allow the creation of an application. \(i.e: The flask service in our examples)
  -A *resource* is a specific domain of an application \(single endpoint, single query) \(i.e: The specific request http://127.0.0.1:5050/api/trace from the example)

# Final Question:
  ### Is there anything creative you would use Datadog for? 
  DD: I could see a very practical use of collecting metrics from kid’s sceen time. There are applications that can calculate the amount of time spent on each app/device per   kids. A custom Agent check could aggregate all this data and show it on a single pane of glass, while highlighting anomalies and keeping track of the SLO the family has       agreed on.


