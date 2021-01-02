**Prerequisites - Setup the environment**

For this section I went with a linux VM via Vagrant.

I followed the directions provided by Vagrant on the [VM Setup Page](https://learn.hashicorp.com/collections/vagrant/getting-started)

**Collecting Metrics Section**

_Exercise 1:
Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog._

Link:
[DataDog Host](https://app.datadoghq.com/infrastructure/map?host=3443516844&fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=availability-zone&nameby=aws_id&nometrichosts=false&tvMode=false&nogrouphosts=true&palette=green_to_orange&paletteflip=true&node_type=host)

Answer:
Below we have a screenshot of the Host Map. This can be viewed by heading to the sidebar on the DataDog home page and clicking on Infrastructure, then Host Map. To view the DD agent details, simply click on "Agent" within the host. This will direct the user to where the customized tags can be viewed on the front end. To add the tags on the back end, the Agent Configuration file would be to be configured.

/etc/datadog-agent/datadog.yaml  

Screenshots:
Agent on Host Map UI
![Alt text](/photos/host_map.png?raw=true&s=150 "Host Map and Tags")

_Exercise 2:
Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database._

Link:
https://app.datadoghq.com/infrastructure/map?host=3443516844&fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=availability-zone&nameby=aws_id&nometrichosts=false&tvMode=false&nogrouphosts=true&palette=green_to_orange&paletteflip=true&node_type=host

Answer:
To start the MongoDB's install process, from the Host Map, go to the sidebar and click on Integrations >> Integrations. This link directs the user to a page with a list of integration options. From here, search for MongoDB and follow the configuration steps.

Screenshots:
![Alt text](/photos/db_installed.png?raw=true&s=150 "MongoDB Integrations Page")

MongoDB reflecting on Host Map.
![Alt text](/photos/mongodb_host_map.png?raw=true&s=150 "MongoDB on Host Map")

_Exercise 3:
Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000._

Link:
https://app.datadoghq.com/metric/explorer?from_ts=1608782940389&to_ts=1608786540389&live=true&page=0&is_auto=false&tile_size=m&exp_metric=my_metric&exp_agg=avg&exp_row_type=metric

Answer:
To create a custom Agent check, create an empty directory named my_metric.d in /etc/datadog-agent/conf.d.
In this directory, create a file named my_metric.YAML. For now, place an empty list for the instances:

```
instances: [{}]

  ```

One level up from the conf.d/ folder is the check.d/ folder. Here create a custom check file named metric_example.py with the code from the screenshot below.

Then confirm the custom agent check on the front end by click on DD's sidebar >> metrics >> metric summary.
Once directed to the Mertric's Summary page, enter the Metric's name into the metric search bar.

Screenshots:
my_metric.py file
![Alt text](/photos/my_metric.png?raw=true "my_metric.py")

my_metric reflecting on the UI
![Alt text](/photos/ui_my_metric.png?raw=true "my_metric")

_Exercise 4:
Change your check's collection interval so that it only submits the metric once every 45 seconds._

Answer:
Changes are made on the the my_metric.YAML file.

![Alt text](/photos/min_collection_interval.png?raw=true "my_metric")

_Bonus Exercise:
Can you change the collection interval without modifying the Python check file you created?_

Link:
https://app.datadoghq.com/metric/summary?filter=my&metric=my_metric

Answer:
Yes by going to Metrics >> Summary >> Searching for metric name >> Right hand side window click on edit.

Screenshots:
![Alt text](/photos/interval.png?raw=true)

**Visualizing Data Section**

_Exercise 1:
Utilize the Datadog API to create a Timeboard that contains:_


_A) Your custom metric scoped over your host._

Link:
https://app.datadoghq.com/dashboard/qzc-dkv-36m/api-custom-metric-timeboard?from_ts=1609097698053&fullscreen_section=overview&fullscreen_widget=1373939238835056&live=true&to_ts=1609101298053&fullscreen_start_ts=1609097700694&fullscreen_end_ts=1609101300694&fullscreen_paused=false

```{
    "description": "API Timeboard",
    "is_read_only": false,
    "layout_type": "ordered",
    "notify_list": [],
    "title": "API Custom Metric Timeboard",
    "widgets": [
        {
            "definition": {
                "type": "timeseries",
                "title": "My Metric Widget",
                "requests": [
                    {
                        "q": "my_metric{host:vagrant}",
                        "style": {
                            "palette": "dog_classic"
                        }
                    }
                ]
            }
        }
    ]
}
```

Screenshot:
![Alt text](/photos/my_metric_widget.png?raw=true)

_B) Any metric from the Integration on your Database with the anomaly function applied._

Link:
https://app.datadoghq.com/dashboard/qzc-dkv-36m/api-custom-metric-timeboard?from_ts=1609097698053&fullscreen_section=overview&fullscreen_widget=4489668233532641&live=true&to_ts=1609101298053&fullscreen_start_ts=1609097739634&fullscreen_end_ts=1609101339634&fullscreen_paused=false

