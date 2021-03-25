## Datadog Exercise

The following write up is designed to convey the exercise concepts to the reader.

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

2. [Install MongoDB on Ubuntu](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/#install-mongodb-community-edition). I followed this documentation to install MongoDB Community Edition using the apt package manager. These are the commands I used for Ubuntu 18.04 version:
```
wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -

echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list

sudo apt-get update
sudo apt-get install -y mongodb-org
```
I used the following command to determine the init system my platform uses: `ps --no-headers -o comm 1` which resulted in systemd and used the appropriate commands to start MongoDB and check its status:
```
sudo systemctl start mongod
sudo systemctl status mongod
```
(This was resulting in an error which I fixed by changing the permission settings on /var/lib/mongodb and /tmp/mongodb-27017.sock to set the owner to mongodb user using the following commands and then started MongoDB up again.)
```
sudo chown -R mongodb:mongodb /var/lib/mongodb
sudo chown mongodb:mongodb /tmp/mongodb-27017.sock
```
Start a mongo shell on the same host machine as the mongod. The following runs on your localhost with default port 27017:
```
mongo
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

To configure a single agent running on the same node to collect all available mongo metrics, edit mongo.d/conf.yaml file located in (/etc/datadog-agent/conf.d/) of your Agent's configuration directory with the following:
```
init_config:
instances:
  hosts:
    - <HOST>:<PORT>
  username: datadog
  password: <UNIQUEPASSWORD>
  database: <DATABASE>
  options:
    authSource: admin
```
Refer to sample mongo.d/conf.yaml.example for all configuration options.
![image](https://user-images.githubusercontent.com/80560551/112413362-4a786f80-8cdd-11eb-9654-6cb5bf0801bd.png)
(Password not shown in image)

Restart the Agent `sudo service datadog-agent restart`.

Infrastructure List allows us to see the mongodb connections have been configured:
![image](https://user-images.githubusercontent.com/80560551/112413244-1ac96780-8cdd-11eb-8983-c07e1882b924.png)

3. Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

Refer to [Writing a Custom Agent Check](https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7) documentation.

Create a python check file in /etc/datadog-agent/checks.d directory. I created custom_my_metric.py:
![image](https://user-images.githubusercontent.com/80560551/112420847-2a4fad00-8ceb-11eb-9de1-1b7fc946df38.png)

Create a config file with the same name as the check file and place in /etc/datadog-agent/conf.d
I created custom_my_metric.yaml:
![image](https://user-images.githubusercontent.com/80560551/112420948-5c610f00-8ceb-11eb-8d95-1f7e8e6b8c32.png)

Here's my_metric in the Metric Explorer:
![image](https://user-images.githubusercontent.com/80560551/112421381-253f2d80-8cec-11eb-9eb9-91344edb4d16.png)

4. Change your check's collection interval so that it only submits the metric once every 45 seconds.

The default collection interval is 15. I edited my metric config file to change the collection interval of my check:
![image](https://user-images.githubusercontent.com/80560551/112422112-992e0580-8ced-11eb-9aa7-f9a721ea37d9.png)

Bonus Question: Can you change the collection interval without modifying the Python check file you created?

Yes, by editing the config file as seen in the screenshot above. Also, it can be changed via the Metrics Explorer on the UI as seen below:
![image](https://user-images.githubusercontent.com/80560551/112422883-d5ae3100-8cee-11eb-8dcb-1030e0feb4e7.png)
