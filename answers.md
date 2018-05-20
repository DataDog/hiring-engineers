### Setup

I spent far too many hours trying to get VirtualBox to work on High Sierra (it did not work), so I chose to install the agent directly on OS X

Once I reached the APM part of the assignment however, I was not able to install the trace. The current [documentation](https://github.com/DataDog/datadog-trace-agent) is for V5 and I was not able to successfully modify the bash command to get the trace working.

At that point, I started up a hosted ubuntu instance and tried installing the agent and trace with linux. The host was recognized by datadog and showed up in my infrastructure list. However, I eventually ran into an issue where there was an issue with the datadog.yaml file. I could not fix the issue, but I could determine there was an issue with spacing in the code.


## Collecting Metrics

### Add tags in the agent config file

I couldn't find a datadog.yaml file within datadog-agent/, but I did fine one within datadog-agent/etc/. I assume this is the correct file seeing as how the tags were shown on the UI

I un-commented the following tags in the datadog.yaml file

```
tags:
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

I didn't make any changes to the mycheck.py file, my change was the mycheck.yaml file. I think this satisfies the requirements of the question? 

## Visualizing Data

### Timeboard

Here is the picture of the three metrics on separate timeboards over a four hour time frame. I thought this picture would be helpful to visualize though it is not in the instructions to include it

![AllTimeboardsSeparated](https://raw.githubusercontent.com/akambale/hiring-engineers/master/AllTimeboardsSeparated.png)


### JSON Timeboard Script 

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

### Bonus Question: What is the Anomaly graph displaying?

It displays the bounds of the line. Bounds are what is considered normal in terms of deviations in the documentation. I think these deviations refer to standard deviation. 


## Monitoring Data

![Monitor Alert Conditions](https://raw.githubusercontent.com/akambale/hiring-engineers/master/MonitorAlertConditions.png)


I have copied my message template below. I was not able to figure out how to include the metric value in this alert.

```
What does the scouter say about his power level? at IP {{host.ip}}

{{#is_alert}} 
It's over 800!!!
{{/is_alert}} @me@amoghk.com  

{{#is_warning}} 
It's over 500!!!
{{/is_warning}} @me@amoghk.com  

{{#is_no_data}} 
Power level cannot be found at {{host.ip}}
{{/is_no_data}} @me@amoghk.com
```

![Monitor Email Screenshot](https://raw.githubusercontent.com/akambale/hiring-engineers/master/MonitorEmailMessage.png)

### Bonus Question: Downtimes

![DowntimesEmail](https://raw.githubusercontent.com/akambale/hiring-engineers/master/DowntimesEmail.png)

## Collecting APM Data:

I was unable to complete this portion of the challenge. Here is the outline of all the steps I took.

1. Attempted to install the tracer on OSX. I was unsuccessful in launching it (see my explanation at the top).
2. Started up a hosted instance of ubuntu and installed the agent and tracer. I was not able to set tags or send a check to the datadog infrastructure list. I determined this was an issue with the datadog.yaml file.
3. In spite of that, I tried to run the flask app from both my OSX and Linux. In both set-ups I ran into "socket.error: [Errno 48] Address already in use." I tried troubleshooting this, but was unsuccessful. I am not very familiar with Python.
4. I attempted to use [hot-shots](https://github.com/brightcove/hot-shots) to monitor one of my NodeJS apps. As far as I know, there were no issues here. As it is, the documentation for this NPM package is lacking examples. But since my agent configuration was not working, I don't think it could successfully send metrics.

## Final Question: What would I use datadog for

Like many people in SF, I too often took Uber/Lyft to work, especially on Fridays when there wasn't a specific time I had to be in the office. I would set up an app that would send requests to the Uber and Lyft APIs every 30 seconds and receive prices. Using a check in the APM, I would then send prices to Datadog and create an alert that would notify me if prices dipped below a certain threshold so I could request a ride.