```
{
    "description": "API Timeboard",
    "is_read_only": false,
    "layout_type": "ordered",
    "notify_list": [],
    "title": "API Custom Metric Timeboard",
    "widgets": [
        {
          "definition": {
                "type": "timeseries",
                "title": "Number of MongoDB Queries Per Second.",
                "requests": [
                    {
                        "q": "mongodb.opcounters.queryps{*}"
                        }
                    }
                ]
            }
        }
    ]
}

```

Screenshot:
![Alt text](/photos/mongodb_widget.png?raw=true)

_C) Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket_

Link:
https://app.datadoghq.com/dashboard/qzc-dkv-36m/api-custom-metric-timeboard?from_ts=1609097769285&fullscreen_section=overview&fullscreen_widget=8414443735692492&live=true&to_ts=1609101369285&fullscreen_start_ts=1609097771813&fullscreen_end_ts=1609101371813&fullscreen_paused=false

```
{
    "description": "API Timeboard",
    "is_read_only": false,
    "layout_type": "ordered",
    "notify_list": [],
    "title": "API Custom Metric Timeboard",
    "widgets": [
        {
          "definition": {
                "type": "timeseries",
                "title": "My Metric with Rollup Function",
                "requests": [
                    {
                        "q": "sum:my_metric{*}.rollup(sum, 3600)"
                        }
                    }
                ]
            }
        }
    ]
}
```

Screenshot:
![Alt text](/photos/roll_sum_widget.png?raw=true)

_Exercise 2:
Once this is created, access the Dashboard from your Dashboard List in the UI:_

_A) Set the Timeboard's timeframe to the past 5 minutes_

Link:
https://app.datadoghq.com/dashboard/qzc-dkv-36m/api-custom-metric-timeboard?from_ts=1609128993956&live=true&to_ts=1609129293956

Screenshot:
![Alt text](/photos/five_min_dash.png?raw=true)

_B) Take a snapshot of this graph and use the @ notation to send it to yourself._

Screenshot:
![Alt text](/photos/send_to_self.png?raw=true)

![Alt text](/photos/email.png?raw=true)

_C) Bonus Question: What is the Anomaly graph displaying?_

The anomaly graph uses an algorithm that compares the past behavior of a metric to its present behavior. On the graph, the shaded area displays the expected behavior and the line is the actual behavior.

Screenshot:
![Alt text](/photos/Anomaly.png?raw=true)

**Monitoring Data Section**

_Exercise 1: Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:_

Link:
https://app.datadoghq.com/monitors/28023566

_A) Warning threshold of 500_

_B) Alerting threshold of 800_

_C) And also ensure that it will notify you if there is No Data for this query over the past 10m._

![Alt text](/photos/define_metric_monitor.png?raw=true)

_Please configure the monitor’s message so that it will:_

_*Send you an email whenever the monitor triggers._

_*Create different messages based on whether the monitor is in an Alert, Warning, or No Data state._

_*Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state._

![Alt text](/photos/notification_messges.png?raw=true)

_When this monitor sends you an email notification, take a screenshot of the email that it sends you._

![Alt text](/photos/waning_alert_email.png?raw=true)

_Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:_

link:
https://app.datadoghq.com/monitors#downtime

_One that silences it from 7pm to 9am daily on M-F,_

link:
https://app.datadoghq.com/monitors#downtime?id=1085989803

![Alt text](/photos/weekly_downtime.png?raw=true)

_And one that silences it all day on Sat-Sun._

link:https://app.datadoghq.com/monitors#downtime?id=1085992963

![Alt text](/photos/weekend_downtime.png?raw=true)

_Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification._

![Alt text](/photos/weekend_email.png?raw=true)

![Alt text](/photos/weekly_email.png?raw=true)

**Collecting APM Data:**

_Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:_

_Note: Using both ddtrace-run and manually inserting the Middleware has been known to cause issues. Please only use one or the other._

_Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics._

_Please include your fully instrumented app in your submission, as well._

Links:
https://app.datadoghq.com/apm/service/flask/flask.request?end=1609381373923&paused=false&start=1609377773923&env=flask_app

https://app.datadoghq.com/dash/integration/custom%3Atrace?from_ts=1609377893959&live=true&to_ts=1609381493959&tpl_var_scope=host%3Aubuntu-xenial

```
from flask import Flask
import logging
import sys
from ddtrace import tracer

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

![Alt text](/photos/pic_one.png?raw=true)

![Alt text](/photos/pic_two.png?raw=true)

![Alt text](/photos/pic_three.png?raw=true)

![Alt text](/photos/pic_four.png?raw=true)

![Alt text](/photos/pic_five.png?raw=true)

_Bonus Question: What is the difference between a Service and a Resource?_

Source:
https://docs.datadoghq.com/tracing/visualization/

Service:
  Services are the building blocks of modern microservice architectures - broadly a service groups together endpoints, queries, or jobs for the purposes of building your application.

Resources:
  Resources represent a particular domain of a customer application - they are typically an instrumented web endpoint, database query, or background job.

 A service is an operation in the system, like an API call. A resource is an endpoint itself.  

**Final Question:**
_Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!_

_Is there anything creative you would use Datadog for?_

I think it would be fascinating to have a Datadog visualize various genetic and environmental factors that might affect states where the population has high Covid-19 risks. It would be very interesting to have a dashboard that would display what communities are being most affected by the pandemic.
