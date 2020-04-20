Now that we've set up an agent on our host and added some custom tags, lets add a custom check to monitor it. The basic workflow for doing this is to install the Datadog integration that corresponds to your service.

Let's try this with a database. First step is to find the integration [here](https://docs.datadoghq.com/integrations/#cat-data-store} and follow the instructions to install it. Many of the datastore integrations come with the Agent installation so you might not even need to do anything for the installation step.

I'm using MySQL, which has the check already installed with the agent.

After follwing [the steps for setting up the integration](https://app.datadoghq.com/account/settings#integrations/mysql) on my VM, I get a whole bunch of metrics now available to me:
![mysql metrics](./images/mysql.png)

# Creating a Custom Agent Check

It isn't typically necessary to create a custom agent check and you should reference [the documentation about custom checks](https://docs.datadoghq.com/developers/write_agent_check/) to decide if you should create one. However, I'll make one here just to show you how it works anyway.

First we'll create the configuration file for the check at conf.d/firstcheck.yaml. There isn't much required for this file but, at a minimum, this file needs a sequence called `instances` containing at least one mapping, which can be empty. We'll modify this file later to change the collection interval but for now, you can create the file with one line that looks like this:

`instances: [{}]`

Now for the check itself. For a basic example, I'm going to send a random number between zero and 1000 and call the metric `my_metric`. I'm going to create a python file with the same name as the configuration file I created above: `firstcheck.py`

The contents of my file look like this:

```
import random
  
# the following try/except block will make the custom check compatible with any Agent version
try:
    # first, try to import the base class from new versions of the Agent...
    from datadog_checks.base import AgentCheck
except ImportError:
    # ...if the above failed, the check is running in Agent version < 6.6.0
    from checks import AgentCheck

# content of the special variable __version__ will be shown in the Agent status page
__version__ = "1.0.0"

class FirstCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', random.randint(0,1000), tags=['TAG_KEY:TAG_VALUE'])
```

A few things are worth pointing out in this python file. First, is the class `FirstCheck` which must inherit from the base `AgentCheck` class. Next, you define the check in its own class method called check. Finally, in my case, I've created a check type of "gauge" and named the metric that will be sent `my_metric`. You can also see that I'm sending a random value from 0-1000 as the second argument of the call to `self.gauge` and that you can add tags (just like the ones we added in the last section) dynamically as you create the check.

The last thing to know is that there is a default collection interval check of `30s` and you can change that interval by changing the `firstcheck.yaml` configuration file to contain the following:

```
init_config:

instances:
  - min_collection_interval: 30
```


[Previous: Collecting Metrics](./markdown/collecting_metrics.md)  |  [Next: Datadog APIs](./markdown/api_page.md)
