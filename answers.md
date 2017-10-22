### Daniel Farrington

## Environment 

I opted to run the Datadog agent on my Windows 10 64-bit home machine, just for the sake of personal simplicity. However, for the last part of the challenge, I decided to run the agent off of the recommended [Vagrant](https://www.vagrantup.com/downloads.html) Ubuntu VM, using [VirtualBox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1).

*Note: Vagrant wouldn't detect my installation of VirtualBox 5.2. I had to install version 5.1.14 instead to complete the Vagrant installation.*

With the Vagrant VM set aside for now, I signed up for a DataDog trial, and installed the [DataDog Agent for Windows](https://s3.amazonaws.com/ddagent-windows-stable/ddagent-cli-latest.msi).

## Collecting Metrics

### Tags

To begin, I was able to add a couple of descriptive tags and change the name of my host by editing the datadog.conf file inside of the very convenient Datadog Agent Manager editor. The changes were as follows:

`hostname: dfarrington.home`

`tags: office:home, os:win10`

And the result:
![alt text](https://imgur.com/oVjl0iY.jpg "Host map with tags")

Duplicate hosts! 

This was slightly worrying, though I was reassured [here](https://docs.datadoghq.com/faq/#i-just-set-up-my-aws-integration-why-am-i-seeing-duplicate-hosts) that the duplicate would disappear within 10-20 minutes. And that it did. 

### PostgreSQL Database Integration

I downloaded and installed [PostgreSQL 10 for x86-64 Windows](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads#windows), and then followed the PostgreSQL integration instructions found [here](https://app.datadoghq.com/account/settings#integrations/postgres). This was very straightforward: I started psql and executed the following command: 

```
create user datadog with password '*****************';
grant SELECT ON pg_stat_database to datadog;
```

The Verification:
```
psql -h localhost -U datadog postgres -c "select * from pg_stat_database LIMIT(1);"  
 && echo -e "\e[0;32mPostgres connection - OK\e[0m" || \ ||  
echo -e "\e[0;31mCannot connect to Postgres\e[0m"
```

Next I had to edit and enable the PostgreSQL.yaml file as such: 

![alt text](https://imgur.com/w44wwP6.jpg "PostgreSQL.yaml config")

Following an agent restart:

![alt text](https://imgur.com/QDHy2Bf.jpg "Status")

A successful integration! All that was left to do was ![alt text](https://i.imgur.com/AFLLG3K.png "Install") the integration on the DataDog website. 

### A Custom Agent Check

A custom agent check is a user-created check made for collecting metrics from applications and systems that DataDog hasn't yet had the opportunity to cover. This grants the user nearly unlimited freedom to collect whatever metrics they need.

In order to create a custom agent check, I had to read through and follow the information given [here](https://docs.datadoghq.com/guides/agent_checks). From that, I learned that I had to create two files with the same name: 

**mycheck.py** *C:\Program Files\Datadog\Datadog Agent\agent\checks.d* 

```python
import random
from checks import AgentCheck

class testCheck(AgentCheck):

	def check(self, instance):
		self.gauge('my_metric', random.uniform(0,1000))
```

This code was built off of the hello.world check provided in references. I imported the random library, which gave me access to the random.uniform() function. This function takes two integer arguments as a range and produces a random integer within that range. Lastly, I changed the name of the metric from *'hello.world'* to *'my_metric'*.

*Note: The checks.d directory wasn't where the [Agent Check reference document](https://docs.datadoghq.com/guides/agent_checks/#directory-structure) led me to believe it would be, though it wasn't at all hard to find.*

**mycheck.yaml** *C:\ProgramData\Datadog\conf.d*

```
init_config:
    min_collection_interval: 45
instances:
    [{}]
```

This is simply the skeleton of the configuration file for the agent check. The line 'min_collection_interval: 45' will be discussed in the next section.

### Modifying the Check Collection Interval

A check's collection interval governs how often the check can run. It is determined by the presence of `min_collection_interval` in the init_config section of the check's .yaml file, as can be seen above. In my example I use a `min_collection_interval` value of 45. This means that the check will not run until at least 45 seconds have passed. 

The Datadog agent inherently checks to see if any metrics are ready to be collected every 15-20 seconds. This cannot be changed, and thus it is not possible to collect a metric at an interval less than 15 seconds.

### Visualizing Data with a Timeboard

In order to visualize the metrics I've collected, I created a new dashboard
