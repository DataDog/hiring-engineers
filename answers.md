## Collecting Metrics:

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

To assign tags, you can edit the config file located in `/etc/datadog-agent/datadog.yaml`. In the config file, you can assign tags by adding key:value pairs as needed. Below is a screenshot of how tags would be set up in the `datadog.yaml` file. After assigning tags, you can [restart your agent](https://docs.datadoghq.com/agent/basic_agent_usage/ubuntu/#configuration) to begin seeing the tags in the Host Map page. 

 <img src="https://i.imgur.com/ZEhmwqB.png" width="600" height="300" alt=""> </a>
 <img src="https://i.imgur.com/dd4nkFk.png" width="600" height="300" alt=""> </a>

* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

To install a integration for MySQL, you can navigate to the Datadog Agent integrations page. From here, you can select **MySQL** and access the **Congifuration** tab for step by step instructions. Please visit the [MySQL Integration Guide](https://docs.datadoghq.com/integrations/mysql/) for more detailed instructions. 

 <img src="https://i.imgur.com/jutJVM9.png" width="600" height="300" alt=""> </a>
 <img src="https://i.imgur.com/ZVXWcKe.png" width="600" height="300" alt=""> </a>

* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

Agent checks will allow you to collect metrics from custom apps or unique systems. In order to set up a custom Agent check that submits a metric, you will start with creating a configuration file which will go into `conf.d/randval.yaml`.

Below is an example of a configuration file:

```
init_config:

instances:
    -metric: my_metric
```

The check itself inherits from AgentCheck and send a gauge of a random value between 1 and 1000 on each call. We name the metric 'my_metric' and give it a tag of 'randmetric'. This goes in `checks.d/randval.py` and can be seen in the screenshot below.

Please note that the names of the configuration and check files must match. If your check is called **mycheck.py** your configuration file must be named **mycheck.yaml**.

 <img src="https://i.imgur.com/01gUMrt.png" width="600" height="300" alt=""> </a>


* Change your check's collection interval so that it only submits the metric once every 45 seconds.

If you wish to your check to only submit the metric every 45 seconds, you can update the check's configuration file and add `min_collection_interval` at an instance level. As an example, please see the screenshot below:

 <img src="https://i.imgur.com/LTkY5VY.png" width="600" height="300" alt=""> </a>


* **Bonus Question** Can you change the collection interval without modifying the Python check file you created?
 ANSWER: You can update the 'min_collection_interval' value in the YAML config file of the corresponding check.

## Visualizing Data:

Utilize the Datadog API to create a Timeboard that contains:

* Your custom metric scoped over your host. 
 https://app.datadoghq.com/graph/embed?from_ts=1531762405184&to_ts=1531766005184&token=a22525f1cb91e94ae1416244645b138430ee7a2b8de5436931780f5a31ae2b96&height=300&width=600&legend=true&tile_size=m&live=true
* Any metric from the Integration on your Database with the anomaly function applied.
 https://app.datadoghq.com/graph/embed?token=d555bccdbf9fa979ba3b2410ccf31c1d02eacd95b7ed3151d170a670c55d8457&height=300&width=600&legend=true
* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
 https://app.datadoghq.com/graph/embed?token=bea6c08e445447b861664863ec2f044bd704c5cebe467d5af73cc4f3f0849652&height=300&width=600&legend=true
 
  <img src="https://i.imgur.com/vtuuIiZ.png" width="600" height="300" alt=""> </a>
 
 
Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.
Script found here: https://github.com/johanesteves/hiring-engineers/blob/solutions-engineer/createTimeboard.rb

Once this is created, access the Dashboard from your Dashboard List in the UI:

* Set the Timeboard's timeframe to the past 5 minutes

In order to update the Timboard's timeframe to view the past 5 minutes, you can click and drag on a graph from left to right until you are only selecting the intended timeframe. 
 
  <img src="https://i.imgur.com/KR9obUH.png" width="600" height="300" alt=""> </a>
* Take a snapshot of this graph and use the @ notation to send it to yourself.

To take a snapshot of a graph, you can hover over the graph and select camera icon. This will open a comment box where you can mention other users by using @. 
  <img src="https://i.imgur.com/ERhJuOs.png" width="600" height="300" alt=""> </a>
* **Bonus Question**: What is the Anomaly graph displaying?

 ANSWER: The Anamaly graph will detect anomalous behaviour for a metric based on historical data. It will allow you to identify when a metric is behaving differently than it has in the past, taking into account trends, seasonal day-of-week and time-of-day patterns. It is well-suited for metrics with strong trends and recurring patterns that are hard or impossible to monitor with threshold-based alerting. Please visit the [Anamoly Detection Guide](https://docs.datadoghq.com/monitors/monitor_types/anomaly/) for more information


## Monitoring Data

Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

* Warning threshold of 500
* Alerting threshold of 800
* And also ensure that it will notify you if there is No Data for this query over the past 10m.


In order to setup a new monitor, you can navigate to the **Create Monitors** page by hovering over **Monitors** in the main menu and clicking **New Monitor** in the sub-menu. From here you can select **Metric** to begin configuring your monitor. 

For **step 1**, select **Threshold alert**, which compares the value in the selected timeframe against a given threshold.

For **step 2**, you'll select your metric (my_metric). 

Lastly, for **step 3**, you can add your warning and alert thresholds. The **alert threshold** will be set to 800 and the **warning threshold** will be set to 500. Additionally, you can update the 'notify if data is missing' to **Notify** and setting this alert to 10 mintues. The screenshot below shows a sample setup:

 <img src="https://i.imgur.com/M4WMrDo.png" width="450" height="500" alt=""> </a>

Please configure the monitor’s message so that it will:

* Send you an email whenever the monitor triggers.
* Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
* Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.

**Step 4** of the Monitor configuration page will allow you to create email notifications customizing the message based on the state. You can create different messages based on the state by using message template variables. 

Using `{{#is_alert}} {{/is_alert}}` tags will allow you to display a mesage only when the **alert threshold** is met. Using `{{#is_warning}} {{/is_warning}}` tags will allow you to display a mesage only when the **warning threshold** is met.

You can also include other variables in the message such as `{{value}}` which will inlcude the metric value or `{{host.ip}}`. Please visit the [Notifications Guide](https://docs.datadoghq.com/monitors/notifications/#message-template-variables) for deatiled information and additional variables.

Lastly, **step 5** will allow you to notify certain users when the monitor is active. You can type in a users name to inlcude them in the notifaction email. Please see below for a sample set up of step 4 and 5.

  <img src="https://i.imgur.com/kg3LC7q.png" width="600" height="300" alt=""> </a>

 
* When this monitor sends you an email notification, take a screenshot of the email that it sends you. 

Below is a sample of a notifaction email that a user would see:

   <img src="https://i.imgur.com/e9Pzcaq.png" width="600" height="300" alt=""> </a>

* **Bonus Question**: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

  * One that silences it from 7pm to 9am daily on M-F,

In order to schedule downtimes for your monitor, you navigate to the **Manage Downtime** page by highlighting the Monitors tab in the main menu and selecting the **Manage Downtime** link. From here you can select Schedule Downtime to begin configuring your options. 

For **step 1**, you can select the monitor you wish to schedule the downtime for along with constrain your downtime to a specific host.

**Step 2** will allow you to set a schedule for your downtime. Below is an example of downtime scheduled from 7pm to 9am daily on M-F and one scheduled all day on Sat-Sun. 

**Step 3** and **step 4** give you the option to add a message to notify your team. For more information, visit our [Downtimes Guide](https://docs.datadoghq.com/monitors/downtimes/) 

   <img src="https://i.imgur.com/X7VaH8C.png" width="450" height="500" alt=""> </a>

  * And one that silences it all day on Sat-Sun.

   <img src="https://i.imgur.com/VSourSS.png" width="450" height="500" alt=""> </a>

  * Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.
  
   <img src="https://i.imgur.com/veFIrQn.png" width="600" height="300" alt=""> </a>

## Collecting APM Data:

Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.


  To being setting up an APM, you will need already have the latest [Datadog agent](https://app.datadoghq.com/account/settings#agent) installed. 
  
  For Linux, the Trace Agent is pre-packaged with the standard Datadog Agent and no extra configuration is needed. To ensure the APM agent is enabled, you can access your `datadog.yaml` configuration file. You can update the `apm_config` key as see below:

```
apm_config:
  enabled: true
```

Lastly, you can instrument your application to begin tracing. To setup tracing for Python applications, you will need to Datadog Tracing library using pip:
```
pip install ddtrace
```

Once installed you can import tracer and instrument your application:

```
from ddtrace import tracer

with tracer.trace("web.request", service="my_service") as span:
  span.set_tag("my_tag", "my_value")

```

After running your python application, you should begin seeing your services appear in the APM home page. Please visit our [Tracing FAQ](https://docs.datadoghq.com/tracing/faq/) for commonly asked questions.
 
   <img src="https://i.imgur.com/sn9K5X6.png" width="600" height="300" alt=""> </a>


Please include your fully instrumented app in your submission, as well.
Link to App: https://github.com/johanesteves/hiring-engineers/blob/solutions-engineer/apmtest.py

* **Bonus Question**: What is the difference between a Service and a Resource?

ANSWER: A "Service" is the name of a set of processes that work together to provide a feature set, while a resource is a particular query to a service. For a web application, some examples might be a canonical URL like /user/home or a handler function like web.user.home.

## Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?

ANSWER: I previously worked at a Middle School that had an in-school detention called the "Sendout Room". Students would be sent there after receiving a certain number demerits in a school day.

A way to integrate Datadog would have the students check-in or scan when entering/exiting the "Sendout Room". This could allow the teachers to analyze how long students were staying in the "Sendout Room", if the "Sendout Room" was full, or the daily traffic based on a certain time period. 

This could be useful for teacher and leadership to understand trends and how to make changes based on this information.
