### Prerequisites - Setting up the Environment

My Datadog environment setup includes an agent install on my laptop Windows OS and an Ubuntu Linux VM via Vagrant. I utilize my Windows OS for a majority of the exercises and the Linux VM to test tagging and complete the APM instrumentation.

Upon downloading the Datadog Agent on my localhost, I'm now able to browse to http://127.0.0.1:5002/ where I can view my connection as well as other agent info. This UI also provides the ability to restart the agent service. Neat!

<p align="center">
        <img width="700" src="https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/agent_manager.PNG">
</p>

Here's my Windows OS agent manager, up and running. 

***

### Collecting Metrics
#### _Tagging_

Agent configuration occurs in the datadog.yaml file, which is my first stop in the tagging task. On a Windows OS, the file's located in C:\ProgramData\Datadog, and /etc/datadog-agent/ in a Linux environment. 

Within datadog.yaml, I add a variety of tags under the tags section. 

![Windows datadog.yaml File](https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/windows_tags_config.PNG "Windows datadog.yaml") 
![Linux datadog.yaml File](https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/ubuntu_tags_config.PNG "Linux datadog.yaml")

Once the tags are added, the file gets saved, the agent service is restarted, and after 15-30 minutes, the newly-added tags appear in the host info section within the host map. 

![Host Map](https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/host_map_windows_tags.PNG "Windows Host Map - Tags")
![Host Map](https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/host_map_vagrant_tags.PNG "Vagrant Host Map - Tags")

#### _Database Install and Integration_

I utilized PostgreSQL for this portion of the exercise and started the database integration process by creating a dummy Datadog database. This was followed by the creation of the datadog user. 

Note that in the user creation screenshot below, the 1234 password for the user is for show only. In a live Production environment, 1234 would be the last password you'd want to use. Highly unsecure. 0/10--would not recommend. 

![SQL Datadog User Creation](https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/datadog_sql_user_creation.PNG "Datadog DB User Creation")

Once the user's created, we enable the postgres.d configuration file in C:\ProgramData\Datadog\conf.d\postgres.d. The config file is filled out accordingly, and the agent gets restarted for the integration changes to take effect. 

![Postgresql Config Enable](https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/postgres_config_updated.PNG "Postgres.d Configuration")

Following the enabling of the Postgres integration, I'm now able to pull metrics related to postgresql. To do a simple check of how the integration allows Datadog to interact with Postgres, I pull up the db.count Postgres metric graph. An initial look shows I have one database, and upon creating another Test database, the graph count jumps to two. I can confirm now that configurations within Postgres are monitored and mapped in real time in Datadog. 

![Postgresql Metrics](https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/postgresql_metrics.PNG "Postgres Metrics")

Check out the Agent Manager--a postgres collector displays now too.

![Postgres Agent Manager](https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/agent_manager_postgres_collector.PNG "Postgres Agent Manager")

#### _Custom Agent Check_

Setting up a custom agent check begins with the creation of a configuration file in C:\ProgramData\Datadog\conf.d and a check file in C:\ProgramData\Datadog\checks.d. To ensure a proper setup, the file names for both must match, and in our case, we're naming both "my_metric".  

There are a number of different functions or metric types that can be used for custom agent checks. Different functions/metric types result in different graphing capabilities and ultimately different displays. 

For my custom metric, I'm using the gauge function, which takes a value from a specific time interval and then continuously does so for each specified time interval after. This seemed to be the most appropriate type since we're looking to include a random value between 0 and 1000 in our check. 

<p align="center">
        <img src="https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/custom_check_code.PNG">
</p>

Changing the check's collection interval involves updating the config file (my_metric.yaml) we created prior. The original instance of this file is populated by an empty sequence called instances.

<p align="center">
        <img src="https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/my_metric_yaml.PNG">
</p>

To update our collection interval, we'll add a min_collection_interval of 45, so our check submits its metric once every 45 seconds as opposed to the default of 15 seconds. 

