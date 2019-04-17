
# Technical Interview Round - VP

## Introduction
Purpose of this document is to provide the details of steps taken to install, instrument and correlate metrics data for various integrations point.

## Collecting Metrics:

### Step 1:
Instrument DataDog Infrastructure and APM Agents. In this step, I have install the DataDog agents in Ubuntu, CentOS flavors of Linux. over the weekend, I played with various agent types and tech stacks.

> Installation in Linux is **easy with one single command**: I must say this
> was very easy installation compared to other tools I have used.

> DD_API_KEY=<KEY> bash -c "$(curl -L
> https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"

##### Here is the reference of Host Map
![Host Map](https://github.com/TechParmar/hiring-engineers/blob/solutions-engineer/img/hostmap.jpg)

##### Tags are added both in AWS and Agent Configuration
![Adding Tags](https://github.com/TechParmar/hiring-engineers/blob/solutions-engineer/img/tags.jpg)

![APM Tag](https://github.com/TechParmar/hiring-engineers/blob/solutions-engineer/img/apm-tag.jpg)

### Step 2:
I installed MySQL integration. The configuration for the same is below:
![MySQL integration](https://lh6.googleusercontent.com/Ji4mr2CkRplBgn22sbzkNGcivqqP3A7mG4tR4OkzQ1H-APY758dt4sXe-UNEs_XgCwG0EY3aJPFrDGZtunX6d-ExMhjdeJ2d3xbpxazrJgrGQrcYMuDE3iX5o2HhXEpaOQlNFEBg)

### Step 3:
I created a custom agent check with the following file names
![custom agent](https://lh6.googleusercontent.com/7R5uDo4ueNYkJ2ePqiIIixjC09Vh3UsJr4y7fAP8kwff7hKybrjo2z4y7DEYRqnx-5sgiCZL618slh1UmXAmQqqdu-JKZR9saXQr_Bco4DC-9tMkKzF_Z-vYFlZJjDGm9yWpBht2)

Content of **my_metric.yaml** file located at **/etc/datadog-agent/conf.d**

  ```
init_config:
instances:
[{}]
```

I further changed the check's collection interval so that it only submits the metric once every 45 seconds.

Content of **my_metric.py** file located at **/etc/datadog-agent/checks.d**

```
from checks import AgentCheck

# content of the special variable __version__ will be shown in the Agent status page
__version__ = "1.0.0"

# custom counter logic

from random import *

METRIC_NAME_PREFIX = "custom"

class MyMetric(AgentCheck):
    def check(self, instance):
        x = randint(0, 1000)    # Pick a random number between 0 and 1000.
        self.gauge('my_metric', x, tags=['env=production'])
```

**Bonus Question**: I changed the interval in **my_metric.yaml** file instead of python script as suggest in the documentation - [https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6#collection-interval](https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6#collection-interval)
```
init_config:

instances:
  - min_collection_interval: 45
```

## Visualizing Data:

### Step 3:
Create Dashboard using API
I chose python approach here. I added datadog api libraries by using this command - **pip install datadog**

```
from datadog import initialize, api

options = {
    'api_key': 'KEY',
    'app_key': 'KEY'
}

initialize(**options)

title = 'MySQL Stats'
widgets = [{
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'mysql.performance.cpu_time{host:i-0fcaadedac4ac5b29}'}
        ],
        'title': 'Bin Log Disk Use'
    }
}]
layout_type = 'ordered'
description = 'MySQL DB Information via APIs'
is_read_only = True
notify_list = ['creativevikram@gmail.com']
api.Dashboard.create(title=title,
                     widgets=widgets,
                     layout_type=layout_type,
                     description=description,
                     is_read_only=is_read_only,
                     notify_list=notify_list
                                         )
```

Then I updated the dashboard using this API and added Anomalies detection as well as Roll up sum

```
from datadog import initialize, api

options = {
    'api_key': 'KEY',
    'app_key': 'KEY'
}

initialize(**options)

dashboard_id = '3zw-8gj-5pd'

title = 'My Metrics Updated'
widgets = [{
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'avg:mysql.performance.cpu_time{host:i-0fcaadedac4ac5b29}'}
        ],
        'title': 'MySQL CPU Time'
                }
    },
    {
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'avg:my_metric{host:i-08021c29f543d000a}'}
        ],
        'title': 'Last 1 hr Metrics'
                    }
    },
    {
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': "anomalies(avg:my_metric{host:i-08021c29f543d000a}, 'basic', 2)"}
        ],
        'title': 'Anomaly Detection'
                    }
    },
    {
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': "sum:my_metric{host:i-08021c29f543d000a}.rollup(3600)"}
        ],
        'title': 'Metric Sum Roll Up'
                    }
    }
]

layout_type = 'ordered'
description = 'MySQL DB Information Updated'
is_read_only = True
notify_list = ['creativevikram@gmail.com']
api.Dashboard.update(dashboard_id,
                     title=title,
                     widgets=widgets,
                     layout_type=layout_type,
                     description=description,
                     is_read_only=is_read_only,
                     notify_list=notify_list
                                         )
```
### Step 4:
Narrow to 5 minutes timeslice

### Step 5:
Annotate and send metrics to self by clicking on the metric chart and choosing **Annotate this graph** option



### Step 6:
What is the Anomaly graph displaying?
The graph is used to identify the numeric metric range. It help us to understand the abnormal behaviour of the metric in a given environment. It also highlights the standard metric range in the chart in grey color and shows deviation from standards highlighted in red color.

## Monitoring Data:

### Step 7:
Metric Monitor : Specify the range of threshold while setting up a monitor


### Step 8:
Define different messages based on type of threshold and conditions

### Step 9:
Email notification received as soon as the thresholds are met

### Step 10:
Monitor History with current incident


### Step 11:
Scheduled Downtime

##### Daily downtime from 7 PM to 9 AM
Define scheduled downtime window between 7 PM - 9 AM during weekdays
![During weekday](https://github.com/TechParmar/hiring-engineers/blob/solutions-engineer/img/snooze-weekday.jpg)

Define scheduled downtime window on Saturday and Sunday due to weekend
##### Weekend Snooze (Saturday and Sunday)
![During weekend](https://github.com/TechParmar/hiring-engineers/blob/solutions-engineer/img/snooze-weekend.jpg)

## Collecting APM Data:
I instrumented PHP, Java, Ruby, Python applications to see the depth of instrumentation. Java APM agent was the easiest and the fastest to instrument from the above list of agents I tried.

### Step 12
I used this step to install python agent

### Step 13
Fully Instrumented Python(Flask) Script

```
from flask import Flask
import logging
import sys

from datadog import initialize

options = {
    'api_key':'KEY',
    'app_key':'KEY'
}

initialize(**options)

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

![APM Instrumentation](https://github.com/TechParmar/hiring-engineers/blob/solutions-engineer/img/apm-instrumentation.jpg)


## Final Question:
Screen time tracking could be awesome!!! How many hours did I spend to review metrics in DataDog UI

## Links
[Dashboard Link](https://app.datadoghq.com/dashboard/kne-d3n-dvn/application--server-health?tile_size=m&page=0&is_auto=false&from_ts=1554656400000&to_ts=1554742800000&live=true)

[Monitor Link](https://app.datadoghq.com/monitors/9434143)

[Notebook Link](https://app.datadoghq.com/notebook/110047/Analysis-Notebook?cell=mnqavzkq)
