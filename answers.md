# Answers

## Level 1:
-  What is the agent?
	*  The agent is software that runs on your computer and collects data and metrics from database integrations running on your computer. It reports the data to datadog so you can analyze it.
	![Host Map](https://github.com/thechad12/hiring-engineers/blob/master/hostmap.png)

### mongo.py

```
from checks import AgentCheck
import random


class TestCheck(AgentCheck):

	SOURCE_TYPE_NAME = 'mongodb'

	SERVICE_CHECK_NAME = 'test.support.random'

	def check(self,instance):
		self.gauge('test.support.random', random.random(), tags=['kevin3'])
		self.increment('test.support.random', random.random())
		self.log.info('mongo')
```

### mongo.yaml

```
init_config:

instances:

      -   server: mongodb://datadog:6955Xx3Ux9Ckunzv6TPhkrJY@localhost:27017
          tags:
              - Kevin3
              - Kevin4
```

## Level 2:
-  What is the difference between a timeboard and a screenboard?
	*  A timeboard consists of graphs scoped to the same time, and graphs always appear in a grid-like fashion.
	*  A screenboard is created with drag-and-drop widgets that have different time-frames. They are more flexible in terms of the time scope. They can be shared both as a live and a read-only entity, where as timeboards cannot.
	![Graph](https://github.com/thechad12/hiring-engineers/blob/master/level-2.png)

## Level 3:

#### Monitor above 0.9
![Email alert](https://github.com/thechad12/hiring-engineers/blob/master/monitor-alert.png)

#### Monitor downtime email alert
![Downtime alert](https://github.com/thechad12/hiring-engineers/blob/master/monitor-downtime.png)
	

## Links:
-  Dashboard: https://app.datadoghq.com/dash/integration/custom%3Atest?live=true&page=0&is_auto=false&from_ts=1467573684497&to_ts=1467577284497&tile_size=m

-  Monitor: https://app.datadoghq.com/monitors#699301?group=all&live=4h


