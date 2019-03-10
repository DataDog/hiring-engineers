Your answers to the questions go here.

# Prerequisites

According to [pull requests closed](https://github.com/DataDog/hiring-engineers/pulls?utf8=%E2%9C%93&q=is%3Apr+is%3Aclosed+docker),
most of candidates did not adopt containerized approach with Docker for Linux.
Since I like to try new thing for me, I'll adopt containerized approach with Docker for Linux.

Installed [Docker Desktop for Mac](https://docs.docker.com/docker-for-mac/) on my Mac:

- Docker Desktop Version: 2.0.0.3 (31259)
- Docker Engine: 18.09.2
- Docker Compose: 1.23.2
- Docker Machine: 0.16.1

Then, signed up for Datadog and got an one-step install command here.
https://app.datadoghq.com/signup/agent#docker

```bash
## Start datadog/agent container with configurations
## Note that the actual API key is substituted with environmental variable 
docker run -d --name dd-agent \
    -v /var/run/docker.sock:/var/run/docker.sock:ro \
    -v /proc/:/host/proc/:ro \
    -v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro \
    -e DD_API_KEY=$DD_API_KEY datadog/agent:latest
    
## check whether the container is running
docker ps
CONTAINER ID        IMAGE                  COMMAND             CREATED              STATUS                                 PORTS                NAMES
784b07f8bc22        datadog/agent:latest   "/init"             About a minute ago   Up About a minute (health: starting)   8125/udp, 8126/tcp   dd-agent
```

100 metrics are listed under `Metrics > Summary` in Datadog Web UI.
https://app.datadoghq.com/metric/summary

<img width="640" src="https://user-images.githubusercontent.com/48383023/54072145-ea5f2e00-42b9-11e9-9d77-776086b87ead.png">

<img width="640" src="https://user-images.githubusercontent.com/48383023/54072237-79207a80-42bb-11e9-91df-9f723b9e158b.png">

# Collecting Metrics

## Adding tags

Since containerized datadog-agent v6 doesn't have an agent config file. Instead of using config file,
I defined `DD_TAGS` environmental variables for adding tags.

```bash
## Stop & remove a running container
docker rm -f dd-agent

## Start a datadog-agent container with DD_TAGS environmental variable
docker run -d --name dd-agent \
    -v /var/run/docker.sock:/var/run/docker.sock:ro \
    -v /proc/:/host/proc/:ro \
    -v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro \
    -e DD_API_KEY=$DD_API_KEY \
    -e DD_TAGS="country:japan city:tokyo" \
    datadog/agent:6.10.1
```

2 tags (`country:japan` & `city:tokyo`) are displayed on the Host Map page.
<img width="640" src="https://user-images.githubusercontent.com/48383023/54072412-bab22500-42bd-11e9-853c-6f20d5075495.png">

## Install a database & add its integration

Started a MySQL 5.7 container and configured it for collecting metrics.

```bash
## Start a mysql 5.7 container
docker run -d --name dd-mysql \
    -e MYSQL_ALLOW_EMPTY_PASSWORD=yes \
    mysql:5.7

## Create datadog user in mysql & grant privileges
## Note that datadog user can accept login from 172.17.0.0/16 (subnet of Docker default network)
docker exec -it dd-mysql mysql -uroot -e "CREATE USER 'datadog'@'172.17.%' IDENTIFIED BY 'iJX:9KBH1JmyOWFdgkZJhedd';"
docker exec -it dd-mysql mysql -uroot -e "GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'172.17.%' WITH MAX_USER_CONNECTIONS 5;"
docker exec -it dd-mysql mysql -uroot -e "GRANT PROCESS ON *.* TO 'datadog'@'172.17.%';"
docker exec -it dd-mysql mysql -uroot -e "GRANT SELECT ON performance_schema.* TO 'datadog'@'172.17.%';"
```

Configured datadog-agent by adding `conf.d/mysql.yml` to collect the db container's metrics.

```bash
## Create configuration file
cat << EOS > conf.d/mysql.yaml
init_config:

instances:
  - server: dd-mysql
    user: datadog
    pass: iJX:9KBH1JmyOWFdgkZJhedd
    options:
      replication: false
EOS

## Stop the running container and start a datadog-agent container with mounting conf.d
## Add --link dd-mysql to connect the database container
docker rm -f dd-agent
docker run -d --name dd-agent \
    -v /var/run/docker.sock:/var/run/docker.sock:ro \
    -v /proc/:/host/proc/:ro \
    -v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro \
    -e DD_API_KEY=$DD_API_KEY \
    -e DD_TAGS="country:japan city:tokyo" \
    -v $(pwd)/conf.d:/conf.d:ro \
    --link dd-mysql \
    datadog/agent:6.10.1
```

After starting dd-agent with new configurations, metrics of mysql are collected like this:

<img width="640" src="https://user-images.githubusercontent.com/48383023/54079148-05fa2100-431a-11e9-8f32-5df53f7a83b2.png">

## Submit my_metric

Created config file named `conf.d/custom_random.yaml` and `checks.d/custom_random.py`.

```yaml
instances: [{}]
```

```python
import random

try:
    from checks import AgentCheck
except ImportError:
    from datadog_checks.checks import AgentCheck

__version__ = "1.0.0"


class CustomRandomCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', random.randint(0, 1000))

```

Restarted running datadog agent container with new configuration.

```bash
## Stop the running container and start a datadog-agent container with mounting checks.d
docker rm -f dd-agent
docker run -d --name dd-agent \
    -v /var/run/docker.sock:/var/run/docker.sock:ro \
    -v /proc/:/host/proc/:ro \
    -v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro \
    -e DD_API_KEY=$DD_API_KEY \
    -e DD_TAGS="country:japan city:tokyo" \
    -v $(pwd)/conf.d:/conf.d:ro \
    -v $(pwd)/checks.d:/checks.d:ro \
    --link dd-mysql \
    datadog/agent:6.10.1**
```

Datadog agent started to submit my_metric like this:

<img width="640" src="https://user-images.githubusercontent.com/48383023/54079257-cbde4e80-431c-11e9-9b4e-4f2b42a86f50.png">

## Change my check's collection interval

To change the collection interval of your check, use `min_collection_interval` in the configuration file.
Modified conf.d/custom_random.yaml like this:

```yaml
init_config:

instances:
  - min_collection_interval: 45
```

Restarted dd-agent container.

```bash
docker restart dd-agent
```

According to dd-agent logs, the check is executed every 45s.

```bash
docker logs dd-agent | grep custom_random
[ AGENT ] 2019-03-10 01:20:33 UTC | INFO | (pkg/collector/scheduler.go:63 in Schedule) | Scheduling check custom_random
[ AGENT ] 2019-03-10 01:20:33 UTC | INFO | (pkg/collector/scheduler/scheduler.go:76 in Enter) | Scheduling check custom_random with an interval of 45s
[ AGENT ] 2019-03-10 01:20:34 UTC | INFO | (pkg/collector/runner/runner.go:264 in work) | Running check custom_random
[ AGENT ] 2019-03-10 01:20:34 UTC | INFO | (pkg/collector/runner/runner.go:330 in work) | Done running check custom_random
[ AGENT ] 2019-03-10 01:21:18 UTC | INFO | (pkg/collector/runner/runner.go:264 in work) | Running check custom_random
[ AGENT ] 2019-03-10 01:21:18 UTC | INFO | (pkg/collector/runner/runner.go:330 in work) | Done running check custom_random
```

**Bonus Question** : Can you change the collection interval without modifying the Python check file you created?

One solution is modifying the constant value named `DefaultCheckInterval` in [source code](https://github.com/DataDog/datadog-agent/blob/33db6c888082da73e04a7d344b9c78ee3a72371d/pkg/collector/check/check.go#L16).
Obviously, it is a work around solution and affects to all checks.