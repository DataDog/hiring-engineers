# Collecting Metrics

**Tags**
![tags](tags.png?raw=true "Tags")

![tags](tags2.png?raw=true "Tags")

**Hostmap Link**
https://app.datadoghq.com/infrastructure/map?fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=none&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=false&palette=green_to_orange&paletteflip=false&node_type=host

**PostgreSQL Integration**
![PSQL](postgres.png?raw=true "PSQL")

**Custom Agent Check**

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

**Bonus - Can I change collection interval without updating Python?**
Yes! You can change the collection interval in the .yaml file by adding a min_collection
interval to the init_config.

# Vizualizing Data

**Create Timeboard Script**

```python
# create_timeboard.py
from datadog import initialize, api

options = {
    'api_key': '8b61d94149b2d8718b1487ae2d76e6ba',
    'app_key': '94a5f73e754612fe5c027e4bae0c9cfee8705cbd'
}

initialize(**options)

title = "Hiring Exercise Timeboard"
description = "Hiring Exercise Timeboard"
graphs = [{
	"definition": {
		"events": [],
		"requests": [
			{
				"q": "avg:my_metric{*}"
			},
			{
				"q": "anomalies(avg:postgresql.buffer_hit{*}*100, 'basic', 2)"
			},
			{
				"q": "sum:my_metric{*}.rollup(3600)"
			}
		],
		"viz": "timeseries"
	},
	"title": "Visualizing Data"
}]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:my-host"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)
```

**Timeboard Link**
https://app.datadoghq.com/dash/639317/hiring-exercise-timeboard?live=true&page=0&is_auto=false&from_ts=1520460638441&to_ts=1520464238441&tile_size=xl

**Snapshot sent with @ notation**
![snapshot](snapshot.png?raw=true "snapshot")

**Bonus - What is the Anomaly graph displaying**
There is a grey box around it showing where it has dropped or increased. There is also a spike at the end of a graph predicting an increase where it has yet to increase.

# Monitoring Data

**Warning Notification**
![warning](warning.png?raw=true "warning")

**Alert Notification**

**No Data Notification**
![nodata](nodata.png?raw=true "nodata")

**Create Monitor Script**
```python
# create_metric_monitor.py
from datadog import initialize, api

options = {
    'api_key': '8b61d94149b2d8718b1487ae2d76e6ba',
    'app_key': '9d72fc44a77f1394ef465e290f08141699579e19'
}

# Create Monitor with thresholds
initialize(**options)

options = {
	"thresholds": {
		"critical": 800,
		"warning": 500
	},
    "notify_no_data": True,
    "no_data_timeframe": 20
}

api.Monitor.create(
    type="metric alert",
    query="avg(last_5m):avg:my_metric{*} > 500",
    name="Warning Monitor",
    handle="tylerpwilmot@gmail.com",
    message="WARNING: my_metric is over 500! Alert is at 800.",
    options=options
)
```

**Bonus**
**Silenced Notifications**
![silenced](silenced.png?raw=true "silenced")
![silenced2](silenced2.png?raw=true "silenced2")

**Downtime Link**
https://app.datadoghq.com/monitors#downtime?id=296173286

# Collecting APM Data


**Bonus - What is the difference between a Service and a Resource**


# Final Question
I would use DataDog to monitor activity on applications like OpenTable or Resy to see what reservation trends are like seasonally and weather permitting.
