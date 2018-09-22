# Solutions Engineer Exercise - Shuo Jin


## Setting up the Environment

This exercise was done using a flavor of Ubuntu 18.04 called Linux Mint. I went with VirtualBox instead of Vagrant because I am more familiar with it. 

As I am on Ubuntu, I used this command to install the agent. 
```
DD_API_KEY=API_KEY bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```
This message shows that the installation was successful. 

This can be verified by visiting the DataDog welcome screen.

## Collecting Metrics
The agent config file was accessed with the command:
```
sudo nano /etc/datadog-agent/datadog.yaml
```

I added two tags which are shown on the website after restarting the agent. 

The database I went with was MySQL using [this resource](https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-18-04) to assist me.

The next step was creating a mysql.yaml file in the /etc/datadog-agent/conf.d folder. Per instructions, this was what that contained.
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
