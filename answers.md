## Introduction

The purpose of this document is to show an overview of Datadog's capabilities by using different features from spinning up the agent, passing through metrics and using APM and Traces.

## Datadog Agent Setup

The Datadog agent is a set of tools to orchestrate the communication between your legacy and the on-line platform. You have different ways of integrating Datadog to your solution such as a virtual machine via Vagrant or Docker.

For this exercise, we are going to use the official Docker image that will easily spin up a container with the whole set of tools available allowing you to get started.

If you already have Docker installed on your machine, you can run the following command:

```
DOCKER_CONTENT_TRUST=1 \
docker run -d  --name dd-host-mysql \
              -v /var/run/docker.sock:/var/run/docker.sock:ro \
              -v /proc/:/host/proc/:ro \
              -v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro \
              -v ${PWD}/conf.d:/conf.d:ro \
              -v ${PWD}/checks.d:/checks.d:ro \
              -p 127.0.0.1:8126:8126/tcp \
              -e DD_API_KEY=<API_KEY> \
              -e DD_HOSTNAME=dd-host-mysql \
              -e DD_DOGSTATSD_NON_LOCAL_TRAFFIC=true \
              -e DD_SITE="datadoghq.eu" \
              -e DD_APM_ENABLED=true \
              -e DD_TRACE_ANALYTICS_ENABLED=true \
              -e DD_TAGS="environment:mysql, name:tag-mysql, department:database" \
              datadog/agent:latest
````
This list of flags is not exhaustive but is enough to fulfill what we are looking for. Here is the explanation of the most important ones:

#### Container name
```--name dd-host-mysql```
Assigns a meaningful name for your container. It will be useful to query/filter on the UI's Dashboard.

#### Directory mapping
```-v ${PWD}/conf.d:/conf.d:ro```
```-v ${PWD}/checks.d:/checks.d:ro```

These lines create a link between your local computer (host) and the container. 

#### Datadog APM
```-p 127.0.0.1:8126:8126/tcp```
Routes all requests from host port 8126 to container's port 8126. 

#### Datadog API Key
```-e DD_API_KEY=<API_KEY>```
Configures the Agent with your key. Replace this value with a valid API Key for your account

#### Datadog agent hostname
```-e DD_HOSTNAME=dd-host-mysql```
This hostname will be useful when visualizing your metrics and reports on Datadog's platform. 

#### Send metrics externally
```-e DD_DOGSTATSD_NON_LOCAL_TRAFFIC=true``` 
This flag enables your container to send traffic to the external Datadog's endpoints

#### Datadog site
```-e DD_SITE="datadoghq.eu"```
Sets the correct geography that will receive your agent's data. Important for GDPR concerns.

#### Enable APM 
```-e DD_APM_ENABLED=true```
Enables the APM functionality

#### Enable Trace analytics 
```-e DD_TRACE_ANALYTICS_ENABLED=true```
Enables the trace metrics

#### Custom tags
```-e DD_TAGS="environment:mysql, name:tag-mysql``` 
Using the ``DD_TAGS`` option you can create as many tags as needed to correctly identify, filter and manage your resources at Datadog's platform. Tags are comma-separated and use the format <KEY>:<VALUE>

## Collecting Metrics

If you entered a correct ```API_KEY``` value, the container will start the communication with the remote endpoints automatically.

### Host Tags
As soon as your docker container is running, in a couple of minutes will be able to see at your Datadog's account the tags (configured previously with ```DD_TAGS```). Here is an example using our ```docker run``` command:

![Q1](https://github.com/gamferreira/hiring-engineers/blob/master/q1.png)

### Database integration
Monitoring a database is most likely a point of concern on the majority of applications. Therefore, having a good monitoring overview with metrics, numbers, and graphs is crucial for your systems' availability and stability. 

Datadog provides you with a built-in feature to integrate a list of different databases into your monitoring dashboards. 

In this example, we are using a sample MySQL database to illustrate some of the capabilities available to your team.

#### Step 1 - Enable the integration
Go to *Integrations* and select your provider (in our case, MySQL):

![Q2](https://github.com/gamferreira/hiring-engineers/blob/master/q2.png)

#### Integrating your database with the agent
Your agent has to know how to connect to your database and send the appropriate metrics. 

This can easily be achieved by adding a YAML file with the name ```conf.yaml``` under ```conf.d/mysql.d``` with the following content

![Q2](https://github.com/gamferreira/hiring-engineers/blob/master/q2.1.png)

*Important*
* After adding this file you have to run the ```docker run``` step again. This is due to the fact that the agent parses all integrations during its initialization.

* The agent will only be able to read your files if you start the container with the flags described under *Directory Mapping*

* Please refer to Datadog's documentation for more information about possible YAML configuration and how to grant the proper access to the MySQL user used to connect to the instance.

### Custom Metrics using Python

One of the greatest Datadog's features is *Metrics*. Your application can send any set of metrics to the platform allowing you to monitor, group, report and measure any sort of data that makes sense to your business.

In this example, we are creating a Python script that sends a random number from 0 to 1000 to a metric named **my_metric** tagged with **custom_metrics** and a tag value of **1**.

The agent expects all metrics to be saved under ```checks.d``` folder with the name convention *<your_metric_name>.py*. Please refer to **Directory Mapping** and also Datadog's documentation for more information on how to map your host directory to the container.

Here is the complete Python script that implements our metric:

![](https://github.com/gamferreira/hiring-engineers/blob/master/q3.png)

#### Metric's frequency

The metric's interval - how frequent a metric runs - can be set without changing the source script. It can be achieved by adding a YAML file as follows:

![](https://github.com/gamferreira/hiring-engineers/blob/master/q4-bonus.png)

You should place your configuration file under ```conf.d``` . This file must follow the naming convention *<your_metric_name>.yaml

* In the example above we are setting the *min_collection_interval* to *45* which means this metric will send a random number from 0 to 1000 at the minimum interval of 45 seconds.

### Data visualization
Your agent is ready to send some sample data to Datadog's platform. To confirm that you have successfully set it up, open your account and create a dashboard using your newly-created custom metric.

Your dashboard might look like this:

![](https://github.com/gamferreira/hiring-engineers/blob/master/q5.png)

### Sharing your metric with others
With Datadog's mention feature you can easily share a graph with your peers as you can see below:

![](https://github.com/gamferreira/hiring-engineers/blob/master/q7-notation.png)

### Anomaly graph
Graphs are powerful when combined with different algorithms. In this case, I have applied the anomaly pattern to clearly show the deviation from the standard:

![](https://github.com/gamferreira/hiring-engineers/blob/master/q6-bonus.png)


### E-mail alerts
Having a nice dashboard with graphs, metrics and numbers are important to keep your operations healthy. Although you might always proactively be taking a look at it, you may also receive automated e-mail notifications based on thresholds you determine.

In the following screens, we have configured e-mail alerts to be triggered when *my_custom* metric breaches a certain threshold:

![](https://github.com/gamferreira/hiring-engineers/blob/master/q8.1.png)

![](https://github.com/gamferreira/hiring-engineers/blob/master/q8.2.png)

### Downtime periods

You may also configure Datadog to stop sending you alarms and messages through e-mail for a given period of the day. For example, you can set your alarms to be suspended from 7 pm to 8 am:

![](https://github.com/gamferreira/hiring-engineers/blob/master/q8.3-downtime.png)

### Custom messages

It is possible to configure customized messages based on different alert conditions available for you at the Monitor > Metrics page:

![](https://github.com/gamferreira/hiring-engineers/blob/master/q8.4.png)

With a powerful variable replacement engine you can also provide your team with detailed information values, metrics and, host information:

![](https://github.com/gamferreira/hiring-engineers/blob/master/q8.5.png)

### Dashboard with both APM and Infrastructure Metrics.

You can combine different metrics and graphs into a single dashboard as displayed below:

![](https://github.com/gamferreira/hiring-engineers/blob/master/q9.png)

Public link: https://p.datadoghq.eu/sb/pb6bfnbzervbjgv2-7844d9fa95bc7b2325b9a6d38afe6560

### API Automation

Configuring everything manually is pretty straight-forward but what if you want to automate the creation of dashboards, triggers and so on? Datadog provides a powerful and simple-to-use API that allows you to orchestrate your monitoring artifacts. 

The prerequisite is to create a specific *App Key* that grants the script permission to create things on your behalf.

The script below is an example of how to create a dashboard based on some metrics such as database and custom metrics with some algorithm applied:

```
from datadog import initialize, api

options = {'api_key': 'api_key',
           'app_key': 'api_key',
           'api_host': 'https://api.datadoghq.eu'}

initialize(**options)

scope = 'host:dd-host-mysql'
title = 'API - My Dashboard'

widgets = [
  {
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'my_metric{'+scope+'}'}
        ],
        'title': 'My Custom Metric'
    }
  },
    {
    'definition': {
        'type': 'query_value',
        'requests': [
            {'q': 'my_metric{'+scope+'}.rollup(sum,3600)'}
        ],
        'autoscale': True,
        'title': 'My Custom Metric with Rollup'
    }
  },
  {
    'definition': {
         'type':'timeseries',
         'requests': [ 
               { 
                  'q':'anomalies(system.load.1{'+scope+'}, "basic", 2)'
               },
               { 
                  'q':'anomalies(system.load.5{'+scope+'}, "basic", 2)'
               },
               { 
                  'q':'anomalies(system.load.15{'+scope+'}, "basic", 2)'
               }
            ],
            'title':'MySQL System load',
            'show_legend': False,
            'legend_size': '0'
    }
  }
]
layout_type = 'ordered'
description = 'Dashboard created through API'
is_read_only = True
notify_list = ['gmendes.ferreira@gmail.com']
template_variables = []
print(api.Dashboard.create(title=title,
                     widgets=widgets,
                     layout_type=layout_type,
                     description=description,
                     is_read_only=is_read_only,
                     notify_list=notify_list,
                     template_variables=template_variables))
```

Please refer to the API documentation for more information and examples.

## Services and a Resources
Datadog brings a set of concepts and definitions that are important to extract the best out of the platform. One common question concerns the difference between a service and a resource.  In a nutshell:

*Service*: Logical group of resources. Example: Transactions Service contains all tables, jobs, queues of that specific goal.

*Resource*: Using the previous example, a resource would be: an SQS Queue, RDS Database, Lambda Steps State Machine, Lambda Function, API Gateway Endpoints, etc.

### Thank you

First of all, I am personally impressed with the tool, I had lots of fun creating the exercises! There are tons of features that I will be exploring soon.

I have a few ideas in my mind but to stick with one: I am coming from Brazil a country known by its beauty of natural resources, beaches, mountains and so on. However, away from the touristic places, the population suffers from an increasing number of crimes happening in all metropolitan areas. Nowadays, there are some mobile apps to report crimes (such as robbery, assaults, kidnaps, rapes) and those apps could provide important and centralized metrics to the authorities, allowing them to create an endless set of dashboards to fight against the gangs all over the country.
