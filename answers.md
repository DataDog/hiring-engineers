# Datadog Hiring Challenge - Solutions Engineer

**Table of contents:**
* Preface
* Solution: Prerequisites - Setup the environment
* Solution: Collecting Metrics
* Solution: Visualizing Data
* Solution: Monitoring Data
* Solution: Collecting APM Data
* Solution: Final Question

## Preface

The preface comes here...

## Prerequisites and Environment Setup

**Note:** The default username and password for vagrant machines is vagrant and vagrant respectively. For enhanced security it is advised to use an SSH key as password instead.

Once your Ubuntu image has been downloaded you'll find a 'Vagrantfile' in the folder.

![Prerequisites_Host-is-reporting-data-to-Datadog](./img/Prerequisites/Prerequisites_Host-is-reporting-data-to-Datadog.png)

## Solution: Collecting Metrics

### Adding tags to your Host in Datadog

Learn more about tags in the Datadog Docs: [Getting started with tagging](https://docs.datadoghq.com/getting_started/tagging/).

#### Solution:

**1)** List all files in your `datadog-agent` directory:

```
ls -la /etc/datadog-agent
```

Youl'll notice that you have a file here called `datadog_example.yaml`.

**2)** Make a copy of the Agent configuraton file that we can work in:

```
cp /etc/datadog-agent/datadog_example.yaml/etc/datadog-agent/datadog.yaml
```

**3)** Open the [Agent main configuration file](https://docs.datadoghq.com/agent/guide/agent-configuration-files/?tab=agentv6v7) in Vim:

```
vim /etc/datadog-agent/datadog.yaml
```

**4)** The first thing that you'll notice is that the **API** setting is uncommented but has no value. In order to make your Agent communicate with Datadog, it must know the your API key. An API key is unique to your organization and can be found in your [Datadog API configuration page](https://app.datadoghq.eu/account/settings#api):

![Datadog_API-keys](./img/Collecting%20Metrics/Task1/Task1-API_keys.png)

Paste your API-key and paste it in your datadog.yaml file:

![Task1-Add_API_key_to_yaml](./img/Collecting%20Metrics/Task1/Task1-Add_API_key_to_yaml.png)

**5)** If you chose your Datadog region to be Europe (EU) during signup, you must change the site of the Datadog intake `@param site` as well as the host address of the Datadog intake server `@param dd_url` in your `datadog.yaml` file. This is necessary as your API key is only valid for the region it was generated for:

![Task1-Change-region-to-EU](./img/Collecting%20Metrics/Task1/Task1-Change-region-to-EU.png)

**6)** Finally find the tags section of your config file. Uncomment it and add two new tag. Set an `environment` tag with a value of `dev` and set a `name`-tag with the value `kevins_datadog_demohost`:

![Task1-Agent_configfile_tags](./img/Collecting%20Metrics/Task1/Task1-Agent_configfile_tags.png)

**7)** After you've saved the file the Datadog agent must be restarted. As stated in the [https://docs.datadoghq.com/agent/basic_agent_usage/ubuntu/?tab=agentv6v7](https://docs.datadoghq.com/agent/basic_agent_usage/ubuntu/?tab=agentv6v7), this can be done by typing the following command in you Vangart SSH:

```
sudo service datadog-agent restart
```

**8)** After the Agent has restarted it picked up the new config settings and tagged your host as expected. Open your DD Host Map to validate the changes:

![Task1-Host_has_tags](./img/Collecting%20Metrics/Task1/Task1-Host_has_tags.png)



### Datadog Integration with MySQL

