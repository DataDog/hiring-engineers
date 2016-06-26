#General qustions: 
## What is Datadog Agent? 
## What is the difference between a timeboard and a screenboard?


#Virtual Machine (Vagrant Ubrantu 12.04):
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

#Local Machine (Mac OSX)
##Level 1
  * Sign Up for Datadog and Install datadog agent 
   For Mac OSX: 
      [install datadog agent link](https://app.datadoghq.com/account/settings#agent/mac)
      [basic usage](http://docs.datadoghq.com/guides/basic_agent_usage/osx/)
  
  * Add Tags  
   Mac osx: edit congifure file -  ~/.datadog-agent/datadog.conf
      then restart datadog agent 
   screenshots for tags & hosts: 

   ![alt text](https://github.com/zhengshizhao/hiring-engineers/blob/support-engineer/img/hostmap_mac.png "HostMap Mac")


##Level 2