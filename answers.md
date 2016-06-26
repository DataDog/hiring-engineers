##General qustions:

  ### What is Datadog Agent?
    Datadog Agent is a software running on systems (hosts). It collects system events and matrics, for example, CPU usages, disk usages, network traffics etc. and send those data to Datadog. By adding integrations and setting up corresponding configurations, Datadog Agent can also collect intergrations' metrics. In addition, it also has a small server, DogStatsd, which aggregates custom app metrics.

  ### What is the difference between a timeboard and a screenboard?
   Timeboard and screenboard are two different types of costum dashboards. Timeboard is better for troubleshooting and correaltion while screenboard is better for looking into system status. Thus, screenboards has more options, such as Eventstream, check status, Free text, etc.

   All graphs of timeboards are scoped to the same time slot. for example, in the past 1 hour. On the contrary, screenboards can have different time frames. 
 
   Each graphs of timeboards can be shared individualy by generating embeded code, while screenboards can be shared as a whole by generating public url. 
   
   timeboard: [link to my timeboard](https://app.datadoghq.com/dash/152383/zhengshis-timeboard-25-jun-2016-1803?live=true&page=0&is_auto=false&from_ts=1466911339692&to_ts=1466914939692&tile_size=m&fullscreen=false)
   ![alt text](https://github.com/zhengshizhao/hiring-engineers/blob/support-engineer/img/timeboard.png "Timeboard")

   screenboard: [link to my screenboard](https://p.datadoghq.com/sb/b32ee517e-8c5f4c1c2a)
   ![alt text](https://github.com/zhengshizhao/hiring-engineers/blob/support-engineer/img/screenboard.png "Screenboard")

### I installed datadog Agent for both Vagrant VM, Ubantu system and my local machine, Mac os X. Although there are little differences on installing agent and databases, but the other setttings on datadog are the same. So here I am giving answers only using Vitual Machine. 

##Virtual Machine (Vagrant Ubrantu 12.04):
##Level 0 Install VM
   Set up: 
  * Install VirtualBox
  * Intall Vagerant
  * Install mongoDB

##Level 1 Collecting Data
  * Sign Up for Datadog and Install datadog agent 

   For ubantu: 
      [install datadog agent link](https://app.datadoghq.com/account/settings#agent/ubuntu)
      [basic usage](http://docs.datadoghq.com/guides/basic_agent_usage/ubuntu/)
  
  * Add Tags  
   Edit congifure file - /etc/dd-agent/datadog.conf

   screenshots for tags & host: 
  ![alt text](https://github.com/zhengshizhao/hiring-engineers/blob/support-engineer/img/hostmap_vm.png "hostmap VM")
  * Add Datadog integration for MongoDB:
  
  ep. mongoDB - [link](http://docs.datadoghq.com/integrations/mongodb/)
  
  -configuration file: /etc/dd-agent/conf.d/mongo.yaml:
  ```
  init_config:
  instances:
  - server: mongodb://datadog:84917zzsjingang@localhost:27017/admin
   
    tags:
      - role:database
    additional_metrics:
      - top
   ```
  * Custom Agent check 
  check file: /etc/dd-agent/checks.d/first_check.py  
  ```python
  from checks import AgentCheck
  import random
  def randomValue():
      return random.random()

  class RandomSampleCheck(AgentCheck):
      def check(self, instance):
          self.gauge("test.support.random",randomValue())
  ```
  -configuration file: /etc/dd-agent/conf.d/first_check.yaml
  ```
  init_config:
  instances:
    [{}]
  ```
##Level 2 Visualizing Data

  * Database intergration dashboard: 
  [link](https://app.datadoghq.com/screen/97078/mongodb)

  Screenshot: 
  ![alt text](https://github.com/zhengshizhao/hiring-engineers/blob/support-engineer/img/dashboard.png "Database Intergration Dashboard")
  
  * test.support.random graph

  ![alt text](https://github.com/zhengshizhao/hiring-engineers/blob/support-engineer/img/snapshot.png "Graph snapshot")

##Level 3 Alerting on Data
  * Set up a monitor and set an alert 
  screenshot for the setting: 
  ![alt text](https://github.com/zhengshizhao/hiring-engineers/blob/support-engineer/img/set_monitor.png "Alert Setting")
  * Alert sent to email 
  
  * Downtime notification
  ![alt text](https://github.com/zhengshizhao/hiring-engineers/blob/support-engineer/img/downtime_vm.png "Downtime")
