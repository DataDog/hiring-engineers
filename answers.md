# David Judge's Answers for _Hiring-Engineers_

<!-- ## Table of Contents
-->

<!-- TOC START min:2 max:4 link:true update:true -->
  - [Level 0 - Setup an Ubuntu VM](#level-0---setup-an-ubuntu-vm)
  - [Level 1 - Collecting your Data](#level-1---collecting-your-data)
    - [In your own words, what is the Agent?](#in-your-own-words-what-is-the-agent)
    - [Add tags in the Agent config file](#add-tags-in-the-agent-config-file)
      - [What are tags?](#what-are-tags)
      - [Screenshots: Tags](#screenshots-tags)
    - [Install a database on your machine](#install-a-database-on-your-machine)
      - [Screenshots: MySQL](#screenshots-mysql)
      - [Screenshot: PostgreSQL](#screenshot-postgresql)
    - [Write a custom Agent check that samples a random value.](#write-a-custom-agent-check-that-samples-a-random-value)
      - [Screenshots: randomvalue Agent Check](#screenshots-randomvalue-agent-check)
      - [Screenshots: Further use of Agent Checks](#screenshots-further-use-of-agent-checks)
  - [Visualizing your Data](#visualizing-your-data)
    - [Since your database integration is reporting now, ...](#since-your-database-integration-is-reporting-now-)
    - [Bonus question: What is the difference between a timeboard and a screenboard?](#bonus-question-what-is-the-difference-between-a-timeboard-and-a-screenboard)
    - [Take a snapshot of your `test.support.random` graph ...](#take-a-snapshot-of-your-testsupportrandom-graph-)
  - [Level 3 - Alerting on your Data](#level-3---alerting-on-your-data)
    - [Set up a monitor on this metric](#set-up-a-monitor-on-this-metric)
    - [Bonus points:  Make it a multi-alert by host](#bonus-points--make-it-a-multi-alert-by-host)
    - [Give it a descriptive monitor name and message](#give-it-a-descriptive-monitor-name-and-message)
    - [This monitor should alert you within 15 minutes.](#this-monitor-should-alert-you-within-15-minutes)
    - [Bonus: Since this monitor is going to alert pretty often, ...](#bonus-since-this-monitor-is-going-to-alert-pretty-often-)

<!-- TOC END -->





<!--
## Answers
-->

## Level 0 - Setup an Ubuntu VM

<!---
* Fresh Linux VM:
  * Running `vagrant up`
    ![Vagrant up output][Initial Vagrant up]  
-->
  * `vagrant up` created the virtualbox automatically  

    ![VM Just created in VirtualBox][VM Just Created in VBox]  

<!---   * Virtualbox "screen" showing the output of `ipconfig`
    ![New VM screengrab][VM Just built]

  * Access to the virtualbox is easiest through `vagrant ssh`:
    ![vagrant ssh][vagrant ssh]
-->
  * To be better able to show the usage/impact of tags and, DataDog's agent was also installed on a second server, though this one is physical and running Ubuntu:  

    ![All Hosts][All Hosts]   






## Level 1 - Collecting your Data

* Sign up for DataDog
  *  Done - user is _david.judge@computer.org_


### In your own words, what is the Agent?
  * Management-focused answer:  
    The agent collects the metric data and their associated tags and sends them to the DataDog servers.  The agent is resilient and if a networking issue occurs, it holds onto the data until such time as it can be sent to the DataDog servers.  The agent monitors itself and can restart agent components should they fail.  The agent sometimes hosts integrations that have been deployed to measure metrics from over 100 sources such as Docker or MySQL.  This list of integrations that are available out of the box can be found [in the DataDog web site.](https://www.datadoghq.com/product/integrations/)  

  * Technical answer:  
    The agent is made up of 4 parts: a collector, a daemon called "dogstatsd", a forwarder and a 2nd daemon called "supervisord".  
	  **Supervisord**: The supervisord starts the various processes that are part of the agent.  Should a process die unexpectedly, supervisord will restart them.  
    **Forwarder**: The forwarder is a queue and forward component which receives data from the collector and the daemon over http and sends it up to the DataDog servers over https.  If there is a network issue stopping the forwarder from sending its data to DataDog, it hold the data until such time as the connection is available again.  However it also keeps tabs on its memory usage and should the outage go on for too long and memory consumption increase too much, the forwarder will drop older data starting with the oldest.
    **Collector**: The collector collects _standard_ metrics and can also run "checks" which can either be pre-built "data sources" such as NTP check or custom "Agent Checks".  The latter are written in Python and can collect any data the user chooses at either the default interval or at a user-defined interval.  The "checks" that are present for your agent can be found as python files in the `/etc/dd-agent/check.d directory`.  Configuration data such as parameters and tags for the checks are held in the `conf.d` directory.  Note that the configuration file is not optional and at the very least a minimal configuration file must be present.  Instructions on how to create an "Agent Check" can be found [in the DataDog documentation on Agent Checks.](http://docs.datadoghq.com/guides/agent_checks/)  
    **DogStatsd**: The "dogstatsd" daemon (which is also known as the "StatsD server") receives custom metric data which it collates and sends to the forwarder to send on to the DataDog servers.  Metrics can be sent to dogstatsd using sample Python or Ruby code provided in the DataDog documentation.  DataDog do not recommend using the dogstatsd API directly but recommend using one of the libraries they provide [in the DataDog documentation on libraries.](http://docs.datadoghq.com/libraries/.  )

    **Integrations**:  DataDog hosts "integrations" in the agent.  These integration agents can monitor over 100 sources such as Docker or MySQL and even collaboration tools such as Slack.  The list of integrations that are available out of the box can be found [in the DataDog web site](https://www.datadoghq.com/product/integrations/) or in the DataDog GUI under Integrations > Integrations.  In this exercise, the Docker, MySQL and PostgreSQL integrations have been deployed.  Deployment is simple as it is mostly GUI-driven, though a command needs to be run on the machine running the agent which hosts the integration.  

  * Extra notes and observations:  
    The supervisord actually started 6 processes.  The three listed above plus "trace-agent", "jmxfetch" and "go-metro".  "jmxfetch and "go-metro" both exited within seconds with log file entries "exit status 0; expected".  "trace-agent" continued to run.  From the documentation I can infer that "trace-agent" receives trace information from instrumented code.   
    The documentation [seems to suggest that dogstatsd sends the data directly](http://docs.datadoghq.com/guides/dogstatsd/) over https to the DataDog servers, while a [post written on March 15th, 2017 would suggest that the data is pulled](https://help.datadoghq.com/hc/en-us/articles/203034929-What-is-the-Datadog-Agent-What-resources-does-it-consume-) by the forwarder.  The readme.md file of dd-agent (in github) states that the forwarder receives data from both the collector and dogstatsd.  
    The user-defined interval for agent check is not strictly speaking an interval for collection but rather the minimum time between intervals.
    The agent's source code is available on github and users are encouraged to write any integration they think is missing.


### Add tags in the Agent config file
  ... and show us a screenshot of your host and its tags on the Host Map page in DataDog.

#### What are tags?
  * **What are tags**:    
    DataDog associates tags or named labels with the data it collects.  An example of this could be a "MachineType" tag which could have values such as "physical", "VM" or "container".  In the DataDog UI, tags facilitate the slicing, dicing and aggregation of the collected data and can be seen as another dimension to the data.  (See [this video on DataDog's data collection - from 2:40](https://youtu.be/xKIO1aWTWrk?t=2m44s) for a visual explanation.)  These tags can, for example, be used to filter the contents of dashboards or to select the hosts or instances to include in a monitor, and tags are especially useful in filtering event lists. Furthermore, in dashboards, tags can be used to group information.  
    Tags can be defined for an agent installation (in `/etc/dd-agent/datadog.conf`) and are then inherited by any Agent Check (see [Agent Checks section below](#write-a-custom-agent-check-that-samples-a-random-value)) or integration run on that agent.  Some tags are automatically created by integrations (i.e. AWS's integration will create tags for the region of an instance and the Docker integration creates tags with the container name and the image name).  These tags are said to be inherited from the integration.  

  * **Significance of Tagging**:  
    As tags can be used to filter and group the data displayed in DataDog, they are key to being able to quickly triage issues, allowing the user to focus on, say, a service and all it includes rather than specific components and thus get to root cause quicker.  
    Tagging is largely automatic which helps keep deployment effort and costs low.  
    When creating dashboards or monitors, tags can be used to automatically select which components, hosts or databases to include in the dashboards and monitors or how their data is aggregated.  For example a dashboard could have average transaction counts grouped by the tag "availabilityzone" (for their AWS availability zone) and include only metrics for hosts which have the tag "environment" set to "production".  If new hosts are added which have the same environment tag value, they will automatically be included in the dashboard or monitor.  

  * **Extra notes and observations:**   
    The tags I created for both agents were "machinetype" with values "virtualboxvm" and "physical", and "purpose" with values "learning" and "hiringexcercise".  For the physical host I added tags for "machinemodel" and "machinemanufacturer".  
    For the NewGenerateDBLoad Agent Check, I created a tag by putting the tag in the `NewGenerateDBLoad.yaml` configuration file:  
      ```yaml
      init_config:
          min_collection_interval: 120

          instances:
              -   theDB: mysql
                  iterations: 10
                  userName: root
                  userPassword: Chestnut1999
                  concurrentUsers: 100
                  tags:
                     - GenerateDBLoad: MySQL
      ```  
    For maximum benefit, when deploying into production, a good analysis of the environment will be required to identify the best tags to use.

#### Screenshots: Tags
  * Agent-level tags are added to the configuration file `/etc/dd-agent-datadog.conf` ([link](precise64/etc/dd-agent/datadog.conf)):
  ```
  # Set the host's tags (optional)
  # tags: mytag, env:prod, role:database
  tags: purpose:learning, machinetype:VirtualBoxVM
  ```
  <!---
    ![datadog.conf entry for tags][tags in datadog config file]
    -->
  * Viewing tags for a host in the DataDog UI:  

    ![Host entry and tags in UI][Host with tags]  

  * Using tags to group components:  
    * All the hosts that have been set-up (i.e. no tags entered in the filter):  

      ![All Hosts][All Hosts]  

    * All hosts grouped by tag "machinetype"  

      ![Hosts grouped by tag "machinetype"][Hosts grouped by tag "machinetype"]  

  * Using tags to correlate events with time-series graphs in a Timeboard:  

    ![Tag filter timeboard][Tag filter timeboard]

### Install a database on your machine  
  ... (MongoDB, MySQL, or PostgreSQL) and then install the respective DataDog integration for that database.

#### Screenshots: MySQL
* MySQL Installed on virtualbox VM:  

  ![Install MySQL Monitoring part 1][Install MySQL Monitoring part 1]  

* Configuring `mysql.yaml` with the details for the database:  
  ```yaml
  init_config:

  instances:
    - server: localhost
      user: datadog
      pass: 4f7OUn5pjFV2f0zolO1Mezsi
      tags:
          - Purpose:Learning
          - Env:Training
      options:
          replication: 0
          galera_cluster: 1
  ```

  <!-- ![mysql.yaml updated][Tags in mysql.yaml]    -->

* Checking with `dd-agent info`:  

  ![Info showing mysql][info showing mysql]  

* The MySQL integration displays on the host map (up to a maximum of 6 integrations will display there):  

  ![Map now shows MySQL][Map now shows MySQL]  

#### Screenshot: PostgreSQL

* Also installed PostgreSQL on the physical server:  

  ![PostgreSQL from infrastructure map][PostgreSQL from infrastructure map]


### Write a custom Agent check that samples a random value.
  ... Call this new metric: `test.support.random`  

  Agent Checks are python scripts which run based on configuration statements found in a corresponding yaml file.  On Linux hosts, the scripts are found in the `/etc/dd-agent/checks.d` directory and the configuration files are found in `/etc/dd-agent/conf.d`.  

  Agent Checks scripts use one of 7 functions available in the Agent Check interface to send metrics, events or service checks to DataDog.  The interfaces can receive optional parameters including tags.  Alternatively, tags can be set in the Agent Check's conf.d yaml file.  Any metrics sent will automatically be tagged with the DataDog Agent's tags as defined in `datadog.conf`.  Agent Checks can also send events and service checks.  

  Documentation on how to write an Agent Check can be found in DataDog's documentation: [Agent Checks Documentation](http://docs.datadoghq.com/guides/agent_checks/)  

#### Screenshots: randomvalue Agent Check


  * Created "randomvalue" Agent Check:
    * Configuration file [`randomvalue.yaml`](precise64/etc/dd-agent/conf.d/randomvalue.yaml):  
      ```yaml  
      init_config:

      instances:
          [{}]
      ```
      <!-- ![Random Value YAML][Random Value YAML]   -->
      Notice the empty set in the "instances section".  This section can be used to pass "instances" (i.e. instances of the check) and the parameters of the instances into the agent check.  An example of how to do this is included in the [DataDog Agent Check documentation](http://docs.datadoghq.com/guides/agent_checks/#http).  
      In that example, 3 instances - in this case, sites to be retrieved - are listed, one of which has the extra parameter called "timeout".  
      Tags can also be added to the yaml file (_note that the below is an example and has not been tested_).  
      ```yaml
      init_config:
        default_timeout: 5

      instances:
        -   url: https://google.com

        -   url: http://httpbin.org/delay/10
            timeout: 8
            tags:
                - Expected:slow

        -   url: http://httpbin.org/status/400
            tags:
                - Expected:fail
      ```

    * Python Script [`randomvalue.py`](precise64/etc/dd-agent/checks.d/randomvalue.py):  
      ```python
      import random
      from checks import AgentCheck
      class HelloCheck(AgentCheck):
          def check(self, instance):
              self.gauge('test.support.random', random.random())
      ```
      <!-- ![Random Value Python][Random Value Python]   -->

    * Collected metrics:
      ![Metrics Explorer test.support.random][Metrics Explorer test.support.random]

#### Screenshots: Further use of Agent Checks
  * To make the graphs more interesting in the MySQL dashboards, I subverted Agent Check to create load on the MySQL database with GenerateDBLoad every 3 minutes:  

    ![MySQL DB with load][MySQL DB with load]  

    * generateDBLoad.py from checks.d directory:  
      ```python  
      import subprocess

      from checks import AgentCheck
      class HelloCheck(AgentCheck):
          def check(self, instance):
          	subprocess.check_output(['mysqlslap', '-u', 'root', '-pChestnut1999', '--auto-generate-sql', '--iterations=10', '--concurrency=100'])
              self.gauge('loadgeneration.mysql.done', 1)
      ```
      <!-- ![Python code for GenerateDBLoad][Python code for  GenerateDBLoad] -->

      Further changes to the code and a new (configurable) version was also written on "precise64" to get a better grip on the yaml file and investigating the functionality for submitting multiple metrics.  However as this is quite outside the scope of the exercise, I have simply included the code and yaml file in the repo:
      * [NewGenerateDBLoad.py](precise64/etc/dd-agent/checks.d/NewGenerateDBLoad.py)
      * [NewGenerateDBLoad.yaml](precise64/etc/dd-agent/checks.d/NewGenerateDBLoad.yaml)






## Visualizing your Data

### Since your database integration is reporting now, ...  
  ... clone your database integration dashboard and add additional database metrics to it as well as your `test.support.random` metric from the custom Agent check.

  The MySQL integration dashboard is a Timeboard (see below) and thus the cloned dashboard is also a Timeboard.


*  Cloned dashboard with a few extra metrics including test.support.random:  

  ![Customised MySQL Timeboard][Customised MySQL Timeboard]

### Bonus question: What is the difference between a timeboard and a screenboard?

  * Management-focused answer:  
    Screenboards are typically used for high-level status information.  These are the dashboards which would normally be shown on large screens in the operations centre.  A screenboard can be made public and shared with people who do not have a DataDog login or even embedded into websites and intranets.    
    Timeboards shows graphs which are all scoped to the same time period to facilitate correlation and are usually used in trouble-shooting issues.  
    Users can create both types of dashboards as well as copying and modifying existing timeboards and screenboards to suit their needs.     

  * Technical answer:
    Users can create both Timeboards and Screenboards as well as copying and modifying existing ones to suit their needs.  
    Screenboards tend to be used to display status information and can be shared with users who cannot log in to DataDog or even integrated into web sites or intranets through an iframe.  Individual items on the screenboard can have different time ranges associated with them.  Screenboards can be templatised so that they can show information based on specific tags or values - e.g. the Docker Screenboard could show just the information relating to containers  with the name "cranky_leavitt".  Often Screenboards will be used to display information across sources - the Random Value screenboard (see below) shows information from the random value generator, MySql, PostgreSql, Docker, hosts and events.  
    Timeboards are used for troubleshooting issues.  They show the same user-configurable time period for all graphs which are placed in a grid.  Users can "zoom in" on a particular time period by selecting that period on a graph and reset the time period by selecting one of the predefined ones from the drop-down.  whenever there is a change to the time period, either through selecting a period, zooming out or selecting a period from the drop-down, all graphs in the timeboard are updated to show the same period.  
    Timeboards can also show events in graphs and list format.  The events list can be filtered based on tags or other information.  When the user clicks on an event marker in a graph, the event is highlighted is the list of events.  Users can annotate graphs.  Annotations appear in the timeline.  Furthermore, annotations can include notifications which can send the annotation as a notification to another DataDog user, an email address as well as to some collaboration tools such as Slack.  

  * Timeboard showing the correlation between the queries and the CPU usage on the server running MySQL - Note that the period shown can be changed:  

    ![Timeboard showing correlation][Timeboard showing correlation]  

  * Screenboard example combining status and metric displays - Note that there is no option to change the period shown:  

    ![Random Value Screenboard][Random Value Screenboard]


### Take a snapshot of your `test.support.random` graph ...  
  ... and draw a box around a section that shows it going above 0.90. Make sure this snapshot is sent to your email by using the @notification
  * Creating the annotation:  

    ![Annotation Creation][Annotation Creation]  

    **The annotation was not actually sent to the email address** associated with my DataDog account as DataDog does not let you email notifications to yourself.  To ensure I received the email I had to send it to an alternate email address (david.m.judge@gmail.com).  This behaviour is [noted in one of DataDog's blogs.](https://help.datadoghq.com/hc/en-us/articles/203038119-What-do-notifications-do-in-Datadog-)

    ![Emailed Notification 1][Emailed Notification 1]


## Level 3 - Alerting on your Data

Since you've already caught your test metric going above 0.90 once, you don't want to have to continually watch this dashboard to be alerted when it goes above 0.90 again.  So let's make life easier by creating a monitor.

Monitors check for conditions and send notifications.  These notifications can be seen in the events stream and can also be sent by including in the alert a notification using DataDog's @-notification notation to emails or collaboration tools such as Slack.  Monitors have alert and warning thresholds and the message of the notification can be varied depending on whether the notification is for a warning, an alert or a resolution.  Monitors also have the ability to escalate alerts should the alert not be "resolved" within a configurable timeframe.
Contrary to annotations, you can send monitor notifications to yourself.

### Set up a monitor on this metric
  ... that alerts you when it goes above 0.90 at least once during the last 5 minutes
  * Alert definition:  
  Note that the screenshot was taken after the change required for the "bonus" was made.  Before the "bonus" stage, the "Trigger a separate alert for each:" field was left blank.  

    ![Monitor Creation part 1][Monitor Creation part 1]
    ![Monitor Creation part 2][Monitor Creation part 2]  

### Bonus points:  Make it a multi-alert by host
  ... so that you won't have to recreate it if your infrastructure scales up.  

  * Monitor definition as a multi-alert:  

    ![Monitor Creation part 1][Monitor Creation part 1]

  * Email for host precise64:  

    ![Alert on Precise64][Alert on Precise64]  

  * Email for host DellR520.local  

    ![Alert on DellR520][Alert on DellR520]  

  * Note that the alerts are also events:

    ![Alert as an event][Alert as an event]


### Give it a descriptive monitor name and message
  ... (it might be worth it to include the link to your previously created dashboard in the message).  Make sure that the monitor will notify you via email.
  * Descriptive name is "Random Number is exceeding threshold for {{host.name}}"
  * Links to both a timeboard and a screenboard have been included.  
    The screenboard is included just in case the notification is sent to or forwarded to someone who does not have a login to DataDog.  As it is publically shared, no login is necessary.  Note that in some customer environments this may be considered a security issue.

### This monitor should alert you within 15 minutes.
  So when it does, take a screenshot of the email that it sends you.

  I kept the messages simple.  In a environment where DataDog is used in production (or in a POC), I would like to include suggested steps to fix the issue or a link to a KB article.  
  To assist the DataDog user or recipient of the notification in the triaging of issues, the message was configured to include the host name, the value that triggered the alert

  * Screenshot of the alert:  

    ![Emailed Alert on RandomNumber][Emailed Alert on RandomNumber]  


  * The alert subject and body can have **conditional formatting**:  

    ![Different alert and recovery messages][Different alert and recovery messages]  

  * Subject and Body formatting required to achieve the above:  

    ![Updated Notification Mail Template][Updated Notification Mail Template]  

  * Changes after taking the above screenshots:
    I changed the body of the alert message to include the value, the comparator and the threshold value so that if these are changed in the future, the message won't have to be updated.  Furthermore, providing the value which triggered the alerts can be useful in triage.  
    The line I changed was the one for alerts:
    ```
    {{#is_alert}}The random number generator on host {{host}} at ip {{host.ip}} has had a value of {{value}} which is {{comparator}} {{threshold}}  in the last 5 minutes.{{/is_alert}}
    ```
    After that I also added the value, comparator and threshold for the alert.  

    ```
    The random number generator on host {{host}} at ip {{host.ip}} has had a value of {{value}} which is {{comparator}} {{threshold}}  in the last 5 minutes.
    ```

    The `{{value}}`, `{{comparator}}` and `{{threshold}}` are replaced with actual valuesused by the monitor at the time of evaluation:

    ![Value comparator and threshold][Value comparator and threshold]


### Bonus: Since this monitor is going to alert pretty often, ...
  ... you don't want to be alerted when you are out of the office. Set up a scheduled downtime for this monitor that silences it from 7pm to 9am daily. Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.  

  The Schedule Downtime functionality allows the DataDog user to stop event creation and alerts for certain monitors at defined times.  the Schedules are scoped to tags which makes it trivial to define downtime for specific groups of hosts.  Having the ability to schedule down time so easily and to scope it to only apply if certain tags are present is a great way to define recurring maintenance windows.  


  * The time chosen was from 8PM local time (4PM UTC) until 9AM.  The reason for this variance is that the schedule was created just after 7pm, so I selected the next hour as the start time rather than wait 23 hours.  

    ![Scheduling Monitor Down time][Scheduling Monitor Down time]

  * Email received from DataDog:  

    ![Scheduled Down Time email][Scheduled Down Time email]







<!---
## Timings
* 2017-06-05 Installed Vagrant, VirtualBox (disabled Hyper-V); ran first vagrant up to create "precise64"
* 2017-06-06 Installed the Ubuntu agent on precise64
* 2017-06-06 10:53 Resolving issue with VM not appearing in virtualbox (vagrant up must be run as same user as virtualbox)
* 2017-06-06 11:36 - Now working:
  ![Vagrant up output][Initial Vagrant up]
  ![VM Just created in VirtualBox][VM Just Created in VBox]
  ![New VM screengrab][VM Just built]
* 2017-06-06 11:40 Installing curl and then the DataDog agent
  ![Installing the agent Command][Agent Install Command]
  ![Installing the agent part 1][Agent Install Part 1]
  ![Installing the agent part 2][Agent Install Part 2]
* 2017-06-06 11:50 Success - Host is now in DataDog's dashboard
  ![Initial host entry in DataDog infrastructure dashboard][Initial Host in DataDog]

-->











[VM Just Created in VBox]: images/VirtualBox_Vagrant_VM_created.png "Initial VM created in VirtualBox"
[VM Just built]: images/VM_Just_Built.png "ScreenGrab of VM showing host name and IP configuration"
[Initial Vagrant up]: images/Initial_Vagrant_up_command_output.png
[vagrant ssh]: images/Vargant_ssh.png
[Agent Install command]: images/Agent_Installation_Command.png
[Agent install part 1]: images/Installation_of_agent_part_1.png
[Agent install part 2]: images/Installation_of_agent_part_2.png
[Initial Host in DataDog]: images/Initial_Host_in_DataDog_UI.png
[Host with tags]: images/Host_entry_after_tag_creation.png
[All Hosts]: images/All_Hosts.png
[Hosts grouped by tag "machinetype"]: images/Hosts_Grouped_by_MachineType.png
[tags in datadog config file]: images/Tags_in_config_file.png
[Install MySQL Monitoring part 1]: images/Install_MySQL_Monitoring_part_1.png
[Tags in mysql.yaml]: images/Tags_in_mysql.yaml.png
[info showing mysql]: images/info_showing_mysql.png
[Map now shows MySql]: images/Map_now_shows_msql.png
[Annotation Creation]: images/Annotation_Creation.png
[Emailed Notification 1]: images/Emailed_notification.png
[Random Value YAML]: images/randomvalue_yaml.png
[Random Value Python]: images/RandomValue_Python.png
[MySQL DB with load]: images/MySQL_Db_with_load.png
[Metrics Explorer test.support.random]: images/Metrics_Explorer_-_test.support.random.png
[Python code for GenerateDBLoad]: images/GenerateDBLoad_Python.png
[Scheduling Monitor Down time]: images/Scheduling_Monitor_Downtime.png
[Emailed Alert on RandomNumber]: images/Email_alert_Random_Number_over_threshold.png
[Scheduled Down Time email]: images/Scheduled_Downtime_Starting_email.png
[Alert as an event]: images/Alert_as_an_event.png
[Monitor Creation part 1]: images/Monitor_Creation_part_1.png
[Monitor Creation part 2]: images/Monitor_Creation_part_2.png
[Alert on Precise64]: images/Datadog_Alerting_on_Precise64.png
[Alert on DellR520]: images/Alert_on_DellR520.png
[Tag filter timeboard]: images/Tags_to_filter_events_and_correlate_in_timeboard.png
[PostgreSQL from infrastructure map]: images/PostgreSQL_installed_on_R520.png
[Customised MySQL Timeboard]: images/Customised_MySQL_Dashboard.png
[Different alert and recovery messages]: images/Alert_and_Recovery_Messages.png
[Updated Notification Mail Template]: images/Updated_notification_template.png
[Timeboard showing correlation]: images/Timeboard_showing_correlation.png
[Random Value Screenboard]: images/Random_Value_Screenboard.png
[Alert and Recovery Messages after change]: images/Alert_and_Recovery_Messages.png
[Value comparator and threshold]: images/Value_comparator_and_threshold_in_event.png
