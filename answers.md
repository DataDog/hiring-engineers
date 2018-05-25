## Prerequisites - Setup the environment

[I chose Ubuntu 16.04 LTS as my host running on VM Virtual Box](https://p.datadoghq.com/sb/7af5f9814-243e179005f19f7df668a6d7dad75b3c)

![alt text](https://github.com/mjmanney/hiring-engineers/blob/solutions-engineer/images/vbox.PNG "Virtual Box")

## Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
datadog-agent/datadog.yaml
``` yaml
# Set the host's tags (optional)
tags: mytag:newhost, env:prod, role:database
```
![alt text](https://raw.githubusercontent.com/mjmanney/hiring-engineers/solutions-engineer/images/hostmap.PNG "Host Map with custom tags")

## Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

I chose to integrate MongoDB with my Datadog agent.

![alt text](https://raw.githubusercontent.com/mjmanney/hiring-engineers/solutions-engineer/images/mongo.png "MongoDB")

mongo shell
```sh
# MongoDB 3.x
db.createUser({
  "user":"datadog",
  "pwd": "admin",
  "roles" : [
    {role: 'read', db: 'admin' },
    {role: 'clusterMonitor', db: 'admin'},
    {role: 'read', db: 'local' }
  ]
})
```
datadog-agent/conf.d/mongo.d/mongo.yaml
``` yaml
init_config:
  instances:
    - server: mongodb://datadog:admin@localhost:27017/admin
      additional_metrics:
        - collection       # collect metrics for each collection
        - metrics.commands
        - tcmalloc
        - top
```

## Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

datadog-agent/checks.d/my_metric.py
``` python
#import dd AgentCheck
from checks import AgentCheck

#import randit
from random import randint

class myCheck(AgentCheck):
    def check(self, instance):
        x = randint(0, 1000)
        self.gauge('my_metric', x)
```

## Change your check's collection interval so that it only submits the metric once every 45 seconds.

## Bonus Question Can you change the collection interval without modifying the Python check file you created?
This can be done by altering
datadog-agent/conf.d/my_metric.yaml
``` yaml
init_config:

instances:
    -    host: localhost
         min_collection_interval: 45
         name: my_metric
```
