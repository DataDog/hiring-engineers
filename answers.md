# Challenge Answers

Below are the answers to the Support Engineer challenge. It was really fun getting to dive in and figure out how everything worked!

## Level 1 - Collecting Data

I setup various VMs while solving this challenge. I did this to get better acquainted with the process of installing and configuring Agents and Integrations,
and also to see how the Dashboard changed when setting up multiple hosts. This presented some interesting problems of its own, which I will explain at the end of this section.

### Bonus Question: What is an Agent?

An Agent is the software that runs on your host that is responsible for both collecting information about your system and
integrations, and sending that information to Datadog where it can be visualized and monitored.

### Adding Tags to Agents

There are two ways to add tags to a host.

First, tags can be added to the agent's `datadog.conf` configuration file. Here is a snippet from my configuration file for my `testbox` host:

```# Set the host's tags
tags: testboxtag, env:answers, role:testing
```

Second, User tags can be added through the Datadog app or API. Agent tags can only be modified on the host itself, while User tags can be added and removed at-will.

Here is a screenshot of my `testbox` host with both Agent and User tags as seen on the Host Map:

![Tags on the Host Map](screenshots/host_tags_host_map.png)

Tags can also be managed on the Infrastructure List by clicking the **Update Host Tags** button. This is useful if you need to update the tags on a host that is down,
and therefore not appearing on the Host Map:

![Tags on the Infrastructure List](screenshots/host_tags_infrastructure_list.png)

### Installing a Database Integration

I installed Postgres on my `testbox` host and installed the Postgres integration using the setup instructions provided in the Integrations section of the Datadog app. Side note:
The "Generate Password" link was really cool.

After restarting my agent, I confirmed the integration was working:

```vagrant@testbox:~$ sudo service datadog-agent info
(...)
    postgres
    --------
      - instance #0 [OK]
      - Collected 2 metrics, 0 events & 2 service checks
```

And moments later, Postgres metrics were being recorded in the app:

![Postgres metrics on the Host Map](screenshots/postgres_host_map.png)

### Writing a Custom Agent Check

I followed the [documentation on setting up an Agent Check](http://docs.datadoghq.com/guides/agent_checks/) to create a custom Agent Check. Admittedly, I was unsure of which method to use
for sending my random value metric, as some of the terminology was foreign to me, but after reading through the [Sending Metrics with DogStatsD](http://docs.datadoghq.com/guides/metrics/) documentation
I decided that `gauge()` was the correct solution. I would later scroll down to the "Your First Check" section and see a custom check already written, but I withheld a slap
to the forehead and was instead thankful for learning something new.

My custom Agent check for sampling a random number is committed to this project along with its configuration file, but because they are small I have copied them here:

`checks.d/random.py`:

```from checks import AgentCheck
import random


class RandomCheck(AgentCheck):
    def check(self, instance):
        self.gauge('test.support.random', random.random())
```

`conf.d/random.yaml`:

```init_config:

instances:
    [{}]
```

After creating the check and related configuration file, I restarted the Agent and similar to the Postgres integration, confirmed that it was working:

```vagrant@testbox:~$ sudo service datadog-agent info
(...)
    random
    ------
      - instance #0 [OK]
      - Collected 1 metric, 0 events & 1 service check
```

Moments later, the random values were correctly being tracked in the app:

!(Custom Agent Check Metrics)[screenshots/random_metrics.png]

### Other Things I Stumbled Across