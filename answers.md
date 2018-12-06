# Hiring Challenge for Data Dog:

## Setting the environment:

Before collecting the metrics, I needed to first set up the environment. To do this, I downloaded two tools, Vagrant and Virtual Box. I first installed Virtual Box as it needed to be opened before installing Vagrant. I went on the documentation on the Vagrant website that showcased the instructions of installing the application. As soon as I had followed  the instructions, I had Vagrant set up along with Precise64, which was a variation of Ubuntu.

## Collecting Metrics:

Once I had set up Ubuntu, I needed to register on the Data Dog website in order to download an agent, which should allow me to collect events and metrics from my Virtual Machine into Data Dog for monitoring and performance data.

In order to add tags, I needed to first follow the directions in setting up the agent by following the instructions labeled in the documentation. Once I've had that set up, and installed the agent on my virtual machine, I was able to get into the configuration files, which allowed me to edit the tags through the text editor vi.

### The location of the tags:

![](tags%20on%20ubuntu.png)


### The results:

![](Tags.png)


Once I have verified that the tags were edited within the agent, I decided to work on setting up the MySQL integration with Datadog. To do this, I needed to first update Ubuntu to the latest version, then run an installer for MySQL server. As soon as MySQL was installed on my machine, I went to the list of integrators on Datadog, which allowed me to select a list of any sort of integrations I wanted to use within my agent. I selected MySQL, and followed the directions to allow me to create a connection between MySQL and my Datadog agent. To verify this, I went back to the Host Map, which shows my results:

![](mysql%20integration.png)

I was also able to verify this by running the command line: sudo datadog-agent status, which returned this:


![](mysql%20check.png)

As soon as I was able to verify that mysql had been integrated within my agent, I finally started to work on collecting my metrics. 

To do this, I needed first understand the documentation for Metrics, which I was able to here: https://docs.datadoghq.com/developers/metrics/

And the documentation needed to write up an agent check:

https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6

Once I was able to understand the different types of metrics, I was able to begin the process. Though I am still not as proficient in Python, I felt it was necessary to write this file using the language rather than writing on Java. 

Here is the script:

```
import random

from datadog_checks.checks import AgentCheck

class CustomCheck(AgentCheck):
    def check(self, instance):
        self.gauge('custom.mycheck', random.randint(0,1000))
```

Submitting a metric once every 45 seconds:

To do this, all you would need to do is changing the configuration file, so entering the conf, which I have named datadog.yaml. In the file, you would need to include the following under instances:

```
instances:
  - min_collection_interval: 45
```

Answer to bonus question: You wouldn't necessarily need to modify the python script that was created since all you would need to do is modify the configuration file.