<p align="center">
        <img src="https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/instances_yaml.PNG">
</p>

Once the code is run, a random value between 0 and 1000 is chosen every 45 seconds. 

![my_metric Fullscreen](https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/metric_stats_fullscreen.PNG "My_metric.gauge Fullscreen")

In case you were wondering, and I know you are--yes, the collection interval can be changed without needing to modify the configuration file. In the Datadog Metrics - Summary GUI, you can pull up individual metrics and edit their metadata accordingly.

![Interval GUI Change](https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/my_metric_interval_gui_change.PNG "Interval GUI Change")

***

### Visualizing Data

Having worked with APIs in the past, I'm utilizing Postman to send my API calls to Datadog in this portion of the exercise. 

Postman's an API client that allows developers to better test and create APIs. I have it installed on my Windows OS and just need to download the Datadog Postman collection, which includes pre-configured API templates. 

![Postman Datadog API Collection](https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/postman_datadog_collection.PNG "API Collection")

Upon importing the Datadog collection json, I'm able to view a large variety of Datadog-specific API calls. Before I can start sending calls though, I need to setup my environment, which includes my Datadog site, API and applications keys required for authentication. 

![Postman Datadog Env Creation](https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/postman_env_creation.PNG "Postman Env Creation")

With the environment now setup, all I need to do is define the environment I'm in, and I'm ready to create this timeboard! 

![Env Define](https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/Postman_datadog_env.PNG)

Within the Dashboard dropdown in Postman, I choose POST - Create a Dashboard. The Body tab includes the code I need to edit to fit my customizations. My goal here is to create one dashboard that includes three separate graphing displays--one for my custom metric, one for my Postgres integration with the anomaly function applied, and one for my custom metric with the rollup function applied. 

I'm using timeseries widgets here to visualize the evolution of these metrics over time. 

The first one is relatively straightforward. We're specifying the definition of this code block with the type of widget (timeseries) and the request we want the widget to display (average of all my_metric.gauge calls).
```
        {
            "definition": {
                "type": "timeseries",
                "requests": [
                    {
                        "q": "avg:my_metric.gauge{*}"
                    }
                ],
                "title": "Avg of my_metric.gauge"
            }
        },
```
For my second widget code block, I'm pulling a Postgres integration metric (buffer hits) with the addition of the anomaly function. The anomaly function detects abnormal metric fluctuations and is displayed on our graph as a gray band that maps expected behavior based on historical trends. Anything out of the expected behavior range is flagged.

Within my anomalies function, I've specified which metric I want to utilize, the algorithm to detect said anomalies and the bounds. Algorithms to detect anomalies include basic, agile and robust. Here we're using basic as this is a metric with no repeating seasonal patterns. Bounds dictate the width of the gray band and are essentially the standard deviations for your metric. As indicated in the Datadog dashboard documentation, "2 or 3 should be large enough to include most 'normal' points". 

```
        {
             "definition": {
                "type": "timeseries",
                "requests": [
                    {
                        "q": "anomalies(avg:postgresql.buffer_hit{*}, 'basic', 2)"
                    }
                ],
                "title": "Avg of PostgreSQL.buffer_hit with Anomalies"
            }
        }

```

The final widget block pulls my custom metric gauge with the rollup function applied. The rollup function allows you to define the time intervals for your graph and how the data points are collected during that time interval. 

In my code snippet, my method is sum, and my the time interval is set to 3600 seconds (1 hour).

```
        {
             "definition": {
                "type": "timeseries",
                "requests": [
                    {
                        "q": "avg:my_metric.gauge{*}.rollup(sum, 3600)"
                    }
                ],
                "title": "Avg of my_metric.gauge with Rollup"
            }
        }

```

The code below is my finished script for the requested timeboard (displayed in raw json). 

