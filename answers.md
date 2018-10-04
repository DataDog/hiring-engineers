Your answers to the questions go here.
## Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
# Collecting Metrics: 

![Tags Screenshot](https://github.com/agallav/hiring-engineers/blob/draft/screenshots/host_tags_screenshot.png)


## Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
## Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

`my_metric.py`
```
import random
from checks import AgentCheck

class my_metric(AgentCheck):
    def check(self, instance):
        myrand = random.randint(1, 1000)
        #force NoData for testing
        #myrand = None
        self.gauge('my_metric', myrand)
```


## Change your check's collection interval so that it only submits the metric once every 45 seconds.
## Bonus Question Can you change the collection interval without modifying the Python check file you created?


# Monitoring:

## Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes.

Email showing monitor alert triggered when value breached 500: 
![Screenshot](https://github.com/agallav/hiring-engineers/blob/draft/screenshots/monitor_alert_email.png)

Email showing monitor alert triggered when value breached 800: 
![Screenshot](https://github.com/agallav/hiring-engineers/blob/draft/screenshots/monitor_warning_email.png)

Email showing monitor alert triggered when value had No Data: 
![Screenshot](https://github.com/agallav/hiring-engineers/blob/draft/screenshots/monitor_nodata_email.png)


## Bonus Question - Setup scheduled downtimes

Silence from 7pm to 9am daily on M-F:

![Screenshot](https://github.com/agallav/hiring-engineers/blob/draft/screenshots/monitor_downtime_start.png)

And one that silences it all day on Sat-Sun:

![Screenshot](https://github.com/agallav/hiring-engineers/blob/draft/screenshots/monitor_downtime_weekends.png)