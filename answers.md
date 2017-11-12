## Collecting Metrics:

### Tags
![Tags](/imgs/tags.png)
Added the tags:
- #mytag,
- #env:prod,
- #role:database

### Database Integration

### Custom Agent Check
![Custom Agent Check](/imgs/my_metric.png)

~/.datadog-agent/conf.d/my_metric.yaml
```
init_config:
  min_collection_interval: 45

instances:
    [{}]
```

~/.datadog-agent/checks.d/my_metric.py
```
import random
from checks import AgentCheck

class HelloCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', random.randint(0, 1001))
```

*Bonus -- How to change collection interval without modifying the Python check file:*

In the Agent Config file, configure the `collector_profile_interval` setting.

```
collector_profile_interval: 45
```
