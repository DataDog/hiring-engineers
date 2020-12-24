Your answers to the questions go here.

Collecting Metrics:

1) Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

Link:
https://app.datadoghq.com/infrastructure/map?host=3443516844&fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=availability-zone&nameby=aws_id&nometrichosts=false&tvMode=false&nogrouphosts=true&palette=green_to_orange&paletteflip=true&node_type=host

Screenshots:
Host and Tags on Host Map UI
![Alt text](/photos/host_map.png?raw=true "Host Map and Tags")


2) Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

Link:
https://app.datadoghq.com/infrastructure/map?host=3443516844&fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=availability-zone&nameby=aws_id&nometrichosts=false&tvMode=false&nogrouphosts=true&palette=green_to_orange&paletteflip=true&node_type=host

Screenshots:
MongoDB reflecting on Host Map.
![Alt text](/photos/mongodb_host_map.png?raw=true "MongoDB on Host Map")


3)Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

Link:
https://app.datadoghq.com/metric/explorer?from_ts=1608782940389&to_ts=1608786540389&live=true&page=0&is_auto=false&tile_size=m&exp_metric=my_metric&exp_agg=avg&exp_row_type=metric

Screenshots:
my_metric.py file
![Alt text](/photos/my_metric.png?raw=true "MongoDB on Host Map")

my_metric on the UI
![Alt text](/photos/ui_my_metric.png?raw=true "MongoDB on Host Map")
