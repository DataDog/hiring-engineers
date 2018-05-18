Your answers to the questions go here.

### Setup

I spent far too many hours trying to get VirtualBox to work on High Sierra (it did not work), so I chose to install the agent directly on OS X


### Collecting Metrics

## Add tags in the agent config file

I couldn't find a datadog.yaml file within datadog-agent/, but I did fine one within datadog-agent/etc/. I assume this is the correct file seeing as how the tags were shown on the UI

I uncommented the following tags in the datadog.yaml file

```tags:
  - mytag
  - env:prod
  - role:database
```
![Tags picture](https://raw.githubusercontent.com/akambale/hiring-engineers/master/ConfigFileTags.png)

### Install database and Datadog configuration

 ![MySQLIntegration](https://raw.githubusercontent.com/akambale/hiring-engineers/master/MySQLIntegration.png)

### Create custom Agent Check

I created two files 

mycheck.yaml

```
init_config:
  

instances:
    [{}]
```

mycheck.py

```
from checks import AgentCheck
from random import randint


class HelloCheck(AgentCheck):
    def check(self, instance):
        random_number = randint(0, 1000)
        self.gauge( 'mymetric',  random_number )
```

### Change collection interval to 45 seconds

I changed the mycheck.yaml file to the following

```
init_config:
  

instances:
    - min_collection_interval: 45
```

### Bonus Question

I didn't make any changes to the mycheck.py file, my change was the mycheck.yaml file. I think this satisifes the requiremes of the question? 

## Visualizing Data

### Timeboard

Here is the picture of the three metrics on separate timeboards over a four hour timeframe. I thought this picture would be helpful to visualize though it is not in the instructions to include it

![AllTimeboardsSeparated](https://raw.githubusercontent.com/akambale/hiring-engineers/master/AllTimeboardsSeparated.png)


### Timeboard Script 

JSON object for the board
```
{
  "status": "done",
  "autoscale": true,
  "markers": [
    {
      "dim": "y",
      "type": "error dashed",
      "val": 0,
      "value": "y = 0"
    }
  ],
  "viz": "timeseries",
  "requests": [
    {
      "q": "avg:mymetric{host:Amoghs-MacBook-Air.local}",
      "type": "line",
      "style": {
        "palette": "dog_classic",
        "type": "solid",
        "width": "normal"
      },
      "conditional_formats": [],
      "aggregator": "avg"
    },
    {
      "q": "avg:mymetric{host:Amoghs-MacBook-Air.local}.rollup(sum, 3600)",
      "type": "line",
      "style": {
        "palette": "dog_classic",
        "type": "solid",
        "width": "normal"
      }
    },
    {
      "q": "anomalies(avg:mysql.performance.queries{host:Amoghs-MacBook-Air.local}, 'basic', 2)",
      "type": "line",
      "style": {
        "palette": "dog_classic",
        "type": "solid",
        "width": "normal"
      }
    }
  ]
}
```


### Timeboard Snapshot

![MyTimeboardEmail](https://raw.githubusercontent.com/akambale/hiring-engineers/master/MyTimeboardEmail.png)

### Bonus Question: What is the Anomaly graph displaing?

It displays the bounds of the line. Bounds are what is considered normal in terms of deviations in the documentation. I think these deviations refer to standard deviation.


## Monitoring Data

### 