<h1>Table of Content</h1>
1. Installing DataDog Agent

2. Collecting Metrics
  
  
 <h2>1. Installing Datadog Agent</h2>
  
Begin by signing up the Datadog website and filling out all required credentials and information.
![screenshot](https://raw.githubusercontent.com/FantasyStarr/hiring-engineers/debdbde804f263ec43926b810dc206986dd7639d/Screenshot%20from%202017-12-05%2021-19-32.png)
   
Reach this screen by clicking the link below.
![screenshot](https://raw.githubusercontent.com/FantasyStarr/hiring-engineers/master/Screenshot%20from%202017-12-05%2021-22-40.png)
 <br>https://app.datadoghq.com/signup/agent
  
Depending on the Operarting system you are using, click on the operating system on the left bar and click on it. In this case since we are using Ubuntu, click on Ubuntu.
  
Press CTRL + ALT + T to pull up the terminal. Copy the key and paste it into the terminal and press enter.
![screenshot](https://raw.githubusercontent.com/FantasyStarr/hiring-engineers/master/Screenshot%20from%202017-12-05%2021-30-01.png)

The installation should be successful if you see the screen below.

![screenshot](https://raw.githubusercontent.com/FantasyStarr/hiring-engineers/master/Screenshot%20from%202017-12-05%2022-20-42.png)

<h2>2. Collecting Metrics</h2>
To show that your machine is currently being monitored, it has to tagged to be shown on the Host Map. 

In your command prompt with in `vagrant ssh`

Type in `sudoedit /etc/dd-agent/datadog.conf`

Press `CRTL + V` until you see the line below.

#tags: country:au, state:nsw, role:database

Remove the "#" and add the tag of your choice, in my case it looks like above.

![screenshot](https://raw.githubusercontent.com/FantasyStarr/hiring-engineers/master/sudoeditagent.PNG)

Press CTRL + X , Press Y then Enter to save the changes.
 
[Go to your Host Map by clicking here](https://app.datadoghq.com/infrastructure/map)

<h2> Configuring Database </h2>

Install my SQL with the commands below

`sudo apt-get update`<br>
`sudo apt-get install mysql-server`<br>
`/usr/bin/mysql_secure_installation`<br>

Access MySQL by using `/usr/bin/mysql -u root -p`

Following the configuration steps in the link below. This will be for MYSQL integation.

https://app.datadoghq.com/account/settings#integrations/mysql 

This didn't work for me, so I followed the steps in the knowledge base.

https://docs.datadoghq.com/integrations/mysql/

![screenshot](https://raw.githubusercontent.com/FantasyStarr/hiring-engineers/master/mysqlsuccess.PNG)
![screenshot](https://raw.githubusercontent.com/FantasyStarr/hiring-engineers/master/mysqlverification.PNG)

<h2>Custom Metrics</h2>
 
 The basic creation of a random number generator being returned as a metric on Datadog dashboard is made by following this link
 
 https://docs.datadoghq.com/guides/agent_checks/
 
Create two files using the commands below<br>

`sudo touch /etc/dd-agent/conf.d/my_metric.yaml`<br>
`sudo touch /etc/dd-agent/checks.d/my_metric.py`

Edit the my_metric.py with the code below
```python
import random
from checks import AgentCheck

class randomCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', random.randint(0,1000))
```
Edit the configuration my_metric.yaml file with the code below
```yaml
init_config:
 min_collection_interval: 45
instances:
    [{}]
```

