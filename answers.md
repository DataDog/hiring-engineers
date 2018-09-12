# Solutions Engineer Exercise

## Setup
For this open source exercise I'm running Ubuntu 16.04 on my device. Before installing the agent, I read through the documentation located at the bottom of the assignment in order to gain an understanding of the Datadog agent.  

Download the Datadog Agent in terminal.
You will be given your own API key(DO NOT show your API key to the public)
```
DD_API_KEY=YOUR_API_KEY bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```
<img src="https://github.com/alexandera9996/hiring-engineers/blob/master/datadog_screenshots/agent_ok.png" />


## Collecting Metrics
Tagging gives the user a method of aggregating data across a number of hosts. This is useful because users can then compare and observe how metrics behave across a number of hosts or collection of systems. 
navigate to Datadog directory

```
cd /etc/datadog-agent
```
Open Datadog.yaml:
```
sudo vim Datadog.yaml
```
Configure your .yaml file and change the tags to your preference. These are my tags:
<img src="https://github.com/alexandera9996/hiring-engineers/blob/master/datadog_screenshots/tags.png" />

Restart the agent:
```
sudo service datadog-agent restart
```
Navigate to Host Map page in Data dog. Reload the page if your new tags do not appear.
Here is my Host Page map for reference.
<img src="https://github.com/alexandera9996/hiring-engineers/blob/master/datadog_screenshots/Host_page.png" />

### Install a database. For this part, I went ahead with MySQL.
to install MySQL, run:
```
sudo apt-get update
sudo apt-get install mysql-server
```
After installation, configure it with Datadog. 
First I create a datadog user with replication rights in my MySQL server. Then I add the full metrics. 
Next I edit conf.d/mysql.yaml.
<img src="https://github.com/alexandera9996/hiring-engineers/blob/master/datadog_screenshots/mysql_yaml.png" />

To see that MySQL is sucessfully running its metrics, restart the Datadog agent then type, 
```
sudo datadog-agent status
```
This shows that my metric is running successfully:

<img src="https://github.com/alexandera9996/hiring-engineers/blob/master/datadog_screenshots/check_sql.png" />

MySQL is shown to be configured and can be seen on the dashboard:
<img src="https://github.com/alexandera9996/hiring-engineers/blob/master/datadog_screenshots/mysql_dashboard.png" />

### Adding a custom Agent check
Again, I spent alot of time reading through the agent_check documentation. From the guidelines and example .py and .yaml files in that document, I created two files, one python file named my_metric.py which was placed in directory /etc/datadog-agent/checks.d/my_metric.py. The other files, my_metric.yaml was placed in directory /etc/datadog-agent/conf.d/my_metric.yaml.
My my_metric.py:

<img src="https://github.com/alexandera9996/hiring-engineers/blob/master/datadog_screenshots/my_metric_py.png" />

My my_metric.yaml:

<img src="https://github.com/alexandera9996/hiring-engineers/blob/master/datadog_screenshots/my_metric_yaml.png" />

Also remember to restart the Agent so that the metrics can be updated. 

We are now creating random numbers between 0-1000 as seen on my dashboard.
<img src="https://github.com/alexandera9996/hiring-engineers/blob/master/datadog_screenshots/my_metric_dash.png" />

To change my checks collection interval so that it only submits once every 45 seconds is done by changing my_metric.yaml. Now according to the checks_agent documentation, the ```min_collection_interval``` is defaulted to 0 seconds when it is not added. 
my_metric.yaml now looks like this with a collection interval time of 45 seconds:
<img src="https://github.com/alexandera9996/hiring-engineers/blob/master/datadog_screenshots/interval_my_metric.png" />
<img src="https://github.com/alexandera9996/hiring-engineers/blob/master/datadog_screenshots/collection_metric.png" />

*Bonus: Can you change the collection interval without modifying the Python check file you created?*
Yes, I can change the interval by editing my my_metric.yaml file and setting ```min_collection_interval``` to 45. 


## Visualizing Data

### Creating a Timeboard

To approach this problem, I started reading about the basics of Dashboards which is a strong gateway into learning about the specifics of a Timeboard. In addition, since the Timeboard will be requesting data, I learned I will need an APP and API key.
First we need to install the python Datadog module onto our machine. 

```
pip install datadog
```
Next our API key can be found in the integrations tab under APIs on our event page. As such, we can also generate our new APP key from this tab too.

