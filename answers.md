### JAIME ALONSO answers 

Hi,

This is Jaime Alonso from DataDog. My goal today is to show you not only the strengths and deep insight DatDog is able to provide you but also the easy-of-use and the friendly management and configuration. This makes DataDog the best tool to have visibility across **any cloud, any app, any metric**

## Collecting Metrics:

First of all, we will start by collecting metrics. For this example, we have installed the DataDog agent in an Ubuntu VM.
In order to add dimensions to metrics, so they can be filtered, aggregated, and compared, we can use **tags**. We can easily add tags in the UI or by editing the agent file, in this case we have added two, one to identify the host owner (`host:Jaime`) and another one for the environment (`env:demo`). Immediately, we can use hostMap UI to visualize our server and the tags, here there is only one but if we add more hosts with the same tags we will be able to visualizing all together:

<a data-flickr-embed="true"  href="https://www.flickr.com/photos/147840972@N03/47505496652/in/dateposted-public/" title="Capture"><img src="https://live.staticflickr.com/7815/47505496652_99c846d5ee_h.jpg" width="1600" height="744" alt="Capture"></a>


DataDog admits more than +200  built-in **integrations**. In this case we have installed a postgreSQL DB in our host, and then in order to start collecting  metrics we just need to modify the `postgres.d/conf.yaml` in the agent config  directory. This file also accepts tagging so we can filter not only by hosts, but also by app.

```
instances:
  - host: localhost
    port: 5432
    username: datadog
    password: kmEcy8FcXk6sOpZRDF2HeDxK
    tags:
      - jaime_sql
      - demo_sql
```

DataDog brings by default lots of metrics in order to collect information from a broad environment but following the idea of “any host, any app” it also allows us to submit **custom metrics**. Here we have created a python script which submits a custom metric what is basically a random number between 1 and 1000:

```
import random
# the following try/except block will make the custom check compatible with any Agent version
try:
    # first, try to import the base class from old versions of the Agent...
    from checks import AgentCheck
except ImportError:
    # ...if the above failed, the check is running in Agent version 6 or later
    from datadog_checks.checks import AgentCheck

# content of the special variable __version__ will be shown in the Agent status page
__version__ = "1.0.0"


class HelloCheck(AgentCheck):
    def check(self, instance):
        var = random.randint(1, 1000)
        self.gauge('my_metric', var)

```

Then as with the postgresSQL integration we can create a custom integration for my metric by adding a configuration file in the agent conf.d directory. Here we want the metric to be collected every 45 secs to we add the min_collection_interval variable:

`/etc/datadog-agent/conf.d/my_metric.yaml:`
```
root@precise64:/etc/datadog-agent/conf.d# more my_metric.yaml
init_config:

instances:
  - min_collection_interval: 45
```

## Visualizing Data:

Now that our environment has been configured to collect the data it is time to start visualizing it. For this we would like to show you also the strength and easy-to-use of the the **Datadog API**.

We can use the API through different methods, like pythong ruby or curl.

Below example shows how to create a timeboard using API through curl. It will create a timeboard which contains our custom metric scoped over our host. And also a rollup function applied to sum up all the points for the past hour:
```
api_key=8afff3f9fbf730889172d9f07993a9bb
app_key=95bd59d7e0acaee62fcc3e54aa6d276cfdcabc05
dashboard_id="jaime_dashboard_api"

curl  -X POST -H "Content-type: application/json" \
-d '{
      "title" : "Jaime API dashboard v2",
      "widgets" : [{
          "definition": {
              "type": "timeseries",
              "requests": [
                  {"q": "avg:my_metric{host:jaime}, hour_before(avg:my_metric{host:jaime}.rollup(sum))"}
              ],
              "title": "My timeboard"
          }
      }],
      "layout_type": "ordered",
      "description" : "Jaime API dashboard",
      "notify_list": ["user@domain.com"],
      "template_variables": [{
          "name": "host1",
          "prefix": "host",
          "default": "my-host"
      }]
}' \
"https://api.datadoghq.com/api/v1/dashboard?api_key=${api_key}&application_key=${app_key}"

```
After that, using the UI we can modify the Timeboard. Here we have added a **anomaly** function to the metric max_connections of our PostgreSQL in order to detect any if a metric is behaving abnormally, in this case if anyone has changed the max_connection configuration which could affect the entire host performance:

