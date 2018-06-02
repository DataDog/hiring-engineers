The below documentation is a guide to my first steps with Datadog and covers a how to of collecting, visualising & monitoring data.

The below is based on an Ubuntu 16.04 local machine.
The pre-requisite is to install the Datadog agent on the local machine to allow reporting to your Datadog account, the install process is documented at [Datadog Docs - Agent](https://docs.datadoghq.com/agent/) to select your platform of choice. 

For the [Ubuntu installation](https://docs.datadoghq.com/agent/basic_agent_usage/ubuntu/) the Datadog Docs provides the single line of code for installation:

` DD_API_KEY=YOUR_API_KEY bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)`

Your API key can either be found at `https://app.datadoghq.com/account/settings#api` or using the "Install an Agent" step of the Datadog GUI "Get Started" wizard.

## Collecting Metrics:
#### 1. Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog

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

#### 2. Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

Datadog provides more than 200 built-in integrations for monitoring across systems, apps & services. 

2.1 To enable an Integration, navigate to `https://app.datadoghq.com/account/settings#integrations` to view the available Integrations and select the one to configure. For example, the MongoDB Integration.

Clicking on an Integration will display an Overview description, Configuration steps & Metrics that are tracked.

2.2 Under the Configuration tab you will find the setup required for the MongoDB Integration. 

First, you need to create a read-only user in MongoDB for the Datadog Agent, these commands are run from the Mongo shell

![mongoDB integration step 1](https://github.com/ali-shaw/hiring-engineers/blob/ali-shaw-se/images/MongoDB_Integration_1.png)

Second, you then edit the Integration config file at `/etc/datadog-agent/conf.d/mongo.d/mongo.yaml`

![mongoDB integration step 2](https://github.com/ali-shaw/hiring-engineers/blob/ali-shaw-se/images/MongoDB_Integration_2.png)

Finally, restart the Datadog agent using `sudo service datadog-agent restart` and run a Check to confirm the Integration was successfully created.

Screenshot 3: Integrations tab - MongoDB succesfully installed

![mongoDB integrations](https://github.com/ali-shaw/hiring-engineers/blob/ali-shaw-se/images/Integrations_tab_MongoDB.png)

Screenshot 4: MongoDB installation created event on Dashboard

![MongoDB on dashboard](https://github.com/ali-shaw/hiring-engineers/blob/ali-shaw-se/images/MongoDB_installed.png)

Screenshot 5: MongoDB integration yaml edited

![MongoDB yaml](https://github.com/ali-shaw/hiring-engineers/blob/ali-shaw-se/images/MongoYAML.png)

#### 3. Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000

Custom Agent checks are a way to collect metrics from custom applications or systems where a Datadog Integration does not already exist. They are run in the main Datadog Agent check run loop which, by default, is set to every 15 seconds.

For more information, follow the guide at [Datadog Docs - Agent Checks](https://docs.datadoghq.com/developers/agent_checks/)

Custom Agent Checks are made up of 2 files:
- A configuration .yaml file that goes in to `/etc/datadog-agent/conf.d`
- A python script .py file that goes in to `/etc/datadog-agent/checks.d`

**Important: the naming convention for both files must match**

3.1 Create the 'mymetric.yaml' configuration file in `/etc/datadog-agent/conf.d` with the simple configuration below. This contains no real information other than the instruction to initialise the configuration and run it for an undefined number of instances:

![mycheck.yaml](https://github.com/ali-shaw/hiring-engineers/blob/ali-shaw-se/images/mycheck_yaml.png)

3.2 Create the 'mymetric.py' python file in `/etc/datadog-agent/checks.d` with the below to execute the code to Import the Random Module in Python, then Import the Datadog AgentCheck to inherit from, then define your check & randomly generate a number between 1 - 1000.

![mycheck.py](https://github.com/ali-shaw/hiring-engineers/blob/ali-shaw-se/images/mycheck_py.png)

3.3 Once both files are created you can restart the Datadog Agent with `sudo service datadog-agent restart` then test your check by running:

`sudo -u dd-agent -- datadog-agent check mymetric` to test it runs without errors.

3.4 The metric can now be visualised in the Datadog portal by navigating to `https://app.datadoghq.com/metric/explorer` and filtering by "my_metric" under "Graph":

![mycheck in GUI](https://github.com/ali-shaw/hiring-engineers/blob/ali-shaw-se/images/mycheck_GUI.png)

*personal note: this part of the challenge was the most complicated for me having not written Python before. I based my code on the Datadog Docs example, then modified based on googling of the Python Random Module however didn't have the code in the correct order to execute in the right steps*

#### 4. Change your check's collection interval so that it only submits the metric once every 45 seconds.

To change the collection interval of a Custom Agent Check, you must edit the .yaml configuration file to include `min_collection_interval` as per below:

![collection interval change](https://github.com/ali-shaw/hiring-engineers/blob/ali-shaw-se/images/mymetric_collectioninterval.png)

**bonus question**: Using the method above, I did not need to edit my Python check file.

## Visualising Data:

## Monitoring Data:

## Collecting APM Data:

## Final Question:

## Personal notes:
1. datadog.yaml requires sudo priviledges to edit


