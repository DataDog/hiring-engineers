## Overview

This answers.md file only contains the aswers to the challenges itself. The goal here is to me the more objective as possible, only pointing to screenshots and dashboards.

## Collecting Metrics:

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
https://app.datadoghq.com/infrastructure/map?fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=state%2Ccity%2Cowner&nameby=aws_name&nometrichosts=false&tvMode=false&nogrouphosts=true&palette=green_to_orange&paletteflip=false&node_type=host&filter=country%3Abr&host=4311366112
![](https://i.imgur.com/WCwXpzw.png)


* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
https://app.datadoghq.com/screen/integration/30404/my-sq-l?from_ts=1617669337576&live=true&to_ts=1617755737576
![](https://i.imgur.com/17iOAUD.png)

* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
https://app.datadoghq.com/metric/explorer?from_ts=1617752385757&to_ts=1617755985757&live=true&page=0&is_auto=false&tile_size=m&exp_metric=my_metric&exp_agg=avg&exp_row_type=metric
![](https://i.imgur.com/a85Q6fr.png)

* Change your check's collection interval so that it only submits the metric once every 45 seconds.
![https://i.imgur.com/vUTI1sz.png](https://i.imgur.com/vUTI1sz.png)

* **Bonus Question** Can you change the collection interval without modifying the Python check file you created?

	**Answer: You can just change the .yaml file, adding the option min_collection_interval, without touching the Python file.**

## Visualizing Data:

Dashboard Requested:

https://app.datadoghq.com/dashboard/e3y-ddn-cdu/criando-um-timeseries-atravs-da-api?from_ts=1617756592472&live=true&to_ts=1617756892472

![https://i.imgur.com/fUqbrZZ.png](https://i.imgur.com/fUqbrZZ.png)

* **Bonus Question**: What is the Anomaly graph displaying?
**Answer: It's displaying the metric mysql.performance.com_select, which shows the rate of select statements, if there is any kind of anomaly, the graph will show it.**

## Monitoring Data

![](https://i.imgur.com/D9WFe9X.png)

https://app.datadoghq.com/monitors/33419785
 * **Bonus Question**: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:
 * One that silences it from 7pm to 9am daily on M-F
![](https://i.imgur.com/J89SklP.png)
 * And one that silences it all day on Sat-Sun

![](https://i.imgur.com/9rPIT7l.png)

 - Make sure that your email is notified when you schedule the downtime
   and take a screenshot of that notification

![https://i.imgur.com/BaCvqt2.png](https://i.imgur.com/BaCvqt2.png)

## Collecting APM Data:

 * **Bonus Question**: What is the difference between a Service and a Resource?
Answer: Resource is an unique resource into an application, it can be a request, a view, a page, an image, anything that an application can process. Service is the grouping of various resources into the same application context.

Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.
https://app.datadoghq.com/dashboard/r7a-xhm-dgk?from_ts=1617759195734&live=true&to_ts=1617760095734
![](https://i.imgur.com/UQ23GIM.png)
 * Please include your fully instrumented app in your submission, as
   well.

**Follow attached in app.py**

## Final Question:
Is there anything creative you would use Datadog for?

Datadog gives us the possibility to basically monitor any asset that comes to mind. Whether it is a cryptocurrency monitoring farm, IoT devices such as smartbands, in short, there is no possible limit to creativity. I have already used Datadog in personal projects where I needed to use Forecast to detect some Covid situations in 2020, as well as I used it to measure the bandwidth usage of my devices at my home.

3 ultra creative and hypothetical situations that I would use the Datadog, would be:

1 - The first one would be to use in some way to find the winning numbers of the lottery. (Just kidding, we know that mathematically doesn't work).

2 - Secondly, if I could teleport in time, I would use Datadog to monitor my favorite game, which was Ragnarok Online in the middle of 2006 and to avoid several problems and create several improvements.

3 - And nowadays, I could use Datadog to monitor some Arduino and ESP32 projects that I have for sound automation with my digital piano and message exchange via MIDI.