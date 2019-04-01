# Collecting Metrics:

## 1. Tags

## 2. Postrgres Integration
```
more /etc/datadog-agent/conf.d/postgres.yaml

init_config:

instances:

  - host: localhost
  
    port: 5432
    
    username: postgres
    
    password: postgres
    
    tags:
    
- optional_tag1
      
- optional_tag2
```

## 3. Custom Metrics
```
[root@datadogdemo conf.d]# more /etc/datadog-agent/checks.d/my_metric.py
import random
try:
    from checks import AgentCheck
except ImportError:
    from datadog_checks.checks import AgentCheck
__version__ = "1.0.0"

class My_MetricCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', random.randint(0,1000))


```
## 4. Collection Interval
```
[root@datadogdemo conf.d]# more /etc/datadog-agent/conf.d/my_metric.yaml

init_config:

instances:

  - min_collection_interval: 45

```
**Bonus Question:**

Yes, it is possible to change without modify python script. I have created configuration file my_metric.yaml in conf.d with the parameter min_collection_interval
      
# Visualizing Data:

## Timeboard 

