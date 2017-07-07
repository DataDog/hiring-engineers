DataDog Candidate Technical Checklist
  -------------------------------------

- Linux VM (Mint Ubuntu 16.04)
- Sign up for DataDog account
-  Define Agent

   The Datadog agent is a very lightweight piece of software with 1% of overhead that gets installed on the host system you want to monitor.  The agent is capable of capturing metrics as frequently as every second with minimal impact to the host system.  Metrics can include host metrics like CPU, RAM, application monitoring inside Docker containers, or you can write your own agent to capture custom metrics.  Datadog has been written from the ground up as as a SAAS offering allowing for maximum flexibility and scalability.   

- Install MongoDB w/Auth and DataDog Integration

  Datadog comes with over 200 built in and supported integrations covering the modern application stack from your Continuous Integration Server to the Platform.  We already cover majority of the technology stack in the legacy and modern Enterprise .  In the absence of a built-in integration the agent is open source so you can build your own custom agent using our API.

- Here is a sample of a custom agent that will generate a random value
  ```
  import random

  from checks import AgentCheck

  class TestSupportRandomCheck(AgentCheck):
      def check(self, instance):
        self.gauge('test.support.random', random.random())
  ```
  Dashboards are real time graphs of metrics that are synchronized over time.  As you move your cursor along a timeline of an individual graph the cursor simultaneously moves on all the other graphs on the screen.    
  
- In this example I cloned the Database [Dashboard](<https://app.datadoghq.com/dash/311475/mint-cloned?live=true&page=0&is_auto=false&from_ts=1498752492052&to_ts=1498756092052&tile_size=m>) then added additional metrics to capture the *number of Mongo DBs*  and our custom *test.support.random* metric.

  ![](https://github.com/sbeamish/hiring-engineers/blob/master/screenshots/2017-06-28%20Snapshot%20and%20Notification.png)

   Dashboards can be created as Timeboards or Screenboards.  A Timeboard is used to display captured metrics using the same synchronized time period.  A Screenboard adds the ability to mix widgets and time lines giving you the ability to setup complex forensic views into the system.  If you are monitoring a hybrid environment across Platforms (on-prem, Azure, and EC2) you can view this heterogeneous environment on a single pane of glass and correlate events with issues in real time.  

- In this example I sent a Snapshot of the graph and notification when our random number metric goes over .90.

  ![](https://github.com/sbeamish/hiring-engineers/blob/master/screenshots/2017-06-28%20Snapshot%20and%20Notification.png) 
   
- Monitor/[Alert](<https://app.datadoghq.com/monitors#2299689?group=triggered&live=4h>) when test.support.random >= .90 Warn >=.80 and make alert scalable (I used a tag instead of hostname)

   Tagging in an incredibly powerful asset in Datadog.  This simple concepts allows you to scale your monitoring very quickly without having to explicitly add metrics to a host.  For example adding the role tag (database) will automatically capture the metrics (# of connections, read/write) to monitor your database server. As you add new servers to the pool simply add the necessary server role to immediately capture metrics.  In a Development environment you may have a single server that hosts the UI, Services, and Database but these server roles (tags) are separated as you move up and scale the environment stack.  Tagging also gives you the ability to see more complex scenarios like host performance per environment plus server-role.  So if a code promotion to a Dev Database is performing poorly you can quickly isolate the problem and diagnose the issue as a long running query. This immediate feedback allows you to fail fast and discover issues sooner in the SDLC.

   Monitoring/Alerts are set to watch and automatically alert team members when a metric reaches a certain threshold.  You may want to set an alerts when CPU of a database is pegged at 100% for a defined period of time.  You can also choose from one of the built in machine learning algorithms that will alert you when a value has deviated by 2 standard deviations.  

- In addition to sending notifications you can send email alerts.

  ![](https://github.com/sbeamish/hiring-engineers/blob/master/screenshots/2017-06-29%20Email%20Alerts.png)  
- Converting to a [Multi Alert](<https://app.datadoghq.com/monitors#2299689?group=triggered&live=4h>) will notify for each individual host or role for that threshold.

  ![](https://github.com/sbeamish/hiring-engineers/blob/master/screenshots/2017-06-29%20Multi%20Alert.png)
- Schedule [Downtime](<https://app.datadoghq.com/monitors#downtime?>) from 7pm-9am

 You can schedule alert downtime in preparation for code deployments, planned outages, or environment maintenance.

   ![](https://github.com/sbeamish/hiring-engineers/blob/master/screenshots/2017-06-29%20Scheduled%20Downtime.png)
- Here is the email Alert from the Scheduled Downtime

  ![](https://github.com/sbeamish/hiring-engineers/blob/master/screenshots/2017-06-29%20Scheduled%20Downtime%20Email.png)
