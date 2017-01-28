
# Level 0:
- Vagrant Ubuntu 12.04 Created (see Level0/Vagrantfile)
```
    $ vagrant init hashicorp/precise64
    $ vagrant up
    $ vagrant ssh
```

# Level 1:
- Signed up under mike@t******d.com.
- Activated, and installed agent on host as well as added tags for the host to [datadog.conf](./Config/datadog.conf):

    `$ DD_API_KEY=XXXXXXXXXXXXX bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/dd-agent/master/packaging/datadog-agent/source/install_agent.sh)"`
    
      ```
      $ vi /etc/dd-agent/datadog.conf
      ...
      tags: myubuntu, env:demo, role:database
      ...
      ```
- *Bonus*: What is the agent?
    - The agent is a software or service that runs on a host that contains a collector, a stats daemon (statsd) to collect custom metrics (see later for the python code as an example), 
      and a forwarder that will take the data from the collector and statsd and send it to Datadog. 
- Validated host data reporting and tags (see [Level1/HostMap.png](./Level1/HostMap.png))
  ![alt text](./Level1/HostMap.png "Host Map")
- Installed mongoDB:
    `$ sudo apt-get install mongodb`
5. Installed mongoDB agent:
    ```
    $ mongo
    > use admin
    > db.auth("admin", "admin-password")
    > db.addUser("datadog", "xxxxxxxxxx", true)
    bye
    ```
    ```
    $ echo "db.auth('datadog', 'xxxxxxxxxx')" | mongo admin | grep -E "(Authentication failed)|(auth fails)" && echo -e "\033[0;31mdatadog user - Missing\033[0m" || echo -e "\033[0;32mdatadog user - OK\033[0m"
      datadog user - OK
    ```
    Updates for monogoDB agent configuration in [mongo.yaml](./Config/mongo.yaml):
    ```
    $ vi /etc/dd-agent/conf.d/mongo.yaml
        init_config:

        instances:
        -   server: mongodb://datadog:xxxxxxxxx@localhost:27017
            tags:
              - mytag1
              - mytag2
    ```
    ```
    $ sudo service datadog-agent info
        ====================
        Collector (v 5.10.1)
        ====================

          Status date: 2017-01-28 14:29:39 (12s ago)
          Pid: 912
          Platform: Linux-3.2.0-23-generic-x86_64-with-Ubuntu-12.04-precise
          Python Version: 2.7.12, 64bit
          Logs: <stderr>, /var/log/datadog/collector.log, syslog:/dev/log

          ...

          Checks
          ======

            ntp
            ---
              - Collected 0 metrics, 0 events & 0 service checks

            disk
            ----
              - instance #0 [OK]
              - Collected 40 metrics, 0 events & 0 service checks

            mongo
            -----
              - instance #0 [OK]
              - Collected 75 metrics, 0 events & 1 service check
              - Dependencies:
                  - pymongo: 3.2

            ...
  ```
- Checked MongoDB Dashboard at [https://app.datadoghq.com/screen/integration/mongodb?tpl_var_scope=host%3Aprecise64](https://app.datadoghq.com/screen/integration/mongodb?tpl_var_scope=host%3Aprecise64)  to verify proper data coming in. (see [Level1/MongoDB-Dashboard.png](./Level1/MongoDB-Dashboard.png))
  ![alt text](./Level1/MongoDB-Dashboard.png "MongoDB Dashboard")
- Installed DataDog python library: 
    ```
    $ pip install datadog
    ```
- Created randomCheck.py (see [Level1/randomCheck.py](./Level1/randomCheck.py)) to run on a minute-by-minute basis with crontab as follows:
  ```
    $ crontab -e
      * * * * * sh /root/runRandon.sh > /tmp/randomlog 2>&1
  ```
- Validated random variable reporting on hostmap (see [Level1/TestSupportRandomMetric.png](./Level1/TestSupportRandomMetric.png))
  ![alt text](./Level1/TestSupportRandomMetric.png "test.support.random Metrics Screen")

# Level 2: 
- Cloned MongoDB Dashboard to Custom MongoDB Dashboard at [https://app.datadoghq.com/screen/151875/custom-mongodb](https://app.datadoghq.com/screen/151875/custom-mongodb) and added test.support.random to the view along with other metrics. (see [Level2/Custom-MongoDB-Dashboard.png](./Level2/Custom-MongoDB-Dashboard.png))
  ![alt text](./Level2/Custom-MongoDB-Dashboard.png "Custom Mongo Dashboard with Random Metric")
- *Bonus*: What is the difference between a timeboard and a screenboard?
    A timeboard is scoped to the same time across all reporting (ie. 1hr, 4hrs, 1d, etc) and all graphs are presented in a grid.
    A screenboard is more flexible and allows multiple graphs across different timelines and are far more customizable.
- Snapshot of test.support.random was created using the Metrics tab and sent to e-mail. Oddly, sending something to yourself didn't seem to really work (probably because you're sending to yourself!) so I created a second user to tag and send an e-mail to. (see [Level2/MetricSnapshot.png](./Level2/MetricSnapshot.png) and [Level2/MetricNotification.pdf](./Level2/MetricNotification.pdf))
  ![alt text](./Level2/MetricSnapshot.png "test.support.random Metrics Snapshot")


# Level 3: 
- Set up a monitor that alerts when test.support.random goes above 0.90 at least once during the last 5 minutes. (see [Level3/MonitorAlertSettings.png](./Level3/MonitorAlertSettings.png))
  ![alt text](./Level3/MonitorAlertSettings.png "Random Metric Monitor Alert Settings")
- *Bonus*: Multi-alert (see [Level3/MonitorAlertSettings-MultiAlert.png](./Level3/MonitorAlertSettings-MultiAlert.png))
  ![alt text](./Level3/MonitorAlertSettings-MultiAlert.png "Random Metric Monitor Alert Settings with Multi-Alert")
- Received e-mail from alert. (see [Level3/MonitorAlertEmail.pdf](Level3/MonitorAlertEmail.pdf))
- *Bonus*: Set downtime from 7PM-9AM daily and notified users. (see [Level3/DowntimeConfiguration.png](./Level3/DowntimeConfiguration.png) and [Level3/DowntimeNotification.pdf](./Level3/DowntimeNotification.pdf))
  ![alt text](./Level3/DowntimeConfiguration.png "Downtime Configuration Screen")
