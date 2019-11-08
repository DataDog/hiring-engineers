# Introduction

## Agent Install
I have deployed the agent on my Intel Nuc running Ubuntu 18.04. Deployment is done easily by running the following command:

`DD_API_KEY=792aad7f4bd921fba0e91560d2382275 DD_SITE="datadoghq.eu" bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"`

For step-by-step instructions, or other architectures, check out: https://app.datadoghq.eu/account/settings#agent/ubuntu

## Tags
Tags are a convenient way of adding dimensions to metrics. They can be filtered, aggregated and compared in visualizations. Tags are a key:value pair with some restrictions for the key. 

In complex cloud and container deployments, it's a good idea to look at service level in a collection of hosts apposed to looking at a single host due to the dynamic nature.

For more information on tags, take a look at: https://docs.datadoghq.com/tagging/. Using tags in visualisations is described in https://docs.datadoghq.com/tagging/using_tags/?tab=assignment

## Applying tags to Ubuntu
To apply tags to an Ubuntu host, edit /etc/datadog-agent/datadog.yaml. Under **&#64;param tags** you can define your tags.

Here is an example:
```yaml
tags:
  - environment:dev
  - data:dog

```
For a full copy of the yaml, check out agent/datadog.yaml


