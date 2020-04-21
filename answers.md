
Setting up the Env - docker

Prerequisite:
https://docs.docker.com/get-docker/

DOCKER_CONTENT_TRUST=1 docker run -d --name dd-agent -v /var/run/docker.sock:/var/run/docker.sock:ro -v /proc/:/host/proc/:ro -v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro -e DD_API_KEY=3dc72688feb6342af97700ae5b158d39 -e DD_TAGS= author:raonny environment:docker-dev -e DD_APM_ENABLED=trye -e DD_DOGSTATSD_NON_LOCAL_TRAFFIC=true -p 8125:8125/udp -p 8126:8126/tcp -e DD_SITE="datadoghq.eu" datadog/agent:7

This will spin up a docker container called `dd-agent`

docker ps

docker exec -it dd-agent /bin/bash




TAG:

apt-get install vim (or vi)

https://docs.datadoghq.com/tagging/

vim /etc/datadog-agent/conf.d/docker.d/conf.yaml.default



```yaml
tags:
  - author:raonny
  - environment:docker-dev
```

save

check
cat /etc/datadog-agent/conf.d/docker.d/conf.yaml.default | grep tags -C 5

exit the container with `exit`

docker restart dd-agent

wait for restart to complete



Database:

docker pull mariadb/server:10.3

docker run --name datadogdbtest -p 33061:3306 -e MYSQL_ROOT_PASSWORD=root -d mariadb/server:10.3

docker exec -it datadog-db-test 

https://mariadb.com/kb/en/installing-and-using-mariadb-via-docker/




host host.docker.internal
port 33061

cp conf.yaml.example conf.yaml

vim /etc/datadog-agent/conf.d/mysql.d/conf.yaml

save

docker restart dd-agent



CUSTOM METRIC

https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7


echo "instances: [{}]" > "/etc/datadog-agent/conf.d/my_metric.yaml"


vim /etc/datadog-agent/checks.d/my_metric.py

pyton sample code

```python

#!/usr/bin/python
# the following try/except block will make the custom check compatible with any Agent version
try:
    # first, try to import the base class from new versions of the Agent...
    from datadog_checks.base import AgentCheck
except ImportError:
    # ...if the above failed, the check is running in Agent version < 6.6.0
    from checks import AgentCheck

from random import randint
# content of the special variable __version__ will be shown in the Agent status page
__version__ = "1.0.0"
class MyMetric(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', randint(0, 1000), tags=['env:docker-dev'])

```

To change the interval update the my_metric.yaml as follows:
```yaml
instances:
  - min_collection_interval: 45
```



Visualizing Data

https://docs.datadoghq.com/getting_started/api/

https://docs.datadoghq.com/api/?lang=python#dashboards


API credentials:
https://app.datadoghq.eu/account/settings#api

timetable code:
```json
{
    "title": "My Custom Timetable",
    "widgets": [
        {
            "definition": {
                "type": "timeseries",
                "requests": [
			        {
			            "q": "avg:my_metric{host:docker-desktop}"
			        }
                ],
                "title": "my_metric overtime scoped on my host"
            }
        },
        {
            "definition": {
                "type": "timeseries",
                "requests": [
			        {
			            "q": "anomalies(avg:mysql.net.max_connections{*}, 'basic', 2)"
			        }
                ],
                "title": "Anomalies on max_connections"
            }
        },
        {
            "definition": {
                "type": "timeseries",
                "requests": [
			        {
			            "q": "avg:my_metric{*}.rollup(sum, 3600)"
			        }
                ],
                "title": "Rollup Metric"
            }
        }
    ],
    "layout_type": "ordered",
    "description": "My Custom Timetable",
    "is_read_only": true,
    "notify_list": [
        "findme@raonny.com"
    ],
    "template_variables": [
        {
            "name": "host",
            "prefix": "host",
            "default": "docker-desktop"
        }
    ]
}
```

Anomaly:
Anomaly detection is an algorithmic feature that identifies when a metric is behaving differently than it has in the past, taking into account trends, seasonal day-of-week, and time-of-day patterns. It is well-suited for metrics with strong trends and recurring patterns that are hard to monitor with threshold-based alerting.
In my case, it will detect as anomaly any number of max connections different than 1


Monitoring Data

https://docs.datadoghq.com/monitors/notifications/?tab=is_alert

```yaml
Attention!
Host {{host.name}} is behaving abnormally. 

{{#is_alert}} 
My Metric is too high! Currently {{value}}
Server {{host.name}} {{host.ip}} 
{{/is_alert}}
 
{{#is_warning}} 
My Metric is increasing more than it should!
{{/is_warning}}
 
{{#is_no_data}} 
My Metric is gone!
{{/is_no_data}}
 
 @----@r****y.com
```

Metric URL: https://app.datadoghq.eu/monitors#134072/edit


Downtime:
https://app.datadoghq.eu/monitors#downtime


Collecting APM Data:

apm_non_local_traffic: true

What is the difference between a Service and a Resource?

https://docs.datadoghq.com/tracing/visualization/


for ((i=1;i<=100;i++)); do   curl "localhost:5050/api/apm"; curl "localhost:5050/api/trace"; sleep(1); done


A resource is a component, action or a part of a system/service
A service, is a collection of resources/components, that provides feature set as an utility for the end user


