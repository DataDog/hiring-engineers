### JAIME ALONSO answers 

## Collecting Metrics:



* *Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.*

<a data-flickr-embed="true"  href="https://www.flickr.com/photos/147840972@N03/47505496652/in/dateposted-public/" title="Capture"><img src="https://live.staticflickr.com/7815/47505496652_99c846d5ee_h.jpg" width="1600" height="744" alt="Capture"></a>

* *Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.*

I installed postgresql and configured postgress.yaml integration file:
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
* *Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.*
my_metric.py pythong script:
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

* *Change your check's collection interval so that it only submits the metric once every 45 seconds.*
Output of /etc/datadog-agent/conf.d/my_metric.yaml
```
root@precise64:/etc/datadog-agent/conf.d# more my_metric.yaml
init_config:

instances:
  - min_collection_interval: 45
```
* **Bonus Question** *Can you change the collection interval without modifying the Python check file you created?*

Using the min_collection_interval in the configuration file


## Visualizing Data:

*Utilize the Datadog API to create a Timeboard that contains:*

* *Your custom metric scoped over your host.*
* *Any metric from the Integration on your Database with the anomaly function applied.*
* *Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket*

*Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.*

Created Timeboard using curl:
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
Tried to add the anomaly function using following script but got Json Parse error:

`anomalies(avg:postgresql.max_connections{host:jaime}, 'basic', 2)`

So I added it using UI with following results:

"https://app.datadoghq.com/graph/embed?token=7c1db6f1ca5f3c1d4264757db163bb6657ab82f1f68853471435e14b9efe02db&height=300&width=600&legend=true" 

Once this is created, access the Dashboard from your Dashboard List in the UI:

* Set the Timeboard's timeframe to the past 5 minutes
* Take a snapshot of this graph and use the @ notation to send it to yourself.
<a data-flickr-embed="true"  href="https://www.flickr.com/photos/147840972@N03/47505496682/in/dateposted-public/" title="3 metrics"><img src="https://live.staticflickr.com/7828/47505496682_b95b49cb41_h.jpg" width="1600" height="1145" alt="3 metrics"></a>
* **Bonus Question**: What is the Anomaly graph displaying?
It can be used to detect when a metric is behaving differently.

# Monitoring Data

Created following monitor:
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
TEST for each notification:
* ALERT:
<a data-flickr-embed="true"  href="https://www.flickr.com/photos/147840972@N03/47505496512/in/dateposted-public/" title="test alert"><img src="https://live.staticflickr.com/7909/47505496512_0bced4d492_h.jpg" width="1600" height="1041" alt="test alert"></a>
* WARNING:
<a data-flickr-embed="true"  href="https://www.flickr.com/photos/147840972@N03/32615839867/in/dateposted-public/" title="test warn"><img src="https://live.staticflickr.com/7879/32615839867_db674cb099_h.jpg" width="1600" height="1189" alt="test warn"></a>
* NO DATA:
<a data-flickr-embed="true"  href="https://www.flickr.com/photos/147840972@N03/46834723974/in/dateposted-public/" title="test no data"><img src="https://live.staticflickr.com/7881/46834723974_3e4f7199e3_h.jpg" width="1600" height="728" alt="test no data"></a>

* Real WARNING example:
<a data-flickr-embed="true"  href="https://www.flickr.com/photos/147840972@N03/47505496482/in/dateposted-public/" title="WARN"><img src="https://live.staticflickr.com/7923/47505496482_420f945101_h.jpg" width="1600" height="1225" alt="WARN"></a>



* **Bonus Question**: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

  * One that silences it from 7pm to 9am daily on M-F,
  * And one that silences it all day on Sat-Sun.
  * Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

Two downtimes configured as following:
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
Notification received for both downtimes:

<a data-flickr-embed="true"  href="https://www.flickr.com/photos/147840972@N03/40592510253/in/dateposted-public/" title="Downtime daily"><img src="https://live.staticflickr.com/7877/40592510253_4dbc0a5500_h.jpg" width="1600" height="880" alt="Downtime daily"></a>

<a data-flickr-embed="true"  href="https://www.flickr.com/photos/147840972@N03/46642957685/in/dateposted-public/" title="downtime weekend"><img src="https://live.staticflickr.com/7923/46642957685_c7da868707_h.jpg" width="1600" height="750" alt="downtime weekend"></a>

## Collecting APM Data:

app.py:
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
Link to dashboard with both 

<iframe src="https://app.datadoghq.com/graph/embed?token=0b3c0f28319a23dd2de5648f96470c6ac3d1d84cc1f68b4e9cc318d082ef6416&height=300&width=600&legend=false" width="600" height="300" frameborder="0"></iframe>

Dashboard showing system.net.tcp.in_segs/cpu for process app.py/hit flask requests:
<a data-flickr-embed="true"  href="https://www.flickr.com/photos/147840972@N03/47505496602/in/dateposted-public/" title="dashboard"><img src="https://live.staticflickr.com/7808/47505496602_05a5c54803_h.jpg" width="1600" height="547" alt="dashboard"></a><script async src="//embedr.flickr.com/assets/client-code.js" charset="utf-8"></script>

* Service: it is a set of processes that do the same job, it can be a single process or a set of process. In this particular case the service is the app itself.
<a data-flickr-embed="true"  href="https://www.flickr.com/photos/147840972@N03/32615839887/in/dateposted-public/" title="Service"><img src="https://live.staticflickr.com/7863/32615839887_f71ec96b92_h.jpg" width="1600" height="220" alt="Service"></a>
* Resources: Actions performed by the service. In this example we have three resources:

<a data-flickr-embed="true"  href="https://www.flickr.com/photos/147840972@N03/47505496572/in/dateposted-public/" title="resource"><img src="https://live.staticflickr.com/7866/47505496572_8b764daf4f_h.jpg" width="1600" height="257" alt="resource"></a>

## Final Question:

In a world where most of the software is being developed in "decoupled way", with thousands of microservices running in different cloud and communicating each other through a service mesh platform, having a tool which provides end to end visibility, monitoring and alert, put DataDog in a unique position in the market.
