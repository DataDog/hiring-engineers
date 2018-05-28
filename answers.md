To carry out this exercise I used a laptop running Ubuntu 16.04.

## Collecting Metrics:
1. Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog

To add tags in the Agent config file I first located the .yaml config file by finding it using [Datadog Docs - agent usage] (https://docs.datadoghq.com/agent/basic_agent_usage/ubuntu/)

I then used [Datadog Docs - tagging] (https://docs.datadoghq.com/getting_started/tagging/assigning_tags/) to understand how to assign tags using the configuration files

I then edited the datadog.yaml file by uncommenting the "tags" line and added the tag "localhost:alishaw"

Screenshot 1: editing the datadog.yaml
![datadog.yaml](https://github.com/ali-shaw/hiring-engineers/blob/ali-shaw-se/images/assiging-tag-datadogyaml.png)

Screenshot 2: Host Map with new tag
![hostmap](https://github.com/ali-shaw/hiring-engineers/blob/ali-shaw-se/images/assigning-tag-HostMap.png)

2. Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then installed the respective Datadog integration for that database.

For this exercise I installed MongoDB on my machine.

I then used the 'Integrations' section of the Datadog GUI to install the MongoDB integration.

Screenshot 1: Integrations tab - MongoDB installed

Screenshot 2: MongoDB installation created

Screenshot 3: MongoDB integration yaml edited

3. Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000

To create a custom Agent check I followed the guide at [Datadog Docs - Agent Checks] (https://docs.datadoghq.com/developers/agent_checks/)

First - I created my mycheck.yaml in /etc/datadog-agent/conf.d - screenshot below:

Second - I then wrote my mycheck.py in /etc/datadog-agent/checks.d - screenshot below

*personal note: the challenging part for me here was understanding how to write the mycheck.py having not written Python before. I based my code on the Datadog Docs example, then modified based on googling of random number generators*

4.

## Visualising Data:

## Monitoring Data:

## Collecting APM Data:

## Final Question:

## Personal notes:
1. datadog.yaml requires sudo priviledges to edit


