# Datadog Hiring Challenge - Solution Engineer

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

## Solution: Prerequisites Setup the environment

## Solution: Collecting Metrics

### Task: Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

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

### Task: Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

### Task: Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

### Task: Change your check's collection interval so that it only submits the metric once every 45 seconds.

### Task: Bonus Question Can you change the collection interval without modifying the Python check file you created?

## Solution: Visualizing Data

## Solution: Monitoring Data

## Solution: Collecting APM Data

## Solution: Final Question
