## PREREQUISITES/SETUP:

I spun a fresh linux VM via vagrant (so I would be using Ubuntu 16.04) using its set up [documentation](https://www.vagrantup.com/intro/getting-started/index.html):

![vagrant installation](./Prereqs/vagrant-setup.png?raw=true "Vagrant Setup")

Then, completed my sign up for Datadog, installed the agent on Ubuntu, and set up the config file via the instructions provided on the integrations page:

![datadog agent installation](./Prereqs/ubuntu-datadog-install.png?raw=true "Datadog Agent Setup")

## COLLECTING METRICS:

### Adding Tags:

I added some tags to the Agent [config file](./scripts/datadog.yaml) located at `/etc/datadog-agent/datadog.yaml`:

      tags: sondhayni, key-test:key-value, sondhayni-ubuntu-test


It took a couple of restarts, but eventually the tags appeared on the Host Map page in Datadog as well:

![datadog hostmap with tags](./Collecting-Metrics/ubuntu-hostmap-tags.png?raw=true "Datadog Hostmap Tags")

### Installing MySQL:

I chose to use MySQL. I installed it on to my VM following [these instructions](https://support.rackspace.com/how-to/installing-mysql-server-on-ubuntu/).

Following the [datadog docs](https://docs.datadoghq.com/integrations/mysql/#prepare-mysql), upon installing MySQL, I created a `datadog@localhost` user and granted it the appropriate permissions:

![create datadog user](./Collecting-Metrics/ubuntu-create-datadog-user.png?raw=true "Create Datadog User")


I then set up a MySQL [config file](./scripts/mysql.yaml) at `/etc/datadog-agent/conf.d/mysql.yaml`:

      init_config:

        instances:
          - server: localhost
            user: datadog
            pass: passdd
            tags:
              - smurmu-ubuntu-tag-1
              - smurmu-ubuntu-tag-2
          options:
            replication: 0
            galera_cluster: 1
            extra_status_metrics: true
            extra_performance_metrics: true


I ensured that MySQL was integrated/installed correctly by running a `sudo datadog-agent status` which showed:

![mysql agent check](./Collecting-Metrics/ubuntu-mysql-passes-checks.png?raw=true "MySQL Datadog Integration Successful")

### Custom Metric/Agent Check:

I consulted the datadog docs about the options for [custom metrics](https://docs.datadoghq.com/developers/metrics/) as well as the example provided in the docs for [custom agent checks](https://docs.datadoghq.com/developers/agent_checks/). Following the example, I created two files for `my_metric`.

[my_metric_check.py](./scripts/my_metric_check.py) (in  `/etc/datadog-agent/checks.d/`):

    from checks import AgentCheck

    import random

    class RandVal(AgentCheck):
      def check(self, instance):
        self.gauge('my_metric', random.randint(0,1001))


[my_metric_check.yaml](./scripts/my_metric_check.yaml) (in `/etc/datadog-agent/conf.d`).

    init_config:

    instances:
     [{}]

To ensure it was running properly, I first ran a `sudo datadog-agent status` check:

![my_metric terminal](./Collecting-Metrics/ubuntu-my-metric-check.png?raw=true "my_metric terminal check")

Then, I looked at the timeseries graph in my Metrics Explorer:

![my_metric timeseries](./Collecting-Metrics/datadog-my-metric.png?raw=true "Datadog Metrics Explorer")

*[The long line in the center is from the downtime of when my laptop was off, so metrics weren't being collected.]*

#### Changing Collection Intervals

In order to modify the collection interval, I simply modifed `my_metric_check.yaml` to account for a 45 second interval:

      init_config:

      instances:
       -  min_collection_interval: 45

On Datadog, the timeseries now looked like this:

![my_metric 45s collection interval](./Collecting-Metrics/datadog-my-metric-45.png?raw=true "Datadog my_metric 45s timeseries")

#### Bonus Question: *Can you change the collection interval without modifying the Python check file you created?*

Yes. Setting the collection interval in the first place did not require any changes to the Python check file; changing the interval would require updating the `min_collection_interval` value found in the related config file.
