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
    
## Check whether the container is running
docker ps
CONTAINER ID        IMAGE                  COMMAND             CREATED              STATUS                                 PORTS                NAMES
784b07f8bc22        datadog/agent:latest   "/init"             About a minute ago   Up About a minute (health: starting)   8125/udp, 8126/tcp   dd-agent
```

100 metrics are listed under `Metrics > Summary` in Datadog Web UI.
https://app.datadoghq.com/metric/summary

<img width="640" src="https://user-images.githubusercontent.com/48383023/54072145-ea5f2e00-42b9-11e9-9d77-776086b87ead.png">

<img width="640" src="https://user-images.githubusercontent.com/48383023/54072237-79207a80-42bb-11e9-91df-9f723b9e158b.png">

