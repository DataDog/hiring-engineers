Your answers to the questions go here.

Collecting Metrics:

1) Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

Link:
https://app.datadoghq.com/infrastructure/map?host=3443516844&fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=availability-zone&nameby=aws_id&nometrichosts=false&tvMode=false&nogrouphosts=true&palette=green_to_orange&paletteflip=true&node_type=host

Below we have a screenshot of the Host Map. This can be viewed by heading to the sidebar on the DataDog home page and clicking on Infrastructure, then Host Map. To view the DD agent details, simply click on "Agent" within the host. This will direct the user to where the customized tags can be viewed on the front end. To add the tags on the back end, the Agent Configuration file would be to be configured.

/etc/datadog-agent/datadog.yaml  

Screenshots:
Host and Tags on Host Map UI
![Alt text](/photos/host_map.png?raw=true "Host Map and Tags")


2) Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

Link:
https://app.datadoghq.com/infrastructure/map?host=3443516844&fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=availability-zone&nameby=aws_id&nometrichosts=false&tvMode=false&nogrouphosts=true&palette=green_to_orange&paletteflip=true&node_type=host

To install MongoDB from the Host Map, click on Integrations >> Integrations from the DD home page sidebar. This link directs the user to a page with a list of integration options. From here, one can search for MongoDB and follow the configuration steps.

Screenshots:
![Alt text](/photos/db_installed.png?raw=true "MongoDB Integrations Page")

MongoDB reflecting on Host Map.
![Alt text](/photos/mongodb_host_map.png?raw=true "MongoDB on Host Map")


3)Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

Link:
https://app.datadoghq.com/metric/explorer?from_ts=1608782940389&to_ts=1608786540389&live=true&page=0&is_auto=false&tile_size=m&exp_metric=my_metric&exp_agg=avg&exp_row_type=metric

To create a custom Agent check, create an empty directory named my_metric.d in /etc/datadog-agent/conf.d.
In this directory, create a file named my_metric.YAML. For now, place an empty list for the instances:

instances: [{}]

One level up from the conf.d/ folder is the check.d/ folder. Here create a custom check file named metric_example.py with the code from the screenshot below.

Then confirm the custom agent check on the front end from the DD home page's sidebar >> metrics >> metric summary. Here, enter the metric's name into the metric search bar.

Screenshots:
my_metric.py file
![Alt text](/photos/my_metric.png?raw=true "my_metric.py")

my_metric reflecting on the UI
![Alt text](/photos/ui_my_metric.png?raw=true "my_metric")

4)Change your check's collection interval so that it only submits the metric once every 45 seconds.
![Alt text](/photos/min_collection_interval.png?raw=true "my_metric")


5) Bonus Question Can you change the collection interval without modifying the Python check file you created?
Answer: Yes by going to Metrics >> Summary >> Searching for metric name >> Right hand side window click on edit.

Link:
https://app.datadoghq.com/metric/summary?filter=my&metric=my_metric

![Alt text](/photos/interval.png?raw=true)

Visualizing Data:
