DataDog Candidate Technical Checklist
  -------------------------------------

- Linux VM (Mint Ubuntu 16.04)
- Sign up for DataDog account
- Define Agent
  ```
  Agent is a small piece of software that gets installed on the host you want to monitor.  
  It consists of 3 main parts (A collector, server, and forwarder)
  This architecture allows for minimal overhead while collecting data at different frequencies.
  ```    
- Install MongoDB w/Auth, and DataDog Integration
- Write a custom agent test.support.random that generates random value
  ```
  import random

  from checks import AgentCheck

  class TestSupportRandomCheck(AgentCheck):
      def check(self, instance):
        self.gauge('test.support.random', random.random())
  ```  
- Clone Database [Dashboard](<https://app.datadoghq.com/dash/311475/mint-cloned?live=true&page=0&is_auto=false&from_ts=1498752492052&to_ts=1498756092052&tile_size=m>) (Added ***number of Mongo DBs***  and ***test.support.random***)

  ![](https://github.com/sbeamish/hiring-engineers/blob/master/screenshots/2017-06-28%20Snapshot%20and%20Notification.png)

- Difference between Timeboard and Screenboard
  ```
  A Timeboard is used to display values over the same time period.  
  A Screenboard is highly customizable and allows you mix widgets with timelines to get a better view of the entire system.
  ```
- Snapshot test.support.random going over .90 and send notification

  ![](https://github.com/sbeamish/hiring-engineers/blob/master/screenshots/2017-06-28%20Snapshot%20and%20Notification.png)  
- Monitor/[Alert](<https://app.datadoghq.com/monitors#2299689?group=triggered&live=4h>) when test.support.random >= .90 Warn >=.80
- Make alert scalable (I used a tag instead of hostname)
- Have alerts sent via email

  ![](https://github.com/sbeamish/hiring-engineers/blob/master/screenshots/2017-06-29%20Email%20Alerts.png)  
- Setup [Multi Alert](<https://app.datadoghq.com/monitors#2299689?group=triggered&live=4h>)

  ![](https://github.com/sbeamish/hiring-engineers/blob/master/screenshots/2017-06-29%20Multi%20Alert.png)
- Schedule [Downtime](<https://app.datadoghq.com/monitors#downtime?>) from 7pm-9am

   ![](https://github.com/sbeamish/hiring-engineers/blob/master/screenshots/2017-06-29%20Scheduled%20Downtime.png)
-Email Alert from Scheduled Downtime

  ![](https://github.com/sbeamish/hiring-engineers/blob/master/screenshots/2017-06-29%20Scheduled%20Downtime%20Email.png)
