### Prerequisites - Setting up the Environment

My Datadog environment setup includes an agent install on my laptop Windows OS and an Ubuntu Linux VM via Vagrant. I utilize my Windows OS for a majority of the exercises and the Linux VM to test tagging and complete the APM instrumentation.

Upon downloading the Datadog Agent on my localhost, I'm now able to browse to http://127.0.0.1:5002/ where I can view my connection to Datadog as well as other agent info. This UI also provides the ability to restart the agent service.

<p align="center">
        <img width="700" src="https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/agent_manager.PNG">
</p>

Here's my Windows OS agent manager, up and running. 

***

### Collecting Metrics
#### _Tagging_

Agent configuration occurs in the datadog.yaml file, which is my first stop in the tagging task. On a Windows OS, the file's located in C:\ProgramData\Datadog, and in a Linux environment, /etc/datadog-agent/. 

Within datadog.yaml, I can add a variety of tags under the tags section. 

![Windows datadog.yaml File](https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/windows_tags_config.PNG "Windows datadog.yaml") 
![Linux datadog.yaml File](https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/ubuntu_tags_config.PNG "Linux datadog.yaml")

Once the tags are added, the file gets saved, the agent service is restarted, and after 15-30 minutes, the newly-added tags appear in the host info section within the host map. 

<p align="center">
        <img width="780" src="https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/host_map_windows_tags.PNG">
</p>

<p align="center">
        <img width="780" src="https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/host_map_vagrant_tags.PNG">
</p>

#### _Database Install and Integration_

I utilized PostgreSQL for this portion of the exercise and started the database integration process by creating a dummy Datadog database. This was followed by the creation of the datadog user. 

Note that in the user creation screenshot below, the 1234 password for the user is for show only. In a live Production environment, 1234 would be the last password you'd want to use. It's highly unsecure and scores a 0/10 in password security--would not recommend. 

<p align="center">
        <img width="800" src="https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/datadog_sql_user_creation.PNG">
</p>

Once the user's created, we enable the postgres.d configuration file in C:\ProgramData\Datadog\conf.d\postgres.d. 

Fill out the config file accordingly and then restart the agent for the integration changes to take effect. 

![Postgresql Config Enable](https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/postgres_config_updated.PNG "Postgres.d Configuration")

Following the enabling of the Postgres integration, I'm now able to pull metrics related to Postgres. 

<p align="center">
        <img width="700" src="https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/postgresql_metrics.PNG">
</p>

To do a simple check of how the integration allows Datadog to interact with Postgres, I pull up the db.count Postgres metric graph. An initial look shows I have one database, and upon creating another Test database, the graph count jumps to two. Deleting the Test database changes the db value back to one. I can confirm now that configurations within Postgres are monitored and mapped in real time in Datadog. 

<p align="center">
        <img src="https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/postgres_dbcount_monitor_after_deletion.PNG">
</p>

Check out the Agent Manager--a new Postgres collector displays now too.

<p align="center">
        <img width="700" src="https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/agent_manager_postgres_collector.PNG">
</p>

#### _Custom Agent Check_

Setting up a custom agent check begins with the creation of a configuration file in C:\ProgramData\Datadog\conf.d and a check file in C:\ProgramData\Datadog\checks.d. To ensure a proper setup, the file names for both must match, and in our case, we're naming both "my_metric".  

There are a number of different functions or metric types that can be used for custom agent checks. Different functions/metric types result in different graphing capabilities and ultimately different displays. 

For my custom metric, I'm using the gauge function, which maps a value from a specified time interval and then continuously does so for each specified time interval after. This seemed to be the most appropriate type since we're looking to include a random value between 0 and 1000 in our check and random.randint() does just that.

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

Once the code is run, a random value between 0 and 1000 is mapped at minimum every 45 seconds. 

![my_metric Fullscreen](https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/metric_stats_fullscreen.PNG "My_metric.gauge Fullscreen")

In case you were wondering, and I know you are--yes, the collection interval can be changed without needing to modify the configuration file. In the Datadog Metrics - Summary GUI, you can pull up individual metrics and edit their metadata accordingly. Notice the interval field in the screenshot below. 

![Interval GUI Change](https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/my_metric_interval_gui_change.PNG "Interval GUI Change")

***

### Visualizing Data

Having worked with APIs in the past, I'm utilizing Postman to send my API calls to Datadog in this portion of the exercise. 

Postman's an API client that allows developers to better test and create APIs. I have it installed on my Windows OS and just need to download the Datadog Postman collection, which includes pre-configured API templates. 

