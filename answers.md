## Introduction
Hi, I'm Jordan Storms. For this challenge I used Linux Mint 18.3 (an Ubuntu derivative) and docker. I followed these instructions for setting up my environment: 
* [Datadog Docker-image repo](https://hub.docker.com/r/datadog/docker-dd-agent/)


## Collecting Metrics

#### Adding a tag
In order to add a tag we need to change the Agent config file. Since we are using docker and version 6 of the Datadog Agent in this example, this file will be located at /etc/datadog-agent.yaml (previous versions can be found at /etc/dd-agent.yaml).

To open and edit the file with gedit:
```sudo gedit /etc/datadog-agent/datadog.yaml```