```
{
    "title": "Data Visualization: A Story of Metrics",
    "widgets": [
        {
            "definition": {
                "type": "timeseries",
                "requests": [
                    {
                        "q": "avg:my_metric.gauge{*}"
                    }
                ],
                "title": "Avg of my_metric.gauge"
            }
        },
         {
            "definition": {
                "type": "timeseries",
                "requests": [
                    {
                        "q": "anomalies(avg:postgresql.buffer_hit{*}, 'basic', 2)"
                    }
                ],
                "title": "Avg of PostgreSQL.buffer_hit with Anomalies"
            }
        },
         {
            "definition": {
                "type": "timeseries",
                "requests": [
                    {
                        "q": "avg:my_metric.gauge{*}.rollup(sum, 3600)"
                    }
                ],
                "title": "Avg of my_metric.gauge with Rollup"
            }
        }
    ],
    "layout_type": "ordered",
    "description": "A variety of metrics displayed.",
    "is_read_only": true,
    "notify_list": [],
    "template_variables": [
        {
            "name": "host",
            "prefix": "host",
            "default": "<HOSTNAME_1>"
        }
    ],
    "template_variable_presets": [
        {
            "name": "Saved views for hostname 2",
            "template_variables": [
                {
                    "name": "host",
                    "value": "<HOSTNAME_2>"
                }
            ]
        }
    ]
}
```

After sending the API call, the timeboard is created in Datadog's Dashboard GUI. 

![Timeboard GUI](https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/Timeboard_with_anomalies_new.PNG "Timeboard GUI")

#### _Timeboard UI Tasks_

My last step in visualizing this data is to interact with it via the UI. I've set my Timeboard timeframe to 5 minutes and have taken a snapshot and sent it to myself. 

![Timeboard GUI 5 Minutes](https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/Timeboard_5_Mins.PNG "Timeboard GUI - 5 Mins")
![Timeboard Snapshot](https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/Timeboard_snapshot.PNG "Timeboard Snapshot")

I know what you're thinking... "What in the world is this anomaly graph showing me?" Great question!

The gray band is the anomaly overlay that our function creates over our metric graph. The width of it was set to 2 in our API call, so it's measuring this standard deviation. The consistency of the overlay is dictated by the basic algorithm we specified in our function. The basic algorithm identifies potential anomalies but doesn't incorporate the spike and dip pattern that's occuring throughout the time interval. A robust or agile algorithm would account for that pattern. 

***

### Monitoring Data

Earlier we setup our custom metric to measure a value from 0 to 1000 every 45 seconds. Now we're going to create a few monitors that'll alert us when that metric goes above a certain value.

When navigating to Monitors - Create New Monitor, you're presented with a variety of monitor types. For our purposes, we're choosing a metric monitor and the threshold alert detection method, which will trigger an alert anytime a metric crosses a specific threshold. 

The monitor setup UI gives users the ability to customize their monitors seamlessly. 

![Monitor Setup UI](https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/Monitor_setup_gui.PNG)

I'm defining the parameters for the metric to include three separate monitors:

- Warning threshold of 500

![Threshold Warning](https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/Warning_Monitor.PNG)

- Alerting threshold of 800
- Although the image below displays a test notification, notice how the alert includes the metric value and the host IP.

![Threshold Alert](https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/Alert_Monitor.PNG)

- Notification if there's No Data for the query over the last 10 minutes. 

![No Data Alert](https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/Missing_Data_Monitor.PNG)

With these monitors setup, I'm noticing I'm getting quite a few notifications throughout the day. Scheduling a couple of downtime monitors will help manage this.

- Downtime monitor that silences notifications from 7PM to 9PM daily, Monday through Friday.

![M-F Downtime Monitor](https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/Monitor_Downtime.PNG)
![Weekdays](https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/Monitor_Downtime_Weekdays.PNG)

- Downtime monitor that silences notifications all day Saturday and Sunday. 

![Sat-Sun Downtime Monitor](https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/Monitor_Downtime1.PNG)
![Weekends](https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/Monitor_Downtime_Weekend.PNG)

***

### Collecting APM Data

***

### Final Question
