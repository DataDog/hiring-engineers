## Collecting Metrics 


## Adding tags

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

I followed along the [documentation](https://docs.datadoghq.com/getting_started/tagging/assigning_tags/) I was able to find the datadog.yaml file and make the necessary changes:

- take the comments out the 'tags' section
- change to: 
		tags: project:test,laptop:koshap,role:database

![Custom Tags](https://imgur.com/a/xx5xpqs)


* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

I chose to use PostgreSQL as I was am pretty comfortable with it.  I already have PostgreSQL installed on my machine. 

I used  https://docs.datadoghq.com/integrations/postgres/ to follow to integrate PostgreSQL

1.	Created a read-only Datadog user using the following command line:

```
create user datadog with password '<PASSWORD>';
grant SELECT ON pg_stat_database to datadog;
```

2.	Checked the correct permissions running the following command line:

```
psql -h localhost -U datadog postgres -c \
    "select * from pg_stat_database LIMIT(1);"
    && echo -e "\e[0;32mPostgres connection - OK\e[0m" || \
    || echo -e "\e[0;31mCannot connect to Postgres\e[0m"
And entered our ‘<PASSWORD>’.
```

3.	Then, we edited the conf.d/postgres.yaml file (using this https://github.com/DataDog/integrations-core/blob/master/postgres/conf.yaml.example) and added a few tags to configure the agent and to connect it to our PostgreSQL server. 

```yaml
init_config:

instances:
   -   host: localhost
       port: 5432
       username: datadog
       password: <YOUR_PASSWORD>
       tags:
            - laptop:margot
            - project:postgres
```

4.	We restarted the agent.

```
launchctl stop com.datadoghq.agent
launchctl start com.datadoghq.agent
```

5.	We ran the `datadog-agent status` command line to make sure the PostgreSQL integration has been successfully completed.



![PostgreSQL Integration Validation](https://imgur.com/a/epPq5a3)


* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

Datadog custom agent checks are a way for you to get the Agent to collect metrics from your custom applications or unique systems.

Different types of check can be sent (metric, event, service), however we will here focus on implementing a gauge metric.

To get an Agent check to submit a brand-new metric, I had to create two distinct files: 

* mymetric.yaml that needs to go in `datadog-agent/conf.d`:

```yaml
init_config:

instances:
    [{}]
```

* mymetric.py that has to go in `datadog-agent/checks.d`: 

```python
from random import random
from checks import AgentCheck
class HelloCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', 1000 * random())
```

After that, I restarted the Datadog Agent and executed the `datadog-agent status` command line to make sure the check had successfully been implemented.

![Custom Agent Check Validation](https://imgur.com/a/317okAN)


* Change your check's collection interval so that it only submits the metric once every 45 seconds.


This can be changed by modifying the check’s yaml file: you simply need to add the `min_collection_interval: nb_of_seconds` parameter at the init_config or at the instance level.

To change our check’s collection interval, I therefore slightly modified the `datadog-agent/conf.d/mymetric.yaml` file, and simply added the parameter `min_collection_interval: 45` to the configuration file.

```yaml
init_config:
  min_collection_interval: 45

instances:
    [{}]
```

After that, I restarted again the Datadog agent, and went back to the graph to make sure that the collection interval had, indeed, gone from 15-20 to 45 seconds.

![Change of Collection Interval 47sec](https://imgur.com/a/KDvTJbL)
