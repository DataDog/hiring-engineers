The below documentation is a guide to my first steps with Datadog and covers a how to of collecting, visualising & monitoring data.

The below is based on an Ubuntu 16.04 local machine.
The pre-requisite is to install the Datadog agent on the local machine to allow reporting to your Datadog account, the install process is documented at [Datadog Docs - Agent](https://docs.datadoghq.com/agent/) to select your platform of choice. 

For the [Ubuntu installation](https://docs.datadoghq.com/agent/basic_agent_usage/ubuntu/) the Datadog Docs provides the single line of code for installation:

` DD_API_KEY=YOUR_API_KEY bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)`

Your API key can either be found at `https://app.datadoghq.com/account/settings#api` or using the "Install an Agent" step of the Datadog GUI "Get Started" wizard.

## Collecting Metrics:
###### 1. Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog

Tags provide the ability to easier query and correlate machines and metrics in Datadog. These can be configured automatically through Integrations, or manually though the Configuration file/GUI.

1.1 To add tags manually in the Agent config file, you first locate the .yaml config file for your platform [Datadog Docs - agent usage](https://docs.datadoghq.com/agent/basic_agent_usage/)

For Ubuntu, it is located at: `/etc/datadog-agent/datadog.yaml`. 
**Note: datadog.yaml requires sudo privileges to edit**

1.2 Follow [Datadog Docs- Assigning Tags](https://docs.datadoghq.com/getting_started/tagging/assigning_tags) to understand how to assign tags using the configuration files. It is recommended to follow [tagging best practices](https://docs.datadoghq.com/getting_started/tagging/#tags-best-practices)

Edit the datadog.yaml file by uncommenting the "tags" line and add your chosen tag; i.e "localhost:alishaw"

Screenshot 1: editing the datadog.yaml

![datadog.yaml](https://github.com/ali-shaw/hiring-engineers/blob/ali-shaw-se/images/assiging-tag-datadogyaml.png)

1.3 Save your edits to the configuration file and confirm them in the Datadog GUI by selecting your host in `https://app.datadoghq.com/infrastructure/map`

Screenshot 2: Host Map with new tag

![hostmap](https://github.com/ali-shaw/hiring-engineers/blob/ali-shaw-se/images/assigning-tag-HostMap.png)

###### 2. Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then installed the respective Datadog integration for that database.

For this exercise I installed MongoDB on my machine.

I then used the 'Integrations' section of the Datadog GUI to install the MongoDB integration.

Screenshot 1: Integrations tab - MongoDB installed

![mongoDB integrations](https://github.com/ali-shaw/hiring-engineers/blob/ali-shaw-se/images/Integrations_tab_MongoDB.png)

Screenshot 2: MongoDB installation created

![MongoDB on dashboard](https://github.com/ali-shaw/hiring-engineers/blob/ali-shaw-se/images/MongoDB_installed.png)

Screenshot 3: MongoDB integration yaml edited

![MongoDB yaml](https://github.com/ali-shaw/hiring-engineers/blob/ali-shaw-se/images/MongoYAML.png)

###### 3. Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000

To create a custom Agent check I followed the guide at [Datadog Docs - Agent Checks](https://docs.datadoghq.com/developers/agent_checks/)

First - I created my mycheck.yaml in /etc/datadog-agent/conf.d:

![mycheck.yaml](https://github.com/ali-shaw/hiring-engineers/blob/ali-shaw-se/images/mycheck_yaml.png)

Second - I then wrote my mycheck.py in /etc/datadog-agent/checks.d:

![mycheck.py](https://github.com/ali-shaw/hiring-engineers/blob/ali-shaw-se/images/mycheck_py.png)

I then checked my check in the Datadog GUI:

![mycheck in GUI](https://github.com/ali-shaw/hiring-engineers/blob/ali-shaw-se/images/mycheck_in_gui.png)

*personal note: the challenging part for me here was understanding how to write the mycheck.py having not written Python before. I based my code on the Datadog Docs example, then modified based on googling of random number generators*

###### 4. Change your check's collection interval so that it only submits the metric once every 45 seconds.



## Visualising Data:

## Monitoring Data:

## Collecting APM Data:

## Final Question:

## Personal notes:
1. datadog.yaml requires sudo priviledges to edit


