This is Michael Hawley's submission for a Sales Engineer role. I decided for the sake of originality to make a sudo (hah get it?) tutorial, to help outline the steps I took for this challenge and present it in a way that a potential end user could follow easily.

## Setting Up Your Environment

While you can use any environment really, the recommended option is use a virtual machine, linux-based. To learn a new tool for my own personal experience, I used Vagrant with an Ubuntu OS. It's highly recommended that you're on 16.04 or later to avoid any dependency issues with package management.

Follow the [Vagrant Getting Started](https://www.vagrantup.com/intro/getting-started/index.html) guides to set up the virtual machine. The [Xenial64](https://app.vagrantup.com/ubuntu/boxes/xenial64) box is the used for this guide so instead of `vagrant init hashicorp/precise64`, use `vagrant init ubuntu/xenial64`.

To install the necessary packages, copy [bootstrap.sh](./bootstrap.sh).

In your Vagrantfile, add the line: `config.vm.provision :shell, path: "bootstrap.sh"` to provision the machine with the packages you'll need for this exercise.

Start the machine with `vagrant up --provision`, and access the CLI with `vagrant ssh`.

## Collecting Metrics

### Adding Tags

Within `/etc/datadog-agent/datadog.yaml`, under tags, you can specify what the machine is going to be tagged under for quick access on the Datadog platform. Likewise, multiple machines, like kubernetes clusters, can be grouped together under the same tags if they are running similar processes or working for the same service.

```
tags:
    - dd-tag:se-tag
    - env:sandbox
    - role:database
```

Start the Datadog agent with `sudo datadog-agent service start` and view the [tagged machine](./tags.png), in the hostmap.

Learn more about tagging [here](https://docs.datadoghq.com/tagging/)!

### Creating an Agent Check

In the `/etc/datadog-agent` directory are two folders `checks.d` and `conf.d`.

The `checks.d` folder is for creating a custom metric to be sent from the Datadog Agent to the platform. Addition information on the Agent library can be found [here](https://docs.datadoghq.com/developers/agent_checks/?tab=agentv6).

Let's create a random metric! Add the following Python script to `checks.d`:

```
from checks import AgentCheck
import random

class RandomValCheck(AgentCheck):
    def check(self, instance):
        self.gauge('random_val', random.randrange(1, 1000))
```

In `conf.d`, we set the properties of our Agent Check, like the collection interval, through a YAML file, instead of modifying the Python script directly.

```
init_config:

instances:
    - min_collection_interval: 45
```

Next we'll see how it looks in Datadog!

### Visualizing Data

With Datadog's public API we can send our custom metric, collected based on the interval, to the platform for data visualization.
