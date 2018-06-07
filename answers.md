# Answers

## Collecting Metrics

- Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog:

![tags screenshot](/screenshots/datadog_host_tags.png)

- Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
``` python
# mycheck.py

import random
from checks import AgentCheck

class MyCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', random.randint(0, 1000))
```

- Change your check's collection interval so that it only submits the metric once every 45 seconds. **Bonus Question** Can you change the collection interval without modifying the Python check file you created?

  Based on my understanding of the documentation, it seems that changing the mycheck config file's collection interval would suffice.
``` yaml
init_config:

instances:
    - min_collection_interval: 45
```

## Visualizing Data

- Link and screenshot for Custom Metric Timeboard scoped over local host:

  - [Custom - Metrics Timeboard](https://app.datadoghq.com/dash/825841/custom---metrics?live=true&page=0&is_auto=false&from_ts=1528399035881&to_ts=1528402635881&tile_size=m)

  - Screenshot:

  ![timebaord screenshot](/screenshots/my_metric_timeboard.png)

- script:

  see `timeboard.py`

- Snapshots of graphs with a timeframe of the past 5 minutes sent to self with @ notation:

![my_metric_avg screenshot](/screenshots/my_metric_avg.png)

![my_metric_rollup screenshot](/screenshots/my_metric_rollup.png)

![postgres screenshot](/screenshots/postgres.png)

- **Bonus Question**: What is the Anomaly graph displaying?

  The anomaly graph includes normal results along with a grey band that shows the expected range of the metric based on historical context. In the case of `postgres_rows_fetched`, it uses the basic algorithm for anomaly detection and shows values that are 2 standard deviations apart. Metrics that go out of their expected ranges are anomalies, and should be monitored accordingly.

## Monitoring Data

- screenshots of emails sent when monitor triggers:

  - Alert:

  ![alert screenshot](/screenshots/monitor_alert.png)

  - Warn:

  ![warn screenshot](/screenshots/monitor_warn.png)

  - No Data:

  ![no data screenshot](/screenshots/monitor_nodata.png)

- **Bonus Question**: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor (Note: all of the email notifications are showing UTC, but the scheduled downtime is in EST):

  - One that silences it from 7pm to 9am daily on M-F:

  ![downtime_weekday screenshot](/screenshots/downtime_weekday.png)

  - And one that silences it all day on Sat-Sun:

  ![downtime_weekends screenshot](/screenshots/downtime_weekends.png)

## Collecting APM Data:

- link and screenshot for APM and infrastructure metrics dashboard:
  - [APM & infrastructure metrics for myapp_service Timeboard](https://app.datadoghq.com/dash/830201/apm--infrastructure-metrics-for-myappservice?live=true&page=0&is_auto=false&from_ts=1528398638091&to_ts=1528402238091&tile_size=m)

  - Screenshot:

  ![downtime_weekends screenshot](/screenshots/apm_infrastructure.png)

- Fully instrumented app:

  see `myapp/myapp.py`

- **Bonus Question**: What is the difference between a Service and a Resource?

   A service is a collection of processes that serves the same purpose. For instance, in `myapp.py`, `myapp_service` refers to the entire web app service. If it also had a database, all database related processes would be categorized as a different service from the web app.

   On the other hand, a resource refers to an action that could be taken for a service. For instance, the action to serve an app route like `/api/apm` is a resource.

## Final Question:
Creative ways to use datadog:

Datadog can be used to monitor plant health by detecting their watering needs based on soil moisture and air humidity.  Since humidity varies seasonaly and geographically, it could be difficult to determine and keep track of how much to water a plant in a multi-plant household when they are purchased from out of state or when seasons change. Datadog can help establish a watering baseline and send alerts when a plant needs watering or has been watered too much.

## Links
- [Dashboard for local host](https://app.datadoghq.com/dash/host/491680408?live=true&page=0&from_ts=1528394732587&to_ts=1528409132587&is_auto=false&tile_size=m)
- [APM & infrastructure metrics for myapp_service Timeboard](https://app.datadoghq.com/dash/830201/apm--infrastructure-metrics-for-myappservice?live=true&page=0&is_auto=false&from_ts=1528398638091&to_ts=1528402238091&tile_size=m)
- [Custom - Metrics Timeboard](https://app.datadoghq.com/dash/825841/custom---metrics?live=true&page=0&is_auto=false&from_ts=1528399035881&to_ts=1528402635881&tile_size=m)