<p align="center">
        <img src="https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/postman_datadog_collection.PNG">
</p>

Upon importing the Datadog collection json, I'm now able to view a large variety of Datadog-specific API calls. Before I can start sending calls though, I need to setup my environment, which includes configuring my Datadog site, API, and applications keys required for authentication. 

<p align="center">
        <img src="https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/postman_env_creation.PNG">
</p>

Once the environment is setup, I define the environment I'm in, and voila--I'm ready to create my timeboard.

<p align="center">
        <img src="https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/Postman_datadog_env.PNG">
</p>

Within the Dashboard dropdown in Postman, I choose POST - Create a Dashboard. The Body tab includes the code I need to work with to create my dashboard. In the screenshot below, I've already defined a title for my dashboard and values for my first widget.

<p align="center">
        <img width="800" src="https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/postman%20GUI.PNG">
</p>

My goal is to create one dashboard that includes three separate graphing displays--one for my custom metric, one for my Postgres integration with the anomaly function applied, and one for my custom metric with the rollup function applied. 

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
For my second widget, I'm pulling a Postgres integration metric (buffer hits) with the addition of the anomaly function. 

The anomaly function detects abnormal metric fluctuations and displays on our graph as a gray band that maps expected behavior based on historical trends. Anything out of the expected behavior range is flagged.

Within my anomalies function, I've specified two parameters--the algorithm to detect anomalies and bounds. 

Algorithms to detect anomalies include basic, agile and robust. We'll utilize the basic algorithm as it's best suited for metrics with no repeating seasonal pattern. Bounds dictate the width of the gray band and are essentially the standard deviations for your metric. As indicated in the Datadog dashboard documentation, "2 or 3 should be large enough to include most 'normal' points". 

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

My final widget pulls my custom metric gauge with the rollup function applied. 

The rollup function allows you to graph custom time aggregations and includes method and time parameters.

In my code snippet, my method is sum, and the time interval is set to 3600 seconds (1 hour).

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

The code below is my finished body script for the requested timeboard (displayed in raw json). 

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

After sending the API call through Postman, the timeboard is created in Datadog's Dashboard GUI. 

![Timeboard GUI](https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/Timeboard_with_anomalies_new.PNG "Timeboard GUI")

#### _Timeboard UI Tasks_

My last step in visualizing this data is to interact with it via the GUI. I've set my timeboard timeframe to 5 minutes and have taken a snapshot and sent it to myself. 

<p align="center">
        <img width="900" src="https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/Timeboard_5_Mins.PNG">
</p>

<p align="center">
        <img width="600" src="https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/Timeboard_snapshot.PNG">
</p>

I know what you're thinking... "What in the world is this anomaly graph showing me?" Great question!

The gray band is the anomaly overlay that our function creates over our metric graph. The width of it was set to 2 in our API call, so it's measuring this standard deviation. The consistency of the overlay is dictated by the basic algorithm we specified in our function. The basic algorithm identifies potential anomalies but doesn't incorporate the spike and dip pattern that's occuring throughout the time interval. A robust or agile algorithm would account for that pattern. 

***

### Monitoring Data

Earlier we setup our custom metric to measure a value from 0 to 1000 at minimum every 45 seconds. Now we're going to create a few monitors that'll alert us when that metric goes above a certain value.

When navigating to Monitors - Create New Monitor, you're presented with a variety of monitor types. For our purposes, we're choosing a metric monitor and the threshold alert detection method, which will trigger an alert anytime a metric crosses a specific threshold. 

The monitor setup UI gives users the ability to customize their monitors seamlessly. 

<p align="center">
        <img src="https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/Monitor_setup_gui2.PNG">
</p>

I'm defining the parameters for the custom metric monitor to include three separate monitors. Notice in each notification, the message is customized to fit the alert.

- Warning threshold of 500

<p align="center">
        <img src="https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/Warning_Monitor.PNG">
</p>

- Alerting threshold of 800
  - Although the image below displays a test notification, notice that the alert includes the metric value that triggered the alert and host IP.

<p align="center">
        <img src="https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/Alert_Monitor.PNG">
</p>

- Notification if there's No Data for the query over the last 10 minutes. 

<p align="center">
        <img src="https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/Missing_Data_Monitor.PNG">
</p>

#### _Downtime Scheduling_

With these monitors setup, I'm getting quite a few notifications throughout the day. Scheduling downtime monitors will help manage this.

In Monitors - Manage Downtime, you can create and customize downtime montiors to fit your schedule.

<p align="center">
        <img width="600" src="https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/downtime_monitor.PNG">
</p>

