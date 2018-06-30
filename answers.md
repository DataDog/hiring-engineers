# Hiring Challenge

Greetings! Thank you for taking the time to look through my hiring challenge. As recommended, I have spun up a fresh Ubuntu VM via Vagrant and have [signed up](https://www.datadoghq.com) for Datadog. For more information on setting up and using a Vagrant Ubuntu VM, please refer to this [tutorial](https://www.vagrantup.com/intro/getting-started/).

## Collecting Metrics

### Adding tags in the Agent config file

Tags provide Datadog users with a way to query aggregated data from their metrics. Tags can be assigned in various ways, but I recommend using the configuration files. For Ubuntu users, the configuration file for the overall Agent is located at **/etc/datadog-agent** and is named **datadog.yaml**.

To assign tags, we must edit the datadog.yaml file by first finding the section marked *Set the host's tags (optional)* and then we can make our own tag dictionary with a list of tags. For optimal functionality, it is recommended that we use the key:value syntax for our tags. Below, I've modified the configuration file and checked to see if my host was updated on the Host Map page (Note: your host may not update immediately):

```
# Set the host's tags (optional)
tags: name:jonathan, region:westus, env:test
```

![alt text](https://raw.githubusercontent.com/jonathan-paul-deguzman/hiring-engineers/agent_with_tags_from_host_map.png "Agent overview from Host Map")

For more information on assigning tags, please refer to the Datadog documentation on [assigning tags using the configuration files](https://docs.datadoghq.com/getting_started/tagging/assigning_tags/#assigning-tags-using-the-configuration-files).

### Installing the Datadog MySQL integration

Before we continue, let's set up a MySQL database on our local machine and install the respective Datadog integration for that database. For help with setting up a MySQL database on Ubuntu, please refer to this [MySQL guide](https://help.ubuntu.com/lts/serverguide/mysql.html.en) from the Ubuntu documentationi. To install the MySQL Datadog integration, please refer to the Datadog documentation [here](https://docs.datadoghq.com/integrations/mysql/). An additional method (the way I used) is to, while logged in, start from Datadog's home page, click on Integrations, and click on the MySQL option from the list of integrations. Following the instructions, you should have been able to successfully install the MySQL integration.

To check if your installation has been successful, restart your Agent and then run the status command:

```
sudo service datadog-agent restart
sudo datadog-agent status
``` 

You should see a response that contains something similar  the following in its body:

My results of running the above commands:

```
mysql
-----
  Total runs: 1
  Metric samples: 63, Total: 63
  Events: 0, Total: 0
  Service Checks: 1, Total: 1
  Average Execution Time: 77ms
```

### Creating a custom Agent check

Agent checks are a great way to collect metrics from custom applications or unique systems. For more information, be sure to check out Datadog's documentation on [writing an Agent check](https://docs.datadoghq.com/developers/agent_checks/#your-first-check). We can start making our custom Agent check by first creating a Python script that submits *my_metric* and a random value between 0 and 1000. Navigate to **/etc/datadog-agent/checks.d** and create a Python class **metric_check.py** inside that directory.

metric_check.py:

```python
from checks import AgentCheck
from random import randint
class MetricCheck(AgentCheck):
    def check(self, instance):
        """Sends a gauge between 0 and 1000 for my_metric on each call"""
        self.gauge('my_metric', randint(0, 1000))
```

Now navigate to the **/etc/datadog-agent/conf.d**. Here, we must create a configuration file that matches our check. Since we have named our check **metric_check.py**, we'll have to create a configuration file named **metric_check.yaml** inside the current directory.

metric_check.yaml:

```
init config:

instances:
    [{}]
```

It's possible to [change the collection interval](https://docs.datadoghq.com/developers/agent_checks/#configuration) from inside the configuration file by adding **min_collection_interval** at the instance level.

metric_check.yaml

```
init config:

instances:
    - min_collection_interval: 45
````




