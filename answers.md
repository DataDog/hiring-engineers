# 1:Collecting Metrics:
  Screenshot: see file -> [1-hostmap_screenshot](./1-hostmap_screenshot.png)

  My_metric.py: see file -> [2-my_metric_py](./2-my_metric_py.png)
  
  My_metric.yaml: see file -> [3-my_metric_yaml](./3-my_metric_yaml.png)

  ### Bonus Question Can you change the collection interval without modifying the Python check file you created ?
  DD: Yes through the metric’s config file …/conf.d/my_metric.d/my_metric.yaml

# 2:Visualizing Data:
  Script: See file -> [my_dashboard.py](./my_dashboard.py)
  
  Screenshot: see file -> [4-My_dashboard_screenshot](./4-My_dashboard_screenshot.png)

  5 min timeframe: see file -> [5-my_dashboard_5min_screenshot](./5-my_dashboard_5min_screenshot.png)

  Snapshot @notification: see file-> [6-snapshot_notation_email](./6-snapshot_notation_email.png)

  ### Bonus Question: What is the Anomaly graph displaying? 
  DD: The anomaly graph is highlighting abnormal variations in data value as compared to the majority of values in the given interval. In my case it highlights spikes in cpu   utilization for the given timeframe.

# 3:Monitoring Data:
  Create a metric monitor : see file -> [7-metric_monitor](./7-metric_monitor.png)

  Triggered alert email notification: see file -> [8-Triggered_alert_email](./8-Triggered_alert_email.png)

  ### Bonus Question: 
  Downtime schedules: see file -> [10-Downtime_schedule_screenshot](./10-Downtime_schedule_screenshot.png)

  Downtime email notif : see file -> [9-Downtime_schedule_email](./10-Downtime_schedule_email.png)
 


# 4:Collecting APM data
  Instrumented app: see file -> [./trial_app](trial_app.py)
  
  Screenshot: see file -> [11-Dasboard_with_APM_screenshot](./11-Dasboard_with_APM_screenshot.png)
  
  Dashboard link: https://p.datadoghq.com/sb/pplgzjts4v4gyxk3-4a2301f4a537fdf031350b2b0cb55419



# Final Question:
  ### Is there anything creative you would use Datadog for? 
  DD: I could see a very practical use of collecting metrics from kid’s sceen time. There are applications that can calculate the amount of time spent on each app/device per   kids. A custom Agent check could aggregate all this data an show it on a single pane of glass, while highlighting anomalies and keeping track of the SLO the family has       agreed on.


