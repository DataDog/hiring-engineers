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

1) List all files in your `datadog-agent` directory:

```
ls -la /etc/datadog-agent
```

Youl'll notice that you have a file here called `datadog.yaml.example`.

2) Make a copy of the Agent configuraton file that we can work in:

```
cp /etc/datadog-agent/datadog.yaml.example /etc/datadog-agent/datadog.yaml
```

3) Open the [Agent main configuration file](https://docs.datadoghq.com/agent/guide/agent-configuration-files/?tab=agentv6v7) in Vim:

```
vim /etc/datadog-agent/datadog.yaml
```

4)

Find the tags section and uncomment it and add a new tag. Set the `key` to `name` and its `value` to `kevins_datado_demohost`:


### Task: Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

### Task: Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

### Task: Change your check's collection interval so that it only submits the metric once every 45 seconds.

### Task: Bonus Question Can you change the collection interval without modifying the Python check file you created?

## Solution: Visualizing Data

## Solution: Monitoring Data

## Solution: Collecting APM Data

## Solution: Final Question
