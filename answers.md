# Andy Roberts - Solution Engineer Answers

## Prerequesites

- upgraded VirtualBox on my Mac
- downloaded & installed Vagrant
- vagrant init hashicorp/precise64
- vagrant up
- vagrant ssh
- sudo apt-get install curl
- created DataDog account 
- installed datadog-agent, cut and paste : DD_API_KEY=xxx bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"

### Value to customer / Conversation Points

- very simple to test and demonstrate basic setup and simple for customer to deploy themselves
- simple agent installation and configuration and easily to automated with Chef, Puppet etc
- no monitoring server deployment required massively reducing time to value/demonstration of solution

## Collecting Metrics

- Edited DataDog config : sudo vi /etc/datadog-agent/datadog.yaml
- uncommented tags section and made some changes 

 ![alt text](https://github.com/stackparty/hiring-engineers/blob/master/dd_agent_config.png "Tags in Agent Config")
 
- Restarted service : sudo service datadog-agent restart

![alt text](https://github.com/stackparty/hiring-engineers/blob/master/dd_hostmap.png "Host map in Datadog")

- Installed mysql : sudo apt-get install mysql
- Followed mysql agent install steps from here: [https://docs.datadoghq.com/integrations/mysql/]
```
cat mysql.yaml
  init_config:

  instances:
    - server: 127.0.0.1
      user: datadog
      pass: datadog
      port: 3306
      options:
          replication: 0
          galera_cluster: 1
          extra_status_metrics: true
          extra_innodb_metrics: true
          extra_performance_metrics: true
          schema_size_metrics: false
          disable_innodb_metrics: false
```

- restarted agent

- ![alt_text](https://github.com/stackparty/hiring-engineers/blob/master/dd_withmysql_agent.png "No tricks up my sleeve, Mysql Agent")

- Custom Agent check : [https://docs.datadoghq.com/agent/agent_checks/]
- in /etc/datadog-agent/checks.d/mymetric.py
```
import random
from checks import AgentCheck
class MyMetric(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', random.randint(1,1001))
```
- in /etc/datadog-agent/conf.d/mymetric.yaml
```
init_config:
  min_collection_interval: 45

instances:
    [{}]
```

![alt_text](https://github.com/stackparty/hiring-engineers/blob/master/dd_mymetric_explorer.png "my_metric explored")

Metric Collection time is adjusted in configuration yaml instead of python code. 

### Value to customer / Conversation Points

- Wide range of pre-built agents available for most common tools available with no extra download
- Huge value in tags, in terms of collecting groups of metrics and being able to explore them by tag
- Tags can be added through client or added in the dashboard 

## Timeboards

To simplify and speed up creation of timeboard script, I first created a dashboard to see what the end result would look like. The timeboard creation gives the code in JSON format and I realised I could simply paste this in to the script given in the timeboard API guide. The intial steps were to create the app key and grab the API key for the top of the script. These have been removed from the uploaded script for security. 

The anomaly function attempts to spot trends that are anti-pattern. A load trend may be up and down during the day for example, but an anomaly could load suddenly decreasing during a usually busy period. For this time series captured, as I adjusted the graph to the last 5 minutes, the agent had stopped on my vagrant box so agent had to be restarted. In this case it shows little of actual interest. A metric monitor would have helped here!

[https://github.com/stackparty/hiring-engineers/blob/master/create_dashboard.py]

![alt_text](https://github.com/stackparty/hiring-engineers/blob/master/datadog%20timeseries.png "my timeseries through api snapshot")

### Value to customer / Conversation Points

- API access allows quick deployment and useful for service providers or enterprises performing common tasks between BU/Customers
- Massive range of mathematical functions and features to be able to analyse data however someone wants
- Complex features such as anomaly detection to spotting patterns and trends in data, to improve apps & deployments
- Snaphots allow running commentary of particular events and for them to be captured when observed

## Monitoring Data

created the monitor, configured the alerts and used the flexible conditions to match the specification requested. 

![alt_text](https://github.com/stackparty/hiring-engineers/blob/master/dd_metric_monitor_setup.png "monitor setup")
![alt_text](https://github.com/stackparty/hiring-engineers/blob/master/dd_metric_monitor_alert.png "email alert")
![alt_text](https://github.com/stackparty/hiring-engineers/blob/master/dd_metric_snooze_1.png "weekday downtime")
![alt_text](https://github.com/stackparty/hiring-engineers/blob/master/dd_metric_snooze_2.png "weekend downtime")

### Value to customer / Conversation Points

- Plenty of flexibility in creating alerts, such that important events can be filtered and trapped
- Correct information can be pinpointed in alerting allowing for quicker resolution
- Downtime option reduces false positive alerting, which everyone in Ops hates

## Collecting APM data

Read the APM notes and then copied over the sample code given. A few minor changes were made to make it run: changing host port and IPs, which was discovered to be an issue when running the app. Initially I had assumed nothing was happening when I ran the app and made calls to it with wget. I saw nothing in DataDog. Eventually I realised I had a tag of env:test set and that was obscuring my view of what was going on.

I built a dashboard that included CPU userspace usage and sum of web requests and froze it.

App [https://github.com/stackparty/hiring-engineers/blob/master/flaskapp.py]

![alt_text](https://github.com/stackparty/hiring-engineers/blob/master/dd_apptrace_1.png "app trace dashboard config")
![alt_text](https://github.com/stackparty/hiring-engineers/blob/master/dd_apptrace_2.png "app trace graph")

A service is a high level concept that is defined by the service name and may refer to a database, web app etc that make up a whole application. A resource is something that is served up by or used within that application such as a URL, SQL query. 

### Value to customer / Conversation Points

- Arguably the 'stickest' feature of embedding DataDog value in to customers code and driving revenue opportunity
- Very simple setup to trace common web apps, databases and provide application specific insights
- Discovered of key events largely automated with little extra code needed to gain those insights

## Final Question

This is my DogOps team building their latest 12-factor application to defeat the cat. I would take the sound level from the camera we use to watch them, pass that in to DataDog, building alerts and monitors for them barking. Long term trends ( i.e. the postman, the dog walker ) could then be identified vs unexpected cases of barking.

![alt_text](https://github.com/stackparty/hiring-engineers/blob/master/dogops.jpg "dog ops")

Final advice. Do not attempt to cut off the top of your finger with a carving knife while doing your DataDog Hiring Exercise. It slows typing down and makes using vi hilarious. 
![alt_text](https://github.com/stackparty/hiring-engineers/blob/master/badmotorfinger.JPG "ooops")