<a data-flickr-embed="true"  href="https://www.flickr.com/photos/147840972@N03/46848741134/in/dateposted-public/" title="timeboard"><img src="https://live.staticflickr.com/7854/46848741134_1951f13929_z.jpg" width="640" height="295" alt="timeboard"></a>

We can also modify the Timeboard’s timeframe and take real time graph **annotations**. In this case I have selected the past 5 minutes, take a snapshot and send it to myself:  

<a data-flickr-embed="true"  href="https://www.flickr.com/photos/147840972@N03/47505496682/in/dateposted-public/" title="3 metrics"><img src="https://live.staticflickr.com/7828/47505496682_b95b49cb41_h.jpg" width="640" height="418"  alt="3 metrics"></a>

# Monitoring Data

DataDog allows us to have a **self driving** monitoring experience, letting us to focus on our business instead of being manually monitoring our environment.

To that end, we can create **Monitors**. As an example let’s create a monitor to watch the average of our custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:
*	Warning threshold of 500
*	Alerting threshold of 800
*	And also ensure that it will notify you if there is No Data for this query over the past 10m.
In order to create it, once again we can use the API or the UI. Here we are using the UI to create the monitor:

<a data-flickr-embed="true"  href="https://www.flickr.com/photos/147840972@N03/47572740111/in/dateposted-public/" title="alerts1"><img src="https://live.staticflickr.com/7828/47572740111_acf3c652e5_z.jpg" width="640" height="418" alt="alerts1"></a>

Besides of that, we can configure the notification method. Here we are going to create different messages based on whether the monitor is in an Alert, Warning, or No Data state. Message will include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state. Here you can see some samples:
TEST for each notification:
* ALERT:
<a data-flickr-embed="true"  href="https://www.flickr.com/photos/147840972@N03/47505496512/in/dateposted-public/" title="test alert"><img src="https://live.staticflickr.com/7909/47505496512_0bced4d492_h.jpg" width="640" height="418"  alt="test alert"></a>
* WARNING:
<a data-flickr-embed="true"  href="https://www.flickr.com/photos/147840972@N03/32615839867/in/dateposted-public/" title="test warn"><img src="https://live.staticflickr.com/7879/32615839867_db674cb099_h.jpg" width="640" height="418" alt="test warn"></a>
* NO DATA:
<a data-flickr-embed="true"  href="https://www.flickr.com/photos/147840972@N03/46834723974/in/dateposted-public/" title="test no data"><img src="https://live.staticflickr.com/7881/46834723974_3e4f7199e3_h.jpg" width="640" height="418" alt="test no data"></a>

* Real WARNING example:
<a data-flickr-embed="true"  href="https://www.flickr.com/photos/147840972@N03/47505496482/in/dateposted-public/" title="WARN"><img src="https://live.staticflickr.com/7923/47505496482_420f945101_h.jpg" width="640" height="418" alt="WARN"></a>

You can access that notification from the API:


