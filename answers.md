Hello! Thank you for considering me as a candidate.

This document contains my answers/screenshots to the technical evaluation.

## Prerequisites - Setup the environment

* I spun up a fresh linux VM via Vagrant. I used the recommended `v. 16.04`.
* I then signed up for Datadog and got the Agent reporting metrics from my local machine. [You can see this view here:](https://app.datadoghq.com/dash/host/497203256?live=true&from_ts=1528333343031&to_ts=1528336943031&page=0&is_auto=false&tile_size=m)

![Screenshot 1](1.png "Screenshot 1")

## Collecting Metrics:

* I added tags in the Agent config file; here's a screenshot of my host and its tags on the Host Map page in Datadog. [You can see this view here:](https://app.datadoghq.com/infrastructure/map?fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=availability-zone&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=true&palette=green_to_orange&paletteflip=false&node_type=host&app=hello&host=497203256) ![Screenshot 2](2.png "Screenshot 2")
* I installed a database on my machine (MySQL) and then installed the Datadog integration for MySQL. [You can see this view here:](https://app.datadoghq.com/dash/integration/12/MySQL%20-%20Overview?live=true&tpl_var_scope=host%3Aubuntu-xenial&page=0&is_auto=false&from_ts=1528333560783&to_ts=1528337160783&tile_size=m) ![Screenshot 3](3.png "Screenshot 3")
* I created a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000. [You can see this view here:](https://app.datadoghq.com/metric/summary?filter=my_metr) ![Screenshot 4](4.png "Screenshot 4")
* I changed my check's collection interval so that it only submits the metric once every 45 seconds. In the yaml file for my check, I changed `min_collection_interval: 45`
* **Bonus Question**: Using the configuration change above, I changed the collection interval without modifying the Python check file I created.

## Visualizing Data:

I utilized the Datadog API to create a Timeboard that contains:
* My custom metric scoped over my host
* A metric from the MySQL integration with the anomaly function applied 
* A custom metric with the rollup function applied to sum up all the points for the past hour into one bucket. 

[You can see this view here:](https://app.datadoghq.com/dash/829501/ryans-tech-evaluation?live=true&page=0&is_auto=false&from_ts=1528337274288&to_ts=1528340874288&tile_size=m) ![Screenshot 5](5.png "Screenshot 5")

I've included the script that I used to create the Timeboard here:

```

curl  -X POST -H "Content-type: application/json" \
    -d '{
"graphs": [
{
    "title": "my_metric over host",
    "definition":
    {
        "requests": [
        {
            "q": "avg:my_metric{host:ubuntu-xenial}"
        }]
    },
    "viz": "timeseries"
},
{
    "title": "mysql.net.max_connections_available anomalies",
    "definition":
    {
        "requests": [
        {
            "q": "anomalies(avg:mysql.net.max_connections_available{host:ubuntu-xenial}, \"basic\", 6)",
            "type": "line",
            "style":
            {
                "palette": "dog_classic",
                "type": "solid",
                "width": "normal"
            },
            "conditional_formats": [],
            "aggregator": "avg"
        }],
        "viz": "timeseries",
        "autoscale": true
    },
    "viz": "timeseries"
},
{
    "title": "rollup sum hour",
    "definition":
    {
        "requests": [
        {
            "q": "avg:my_metric{host:ubuntu-xenial}.rollup(sum, 3600)",
            "type": "line",
            "style":
            {
                "palette": "dog_classic",
                "type": "solid",
                "width": "normal"
            },
            "conditional_formats": [],
            "aggregator": "avg"
        }]
    },
    "status": "done",
  "viz": "query_value",
  "autoscale": true
},
{
    "title": "my_metric moving average",
    "definition":
    {
        "requests": [
        {
            "q": "ewma_10(sum:my_metric{*} by {host})",
            "type": "area",
            "style":
            {
                "palette": "dog_classic",
                "type": "solid",
                "width": "normal"
            },
            "conditional_formats": [],
            "aggregator": "avg"
        }]
    },
    "viz": "heatmap",
    "autoscale": true,
    "status": "done"
}],
"title": "Ryans Tech Evaluation",
"description": "The timeboard I created!",
"template_variables": [
{
    "name": "host1",
    "prefix": "host",
    "default": "host:my-host"
}],
"read_only": "True"
}
' \
"https://api.datadoghq.com/api/v1/dash?api_key=83b404e895c0acfbc6777d84b3c20a43&application_key=d654eac78a60809beaee1ffd5a41cd43b63f8aae"

```


Once this was created, I access the Dashboard from my Dashboard List in the UI. I then:

* Set the Timeboard's timeframe to the past 5 minutes: ![Screenshot 6](6.png "Screenshot 6")
* Took a snapshot of this graph and use the @ notation to send it to myself: ![Screenshot 7](7.png "Screenshot 7")
* **Bonus Question**: The anomaly graph is displaying my `mysql.net.max_connections_available` measured by Datadog's *Basic* algorithm. This algorithm uses a simple lagging rolling quantile computation to determine the range of expected values. It adjusts quickly to changing conditions but has no knowledge of seasonality or long-term trends. [You can read more about this here.](https://www.datadoghq.com/blog/introducing-anomaly-detection-datadog/#adding-anomaly-detection-to-graphs-and-alerts)

## Monitoring Data

I created a new Metric Monitor that watches the average of my custom metric (my_metric) that will alert if it’s above the following values over the past 5 minutes:

* Warning threshold of 500
* Alerting threshold of 800
* And also ensure that it will notify you if there is No Data for this query over the past 10m.

I configured the monitor’s message so that it will:

* Send me an email whenever the monitor triggers.
* Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
* Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.

I've included screenshots of this process below, and [you can view this monitor here](https://app.datadoghq.com/monitors#5153850/edit):

* Setting the monitor up: ![Screenshot 8](8.png "Screenshot 8")
* The custom warning email: ![Screenshot 9](9.png "Screenshot 9")

* **Bonus Question**: I set up two scheduled downtimes for this monitor:

  * One that silences it from 7pm to 9am daily on M-F: ![Screenshot 11](11.png "Screenshot 11")
  * And one that silences it all day on Sat-Sun: ![Screenshot 10](10.png "Screenshot 10")
  * When I scheduled the downtime, I took a screenshot of that notification: ![Screenshot 12](12.png "Screenshot 12")

## Collecting APM Data:

Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:

* **Note**: Using both ddtrace-run and manually inserting the Middleware has been known to cause issues. Please only use one or the other.

* **Bonus Question**: What is the difference between a Service and a Resource?

Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

Please include your fully instrumented app in your submission, as well.

## Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?

## Instructions

If you have a question, create an issue in this repository.

To submit your answers:

* Fork this repo.
* Answer the questions in answers.md
* Commit as much code as you need to support your answers.
* Submit a pull request.
* Don't forget to include links to your dashboard(s), even better links and screenshots. We recommend that you include your screenshots inline with your answers.
