## Answers for datadog Solution engineer

# Setup the environment 

I create a  **Ubuntu/xenial** virtual machine  on **VirtualBox** using **Vagrant**  and I used datadog agent V6.

## Installing the agent

To install the agent on a ubuntu machine I run the fellowing command to download and run the installation script :

```bash
DD_API_KEY=<my_api_Key> bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```

# Collecting Metrics

 - **Adding custom tag :**

 Edit the file /etc/datadog-agent/datadog.yaml :

``` /etc/datadog-agent/datadog.yaml
 tags:
 - mytag:myubuntu-agent-onmac
  ```

  ![enter image description here](\screenshots\Screen+Shot+2018-08-08+at+15.24.53.png)

- **install MYSQL**

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
- **configure datadog Agent integration**

[More information about Mysql integration](https://docs.datadoghq.com/integrations/mysql/)

Create database user for the Datadog Agent :

```bash
sudo mysql -e "CREATE USER 'datadog'@'localhost' IDENTIFIED BY '<datadog-dbuser-passowrd>';"

sudo mysql -e "GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'localhost' WITH MAX_USER_CONNECTIONS 5;"

sudo mysql -e "GRANT PROCESS ON *.* TO 'datadog'@'localhost';"

sudo mysql -e "GRANT SELECT ON performance_schema.* TO 'datadog'@'localhost';"
```

Check that datadog user have granted privileges:

```bash
mysql -u datadog --password='<datadog-dbuser-passowrd>' -e "SELECT * FROM performance_schema.threads" && \
echo -e "\033[0;32mMySQL SELECT grant - OK\033[0m" || \
echo -e "\033[0;31mMissing SELECT grant\033[0m" 

mysql -u datadog --password='<datadog-dbuser-passowrd>' -e "SELECT * FROM INFORMATION_SCHEMA.PROCESSLIST" && \
echo -e "\033[0;32mMySQL PROCESS grant - OK\033[0m" || \
echo -e "\033[0;31mMissing PROCESS grant\033[0m"
```

Configure the Agent to connect to MySQL, Create or edit the /etc/datadog-agent/conf.d/mysql.yaml file  :

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

Then restart the Agent

```bash
sudo systemctl restart datadog-agent
```

![enter image description here](/screenshots/Screen+Shot+2018-08-08+at+17.36.57.png)

 - **Create a custom Agent check**

<aside class="notice">
 The file name should match the name of the check module `mycheck.py` and `mycheck.yaml` 
</aside>

To create a custom Agent it's simple just create the python checker `/etc/datadog-agent/checks.d/mycheck.py` file:


```python
import random
from checks import AgentCheck
class HelloCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', random.randint(0,1000))
```

This checker will send random integers between 0 and 1000.

Then the checker config file `/etc/datadog-agent/conf.d/mycheck.yaml` to send my_metric as often as every 45 seconds :

```yaml
init_config:

instances:
   -  min_collection_interval: 45
```

Then restart the Agent.

```bash
sudo service datadog-agent restart
```
![](/screenshots/my_metric.png)

**Bonus**:  yes I can change the collection interval without modifying the Python check file just with adding `min_collection_interval: ` in config file.

# Visualizing Data

* To create a Timeboard using datadog api, 
First of all I started by creating the api and app keys:

![enter image description here](/screenshots/secrets.png)

  * And then I installed the Datadog python library by following the instructions on the Datadog python github: https://github.com/DataDog/datadogpy

```
pip install datadog
```

* Secondly I fellowed instructions from datadog api to create the python script below:

[More information about Datadog API](https://docs.datadoghq.com/api/?lang=python#timeboards)

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

* By executing this script the new Timeboard will be created.

![enter image description here](/screenshots/timeboard.png)

* To change the timeframe to the past 5 minutes I just select this period of time as described below.

![enter image description here](/screenshots/5min-timeboard.png)
![enter image description here](/screenshots/5minpng)

* To send a snapshot of mysql anomaly graph to myself I clicked on the camera icon:

![enter image description here](/screenshots/snapshot.png)

*  And then tag my email:

![enter image description here](/screenshots/sendtome.png)

* I received this email from datadog:

![enter image description here](/screenshots/notificationscreen.png)

**Bonus:** The anomaly graph is displaying metric compared by historical behavior, anomaly detection distinguishes between normal and abnormal metric trends. using [Anomaly Detection Algorithms](https://docs.datadoghq.com/monitors/monitor_types/anomaly/#anomaly-detection-algorithms).

# Monitoring Data

* Create a monitor for my_metric it wil push alert if it’s above:

  * Warning threshold of 500

  * Alerting threshold of 800

    over the past 5 minutes.

  * notify you if there is No Data for this query
  
     over the past 10m.


![my_metric monitor](/screenshots/monitor.png)

![enter image description here](/screenshots/notificationtext.png)

- Alert Email:

![](/screenshots/emailalert.png)

- Scheduling weekly downtime:

![enter image description here](/screenshots/weeklydowntime.png)

- Scheduling weekend downtime:

![enter image description here](/screenshots/weekenDowntime.png)

- Email Scheduling downtime :

![enter image description here](/screenshots/emailDowntime.png)

# Collecting APM Data

The APM Agent (also known as Trace Agent) is shipped by default with the Agent 6 in the Linux I will just need to enable it by editing the file `/etc/datadog-agent/datadog.yaml`:

```yaml
apm_config:
  enabled: true
  env: test  #trace tag
```

* Installing datadog trace library:

```bash
pip install ddtrace
```

* Import the ddtrace in my `app.py` file:

```python
from ddtrace import tracer
from ddtrace.contrib.flask import TraceMiddleware
```

* Create the trace object:

```python
traced_app = TraceMiddleware(app, tracer, service="my-flask-app", distributed_tracing=False)
```

* And run the app. 


![enter image description here](/screenshots/FlaskAPM.png)
![enter image description here](/screenshots/Flaskapp.png)
![enter image description here](/screenshots/APMservice.png)

Please find [*here*](https://p.datadoghq.com/sb/28d01a8f1-b886c7228ff271b31955bad27c554ee2) my public Screenboard.

### Final Question

I think that if we can use datadog monitoring in hospitals it will be good idea, to get health measures from sensors and sends alerts to prevent doctors and avoid an illness.