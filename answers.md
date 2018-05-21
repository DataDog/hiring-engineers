This will be a bit of a streaming conciousness.

## Prerequisites
Got account setup for trial period quite easily. Rather than install the agent
in a traditional sense, I decided to go down the containerized route. I run a
small docker swarm at home for the family's A/V needs and it seemed like a
natural fit. I typically am running a `cAdvisor/Influx/Grafana` stack so I killed
that while going through this exercise.

Starting up the agent in swarm is relatively strait forward. The docker hub
docs made it easy to stand up a metric stack as swarm uses docker-compose
as its definition standard. After a long than expected startup time I realized
that I had started up the 5.x version of the agent rather than  the 6.x version.
With the correct version operating, I quickly began to see my hosts appear in
the Datadog UI and a series of host and container metrics.

Here is my deployment compose file. More on the configs later:
```yaml
version: '3.4'

services:
  dd-agent:
    image: datadog/agent
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - /proc/:/host/proc/:ro
      - /sys/fs/cgroup/:/host/sys/fs/cgroup:ro
    configs:
      - source: hello-py
        target: /checks.d/hello.py
        mode: 755
      - source: hello-yaml
        target: /conf.d/hello.yaml
        mode: 755
      - source: redis-conf
        target: /etc/datadog-agent/conf.d/redisdb.d/conf.yaml
        mode: 755
    environment:
      - SD_BACKEND=docker
      - NON_LOCAL_TRAFFIC=false
      - DD_API_KEY=4f9fba62b97d2f64d1ca92a68847075c
      - DD_TAGS="az:us-home-1"
    deploy:
      mode: global
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 5

configs:
  hello-py:
    file: ./hello.py
  hello-yaml:
    file: ./hello.yaml
  redis-conf:
    file: ./redis_conf.yaml
```

## Collecting Metrics

1. Lots of tags come out of the box with the agent. I can sort via hosts with
Docker running, one's that detect redis, etc. What I was unable to do was use
the container environment variables to properly set host tags. I tried a few
different formats and google searchs to no avail. I eventually set them in the
UI. I saw where I caould set these in the datadog agent file but that doesn't
feel right considering the intended design principles. The above compose file
details my final attempt at setting an ENV VAR for `DD_TAGS`
2. I added a redis stack to my docker swarm for this section. The agent that was
on the same node as the redis container properly autodiscovered in the check
but the datadog agent was unable to properly detect the IP address of the redis
container. I eventually had to expose the redis port through the cluster and
manually set the redisdb conf.yaml to use a swarm node DNS entry as the host.
This is why there is a redis-conf config file. Below is the conf file:
```yaml
init_config:

instances:
  - host: swarm-master.bluehairfreak.com
    port: 6379
```
3. Creating the custom agent check took me some time to learn the nuance of the
conf.d and checks.d directories. There is a clear relationship but it took me
some time to discover that an instance key/value mapping can be read into the
check script. I decided to use the random number max as a test of what I learned
Below are the two files that make up my hello.world random number metric. I
went ahead and added in the `min_collection_interval` to the yaml for the bonus.
```python
from checks import AgentCheck
import random

class HelloCheck(AgentCheck):
    def check(self, instance):
        rand_num = instance['rand_num']
        self.gauge('hello.world', random.randint(0,rand_num))
```
```yaml
init_config:

instances:
  - rand_num: 1000
    min_collection_interval: 45
```
4. Bonus. I made the change initially using the yaml file versus using the
Pyhton file directly, presumably using a sleep method?

## Vizualizing Data
1. Here is screencap of the dashboard that I made programatically using the
Python SDK for Datadog. I found it was easier to build the dashboards
temporarially in the UI and then copy the JSON out into the script.
![prog_dash](https://preview.ibb.co/nQyP5o/Screen_Shot_2018_05_20_at_10_03_34_PM.png "Programatic Dashboard")

And here is the code. It is currently set to update vs create since I was
itterating on this over time. It also took me a moment to realize I needed to
create a APP key. Once I realized that was required things were cooking.
```python
from datadog import initialize, api

options = {
    'api_key': '<removed>',
    'app_key': '<removed>'
}

initialize(**options)

title = "My Programatic Timeboard"
description = "Where the important stuff is managed"
graphs = [{"definition": {
  "viz": "timeseries",
  "status": "done",
  "requests": [
    {
      "q": "sum:hello.world{*}.rollup(sum, 3600)",
      "type": "bars",
      "style": {
        "palette": "dog_classic",
        "type": "solid",
        "width": "normal"
      },
      "conditional_formats": [],
      "aggregator": "avg"
    }
  ],
  "autoscale": "true"
},
  "title": "Hourly Rollup of Hello World Metric"
},
{"definition": {
  "requests": [
    {
      "q": "sum:hello.world{host:swarm-master}",
      "type": "line",
      "style": {
        "palette": "dog_classic",
        "type": "solid",
        "width": "normal"
      },
      "conditional_formats": []
    }
  ],
  "viz": "timeseries",
  "autoscale": "true"
},
"title": "Custom Metric"
},
{"definition": {
  "viz": "timeseries",
  "status": "done",
  "requests": [
    {
      "q": "anomalies(sum:redis.info.latency_ms{host:swarm-master}, 'basic', 2)",
      "type": "line",
      "style": {
        "palette": "purple",
        "type": "solid",
        "width": "normal"
      },
      "conditional_formats": [],
      "aggregator": "avg"
    }
  ],
  "autoscale": "true"
},
    "title": "Redis Latency Anomolies"
}]

read_only = True
print api.Timeboard.update(816029, title=title,
                     description=description,
                     graphs=graphs,
                     read_only=read_only)
```
2. To grab the last 5 minutes I found I had to drag the cursor over a graph. I
had expected to be able to select a custom time range, however that appeared
to only allow me to select dates with no time selection.
3. I was unable to find any documentation of a "snapshot" and using the @
notation to send something. I spent about 15 minutes searching through the docs
with no such luck and moved on. I would love to find out more about this at a
later date. Below is a manual screen cap of the 5min interval.
![5_min_int](https://preview.ibb.co/h2uiWT/Screen_Shot_2018_05_20_at_10_09_20_PM.png "5min Interval Screen Cap")
4. Bonus. The default anamoly setting is basic which I kept as there was not
enough data to use either of the two other settings. The basic setting appears
to try and predeict a range of values it believes is the ever adjusting norm.
I notice that as values have a smaller range of values the anomoly area shrinks
and even relatively small variances in values become an outlier. I would expect
to use this agressively with cyclical and predicable workloads to identify
unusual decreases/increses in values.


