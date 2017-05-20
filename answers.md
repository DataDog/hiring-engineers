Your answers to the questions go here.

**Level 0 (optional) - Setup an Ubuntu VM**

* While it is not required, we recommend that you spin up a fresh linux VM via Vagrant or other tools so that you don't run into any OS or dependency issues. Here are instructions for setting up a Vagrant Ubuntu 12.04 VM.

[Bruce] - Please see the two screenshots below showing the "vagrant status", along with the Ubuntu VM running within Virtual Box:

![Preview](https://github.com/brucepenn/hiring-engineers/blob/solutions-engineer/Vagrant%20Status.png)

![Preview](https://github.com/brucepenn/hiring-engineers/blob/solutions-engineer/Virtual%20Box%20Showing%20VM%20Running%20.png)

**Level 1 - Collecting your Data**

* Bonus question: In your own words, what is the Agent?

[Bruce] - The agent is a python process that runs on a given host and monitors resources, applications, etc... on that host by executing a series of "checks".  The agent then sends the collected information from these checks to the Datadog Cloud to in order to monitor an  entire infrastucture with an emphasis on meeting performance SLAs.

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

[Bruce] - Please see the screenshot below showing my Ubuntu host and its tags on the Host Map page:

![Preview](https://github.com/brucepenn/hiring-engineers/blob/solutions-engineer/My%20host%20and%20its%20tags%20on%20the%20Host%20Map.png)

* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

[Bruce] - Please see a screenshot from Dashboard List showing the MySQL - Overview Dashboard being listed, along with a screenshot showing that the MySQL tag has now been added to the Host Map page and the mysql.yaml config file used to make this happen:

![Preview](https://github.com/brucepenn/hiring-engineers/blob/solutions-engineer/Dashboard%20List.png)

![Preview](https://github.com/brucepenn/hiring-engineers/blob/solutions-engineer/My%20host%20and%20its%20tags%20on%20the%20Host%20Map%20with%20MySQL.png)

**mysql.yaml**

```
init_config:

instances:
  - server: localhost
    user: datadog
    pass: vagrant
    port: 3306             # Optional
    # sock: /path/to/sock    # Connect via Unix Socket
    # defaults_file: my.cnf  # Alternate configuration mechanism
    # connect_timeout: None  # Optional integer seconds
    tags:                  # Optional
      - mysql:bruce_db
    options:               # Optional
      replication: false
      replication_non_blocking_status: false  # grab slave count in non-blocking manner (req. performance_schema)
      galera_cluster: false
      extra_status_metrics: true
      extra_innodb_metrics: true
      extra_performance_metrics: true
      schema_size_metrics: false
      disable_innodb_metrics: false
    #
    #     NOTE: disable_innodb_metrics should only be used by users with older (unsupported) versions of
    #           MySQL who do not run/have innodb engine support and may experiment issue otherwise.
    #           Should this flag be enabled you will only receive a small subset of metrics.
    #
    #     NOTE: extra_performance_metrics will only be reported if `performance_schema` is enabled
    #           in the MySQL instance and if the version for that instance is >= 5.6.0
    #
    #           extra_performance_metrics and schema_size_metrics will run two heavier queries
    #           against your DB to compute the relevant metrics for all your existing schemas.
    #           Due to the nature of these calls, if you have a high number of tables and/or schemas,
    #           you may be subject to some negative impact in the performance of your DB.
    #           Please bear that in mind when enabling them.
    #           Metrics provided by the options:
    #                     - mysql.info.schema.size (per schame)
    #                     - mysql.performance.query_run_time.avg (per schema)
    #                     - mysql.performance.digest_95th_percentile.avg_us
    #
    #           With the addition of new metrics to the MySQL catalog starting with agent >=5.7.0, because
    #           we query additional schemas to get this full set of metrics. Some of these require the user
    #           defined for the instance to have PROCESS and SELECT privileges. Please take a look at the
    #           MySQL integration tile in the Datadog WebUI for further instructions.
    #
    # ssl:               # Optional
    #   key: /path/to/my/key.file
    #   cert: /path/to/my/cert.file
    #   ca: /path/to/my/ca.file

    # queries:               # Optional
    #  - # Sample Custom metric
    #    query: SELECT TIMESTAMPDIFF(second,MAX(create_time),NOW()) as last_accessed FROM requests
    #    metric: app.seconds_since_last_request
    #    tags:               # Optional - only applied to this custom metric query, will not affect default mysql metrics
    #        - custom_tag1
    #        - custom_tag2
    #    type: gauge
    #    field: last_accessed
    #  - # Sample Custom metric
    #    query: SELECT TIMESTAMPDIFF(second,MAX(create_time),NOW()) as last_user FROM users
    #    metric: app.seconds_since_new_user
    #    tags:               # Optional - only applied to this custom metric query, will not affect default mysql metrics
    #        - custom_tag1
    #        - custom_tag2
    #    type: gauge
    #    field: last_user
```

* Write a custom Agent check that samples a random value. Call this new metric: test.support.random.

[Bruce] - Please see the check and config files that were used to create a new metric called test.support.random to sample a random value, along with a screenshot of test.support.random listed on the Metrics > Summary page:

**random.py**

```
import random

from checks import AgentCheck
class RandomCheck(AgentCheck):
    def check(self, instance):
        self.gauge('test.support.random', random.random())
```

**random.yaml**

```
init_config:

instances:
    [{}]

```

![Preview](https://github.com/brucepenn/hiring-engineers/blob/solutions-engineer/test.support.random%20metric.png)

**Level 2 - Visualizing your Data**

* Since your database integration is reporting now, clone your database integration dashboard and add additional database metrics to it as well as your test.support.random metric from the custom Agent check.

[Bruce] - Please see a screenshot of the cloned MySQL - Overview dashboard which includes a times series graph of the test.support.random metric along with the average mysql innodb buffer pool:

![Preview](https://github.com/brucepenn/hiring-engineers/blob/solutions-engineer/My%20Cloned%20MySQL%20Dashboard.png)

* Bonus question: What is the difference between a timeboard and a screenboard?

[Bruce] - With TimeBoards, all widgets/panels on a dashboard are always based on the same moment in time.  ScreenBoards provide a high-level view of a system and are very customizable, and each widget/panel can have different windows of time.

* Take a snapshot of your test.support.random graph and draw a box around a section that shows it going above 0.90. Make sure this snapshot is sent to your email by using the @notification

[Bruce] - Please see a screenshot of the Snapshot below:

![Preview](https://github.com/brucepenn/hiring-engineers/blob/solutions-engineer/Snapshot%20of%20Random%20over%200.9.png)

**Level 3 - Alerting on your Data**

* Set up a monitor on this metric that alerts you when it goes above 0.90 at least once during the last 5 minutes.

[Bruce] - Please see a screenshot of the Monitor for when the test.support.random metric goes above 0.9:

![Preview](https://github.com/brucepenn/hiring-engineers/blob/solutions-engineer/Random%20over%200.9%20Monitor%20.png)

* Bonus points: Make it a multi-alert by host so that you won't have to recreate it if your infrastructure scales up.

[Bruce] - Please see the screenshot below in making it a multi-alert:

![Preview](https://github.com/brucepenn/hiring-engineers/blob/solutions-engineer/Multi-Alert.png)

* Give it a descriptive monitor name and message (it might be worth it to include the link to your previously created dashboard in the message). Make sure that the monitor will notify you via email.
* This monitor should alert you within 15 minutes. So when it does, take a screenshot of the email that it sends you.

[Bruce] - Please see a screenshot of the alert email per the 0.9 monitor below:

![Preview](https://github.com/brucepenn/hiring-engineers/blob/solutions-engineer/Random%20Alert%20%3E%20.9%20Email.png)

* Bonus: Since this monitor is going to alert pretty often, you don't want to be alerted when you are out of the office. Set up a scheduled downtime for this monitor that silences it from 7pm to 9am daily. Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

[Bruce] - Please see a screenshot of the scheduled downtime email below:

![Preview](https://github.com/brucepenn/hiring-engineers/blob/solutions-engineer/Scheduled%20Downtime%20Email.png)





**Screenboard Link:**

Custom Screenboard made public https://p.datadoghq.com/sb/0d90ee21c-af699c6dc9.
