# Support Engineer Challenge

## Questions

### Level 0 - Setup an Ubuntu 12.04 LTS VM with Vagrant

Screenshot of `vagrant up` and `vagrant ssh`:  
<img src="figures/Level0_Vagrant_up_ssh.png" alt="Vagrant up with Ubuntu" width="600">

### Level 1  
  
* Sign up for Datadog (use "Datadog Recruiting Candidate" in the "Company" field), get the Agent reporting metrics from your local machine.

Copy the one-step install instructions from Datadog:  

<img src="figures/Level1_install your first Datadog Agent.png" alt="Install Datadog Agent" width="600">
  
Enter the one-step install insructions at the command line to initiate installation:  
  
<img src="figures/Level1_install on ubuntu.png" alt="Begin Installation" width="600">  

* Bonus question: In your own words, what is the Agent?  

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.  

Editing the Agent config file (`/etc/dd-agent/datadog.conf`):  
<img src="figures/Level1_add tags.png" alt="Add tags to Agent Config file" width="600">  

Screenshot of host and its tags on the Host Map page:  
<img src="figures/Level1_Host Map with tags.png" alt="Host Map with tags" width="600">  

* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

Install MySQL and check that it's listening:
<img src="figures/Level1_apt-get update.png" alt="apt-get update" width="600">  
<img src="figures/Level1_apt-get install mysql-server.png" alt="Install MySQL" width="600">  
<img src="figures/Level1_mysql listening.png" alt="MySQL is listening" width="600">  

Follow the MySQL integration instructions from Datadog (https://docs.datadoghq.com/integrations/mysql/) to connect the Agent to MySQL.  
Create a datadog user, grant it replication rights (and other privileges as desired).   , and edit the conf.d/mysql.yaml to connect the Agent to MySQL:  
`sudo mysql -e "CREATE USER 'datadog'@'localhost' IDENTIFIED BY 'YOURUNIQUEPASSWORDHERE';"`  
`suoo mysql -e "GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'localhost' WITH MAX_USER_CONNECTIONS 5;"  
  
Verify that the user was created and was granted replication rights and other privileges, as appropriate:  
<img src="figures/Level1_MySQL integration_verification commands.png" alt="MySQL integration verification" width="600">  
  
And edit `/etc/dd-agent/conf.d/mysql.yaml` to configure the connection and related monitoring options:  
<img src="figures/Level1_MySQL yaml config.png" alt="MySQL yaml configuration" width="600">  
  

Restart the agent (`sudo /etc/init.d/datadog-agent restart`), and then
use the info command (`sudo /etc/init.d/datadog-agent info`) to check that the MySQL integration is OK:  
<img src="figures/Level1_mysql checks.png" alt="MySQL check" width="600">  

* Write a custom Agent check that samples a random value. Call this new metric: `test.support.random`

custom_agent_check.py:
```python
import random

from checks import AgentCheck

class RandomCheck(AgentCheck):
    def check(self, instance):
        self.gauge('test.support.random', random.random())
```

custom_agent_check.yaml
```yaml
init_config:
    min_collection_interval: 1

instances:
    [{}]
```

### Level 2 - Visualizing your Data  
  
* Since your database integration is reporting now, clone your database integration dashboard and add additional database metrics to it as well as your `test.support.random` metric from the custom Agent check.
