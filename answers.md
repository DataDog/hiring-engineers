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

Edit your PostgreSQL configuration file /etc/postgresql/<version>/main/postgresql.conf and add the following parameters.

```
logging_collector = on
log_directory = 'pg_log'
log_filename = 'pg.log'
log_statement = 'all'
log_line_prefix= '%m [%p] %d %a %u %h %c '
log_file_mode = 0644
```

Collecting logs is disabled by default in the Datadog agent, enable it in your datadog.yaml file by adding the following.

```
logs_enabled: true
```

Restart Datadog Docker agent to engage changes and check status.

```
docker exec -it dd-agent agent stop
docker start dd-agent
docker exec -it dd-agent /bin/bash
service postgresql start
exit
docker exec -it dd-agent agent status
```

![Postgres status](https://i.imgur.com/YerSBhm.png)

Postgres metrics shown

![Postgres metrics shown](https://i.imgur.com/VU8gnxk.png)

## Create custom metric

First install the Datadog API

```
pip install datadog
```

Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000 and change your check's collection interval so that it only submits the metric once every 45 seconds.

```
vi /etc/datadog-agent/checks.d/custom_my_metric.py
```

Add the following code:

```
from checks import AgentCheck
from random import randint


class MyMetricCheck(AgentCheck):
    def check(self, instance):
        random_number = randint(0, 1000)
        self.gauge('my_metric', random_number, tags=['metric:my_metric'])
```

Create the corresponding configuration file.

```
vi /etc/datadog-agent/conf.d/custom_my_metric.yaml
```

Add the following code to change your check's collection interval so that it only submits the metric once every 45 seconds.

```
init_config:

instances:
  - min_collection_interval: 45
```

Bonus question: Can you change the collection interval without modifying the Python check file you created?
The collection interval can be modified in the configuration .yaml file, as I have done above.

# Visualizing data