The MySQL check is included in the [Datadog Agent](https://app.datadoghq.eu/account/settings#agent) package. No additional installation is needed on your MySQL server.



First, change to you Vangart SSH terminal window and update the apt package by running:

```
sudo apt update
```

Then install the MySQL package on your Ubuntu machine with the following command:

```
sudo apt install mysql-server
```

Once the installation is completed, the MySQL service will start automatically. To check whether the MySQL server is running, type in the following command:

```
sudo systemctl status mysql
```

![Task2_Chek-whether-MySQL-is-running](./img/Collecting%20Metrics/Task2/Task2_Chek-whether-MySQL-is-running.png)

Now that MySQL is installed and is running on the Agent, we prepare the Database for the Datadog integration as described in the [Datadog Docs](https://docs.datadoghq.com/integrations/mysql/). To interact with your MySQL instance, login as root:

```
sudo mysql
```

Now create a database user for the Datadog Agent:

```
mysql> CREATE USER 'datadog'@'localhost' IDENTIFIED BY '<UNIQUEPASSWORD>';
```

Finish all further steps described in the [https://docs.datadoghq.com/integrations/mysql/](https://docs.datadoghq.com/integrations/mysql/) from Datadog.



Restart the Agent:

```
sudo service datadog-agent restart
```

and inspect the Agent status log:

```
sudo datadog-agent status
```

![Task2_Agent-status-MySQL](./img/Collecting%20Metrics/Task2/Task2_Agent-status-MySQL.png)

The Database is sucessfully installed on our host and the Agent integration was sucessfully. Now it is time to install you first Datadog integration. Select **Integrations** from the Datadog sidebar and type in **MySQL** in the search field. Click on the MySQL integration and install it:

![Task2-MySQL-Integration-installed](/Users/Kevin/Documents/Projekte/Datadog/hiring-engineers/img/Collecting Metrics/Task2/Task2-MySQL-Integration-installed.png)

Now change to your [MySQL - Overview](https://app.datadoghq.eu/dash/integration/9/mysql---overview?from_ts=1592254130144&to_ts=1592257730144&live=true) Dashboard on the Datadog website and watch your first MySQL database metrics coming in:

![Task2_MySQL-Overview-Dashboard](./img/Collecting%20Metrics/Task2/Task2_MySQL-Overview-Dashboard.png)



**Submission links:**

* [Link to my MySQL-Overview Dashboard](https://app.datadoghq.eu/dash/integration/9/mysql---overview?from_ts=1592254130144&to_ts=1592257730144&live=true)



### Custom Agent Check submitting a random value

Next we will go over the process of creating a **Custom Agent Check** that submits a metric named `my_metric` with a random value between `0` and `1000`. Custom checks are well suited to collect metrics from custom applications and are sheduled to run on a fixed interval.

The perform the custom check as described, you can use a fairly simple Python script:

```python
from datadog_checks.checks import AgentCheck
from random import randint

class CheckMetric(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', randint(0,1000))
```

Copy and paste the script to Vim:

```bash
vim /etc/datadog-agent/checks.d/custom_agent_check.py
```

The execution of the script requires a `.yaml` file defining the the collection interval:

```yaml
init_config:

instances:
  - min_collection_interval: 15
```

Copy and paste the script to Vim:

```bash
vim /etc/datadog-agent/conf.d/custom_agent_check.yaml
```

> **Note:** The names of the configuration and check files must match. If your check is called `custom_agent_check.py`, your configuration file *must* be named `custom_agent_check.yaml`.

Restart the Datadog Agent:

```
sudo service datadog-agent restart
```

And watch your Custom Agent Metric report data to from your Host to Datadog:

![Task3_Custom-Agent-Metric-being-reported-to-datadog](./img/Collecting%20Metrics/Task3/Task3_Custom-Agent-Metric-being-reported-to-datadog.png)



**Submission links:**

* [Link to the Metrics Explorer](https://app.datadoghq.eu/metric/explorer?from_ts=1592256469750&to_ts=1592260069750&live=true&page=0&is_auto=false&tile_size=m&exp_agg=avg&exp_row_type=metric&exp_metric=my_metric)

### Changing the check's collection interval

Changing the interval at which the check is performed from the default value of `15` seconds can easily be done via the the check's `.yaml` file. Open the file with vim

```
vim /etc/datadog-agent/conf.d/custom_agent_check.yaml
```

 and change the `min_collection_interval` value from `15` to `45`:

```
init_config:

instances:
  - min_collection_interval: 45
```

**Bonus:** By setting the collection interval value in the associate `.yaml` file, the Python skript must not be touched to parametrize the data collection.  



## Solution: Visualizing Data

## Solution: Monitoring Data

## Solution: Collecting APM Data

## Solution: Final Question
