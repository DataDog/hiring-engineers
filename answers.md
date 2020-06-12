# Datadog Solutions Engineer Exercise

The intent of the exercise is to get familiar with the Datadog Platform. This document outlines the process from initial
 account setup, Agent installation, collecting metrics, visualizing and monitoring data from an array complex systems.


## Prerequisites - Setup the environment

### Read the Documentation
Before learning any new technology or platform, I start by reading through the main documentation to get a general 10k 
foot view of the technology. I found the [Datadog Platform Documentation](https://docs.datadoghq.com/) to be 
absolutely beautiful visually, easy to navigate, clear and concise. 
![datadog_docs](images/datadog_docs.png)

### Video Resources
Prior to this exercise, I utilized the [Datadog YouTube Channel](https://www.youtube.com/user/DatadogHQ) to quickly learn from the
experts/evangelists at Datadog. The [Datadog 101](https://www.youtube.com/playlist?list=PLdh-RwQzDsaOoFo0D8xSEHO0XXOKi1-5J) playlist allowed me to 
understand key concepts of the product in a short amount of time. I suggest adding this as a resource in the main [README](README.md) under the "Other questions" section. 

### Host Instances
For the exercise, I used my MacBook Pro with the following specs:
```
MacBook Pro (15-inch, Late 2016)
2.7 GHz Quad-Core Intel Core i7
16 GB 2133 MHz LPDDR3

macOS Catalina - v10.15.5
```

I also set up a Vagrant Ubuntu 18.04.4 LTS VM running with VirtualBox, to provide additional host metrics. 


### Sign up for a Datadog Account
To sign up for a Datadog account, I navigated to the main [Datadog signup page](https://app.datadoghq.com/signup) with 
my email `jeremy.daggett@gmail.com` and provided the “Datadog Recruiting Candidate” in the “Company” field as requested.


## Installing the Agent
The following links provide the commands and output for the installation of the Agent:
* [macOS Agent Installation](src/macos_agent_install.md)
* [Ubuntu Agent Installation](src/ubuntu_agent_install.md)

 
## Validate Metric Reporting
After installing the Agents on both host systems I ran a quick experiment to ensure metrics were being pushed to Datadog.

To generate load on my system, I played two YouTube videos simultaneously and watched a recorded show on Sling TV.

Additionally, I ran a duplicate finder application called [Gemini](https://macpaw.com/gemini) over my network to compare two
really large directories for duplicate files. The directories contain my various mp3 collections I've gathered over the past 30 years
and contain many duplicates.

This screenshot of the Host Dashbpard shows that metrics from the macOS host `kalachakra.local` are being reported to Datadog:
![metrics](images/macos_metric_reporting.png)

The following links provide access to the Host Dashboard and Host Map:
* [Host Dashboard](https://app.datadoghq.com/dash/host/2591983488?live=4h&page=0)
* [Host Map](https://app.datadoghq.com/infrastructure/map?fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=availability-zone&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=true&palette=green_to_orange&paletteflip=false&node_type=host&host=2591983488)


## Collecting Metrics
* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

  The following tags were to [`datadog.yaml`](src/datadog.yaml) config file:
  ```
  tags:
    - service:coffee-shop
    - service:coffee-shop:lat:37.747613
    - service:coffee-shop:long:-122.432123
    - version:coffee-shop:09121970
  ```

This screenshot shows the tags that were added to the `kalachakra.local` host:
  ![tags](images/tags.png)


* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

  MySQL was already installed on my MacBook Pro, so I followed the Datadog [integration documentation for MySQL](https://app.datadoghq.com/account/settings#integrations/mysql)
  ![mysql_metrics](images/mysql_metrics.png)


* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

The custom Agent check `custom_check.py`
```python
# the following try/except block will make the custom check compatible with any Agent version
import random
try:
    # first, try to import the base class from new versions of the Agent...
    from datadog_checks.base import AgentCheck
except ImportError:
    # ...if the above failed, the check is running in Agent version < 6.6.0
    from checks import AgentCheck

# content of the special variable __version__ will be shown in the Agent status page
__version__ = "1.0.0"

class CustomCheckmuy(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', random.randint(0,1000), tags=['host:kalachakra.local'])
```

I verified the `custom_check` using the `datadog-agent` "check" command:
```commandline
~/.datadog-agent » datadog-agent check custom_check                             jeremy@kalachakra
=== Series ===
{
  "series": [
    {
      "metric": "my_metric",
      "points": [
        [
          1591984345,
          1
        ]
      ],
      "tags": [
        "TAG_KEY:TAG_VALUE"
      ],
      "host": "kalachakra.local",
      "type": "gauge",
      "interval": 0,
      "source_type_name": "System"
    }
  ]
}
=========
Collector
=========

  Running Checks
  ==============

    custom_check (1.0.0)
    --------------------
      Instance ID: custom_check:d884b5186b651429 [OK]
      Configuration Source: file:/opt/datadog-agent/etc/conf.d/custom_check.yaml
      Total Runs: 1
      Metric Samples: Last Run: 1, Total: 1
      Events: Last Run: 0, Total: 0
      Service Checks: Last Run: 0, Total: 0
      Average Execution Time : 0s
      Last Execution Date : 2020-06-12 10:52:25.000000 PDT
      Last Successful Execution Date : 2020-06-12 10:52:25.000000 PDT


Check has run only once, if some metrics are missing you can try again with --check-rate to see any other metric if available.
```

* Change your check's collection interval so that it only submits the metric once every 45 seconds.

I added the `min_configuration_interval` field in the [custom_check.yaml](src/custom_check.yaml) file, as per the
[main documentation](https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7) listed in 
the References section of the main [README.md](README.md).
```
init_config:
 
instances:
  - min_collection_interval: 45
```

* **Bonus Question** Can you change the collection interval without modifying the Python check file you created?

It can be modified directly in the [custom_check.yaml](src/custom_check.yaml) file
Using the Datadog Agent GUI, I modified the interval directly and restarted the agent:
 ![check_gui](images/check_gui.png)
 

## Visualizing Data


## Monitoring Data


## Collecting APM Data


## Final Question