In my ```/etc/datadog-agent``` directory I created my python file, ```my_timeboard.py``` for my Timeboard.
My python file contains the necessary code to show:
1. Your custom metric scoped over your host.
2. Any metric from the Integration on your Database with the anomaly function applied.
3. Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
```
from datadog import initialize, api

options = {
    'api_key': 'YOUR API KEY', 
    'app_key': 'YOUR APP KEY'
}

initialize(**options)

title = "My Timeboard"
description = "An informative timeboard."
graphs = [{
#custom metric scoped over host 
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{host:kiwi-HP-15-Notebook-PC}"}
        ],
        "viz": "timeseries"
    },
    "title": "Your custom metric scoped over your host."
},
#any metric(in this case, MySQL) with anomaly function
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:mysql.performance.threads_running{*}, 'basic', 2)"}
        ],
        "viz": "timeseries"
    },
    "title": "MySQL metric, mysql.performance.threads_running, with anomaly function"
},
#custom metric with rollup function
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{*}.rollup(sum, 3600)"}
        ],
        "viz": "timeseries"
    },
    "title": "custom metric with the rollup function"
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

Execute the python script.

```
python my_timeboard.py
```

Restart the datadog Agent.

As you can see here, you can access your Timeboard from the dashboard list in the dashboard tab. Looking at mine for reference, you should've created three graphs to show the metrics.  

<img src="https://github.com/alexandera9996/hiring-engineers/blob/master/datadog_screenshots/datadog_screenshots2/dashboard_timeboard.png" />

Link to [my Timeboard](https://app.datadoghq.com/dash/913060/my-timeboard?live=true&page=0&is_auto=false&from_ts=1536704020478&to_ts=1536707620478&tile_size=m)

### Set the Timeboard frame to the past 5 minutes

Manually highlight the time interval I would like to observe. Improving the custom interval option with seconds, minutes, and hours would be easier on the user. 

Below is my Timeboard metrics from the last 5 minutes:

<img src="https://github.com/alexandera9996/hiring-engineers/blob/master/datadog_screenshots/datadog_screenshots2/timeboard_five.png" />

I also sent a snapshot of my_metric to my feed using the camera icon in the top right corner of the desired graph I wanted to send:

<img src="https://github.com/alexandera9996/hiring-engineers/blob/master/datadog_screenshots/datadog_screenshots2/graph_notation.png" />

*Bonus: What is the Anomaly graph displaying?*
Based on the Anomaly documenation, the Anomaly graph is designed to show its user any anomalies that the metric encounters. It does this by comparing previous data with the current data. If there's a drastic change, the graph will spike and show the anomaly with a red graph line. It's a great way to alert its users that the metric might be trending in the wrong direction. 

For my example, my chosen MySQL metric stayed constant, but since I'm only using it for this assignment right now, the same size is small, but with huge amounts of the data there will be inconsistencies that its user will need to report.  


### Monitoring Data
In this step, I want to create a new Monitor that will alert if it’s above the following values over the past 5 minutes:
1. Warning threshold of 500
2. Alerting threshold of 800
3. And also ensure that it will notify you if there is No Data for this query over the past 10m.

I created a new metric Monitor in the Monitors tab after reading about [the metric monitor documentation](https://docs.datadoghq.com/monitors/monitor_types/metric/). These are the steps I took in creating the new metric Monitor:

<img src="https://github.com/alexandera9996/hiring-engineers/blob/master/datadog_screenshots/datadog_screenshots2/met_mon1.png" />

<img src="https://github.com/alexandera9996/hiring-engineers/blob/master/datadog_screenshots/datadog_screenshots2/met_mon2.png" />

<img src="https://github.com/alexandera9996/hiring-engineers/blob/master/datadog_screenshots/datadog_screenshots2/met_mon3.png" />

Once I created the metric Monitor, notifications were sent to my email. Here is my warning:

<img src="https://github.com/alexandera9996/hiring-engineers/blob/master/datadog_screenshots/datadog_screenshots2/alert_email.png" />


*Bonus:  Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:*
*One that silences it from 7pm to 9am daily on M-F,*
*And one that silences it all day on Sat-Sun.*
*Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.*

To schedule a downtime for this monitor, I navigated to the Manage Downtime tab. From there I scheduled a downtime for my Monitor for the weekend and weekdays.

#### My weekday downtimes and notification:

<img src="https://github.com/alexandera9996/hiring-engineers/blob/master/datadog_screenshots/datadog_screenshots2/weekday_alert1.png" />

<img src="https://github.com/alexandera9996/hiring-engineers/blob/master/datadog_screenshots/datadog_screenshots2/weekday_alert2.png" />

<img src="https://github.com/alexandera9996/hiring-engineers/blob/master/datadog_screenshots/datadog_screenshots2/weekday_notify.png" />


#### My weekend downtimes and notification:

<img src="https://github.com/alexandera9996/hiring-engineers/blob/master/datadog_screenshots/datadog_screenshots2/weekend_alert1.png" />

<img src="https://github.com/alexandera9996/hiring-engineers/blob/master/datadog_screenshots/datadog_screenshots2/weekend_alert2.png" />

<img src="https://github.com/alexandera9996/hiring-engineers/blob/master/datadog_screenshots/datadog_screenshots2/weekend_notify.png" />


Once you have created your downtimes, you should receive an email notifying you of your scheduled downtimes. 


## Collecting APM Data



## Final Question

*Is there anything creative you would use Datadog for?*
Yes, there are many things I would love to use Datadog for. One such idea I would use Datadog for is for fantasy basketball, football, baseball, and/or hockey. I'm a fan of fantasy basketball and football so this idea would go more in-depth about those. 
For fantasy basketball I would:
```

```

For fantasy football I would:
```
```






