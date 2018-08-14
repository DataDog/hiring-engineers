## Answers for datadog Solution engineer

# Setup the environment 

I create virtual machine  **Ubuntu/xenial** on **VirtualBox** using **Vagrant**  an I used datadog agent V6.

## Installing the agent

to install the agent on a ubuntu machine i run :

```bash
DD_API_KEY=<my_api_Key> bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```

# Collecting Metrics:

 

 - ***Adding custom tag***  
 edit the file /etc/datadog-agent/datadog.yaml :

``` /etc/datadog-agent/datadog.yaml
 tags:
 - mytag:myubuntu-agent-onmac
  ```

  ![enter image description here](\screenshots\Screen+Shot+2018-08-08+at+15.24.53.png)
 - ***Install Mysql and configure the agent:***

 install Mysql

```bash
sudo apt-get update 
sudo apt-get install mysql-server 
```

```bash
#firewall rule to allow mysql
sudo ufw allow mysql

#enabel mysql on system start
sudo systemctl enable mysql

```

  - configure datadog agent integration
[More information about Mysql integration](https://docs.datadoghq.com/integrations/mysql/)
create database user for the Datadog Agent :

```bash
sudo mysql -e "CREATE USER 'datadog'@'localhost' IDENTIFIED BY '<datadog-dbuser-passowrd>';"

sudo mysql -e "GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'localhost' WITH MAX_USER_CONNECTIONS 5;"

sudo mysql -e "GRANT PROCESS ON *.* TO 'datadog'@'localhost';"

sudo mysql -e "GRANT SELECT ON performance_schema.* TO 'datadog'@'localhost';"
```

check for the datadog user :

```bash
mysql -u datadog --password='<datadog-dbuser-passowrd>' -e "SELECT * FROM performance_schema.threads" && \
echo -e "\033[0;32mMySQL SELECT grant - OK\033[0m" || \
echo -e "\033[0;31mMissing SELECT grant\033[0m" 

mysql -u datadog --password='<datadog-dbuser-passowrd>' -e "SELECT * FROM INFORMATION_SCHEMA.PROCESSLIST" && \
echo -e "\033[0;32mMySQL PROCESS grant - OK\033[0m" || \
echo -e "\033[0;31mMissing PROCESS grant\033[0m"
```

Create  /etc/datadog-agent/conf.d/mysql.yaml file :

```yaml
init_config:

instances:
    server: localhost
    user: datadog
    pass: <datadog-dbuser-passowrd>
    tags:
        - optional_tag1
        - optional_tag2
    options:
        replication: 0
        galera_cluster: 1
```
Then restart the collector
```bash
sudo systemctl restart datadog-agent
```
![enter image description here](/screenshots/Screen+Shot+2018-08-08+at+17.36.57.png)
 3. ***Create a custom Agent check***
To create a custom agent it's simple just create the python checker `/etc/datadog-agent/checks.d/mycheck.py` :
This checker will send random integers between 0 and 10.
```py
import random
from checks import AgentCheck
class HelloCheck(AgentCheck):
    def check(self, instance):
        self.gauge('custom.metric', random.randint(0,1000))
```

Then and the checker config file to collecte metric as often as every 45 seconds 
 `/etc/datadog-agent/conf.d/mycheck.yaml` :
```
init_config:

instances:
   -  min_collection_interval: 45
```

Then restart the collector

```bash
sudo service datadog-agent restart
```
(/screenshots/)

**Bonus**:  yes I can change the collection interval without modifying the Python check file.
## Visualizing Data:
To create a Timeboard using datadog api, 
First of all I started by creating the api and app keys:
![enter image description here](/screenshots/secrets.png)

And then I installed the Datadog python library by following the instructions on the Datadog python github: https://github.com/DataDog/datadogpy

`pip install datadog`

Secondly I felowed istruction from datadog api to create the python script below:

[More information about datadog api](https://docs.datadoghq.com/api/?lang=python#timeboards)

```python
from datadog import initialize , api

options = {
    'api_key':'<my-api-key>',
    'app_key':'<my-app-key>'
}

initialize(**options)

title = "My Timeboard"
description = "An informative timeboard."
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{host:ubuntu-xenial}"}
        ],
        "viz": "timeseries"
    },
    "title": "mycustom metric"
},{
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:mysql.performance.com_select{*}, 'basic', 1)"}
        ],
        "viz": "timeseries"
    },
    "title": "MYSQL Anomalies"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{*}.rollup(sum, 3600)"}
        ],
        "viz": "timeseries"
    },
    "title": "my custom metric rollup by 1h"
}]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:ubuntu-xenial"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)
```

By executing this script the new Timeboard will be created .
![enter image description here](/screenshots/timeboard.png)

To change the timeframe to the past 5 minutes I just select this period of time as described below
![enter image description here](/screenshots/5min-timeboard.png)
![enter image description here](/screenshots/5min.PNG)

To send a snapshot of mysql anomaly graph to myself I clicked on the camera icon
![enter image description here](/screenshots/snapshot.PNG)
And then tag my email
![enter image description here](/screenshots/sendtome.PNG)
to receive this email from datadog:
![enter image description here](/screenshots/notificationscreen.PNG)

**Bonus:** The anomaly graph is displaying metric compared by historical behavior, anomaly detection distinguishes between normal and abnormal metric trends. using [*Anomaly Detection Algorithms*](https://docs.datadoghq.com/monitors/monitor_types/anomaly/#anomaly-detection-algorithms).

# **Monitoring Data**