```

root@precise64:/etc/postgresql/9.1/main# curl -G "https://api.datadoghq.com/api/v1/monitor/${monitor_id}" \
>      -d "api_key=${api_key}" \
>      -d "application_key=${app_key}" \
>      -d "group_states=all" |python -mjson.tool
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  1450  100  1450    0     0   3353      0 --:--:-- --:--:-- --:--:--  4545
{
    "created": "2019-04-06T20:47:21.455311+00:00",
    "created_at": 1554583641000,
    "creator": {
        "email": "jaime.alonso.romero@gmail.com",
        "handle": "jaime.alonso.romero@gmail.com",
        "id": 1174067,
        "name": "Jaime"
    },
    "deleted": null,
    "id": 9430123,
    "message": "{{#is_alert}}ALERT: My metric is at {{value}} above 800  with IP {{host.ip}}{{/is_alert}} \n{{#is_warning}}WARNING: My metric is at {{value}}  above   with IP {{host.ip}}{{/is_warning}} \n{{#is_no_data}}No data for the last 10 min {{/is_no_data}}  @jaime.alonso.romero@gmail.com",
    "modified": "2019-04-07T16:41:25.825670+00:00",
    "multi": true,
    "name": "My metric monitor",
    "options": {
        "escalation_message": "",
        "include_tags": true,
        "locked": false,
        "new_host_delay": 300,
        "no_data_timeframe": 10,
        "notify_audit": false,
        "notify_no_data": true,
        "renotify_interval": 0,
        "require_full_window": true,
        "silenced": {
            "*": 1554793200
        },
        "thresholds": {
            "critical": 800.0,
            "warning": 500.0
        },
        "timeout_h": 0
    },
    "org_id": 255247,
    "overall_state": "Warn",
    "overall_state_modified": "2019-04-07T16:39:44.304536+00:00",
    "query": "avg(last_5m):avg:my_metric{*} by {host} > 800",
    "state": {
        "groups": {
            "*": {
                "last_nodata_ts": 1554644263,
                "last_notified_ts": 1554655183,
                "last_resolved_ts": 1554654283,
                "last_triggered_ts": 1554655183,
                "name": "*",
                "status": "Warn"
            },
            "host:jaime,host:precise64": {
                "last_nodata_ts": null,
                "last_notified_ts": 1554659023,
                "last_resolved_ts": 1554658723,
                "last_triggered_ts": 1554659023,
                "name": "host:jaime,host:precise64",
                "status": "Warn"
            }
        }
    },
    "tags": [],
    "type": "metric alert"
}

```
Besides of that, we are aware that in order to be effective and accurate customers require to **mute notifications** when there are scheduled downtimes or even out of hours. Here we have configured two downtimes, 

  * One that silences it from 7pm to 9am daily on M-F,
  * And one that silences it all day on Sat-Sun.
 
<a data-flickr-embed="true"  href="https://www.flickr.com/photos/147840972@N03/33695868918/in/dateposted-public/" title="downtime2"><img src="https://live.staticflickr.com/7896/33695868918_5ea157ab64_z.jpg" width="640" height="347" alt="downtime2"></a>
<a data-flickr-embed="true"  href="https://www.flickr.com/photos/147840972@N03/33695868268/in/dateposted-public/" title="downtime1"><img src="https://live.staticflickr.com/7832/33695868268_ef50f12f34_z.jpg" width="640" height="335" alt="downtime1"></a>


We have also configured the notification to be notified when downtimes are scheduled:


<a data-flickr-embed="true"  href="https://www.flickr.com/photos/147840972@N03/40592510253/in/dateposted-public/" title="Downtime daily"><img src="https://live.staticflickr.com/7877/40592510253_4dbc0a5500_h.jpg" width="640" height="418"  alt="Downtime daily"></a>

<a data-flickr-embed="true"  href="https://www.flickr.com/photos/147840972@N03/46642957685/in/dateposted-public/" title="downtime weekend"><img src="https://live.staticflickr.com/7923/46642957685_c7da868707_h.jpg" width="640" height="418"  alt="downtime weekend"></a>


