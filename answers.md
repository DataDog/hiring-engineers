##1, Questions:

### What is Datadog Agent?

  Datadog Agent is a software running on systems (hosts). It collects system events and metrics, e.g., CPU usage, disk usage, network traffic, and sends these data to Datadog. By adding integrations and setting up corresponding configurations, Datadog Agent can also collect integrations' metrics. In addition, it also has a small server, DogStatsd, which aggregates custom app metrics.

### What is the difference between a timeboard and a screenboard?

  Timeboard and screenboard are two different types of custom dashboards. Timeboard is better for troubleshooting and tracking correlations between different metrics/events while screenboard is better for looking into system status. Screenboards have more options, such as Eventstream, Check Status, Free Text, etc.

  All graphs in a timeboard display the same time range, for example, the past 1 hour. On the contrary, each panel in a screenboard can display data for a different time period appropriate to that metric.
 
  Each graph of a timeboard can be shared individually by generating embed code (iframe), while screenboards can be shared as a whole using a public url. 
   An example of embed codes: 
  ```  
  <iframe src="https://app.datadoghq.com/graph/embed?token=9b52006b02ad16b4e4266a04932b0c40e65c39e4ebf06a48578c98f10ab49c7f&height=300&width=600&legend=false" width="600" height="300" frameborder="0"></iframe>
  ``` 
   
  Timeboard: [link to my timeboard](https://app.datadoghq.com/dash/152383/zhengshis-timeboard-25-jun-2016-1803?live=true&page=0&is_auto=false&from_ts=1466911339692&to_ts=1466914939692&tile_size=m&fullscreen=false)
  ![alt text](https://github.com/zhengshizhao/hiring-engineers/blob/support-engineer/img/timeboard.png "Timeboard")

  Screenboard: [link to my screenboard - public url](https://p.datadoghq.com/sb/b32ee517e-8c5f4c1c2a)
  ![alt text](https://github.com/zhengshizhao/hiring-engineers/blob/support-engineer/img/screenboard.png "Screenboard")

## 2, Datadog 

  I installed Datadog Agent for both Vagrant VM running Ubuntu and my local machine, Mac OS X. Although there are small differences when installing the agent and databases, other setttings on datadog are the same. Here I am giving answers using Virtual Machine (Vagrant Ubuntu 12.04). 

###Level 0 Install VM
   Set up: 
  * Install VirtualBox
  * Install Vagrant
  * Install MongoDB

###Level 1 Collecting Data
  * Sign up for Datadog and install datadog agent 

   For ubuntu: 

      [Install datadog agent link](https://app.datadoghq.com/account/settings#agent/ubuntu)

      [Basic usage](http://docs.datadoghq.com/guides/basic_agent_usage/ubuntu/)
  
  * Add Tags  
   Edit configuration file - /etc/dd-agent/datadog.conf
   ```
   # Set the host's tags
   tags: Vagrant, os:ubantux86_64, role:host
   ```
   Screenshots for tags & host: 
  ![alt text](https://github.com/zhengshizhao/hiring-engineers/blob/support-engineer/img/hostmap_vm.png "hostmap VM")
  * Add Datadog integration for MongoDB:
  
  Add MongoDB - [link to Datadog docs](http://docs.datadoghq.com/integrations/mongodb/)
  
   Configuration file: /etc/dd-agent/conf.d/mongo.yaml:
   ```
   init_config:
   instances:
   - server: mongodb://datadog:<mypassword>@localhost:27017/admin
   
     tags:
       - role:database
     additional_metrics:
       - top
   ```
  * Custom Agent check 

  Check file: /etc/dd-agent/checks.d/first_check.py  
  ```python
  from checks import AgentCheck
  import random
  def randomValue():
      return random.random()

  class RandomSampleCheck(AgentCheck):
      def check(self, instance):
          self.gauge("test.support.random",randomValue())
  ```
  Configuration file: /etc/dd-agent/conf.d/first_check.yaml
  ```
  init_config:
  instances:
    [{}]
  ```
###Level 2 Visualizing Data

  * Database integration dashboard: 
  [link to database dashboard](https://app.datadoghq.com/screen/97078/mongodb)

  Screenshot: 
  ![alt text](https://github.com/zhengshizhao/hiring-engineers/blob/support-engineer/img/dashboard.png "Database Integration Dashboard")
  
  * Snapshot of test.support.random metric

  ![alt text](https://github.com/zhengshizhao/hiring-engineers/blob/support-engineer/img/snapshot.png "Graph Snapshot")

###Level 3 Alerting on Data
  * Set up monitoring and set one alert 

  Screenshot for the setting: 
  ![alt text](https://github.com/zhengshizhao/hiring-engineers/blob/support-engineer/img/set_monitor.png "Alert Setting")

  * Alert sent to my email 
  Number is higher than 0.9 
  ![alt text](https://github.com/zhengshizhao/hiring-engineers/blob/support-engineer/img/alert.png "Alert Setting")
  * Downtime notification

  Start:
  ![alt text](https://github.com/zhengshizhao/hiring-engineers/blob/support-engineer/img/downtime_start.png "Downtime Starts")
  
  End: 
  ![alt text](https://github.com/zhengshizhao/hiring-engineers/blob/support-engineer/img/downtime_end.png "Downtime Ends")

