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
      - DD_LOGS_ENABLED=true
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
