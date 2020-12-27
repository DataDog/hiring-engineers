**Collecting Metrics**

_Exercise 1:
Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog._

Link:
https://app.datadoghq.com/infrastructure/map?host=3443516844&fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=availability-zone&nameby=aws_id&nometrichosts=false&tvMode=false&nogrouphosts=true&palette=green_to_orange&paletteflip=true&node_type=host

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
![Alt text](/photos/db_installed.png?raw=trues=150 "MongoDB Integrations Page")

MongoDB reflecting on Host Map.
![Alt text](/photos/mongodb_host_map.png?raw=trues=150 "MongoDB on Host Map")

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

Bonus Exercise:
Can you change the collection interval without modifying the Python check file you created?

Link:
https://app.datadoghq.com/metric/summary?filter=my&metric=my_metric

Answer:
Yes by going to Metrics >> Summary >> Searching for metric name >> Right hand side window click on edit.

Screenshots:
![Alt text](/photos/interval.png?raw=true)

**Visualizing Data**

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

Screenshot:
![Alt text](/photos/five_min_dash.png?raw=true)

_B) Take a snapshot of this graph and use the @ notation to send it to yourself._

Screenshot:
![Alt text](/photos/send_to_self.png?raw=true)

_C) Bonus Question: What is the Anomaly graph displaying?_

The Anomaly graph is

**Monitoring Data**