- Downtime monitor that silences notifications from 7PM to 9PM daily, Monday through Friday.

<p align="center">
        <img src="https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/Monitor_Downtime.PNG">
</p>

<p align="center">
        <img width="700" src="https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/Monitor_Downtime_Weekdays.PNG">
</p>

- Downtime monitor that silences notifications all day Saturday and Sunday. 

<p align="center">
        <img src="https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/Monitor_Downtime1.PNG">
</p>

<p align="center">
        <img width="700" src="https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/Monitor_Downtime_Weekend.PNG">
</p>

***

### Collecting APM Data

This section honestly threw me for a loop. 

I was successful in getting the Flask application instrumented and visible in the APM Services GUI the first time I attempted the process, but I was ultimately unable to add additional configurations so that they'd also reflect in the interface. I decided after some troubleshooting to spin up a new VM to start the process over. The second time around, I could instrument the app, but none of the information pulled into the APM GUI, not even the service itself despite confirming the connection.  

I'll go through what I succeeded in doing the first time around and where I'm stuck scratching my head today.

I began by booting up the Linux VM I had created earlier for this exercise. The Datadog agent had already been installed, so it was just a matter of ensuring the agent was running, and APM was enabled in the datadog.yaml file. 

With both confirmed, I moved onto installing pip, flask and ddtrace. 

Once installed, I created my Flask app Python file (datadog_flask.py) and ran the following against it.

```
export DD_SERVICE=hello 
```

followed by:

```
ddtrace-run python datadog_flask.py
```

I received the expected response and confirmed it by running the curl command below in a separate terminal. 

```
curl http://0.0.0.0:5050/
```

<p align="center">
        <img src="https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/APM_vagrant.PNG">
</p>

The service popped up in the APM Services GUI shortly after.

(I spun up another Flask app and instrumented it the same way I did the first following this success, which is why there's a hello2 service as well.)

<p align="center">
        <img src="https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/APM_vagrant3.PNG">
</p>

At this point, I was ready to configure additional environment variables, but this is where I started running into issues. 

Running the configurations below weren't resulting in a change to the APM GUI aka I wasn't seeing the additional information that the configurations should've enabled.

```
DD_SERVICE="hello" DD_ENV="test" DD_TRACE_ANALYTICS_ENABLED=true DD_PROFILING_ENABLED=true
```

I got to a point where I wanted to start again and recreate my VM. Maybe I had missed something.

The second time around, I installed the pre-requisites and confirmed the agent was running and trace logs were generating. I ran the same export and ddtrace-run commands, and tested the setup again with the curl command. Everything looked functional.  

The issue this time was that the GUI no longer populated any active services, and this is where I've been stuck. 

<p align="center">
        <img src="https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/APM_no_services.PNG">
</p>

I've spent more hours than I'd like to admit on this portion of the exercise, so if the issue is obvious, please let me know!

***

### Final Question - Is there anything creative you'd use Datadog for?

I came home two weeks ago to an empty front door after I was informed by a tracking app that a package I ordered had been delivered. I didn't want to jump to conclusions when it occurred, so I checked the address I had specified for the delivery, rechecked the tracking app, and walked around my apartment for half an hour wondering if the mailman had dropped it off in a mailroom I had no knowledge of. 

After a thorough investigation, I concluded the package was stolen. Luckily it was an item that was replaced by the company I ordered it through, but imagine if grandma had sent her world famous chocolate chip cookies, or if you won an eBay auction for a one-of-a-kind item, or if the company you ordered it through simply didn't do anything about it. You'd be saltier than I've been for the past two weeks.

Cue a new way to utilize Datadog... security package monitoring. 

In this use case, the Datadog Agent gets installed on a Raspberry Pi, which is connected to a scale or pressure mat located conveniently in your mailbox or by your front door. Whenever a package is delivered to one of these locations, the scale detects the change in weight and sends that metric to Datadog. Datadog could track the fluctuation in expected weight and send the user a notification when that value meets an expected threshold or doesn't. Sounds a lot like metric monitoring with the anomaly function attached would be useful here.

Imagine you had this setup and were expecting a package. You turn the scale on while you're not home and eventually you're notified that the package was delivered. Your setup could include additional components such as cameras to monitor who's delivering or what's been delivered. Now imagine you go a step further and install a net above your front door. Your package was successfully delivered two hours ago, but now you've been notified that the expected weight has suddenly dropped to zero. Your camera activates, you see the culprit, and **_bam_** you activate your net trap! It works everytime! At least in the movies.

<p align="center">
        <img src="https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/giphy.gif">
</p>
