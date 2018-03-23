# Andy Roberts - Solution Engineer Answers

## Prerequesites

- upgraded VirtualBox on MacOSX
- download & install of Vagrant
- vagrant init hashicorp/precise64
- vagrant up
- vagrant ssh
- sudo apt-get install curl
- created DataDog account 
- installed datadog-agent : DD_API_KEY=xxx bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"

### So What, Who Cares ?

- very simple to test and demonstrate basic setup which means simple for customer to deploy
- simple agent installation and configuration and also easy to automate with Chef, Puppet etc
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

## Timeboards

To simplify and speed up creation of timeboard script, I first created a dashboard to see what the end result would look like. The timeboard creation gives the code in JSON format and I realised I could simply paste this in to the script given in the timeboard API guide. The intial steps were to create the app key and grab the API key for the top of the script. These have been removed from the uploaded script for security. 

The anomoly function attempts to spot trends that are anti-pattern. A load trend may be up and down during the day for example, but an anomoly would be, for example, load suddenly decreasing during a usually busy period. For this time series captured, as I adjusted the graph to the last 5 minutes, the agent had stopped on my vagrant box so agent had to be restarted. In this case it shows little of actual interest. A metric monitor would have helped here!

[https://github.com/stackparty/hiring-engineers/blob/master/create_dashboard.py]

![alt_text](https://github.com/stackparty/hiring-engineers/blob/master/datadog%20timeseries.png "my timeseries through api snapshot")

## Monitoring Data

created the monitor, configured the alerts and used the flexible conditions to match the specification requested. 

![alt_text](https://github.com/stackparty/hiring-engineers/blob/master/dd_metric_monitor_setup.png "monitor setup")
![alt_text](https://github.com/stackparty/hiring-engineers/blob/master/dd_metric_monitor_alert.png "email alert")
![alt_text](https://github.com/stackparty/hiring-engineers/blob/master/dd_metric_snooze_1.png "weekday downtime")
![alt_text](https://github.com/stackparty/hiring-engineers/blob/master/dd_metric_snooze_2.png "weekend downtime")





