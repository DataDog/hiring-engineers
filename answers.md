# Solutions Engineer Exercise - Shuo Jin


## Setting up the Environment

This exercise was done using a flavor of Ubuntu 18.04 called Linux Mint. I went with VirtualBox instead of Vagrant because I am more familiar with it. 

![](img/1_1.PNG?raw=true)

As I am on Ubuntu, I used this command to install the agent. 
```
DD_API_KEY=API_KEY bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```
This message shows that the installation was successful. 

![](img/1_2.PNG?raw=true)

This can be verified by visiting the DataDog welcome screen.

![](img/1_3.PNG?raw=true)

## Collecting Metrics
### Addings tags
The agent config file was accessed with the command:
```
sudo nano /etc/datadog-agent/datadog.yaml
```

I added two tags which are shown on the website after restarting the agent.

![](img/2_1.PNG?raw=true)

![](img/2_3.PNG?raw=true)

### Installing a database

The database I went with was MySQL using [this resource](https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-18-04) to assist me.

The next step was creating a mysql.yaml file in the /etc/datadog-agent/conf.d folder. Per instructions, here's what that file contained.
```
init_config:

instances:
  - server: localhost
    user: datadog
    pass: password
    tags:
        - optional_tag1
        - optional_tag2
    options:
        replication: 0
        galera_cluster: 1
```

Checking the status with the command:
```
sudo datadog-agent status
```
should show this after a successful integration. 

![](img/2_2.PNG?raw=true)

A similar verification can be found on the Integrations page along with some metrics that have been gathered. 

![](img/2_4.PNG?raw=true)

![](img/2_5.PNG?raw=true)

### Creating a custom agent check
Most of this section was done by referencing this [page](https://docs.datadoghq.com/developers/agent_checks/).

Here's the code used to submit my_metric with the assistance of the random standard library.

![](img/2_6.PNG?raw=true)

For the .yaml file, this was what I used to change the check's collection interval so that I would not need to edit the Python file anymore.

![](img/2_7.PNG?raw=true)

Restart the agent with:
```
sudo service datadog-agent restart
```

Run the check with:
```
sudo -u dd-agent -- datadog-agent check my_check
```

![](img/2_1.PNG?raw=true)

