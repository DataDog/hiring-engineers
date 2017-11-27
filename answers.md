This is Long Liu's answer.
# Step 0: Setup an Ubuntu VM.
Setup a virtual machine by utilizing [Vargrant](https://www.vagrantup.com/intro/getting-started/index.html).

# Level 1 - Collecting your Data
## Step 1: Sign up for Datadog, get the Agent reporting metrics from your local machine.
The local machine is a virtual machine in VirtualBox running Ubuntu 12.04 LTS 64-bit. 

Follow the [instruction](https://app.datadoghq.com/account/settings#agent/ubuntu) to install Datadog Agent on local machine.

Once the installation is completed, the status of the Agent can be checked by:
```bash
$sudo \etc\init.d\datadog-agent status
```
The information of the Agent can be checked by:
```bash
$sudo \etc\init.d\datadog-agent info
```

**Definition of Agent**

## Step 2: Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
[Tags](https://docs.datadoghq.com/guides/tagging/) are very useful to group machines and metrics for monitoring. Assigning tags using the Agent configuration file will define the tag for the overall agent.

The configuration file is saved in `/etc/dd-agent`, and the Agent configuration file is named as `datadog.conf`.

To add the tags in the Agent configuration file, we should firstly edit the configuration file:
```bash
$sudo nano \etc\dd-agent\datadog.conf
```
Then find these lines:
```bash
# Set the host's tags (optional)
# tags: mytag, env:prod, role:database
```
Uncomment the second line, and name the tag as `host:long-test`:
```bash
# Set the host's tags (optional)
tags: long-test
```
![Agent tag](./screenshots/agent_tag.png)

Press ctrl + o to save the file, and then exit it by pressing ctrl + x.

Restart the Datadog agent:
```bash
$sudo /etc/init.d/datadog-agent restart
```
The host and its tag on the Host Map page is Datadog is shown here.
![Host_Map](./screenshots/tag_host_map.png)

## Step 3: Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
- Download and install MySQL server:
  ```bash
  $sudo apt-get install mysql-server
  ```
- Test the status of MySQL Server:
  ```bash
  $service mysql status
  ```
  If MySQL Server is running, there will display `mysql start/running, process [PID]`. Otherwise, it can be manually started by: 
  ```bash
  $sudo service mysql start
  ```
- Find the Datadog integration for MySQL from [Integrations](https://app.datadoghq.com/account/settings).
![MySQL](./screenshots/MySQL_integration.png)

- Create a database user for the Datadog Agent by following the [instruction](https://docs.datadoghq.com/integrations/mysql/).

The MySQL metrics can be found from Metric Explorer.
![MySQL_Metrics](./screenshots/MySQL_Metrics.png)

## Step 4: Write a custom Agent check that samples a random value. Call this new metric: test.support.random.
- The custom Agent check will simply sample a random value for the metric `test.support.random`. Therefore, in the configuration file, we do not need to put any information. Hence, we create a configuration file named as `Random.yaml` in the directory `/etc/dd-agent/conf.d`. The content in `Random.yaml` is
```bash
init_config:

instance:
    [{}]
```
- Next, the check file will be created in the directory `/etc/dd-agent/check.d`. The check file must have the same name as the configuration file. Therefore, the check file is named as `Random.py`. According to the [Documents](https://docs.datadoghq.com/guides/agent_checks/), the custom check inherits from the `AgentCheck` class. In addition, we need a random number generator to yield a random value. The code in `Random.py` is
```python
from checks import AgentCheck
from random import random
class HelloCheck(AgentCheck):
  def check(self, instance):
    self.gauge('test.support.random', random())
```

