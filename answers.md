# Collecting Metrics

Tags
![tags](tags.png?raw=true "Tags")

![tags](tags2.png?raw=true "Tags")

PostgreSQL Integration
![PSQL](postgres.png?raw=true "PSQL")

Custom Agent Check

```python
# my_check.py
import random

from checks import AgentCheck

class HelloCheck(AgentCheck):
    def check(self, instance):
    	n = random.randint(1, 1000)
        self.gauge('my_metric', n)
```

```yaml
# my_check.yaml
init_config:
  min_collection_interval: 45

instances:
    [{}]
```

# Vizualizing Data

