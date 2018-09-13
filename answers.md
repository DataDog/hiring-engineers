# Solutions Engineer Exercise

## Setup
For this open source exercise I'm running Ubuntu 16.04 on my device. Before installing the agent, I read through the documentation located at the bottom of the assignment in order to gain an understanding of the Datadog agent.  

Download the Datadog Agent in terminal.
You will be given your own API key(DO NOT show your API key to the public)
```
DD_API_KEY=YOUR_API_KEY bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```
<img src="https://github.com/alexandera9996/hiring-engineers/blob/Alexander_Angelidis_Solutions_Engineer/datadog_screenshots/agent_ok.png" />

Finish by following the instructions on how to create a 14 day trial account on Datadog.

## Collecting Metrics
Tagging gives the user a method of aggregating data across a number of hosts. This is useful because users can then compare and observe how metrics behave across a number of hosts or collection of systems. 

Navigate to Datadog directory via terminal or any other unix interface of your choosing. 

#### Almost everything in this exercise will be executed through your unix command-line.

```
cd /etc/datadog-agent
```
Open Datadog.yaml:
```
sudo vim Datadog.yaml
```
Configure your .yaml file and change the tags to your preference. These are my tags:
<img src="https://github.com/alexandera9996/hiring-engineers/blob/Alexander_Angelidis_Solutions_Engineer/datadog_screenshots/tags.png" />

Restart the agent:

```
sudo service datadog-agent restart
```

Navigate to Host Map page in Data dog. Reload the page if your new tags do not appear.
Here is my Host Page map for reference.
<img src="https://github.com/alexandera9996/hiring-engineers/blob/Alexander_Angelidis_Solutions_Engineer/datadog_screenshots/Host_page.png" />

