# Introduction

Hello there! My name is Alex Gabrielian and I am applying for the Technical Account Manager role at Datadog.
As a part of my application, I was asked to complete the Solutions Engineer technical exercise which you will find below with both my code and the screenshots supporting my work.

# Setting up the environment

I decided to utilize the containerized approach with Docker for Linux.
After creating a Datadog account, I obtained my unique Datadog API key from the online User Interface (UI). Then, I ran the installation command to install a Datadog container on my local host which pulled a Docker image from Docker hub and ran it to create the container. 

![Docker container](https://i.imgur.com/HBXYq9y.png)

# Collecting metrics

First, I need to execute my docker container to install basic components. All commands inside the dd-agent container will be executed as root unless otherwise noted.

```
 docker exec -it dd-agent /bin/bash
 apt-get update 
apt-get install -y vim 

```

Now I edit my Datadog agent configuration by adding my unique API key and a few custom tags to uniquely identify various systems in my infrastructure for easier troubleshooting and analyzing.

```
 vi /etc/datadog-agent/datadog.yaml 

```

![Adding API key to Datadog agent](https://i.imgur.com/yWlaDCE.png)

![Adding tags to Datadog agent](https://i.imgur.com/UewE9Nm.png)

## PostgreSQL

Next, I will install a PostgreSQL database to my host, give Datadog read-only access to it, and configure my PostgreSQL configuration file to collect logs. 

### Installing and starting PostgreSQL

```
apt-get install -y postgresql
 service posgresql start
 su – postgres psql

```

### Preparing and making sure connection check is working

![Preparing PostgreSQL](https://i.imgur.com/0Y6CopP.png)

To start collecting logs, update database password from above, add tags, and update logging path.

```
vi /etc/datadog-agent/conf.d/postgres.d/conf.yaml

```

![PostgreSQL collecting logs](https://i.imgur.com/r2YXxuv.png)