### Setup

I spent far too many hours trying to get VirtualBox to work on High Sierra (it did not work), so I chose to install the agent directly on OSX.

Once I reached the APM part of the assignment however, I was not able to install the trace. The current [documentation](https://github.com/DataDog/datadog-trace-agent) is for V5 and I was not able to successfully modify the bash command to get the trace working.

At that point, I started up a hosted ubuntu instance and tried installing the agent and trace with linux. I also added tags and an agent check. I essentially did the collecting metrics part of the challenge twice. In those places, I have included two screenshots and multiple scripts.


## Collecting Metrics

### Add tags in the agent config file


I un-commented the following tags in the datadog.yaml file on OSX. For linux I edited te tags slightly.

```
tags:
  - mytag
  - env:prod
  - role:database
```
![Tags picture](https://raw.githubusercontent.com/akambale/hiring-engineers/master/ConfigFileTags.png)

![linux tags picture](https://raw.githubusercontent.com/akambale/hiring-engineers/Amogh-SE/linuxtagpicture.png)

### Install database and Datadog configuration

 ![MySQLIntegration](https://raw.githubusercontent.com/akambale/hiring-engineers/master/MySQLIntegration.png)

### Create custom Agent Check

For the osx check

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

For the linux check

linuxcheck.yaml 

```
init_config:

instances:
    - min_collection_interval: 5
```
linuxcheck.py

```
from checks import AgentCheck
from random import randint

class HelloCheck(AgentCheck):
  def check(self, instance):
    random_number = randint(0, 1000)
    self.gauge('linuxcheck', random_number)
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

Note: I made this iframe a week after I originally took the screenshot, so the data is not the same, though the timeboard is.

<iframe src="https://app.datadoghq.com/graph/embed?token=28cc5dc8fc38df2c01a67df7f90634290913bd6333718575f09d33c94641872f&height=300&width=600&legend=true" width="600" height="300" frameborder="0"></iframe>

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

I ran into a number of issues with the Flask app. This project is my first experience with python. I spent a significant amount of time trying to troubleshoot a socket error, but I had no luck. Instead, I attempted to use [hot-shots](https://github.com/brightcove/hot-shots) on my linux host to monitor one of my NodeJS apps. I successfully sent a metric called "metricAPM" which sent a random number between 1 and 1000 every 10 seconds to datadog as long as the server was running.

The repo for the app I used can be found [here](https://github.com/akambale/marketunity). And the specific file I edited in the app to include APM can be found [here](https://github.com/akambale/marketunity/blob/master/server/server.js).

I didn't push my APM edits to the github repo. The code that makes up the core of the app and APM check is copied below:

```
const express = require('express');
const app = express();
const bodyParser = require('body-parser');
const helpers = require('../data/db/helpers.js');
const User = require('../data/db/models/newUser.js');
const searchHelper = require('./searchHelpers/searchHelper.js');
const connection = require('../data/db/connection.js');
const jwt = require('jsonwebtoken');
const path = require('path');
const StatsD = require('hot-shots');

const client = new StatsD();

client.socket.on('error', function(error) {
  console.error("Error in socket: ", error);
});

setInterval(() => {
  let num = Math.ceil(Math.random() * 1000);
  client.gauge('metricAPM', num);
}, 10000);

/***********************************************************************/
/*********** Establishing Server and Listening on Port *****************/
/***********************************************************************/

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

app.use(express.static(path.join(__dirname, '../dist')));

app.listen(1337, function () {
  console.log('App listening on port 1337');
});
```

Dashboard with both APM and infrastructure metrics:
![infraApmMetrics](https://raw.githubusercontent.com/akambale/hiring-engineers/Amogh-SE/InfraAPM.png)

### Bonus Question: Difference Between Service and Resource?

A service is part of an application, whereas a resource is a service query or function execution, be that to a database, a client, a server or other components. 


## Final Question: What would I use datadog for

Like many people in SF, I took Uber/Lyft to work far too often, especially on Fridays when there wasn't a specific time I had to be in the office. I would set up an app that would send requests to the Uber and Lyft APIs every 30 seconds and receive prices. Using a check in the APM, I would then send prices to Datadog and create an alert that would notify me if prices dipped below a certain threshold so I could request a ride for the best price possible.
