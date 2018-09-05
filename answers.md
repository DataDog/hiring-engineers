

# So let's get going - Gerd Plewka, Germany...

Applying as a solutions engineer at Datadog I do feel at the right spot right now...

...and yes, I learnt a lot about Datadog...

...and here is the current view from my desk ;*) ...

<img src=https://github.com/GerdPlewka/hiring-engineers/blob/master/current_view_from_my_desk.jpg width="500"> 


# The Exercise

## Questions

### Prerequisites - Setup the environment
*Vagrant Ubuntu VM installed*

```script
vagrant@precise64:~$ uname -a
Linux precise64 3.2.0-23-generic #36-Ubuntu SMP Tue Apr 10 20:39:51 UTC 2012 x86_64 x86_64 x86_64 GNU/Linux
```
*ok, could use some update...anyway...*

*Datadog agent installed...*



### Collecting Metrics

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

<a href="https://app.datadoghq.com/infrastructure/map?fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=availability-zone&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=true&palette=green_to_orange&paletteflip=false&node_type=host" title="Initial Hostmap">
<img src="https://github.com/GerdPlewka/hiring-engineers/blob/master/InitialHostmap.png" width="750" alt="Initial Hostmap"></a>

* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

```
vagrant@precise64:~$ mysql --version
mysql  Ver 14.14 Distrib 5.5.54, for debian-linux-gnu (x86_64) using readline 6.2
```

* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000. 

* Change your check's collection interval so that it only submits the metric once every 45 seconds.

* Bonus Question Can you change the collection interval without modifying the Python check file you created?

*./checks.d/my_metric.py*

``` Python
import random

from checks import AgentCheck
 
class my_metric(AgentCheck):
	def check(self, instance):
		self.gauge('my_metric', random.randint(1,1001))

```
     
*./conf.d/my_metric.yaml*

``` YAML
init_config:
    min_collection_interval: 45

instances:
    [{}]
```

*setting min_collecting_interval also is the answer to the bonus question...*


### Visualizing Data

Utilize the Datadog API to create a Timeboard that contains:

* Your custom metric scoped over your host.
* Any metric from the Integration on your Database with the anomaly function applied.
* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

*slight challenge here with the exact syntax of the anomalies command*

*...start with the code...*

*GerdsChallenge.sh*

```
api_key=22a62687a16651ff40ac350700bd1489
app_key=5f391773d79ec9ec871d5b1015ca2bd59f86a1de

curl  -X POST -H "Content-type: application/json" \
-d '{
        "title" : "Gerds API Timeboard",
        "description" : "API generated timeboard",
        "template_variables": [{
            "name": "host1",
            "prefix": "host",
            "default": "precise64"
            }],
        "graphs" : [{
            "title": "Gerds custom metric",
            "definition": {
                "events": [],
                "requests": [
                    {"q": "my_metric{host:precise64} "}
                ],
                "viz": "timeseries"
            }
        },
        {
            "title": "MYSQL anomalies"
            "definition": {
            "events": [],
            "requests": [
                {"q": "anomalies(avg:mysql.performance.user_time{host:precise64}, 'basic', 2)"}
                ],
            "viz": "timeseries"}
        },
        {
            "title": "Rollup",
            "definition": {
                "events": [],
                "requests": [
                    {"q": "avg:my_metric{host:precise64}.rollup(sum,3600)"}
                ],
                "viz": "query_value"
            }
        }
      ]
}' \
"https://api.datadoghq.com/api/v1/dash?api_key=${api_key}&application_key=${app_key}"
```

<a href="https://app.datadoghq.com/dash/904666/gerds-api-timeboard?live=true&page=0&is_auto=false&from_ts=1536152782224&to_ts=1536167182224&tile_size=m" title="Initial Timeboard">
<img src="https://github.com/GerdPlewka/hiring-engineers/blob/master/InitialTimeboard.png" width="750" alt="Initial Timeboard"></a>

* Set the Timeboard's timeframe to the past 5 minutes
Take a snapshot of this graph and use the @ notation to send it to yourself.

