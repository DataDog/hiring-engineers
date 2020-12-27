Collecting Metrics

Exercise 1:
Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

Link:
https://app.datadoghq.com/infrastructure/map?host=3443516844&fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=availability-zone&nameby=aws_id&nometrichosts=false&tvMode=false&nogrouphosts=true&palette=green_to_orange&paletteflip=true&node_type=host

Answer:
Below we have a screenshot of the Host Map. This can be viewed by heading to the sidebar on the DataDog home page and clicking on Infrastructure, then Host Map. To view the DD agent details, simply click on "Agent" within the host. This will direct the user to where the customized tags can be viewed on the front end. To add the tags on the back end, the Agent Configuration file would be to be configured.

/etc/datadog-agent/datadog.yaml  

Screenshots:
Agent on Host Map UI
![Alt text](/photos/host_map.png?raw=true "Host Map and Tags")

Exercise 2:
Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

Link:
https://app.datadoghq.com/infrastructure/map?host=3443516844&fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=availability-zone&nameby=aws_id&nometrichosts=false&tvMode=false&nogrouphosts=true&palette=green_to_orange&paletteflip=true&node_type=host

Answer:
To start the MongoDB's install process, from the Host Map, go to the sidebar and click on Integrations >> Integrations. This link directs the user to a page with a list of integration options. From here, search for MongoDB and follow the configuration steps.

Screenshots:
![Alt text](/photos/db_installed.png?raw=true "MongoDB Integrations Page")

MongoDB reflecting on Host Map.
![Alt text](/photos/mongodb_host_map.png?raw=true "MongoDB on Host Map")

Exercise 3:
Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

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

Exercise 4:
Change your check's collection interval so that it only submits the metric once every 45 seconds.

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

Visualizing Data

Exercise 1:
Utilize the Datadog API to create a Timeboard that contains:


A) Your custom metric scoped over your host.

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

B) Any metric from the Integration on your Database with the anomaly function applied.

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

C) Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
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
