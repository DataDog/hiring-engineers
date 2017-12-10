# Collecting Metrics:

***Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.***

```
tags: region:east, app:codingchallenge
```

![host](./screenshots/host_tags.png)

***Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.***

In the postgres.yaml file:
```
init_config:

instances:
  - host: localhost
    port: 5432
    username: datadog
    password: HwUFx2fFVefYm9yc2osaEEoE
    dbname: postgres
    tags:
      - role:db
      - region:east
      - app:backend
```

***Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.***

```Python
from checks import AgentCheck
from random import randint
class MetricCheck(AgentCheck):
  def check(self, instance):
      self.gauge('metric.datadog', randint(0,1000))
```

***Change your check's collection interval so that it only submits the metric once every 45 seconds.***

We can modify the associated yaml file and set the min_collection_interval to 45.

***Bonus: Question Can you change the collection interval without modifying the Python check file you created?***

Yes, we can modify the my_metric.yaml file in /etc/dd-agent/conf.d

```
init_config:
    min_collection_interval: 45

instances:
    [{}]
```

# Visualizing Data:

***Utilize the Datadog API to create a Timeboard that contains:***

- Your custom metric scoped over your host.
- Any metric from the Integration on your Database with the anomaly function applied.
- Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

![timeboard](./screenshots/create_timeboard.png)

***Once this is created, access the Dashboard from your Dashboard List in the UI:***

- Set the Timeboard's timeframe to the past 5 minutes
- Take a snapshot of this graph and use the @ notation to send it to yourself.

![view_timeboard](./screenshots/timeboard_view.png)

- Bonus Question: What is the Anomaly graph displaying?

Anomaly graph looks for strange behavior in a given metric based on the metric's past performance.

# Monitoring Data:

***Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:***

- Warning threshold of 500
- Alerting threshold of 800
- And also ensure that it will notify you if there is No Data for this query over the past 10m.

***Please configure the monitor’s message so that it will:***

- Send you an email whenever the monitor triggers.
- Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.

![monitor_setup](./screenshots/monitor_setup.png)

- Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
- When this monitor sends you an email notification, take a screenshot of the email that it sends you.

![email](./screenshots/email.png)

***Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:***

- One that silences it from 7pm to 9am daily on M-F,
- And one that silences it all day on Sat-Sun.
- Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.
