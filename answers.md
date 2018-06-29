# Hiring Challenge

Greetings! Thank you for taking the time to look through my hiring challenge. As recommended, I have spun up a fresh Ubuntu VM via Vagrant and have [signed up](https://www.datadoghq.com) for Datadog. For more information on setting up and using a Vagrant Ubuntu VM, please refer to this [tutorial](https://www.vagrantup.com/intro/getting-started/).

## Collecting Metrics

Tags provide Datadog users with a way to query aggregated data from their metrics. Tags can be assigned in various ways, but I recommend using the configuration files. For Ubuntu users, the configuration file for the overall Agent is located at **/etc/datadog-agent** and is named **datadog.yaml**.

To assign tags, we must edit the datadog.yaml file by first finding the section marked *Set the host's tags (optional)* and then we can make our own tag dictionary with a list of tags. For optimal functionality, it is recommended that we use the key:value syntax for our tags. Below, I've created a few tags:

```
# Set the host's tags (optional)
tags: name:jonathan, region:westus, env:test
```