*I liked the @ notification, especially the preconfigured selection list...*

<img src="https://github.com/GerdPlewka/hiring-engineers/blob/master/5min%20graph.png" width="500" alt="5 minute graph">

* **Bonus Question:** What is the Anomaly graph displaying?

*not sure, if this question is really meant this straight forward...
It is showing which data are outside the upper or lower bounds, that were calculated out of the past metric values.
From here, one can create triggers (monitors) to create actions for alerting, or other actions*


### Monitoring Data

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

* Warning threshold of 500
* Alerting threshold of 800
* And also ensure that it will notify you if there is No Data for this query over the past 10m.

*...well, that was easy...*

<a href="https://app.datadoghq.com/monitors/6198785" title="Metric Monitor">
<img src="https://github.com/GerdPlewka/hiring-engineers/blob/master/metric%20monitor1.png" width="750" alt="Metric Monitor"></a>
<a href="https://app.datadoghq.com/monitors/6198785" title="Metric Monitor">
<img src="https://github.com/GerdPlewka/hiring-engineers/blob/master/metric%20monitor2.png" width="750" alt="Metric Monitor"></a>

Please configure the monitor’s message so that it will:

* Send you an email whenever the monitor triggers.

* Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.

* Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.

*you can see this configuration on the first monitor snapshot, attached here once again
Have a look at the **Message Section***

<img src="https://github.com/GerdPlewka/hiring-engineers/blob/master/metric%20monitor1.png" width="500" alt="Have a look at the Message section">

When this monitor sends you an email notification, take a screenshot of the email that it sends you.

*that went smoothly*

<img src="https://github.com/GerdPlewka/hiring-engineers/blob/master/WarningAlert.png" width="500" alt="Warning Alert from my mail">

* **Bonus Question:** Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

	* One that silences it from 7pm to 9am daily on M-F,
	* And one that silences it all day on Sat-Sun.
	* Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification

*I have taken snapshots both of the definition, and the mails*

*start with the definition*

<img src="https://github.com/GerdPlewka/hiring-engineers/blob/master/Silenced%20Monitor%20UI1.png" width="500">
<img src="https://github.com/GerdPlewka/hiring-engineers/blob/master/Silenced%20Monitor%20UI2.png" width="500">

*and here are the confirmation emails*

<img src="https://github.com/GerdPlewka/hiring-engineers/blob/master/Silenced%20Monitor%20Mail%201.png" width="500">
<img src="https://github.com/GerdPlewka/hiring-engineers/blob/master/Silenced%20Monitor%20Mail%202.png" width="500">

### Collecting APM Data

Given the ... Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:

*wow, that was a challenge because of a broken Python installation, took some time to discover*

*...but here is the result...*

Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

*...a little bit clunky, could be more beautifully integrate, but it shows the trick...*

<a href="https://app.datadoghq.com/dash/904666/gerds-api-timeboard?live=true&page=0&is_auto=false&from_ts=1535957036725&to_ts=1535971436725&tile_size=m" title="Combined Timeboard">
<img src="https://github.com/GerdPlewka/hiring-engineers/blob/master/Combined%20APM%20and%20Infrastructure.png" width="750" alt="Combined Timeboard"></a>



* **Bonus Question:** What is the difference between a Service and a Resource?

*A "service" is a set of processes, whereas a "resource" is any data that is returned, when querying a "service"*

### Final Question
Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?

**2 things immediately come to my mind:** * 

* *Look into what can be done in terms of aggregating data for security personnel (I am holding a CISSP)
I do think here about integrating Network security, Intrusion detection and (Web-)application data. Bz doing so, the value of an integrated APM and Infrastructure monitoring would become visible to customers with relevant security requirements*
* *see, if I can buy a multisensor [Bosch xdk](http://xdk.bosch-connectivity.com/overview) or [Thingsee One](https://thingsee.com/thingsee-one/), bring it to work and generate some valuable IoT data and visualize them with Datadog, in order to have a good example for the use of Datadog in IoT (small devices to show, and visualizations are **always** catching interest*



### About Me
Physicist, evangelist, technical all-rounder, curious, eager learner...
