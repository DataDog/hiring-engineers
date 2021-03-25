## Datadog Exercise

The following write up is designed to familiarize the reader with [Datadog](http://datadog.com), an end-to-end monitoring and security platform for cloud applications. Topics covered include environment setup, collecting metrics, visualizing data, monitoring data, collecting APM (Application Performance Monitoring) data, and a creative use case. 

## Environment Set Up
To avoid OS or dependency issues, utilize [Vagrant](https://www.vagrantup.com/intro/getting-started/) to spin up a Ubuntu VM. Make sure to use minimum `v. 16.04`. 

1. [Download](https://www.vagrantup.com/downloads) the proper package for your platform and [Install](https://www.vagrantup.com/docs/installation) Vagrant.
![image](https://user-images.githubusercontent.com/80560551/111381353-d39b0100-8662-11eb-895e-3c7e9ef8d5c6.png)

2. Download the appropriate package for [VirtualBox](https://www.virtualbox.org/wiki/Downloads) to use as a hypervisor.
![image](https://user-images.githubusercontent.com/80560551/111381912-94b97b00-8663-11eb-9f14-c23882976751.png)

3. Navigate to your command prompt and enter the following command to initialize Vagrant:
```
vagrant init hashicorp/bionic64
```

4. Start your VM and SSH into it with:
```
vagrant up
vagrant ssh
```
![image](https://user-images.githubusercontent.com/80560551/111412584-e54bcb00-8699-11eb-80bf-255154f4e018.png)

5. Sign up for a Datadog trial at https://www.datadoghq.com/ . After creating a Datadog account, follow [get started with the Datadog agent](https://docs.datadoghq.com/getting_started/agent/) documentation. Select Ubuntu to see installation instructions for your VM and run the one-step install.

Then, get the Agent reporting metrics from your local machine and move on to the next section.

Here's a summary of my Agent's reporting metrics:
![image](https://user-images.githubusercontent.com/80560551/112403345-75f25e80-8ccb-11eb-9d6f-4bab5da88b25.png)


## Collecting Metrics

1. To [add tags](https://docs.datadoghq.com/getting_started/tagging/assigning_tags/?tab=noncontainerizedenvironments#configuration-file) to your host via the agent config file, locate the datadog.yaml file (/etc/datadog-agent/datadog.yaml). I uncommented the tag section and added environment, role and region keys with their values and saved the file with the changes.
![image](https://user-images.githubusercontent.com/80560551/111956489-123c1b80-8aa8-11eb-901d-33b5dae6005b.png)
To view the tags on the [Host Map](https://docs.datadoghq.com/infrastructure/hostmap/#overview) page (found under the Infrastructure tab) in Datadog, restart the Agent running as a service with `sudo service datadog-agent restart` command ([found here](https://docs.datadoghq.com/agent/basic_agent_usage/ubuntu/?tab=agentv6v7)). The Tags section in the following screenshot gets populated with the keys and values defined in the agent config file:
![image](https://user-images.githubusercontent.com/80560551/111961101-d4da8c80-8aad-11eb-9e09-0f516ce64dcf.png)

2. [Install MongoDB on Ubuntu](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/#install-mongodb-community-edition). I followed this documentation to install MongoDB Community Edition using the apt package manager. These are the commands I used:
```
wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list
sudo apt-get update
sudo apt-get install -y mongodb-org
```
  
Install the respective Datadog [integration](https://docs.datadoghq.com/integrations/).
Following the steps listed in [MongoDB](https://docs.datadoghq.com/integrations/mongo/?tab=standalone), I created a read-only user for the Datadog Agent in the admin database:
```
use admin
db.createUser({
  "user": "datadog",
  "pwd": "<UNIQUEPASSWORD>",
  "roles": [
    { role: "read", db: "admin" },
    { role: "clusterMonitor", db: "admin" },
    { role: "read", db: "local" }
  ]
})
```
![image](https://user-images.githubusercontent.com/80560551/111971303-6e5b6b80-8ab9-11eb-8ef3-6d1382f26b9f.png)

Configure mongo.d/conf.yaml file located in (/etc/datadog-agent/conf.d/) of your Agent's configuration directory with the following:
```
init_config:
instances:
  - hosts:
          - <HOST>:<PORT>
    username: datadog
    password: <UNIQUEPASSWORD>
    database: <DATABASE>
    options:
            authSource: admin
```
Refer to sample mongo.d/conf.yaml.example for all configuration options.
![image](https://user-images.githubusercontent.com/80560551/111982217-efb8fb00-8ac5-11eb-8aeb-53db6ebe5d64.png)
(Password not shown in image)

Restart the Agent `sudo service datadog-agent restart`
Metric Collection check has been configured as shown in the Metrics Summary:
![image](https://user-images.githubusercontent.com/80560551/111982886-bcc33700-8ac6-11eb-9fb6-f519df385b47.png)

3. Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

Refer to [Writing a Custom Agent Check](https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7)
