Your answers to the questions go here.

<h1>Collecting metrics:</h1><br>

[Link](https://photos.app.goo.gl/YQVNRjJXyUxxGpZs8) to Host Map with tags screenshot.


- Bonus Question Can you change the collection interval without modifying the Python check file you created?<br>
Yes, we only need to modify Python check's config, a yaml file located in conf.d agent's directory. 
Just add:<br>

```- min_collection_interval: 45 ```

<hr>
<h1>Visualizing data:</h1><br>

[Link](https://photos.app.goo.gl/GB9CfLDGUHMXtZsUA) to Timeboard screenshot.

<h3>Script used to create Timeboard:</h3><br>

```python
#!/usr/bin/env python
from datadog import initialize, api

options = {
    'api_key': 'f100449dca7313b71f6abeb488c312c7',
    'app_key': '82818b84506cc9a41c43181b8b88bfd8567a14da'
}

initialize(**options)


title = "Datadog Hiring"
description = "Mix of graphs."
graphs = [
# first graph, my_metric
{
    "definition": {
        "events": [],
        "requests": [{"q": "custom.my_metric{host:datadog-test}", "type": "area"}],
        "viz": "timeseries"
    },
    "title": "Custom metric, random"
},
# 2nd graph, mysql metric with anomalies function
{
    "definition": {
        "events": [],
        "requests": [{"q": "anomalies(avg:mysql.innodb.buffer_pool_free{host:datadog-test}, 'basic', 2)"}],
        "viz": "timeseries"
    },
    "title": "Mysql, buffer pool free, anomalies"
},
# 3rd graph, again my_metric but with anomalies function
{
    "definition": {
        "events": [],
        "requests": [{"q": "anomalies(avg:custom.my_metric{host:datadog-test}, 'basic', 2)"}],
        "viz": "timeseries"
    },
    "title": "Custom metric, random, anomalies"
},
# 4th graph, my_metric rolled up
{
    "definition": {
        "events": [],
        "requests": [{"q": "custom.my_metric{host:datadog-test}.rollup(avg,3600)"}],
        "viz": "timeseries"
    },
    "title": "Custom metric, random, rolled up"
}
]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     read_only=read_only)
```

<hr>
<h1>Monitoring data:</h1><br>

[Link](https://photos.app.goo.gl/r3emijTofDdN6nh4A) to my_metric monitor config screenshot showing thresholds.

[Link](https://photos.app.goo.gl/9UcJp9emSm4hbBUYA) to my_metric monitor config screenshot showing custom message and receiver.

- Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

    One that silences it from 7pm to 9am daily on M-F,
    And one that silences it all day on Sat-Sun.

[Link](https://photos.app.goo.gl/SzpxQ4ziyP6nR7B56) to my_metric monitor 1st scheduled downtime email notification.

[Link](https://photos.app.goo.gl/1RjhvoM1d4hRiGxW9) to my_metric monitor 2nd scheduled downtime email notification.