Once more everything is accessible using the API:
```
root@precise64:/etc/postgresql/9.1/main# curl -G "https://api.datadoghq.com/api/v1/downtime" \
>      -d "api_key=${api_key}" \
>      -d "application_key=${app_key}" |python -mjson.tool
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   948  100   948    0     0   1969      0 --:--:-- --:--:-- --:--:--  2881
[
    {
        "active": false,
        "canceled": null,
        "creator_id": 1174067,
        "disabled": false,
        "downtime_type": null,
        "end": 1554760800,
        "id": 500678534,
        "message": "mute my metric monitor on Sat-Sun. @jaime.alonso.romero@gmail.com",
        "monitor_id": 9430123,
        "monitor_tags": [
            "*"
        ],
        "org_id": 255247,
        "parent_id": null,
        "recurrence": {
            "period": 1,
            "type": "weeks",
            "until_date": null,
            "until_occurrences": null,
            "week_days": [
                "Sun",
                "Sat"
            ]
        },
        "scope": [
            "*"
        ],
        "start": 1554674400,
        "timezone": "Europe/Paris",
        "updater_id": null
    },
    {
        "active": false,
        "canceled": null,
        "creator_id": 1174067,
        "disabled": false,
        "downtime_type": null,
        "end": 1554793200,
        "id": 500304397,
        "message": " Mute from 7pm to 9am daily on M-F, @jaime.alonso.romero@gmail.com",
        "monitor_id": 9430123,
        "monitor_tags": [
            "*"
        ],
        "org_id": 255247,
        "parent_id": null,
        "recurrence": {
            "period": 1,
            "type": "weeks",
            "until_date": null,
            "until_occurrences": null,
            "week_days": [
                "Mon",
                "Tue",
                "Wed",
                "Thu",
                "Fri"
            ]
        },
        "scope": [
            "*"
        ],
        "start": 1554742800,
        "timezone": "Europe/Paris",
        "updater_id": null
    }
]
```

## Collecting APM Data:

Datadog APM provides you with deep insight into your **application’s performance-from** automatically generated dashboards monitoring key metrics, such as request volume and latency, to detailed traces of individual requests-side by side with your logs and infrastructure monitoring.

Here we have a simple web flask application:

```
root@precise64:/home/vagrant/my_app# more app.py
from ddtrace import patch_all
patch_all()
from ddtrace import tracer
tracer.set_tags({'env': 'PROD_JAIME'})
from flask import Flask
import logging
import sys

# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

app = Flask(__name__)

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

Below you can see a Dashboard showing the metric from the Network stack from host (system.net.tcp.in_segs) from the OS process (cpu for process app.py) and also traces from the application, in such a way it is very easy to correlate and understand the behavior of the application:

<a data-flickr-embed="true"  href="https://www.flickr.com/photos/147840972@N03/47505496602/in/dateposted-public/" title="dashboard"><img src="https://live.staticflickr.com/7808/47505496602_05a5c54803_h.jpg" width="1600" height="547" alt="dashboard"></a>

We are able to create an interactive dashboard with the data: 

<iframe src="https://app.datadoghq.com/graph/embed?token=0b3c0f28319a23dd2de5648f96470c6ac3d1d84cc1f68b4e9cc318d082ef6416&height=300&width=600&legend=false" width="600" height="300" frameborder="0"></iframe>

We can also have a further info using the UI showing some of the APM components, here we will see the following:

* Service: it is a set of processes that do the same job, it can be a single process or a set of process. In this particular case the service is the app itself.
<a data-flickr-embed="true"  href="https://www.flickr.com/photos/147840972@N03/32615839887/in/dateposted-public/" title="Service"><img src="https://live.staticflickr.com/7863/32615839887_f71ec96b92_h.jpg" width="1600" height="220" alt="Service"></a>
* Resources: Actions performed by the service. In this example we have three resources:

<a data-flickr-embed="true"  href="https://www.flickr.com/photos/147840972@N03/47505496572/in/dateposted-public/" title="resource"><img src="https://live.staticflickr.com/7866/47505496572_8b764daf4f_h.jpg" width="1600" height="257" alt="resource"></a>

## Final Question:

In a world where most of the software is being developed in "decoupled way", with thousands of microservices running in different clouds and communicating each other through a service mesh platform, having a tool which provides end to end visibility, monitoring and alerting, makes DataDog the best partner for your business.

**any cloud, any app, any metric**