### Install a database. For this part, I went ahead with MySQL.
to install MySQL, run:
```
sudo apt-get update
sudo apt-get install mysql-server
```
After installation, configure it with Datadog.
First I create a datadog user with replication rights in my MySQL server. Then I add the full metrics found in the Datadog integration page. These configurations can be found [here](https://app.datadoghq.com/account/settings#integrations/mysql).

Next I edit ```mysql.yaml``` in the directory ```/etc/datadog-agent/conf.d/```

<img src="https://github.com/alexandera9996/hiring-engineers/blob/Alexander_Angelidis_Solutions_Engineer/datadog_screenshots/mysql_yaml.png" />

To see that MySQL is sucessfully running its metrics, restart the Datadog agent then type, 

```
sudo datadog-agent status
```

This shows that my metric is running successfully:

<img src="https://github.com/alexandera9996/hiring-engineers/blob/Alexander_Angelidis_Solutions_Engineer/datadog_screenshots/check_sql.png" />

MySQL is shown to be configured and can be seen on the dashboard:

<img src="https://github.com/alexandera9996/hiring-engineers/blob/Alexander_Angelidis_Solutions_Engineer/datadog_screenshots/mysql_dashboard.png" />

### Adding a custom Agent check
Again, I spent alot of time reading through the agent_check documentation. From the guidelines and example .py and .yaml files in that document, I need to create two files, one python file named my_metric.py which was placed in directory /etc/datadog-agent/checks.d/my_metric.py. The other files, my_metric.yaml was placed in directory ```/etc/datadog-agent/conf.d/my_metric.yaml```

My my_metric.py:

<img src="https://github.com/alexandera9996/hiring-engineers/blob/Alexander_Angelidis_Solutions_Engineer/datadog_screenshots/my_metric_py.png" />

My my_metric.yaml:

<img src="https://github.com/alexandera9996/hiring-engineers/blob/Alexander_Angelidis_Solutions_Engineer/datadog_screenshots/my_metric_yaml.png" />

Also remember to restart the Agent so that the metrics can be updated. 

We are now creating random numbers between 0-1000 as seen on my dashboard:

<img src="https://github.com/alexandera9996/hiring-engineers/blob/Alexander_Angelidis_Solutions_Engineer/datadog_screenshots/my_metric_dash.png" />

To change my checks collection interval so that it only submits once every 45 seconds is done by changing ```my_metric.yaml```. Now according to the checks_agent documentation, the ```min_collection_interval``` is defaulted to 0 seconds when it is not added. 
```my_metric.yaml``` now looks like this with a collection interval time of 45 seconds:

<img src="https://github.com/alexandera9996/hiring-engineers/blob/Alexander_Angelidis_Solutions_Engineer/datadog_screenshots/interval_my_metric.png" />

<img src="https://github.com/alexandera9996/hiring-engineers/blob/Alexander_Angelidis_Solutions_Engineer/datadog_screenshots/collection_metric.png" />

*Bonus: Can you change the collection interval without modifying the Python check file you created?*

Yes, I can change the interval by editing the ```my_metric.yaml``` file and setting ```min_collection_interval``` to 45. 


## Visualizing Data

### Creating a Timeboard

To approach this problem, I started reading about the basics of Dashboards which is a strong gateway into learning about the specifics of a Timeboard. In addition, since the Timeboard will be requesting data, I learned I will need an APP and API key to have authentication.

First we need to install the python Datadog module onto our machine using: 

```
pip install datadog
```

Next our API key can be found in the integrations tab under APIs on our event page. As such, we can also generate our new APP key from this tab too.


Taking the sample code from the Timeboard documentation, I navigated to my ```/etc/datadog-agent``` directory and created a python file, ```my_timeboard.py``` for my Timeboard. I added two definitions to ```my_timeboard.py``` so that I could display the anomaly and roll-up functions. 
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

<img src="https://github.com/alexandera9996/hiring-engineers/blob/Alexander_Angelidis_Solutions_Engineer/datadog_screenshots/datadog_screenshots2/dashboard_timeboard.png" />

Link to [my Timeboard](https://app.datadoghq.com/dash/913060/my-timeboard?live=true&page=0&is_auto=false&from_ts=1536704020478&to_ts=1536707620478&tile_size=m)

### Set the Timeboard frame to the past 5 minutes

Manually highlight the time interval I would like to observe. Something I'd like to note is improving the custom interval option with seconds, minutes, and hours would allow more functionality on the user. 

Below is my Timeboard metrics from the last 5 minutes:

<img src="https://github.com/alexandera9996/hiring-engineers/blob/Alexander_Angelidis_Solutions_Engineer/datadog_screenshots/datadog_screenshots2/timeboard_five.png" />

I also sent a snapshot to my feed using the camera icon located in the top right corner of the desired graph I wanted to send:

<img src="https://github.com/alexandera9996/hiring-engineers/blob/Alexander_Angelidis_Solutions_Engineer/datadog_screenshots/datadog_screenshots2/graph_notation.png" />

*Bonus: What is the Anomaly graph displaying?*

Based on the Anomaly documenation, the Anomaly graph is designed to show its user any anomalies that the metric encounters. It does this by comparing previous data with the current data. If there's a drastic change, the graph will spike and show the anomaly with a red graph line. It's a great way to alert its users that the metric might be trending in the wrong direction. 

For my example, my chosen MySQL metric stayed constant, but since I'm only using it for this assignment right now, the sample size is small, but with huge amounts of the data there could be inconsistencies or drops that its user will need to report.  


### Monitoring Data
In this step, I want to create a new Monitor that will alert me if it’s above the following values over the past 5 minutes:
1. Warning threshold of 500
2. Alerting threshold of 800
3. And also ensure that it will notify you if there is No Data for this query over the past 10m.

I created a new metric Monitor in the Monitors tab after reading about [the metric monitor documentation](https://docs.datadoghq.com/monitors/monitor_types/metric/). These are the steps I took in creating the new metric Monitor:

<img src="https://github.com/alexandera9996/hiring-engineers/blob/Alexander_Angelidis_Solutions_Engineer/datadog_screenshots/datadog_screenshots2/met_mon1.png" />

<img src="https://github.com/alexandera9996/hiring-engineers/blob/Alexander_Angelidis_Solutions_Engineer/datadog_screenshots/datadog_screenshots2/met_mon2.png" />

<img src="https://github.com/alexandera9996/hiring-engineers/blob/Alexander_Angelidis_Solutions_Engineer/datadog_screenshots/datadog_screenshots2/met_mon3.png" />

Once I created the metric Monitor, notifications were sent to my email. Here is my warning:

<img src="https://github.com/alexandera9996/hiring-engineers/blob/Alexander_Angelidis_Solutions_Engineer/datadog_screenshots/datadog_screenshots2/alert_email.png" />


*Bonus:  Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:*
*One that silences it from 7pm to 9am daily on M-F,*
*And one that silences it all day on Sat-Sun.*
*Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.*

To schedule a downtime for this monitor, I navigated to the Manage Downtime tab. From there I scheduled a downtime for my Monitor for the weekend and weekdays.

#### My weekday downtimes and notification:

<img src="https://github.com/alexandera9996/hiring-engineers/blob/Alexander_Angelidis_Solutions_Engineer/datadog_screenshots/datadog_screenshots2/weekday_alert1.png" />

<img src="https://github.com/alexandera9996/hiring-engineers/blob/Alexander_Angelidis_Solutions_Engineer/datadog_screenshots/datadog_screenshots2/weekday_alert2.png" />

<img src="https://github.com/alexandera9996/hiring-engineers/blob/Alexander_Angelidis_Solutions_Engineer/datadog_screenshots/datadog_screenshots2/weekday_notify.png" />


#### My weekend downtimes and notification:

<img src="https://github.com/alexandera9996/hiring-engineers/blob/Alexander_Angelidis_Solutions_Engineer/datadog_screenshots/datadog_screenshots2/weekend_alert1.png" />

<img src="https://github.com/alexandera9996/hiring-engineers/blob/Alexander_Angelidis_Solutions_Engineer/datadog_screenshots/datadog_screenshots2/weekend_alert2.png" />

<img src="https://github.com/alexandera9996/hiring-engineers/blob/Alexander_Angelidis_Solutions_Engineer/datadog_screenshots/datadog_screenshots2/weekend_notify.png" />


Once I created my downtimes, I received an email notifying me of my scheduled downtimes. A notification will also be sent if the downtimes are updated. 


## Collecting APM Data
I would recommend re-looking over [the APM tracing setup](https://docs.datadoghq.com/tracing/setup/python/) and then further reading about [flask](http://pypi.datadoghq.com/trace/docs/web_integrations.html#flask) and then about [blinker](https://pythonhosted.org/blinker/).

### Using Datadog's APM code:

I already had Flask installed, but to install Flask:
```
pip install Flask
```
Now install the Datadog Tracing library, ddtrace:
```
pip install ddtrace
```
If you're using the Flask trace middleware to track request timings, it requires the Blinker library
```
pip install blinker
```

In order to use our APM trace collection for our Agent, we need to update the ```apm_config``` key in ```datadog.yaml```
Here is my ```datadog.yaml``` file for reference:

<img src="https://github.com/alexandera9996/hiring-engineers/blob/Alexander_Angelidis_Solutions_Engineer/datadog_screenshots/datadog_screenshots3/apm_config.png" />

Once you have reconfigured your agent, restart the Agent service.

Now to analyze the performance of my application I will create my python file ```my_apm.py```. For this part I decided on manually inserting the Middleware.  

Here is the script of my python file:

```
from flask import Flask
import logging
import sys

#~~~~~~~~~~~~~~~~
import blinker as _

from ddtrace import tracer
from ddtrace.contrib.flask import TraceMiddleware
#~~~~~~~~~~~~~~~

# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

app = Flask(__name__)

#~~~~~~~~~~~~~~
traced_app = TraceMiddleware(app, tracer, service="my-flask-app", distributed_tracing=False)
#~~~~~~~~~~~~~~
@app.route('/')
def api_entry():
    return 'Entrypoint to the Application'

@app.route('/api/apm')
def apm_endpoint():
    return 'Getting APM Started'

@app.route('/api/trace')
def trace_endpoint():
    return 'Posting Traces'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5050')
```

I ran my script with:
```
python my_apm.py
```

Test the https links in your web browser to start APM and traces:
```
http://0.0.0.0:5050
http://0.0.0.0:5050/api/apm
http://0.0.0.0:5050/api/trace
```
Your terminal should now be interacting with the application:

<img src="https://github.com/alexandera9996/hiring-engineers/blob/Alexander_Angelidis_Solutions_Engineer/datadog_screenshots/datadog_screenshots3/apm_terminal.png" />

Looks like Datadog has received the traces and the data can be viewed!

<img src="https://github.com/alexandera9996/hiring-engineers/blob/Alexander_Angelidis_Solutions_Engineer/datadog_screenshots/datadog_screenshots3/datadog_flask.png" />

Under the APM tab, select the traces option to view traces like this:

<img src="https://github.com/alexandera9996/hiring-engineers/blob/Alexander_Angelidis_Solutions_Engineer/datadog_screenshots/datadog_screenshots3/trace_search.png" />

Now I also added the APM metrics and infrastructure metrics to my new Dashboard by adding metric graphs:

<img src="https://github.com/alexandera9996/hiring-engineers/blob/Alexander_Angelidis_Solutions_Engineer/datadog_screenshots/datadog_screenshots3/apm_dash.png" />

The link to my Dashboard in real time can be accessed [here](https://app.datadoghq.com/dash/914487/apm--metric-dashboard?live=true&page=0&is_auto=false&from_ts=1536801800142&to_ts=1536805400142&tile_size=m).


## Final Question

*Is there anything creative you would use Datadog for?*

Yes, there are many things I would love to use Datadog for. One such idea I would use Datadog for is for fantasy basketball, football, baseball, and/or hockey. I'm a fan of fantasy basketball and football so this idea would go more in-depth about those. Typically, participants make their changes in their fantasy lineup because they are watching the game live or they are notified from a sports application such as Bleacher Report, ESPN, or NFL network which usually takes at least a half hour before reporters report the information. With data collected from Datadog's Agent collector, users can be notified instantly, allowing them to have a competitive advantage over their peers. 

For fantasy basketball I would:
```
Use the Agent's collector to collect metrics on individual players stats such as fg%, ft%, TO's, Rebounds, Points scored.
If a player performs unusually well, have Datadog send an anomaly alert to the user.
```

For fantasy football I would:
```
Use the Agent's collector to collect metrics on individual players stats such as total yards, TD's scored, fumbles.
Notify me when a players production dips to 0 due to injury. 
```
With Datadog's product, users can record and analyze huge amounts of data applied to an array of topics. Using them for fantasy applications is only a fraction of what we could use Datadog for. 


## How I approached this exercise

This exercise was challenging but also educational. While a majority of the code could be found in various Datadog documentation, learning about the many aspects of Datadog's product was the most interesting part of this assignment. Re-reading the documentation as I progressed helped me understand more about that particular aspect I was working on. As far as the documentation goes, it was the gateway to completing this project since everything I needed to learn could be found in them.    



