# Answer for Recuiting Challenge
I took the docker-containerized approach to complete the Challenge.  
You can reproduce the environment by docker-compose with a deploy script.  

**```DD_API_KEY="<DatadogAPIKEY>" YOUR_LOCAL_IP="<LOCAL_HOST_IP>" sh deploy_local.sh```  **  

The script launches four containers (web, app, db, and datadog-agent), which work with all the configs mentioned in the answer.  

After launching, access http://localhost to see the app working.   
  ** Containers cannot cooperate when`YOUR_LOCAL_IP` = 127.0.0.1, so it shuold be a private address like 192.168.0.5 or 10.4.167.168.  
  ** Docker host ip for APM is configured as 172.19.0.1. Export `Docker_Default_GW` if needed.  

---
# 1. Collecting Metrics
### Tags in the Agent config file and a screenshot of the Host Map page.
* [x] Agent cofing file: [datadog.yaml](datadog/datadog.yaml)  
```yaml
tags:
  - project:testweb
  - env:dev
```  
* [x]  Screenshots (Host Map)  
  ![Host Map](screenshots/1-hostmap.png)  
  ![Host Map 2](screenshots/1-config.png)

### Datadog Agent integration for postgresql.

* [x] Agent config file: [postgres.d/conf.yaml](datadog/conf.d/postgres.d/conf.yaml)  
```yaml
init_config:

instances:
  - host: ${DB_HOST}
    port: 5432
    username: postgres
    password: Test1Pass
    dbname: testweb
    tags:
      - project:testweb
      - role:db
      - env:dev
```  
* [x] Postgresql integration on the Integration Page  
  ![pSQL Integration](screenshots/1-install-db.png)  
  ![pSQL Integration 2](screenshots/1-postgres-integration.png)


### A custom Agent check with a random value between 0 and 1000.

* [x] Agent check python: [test_check.py](datadog/checks.d/test_check.py)  
```python
__version__ = "1.0.0"

from checks import AgentCheck
import random
class HelloCheck(AgentCheck):
    def check(self, instance):
        some_num = random.randint(0,1001) #Return random integers from low (inclusive) to high (exclusive)
        self.gauge('my_metric', some_num, tags=['test_check'])
```

### Configure Agent check's interval to every 45 seconds.
* [x] Agent check config : [test_check.yaml](datadog/conf.d/test_check.yaml)  
```yaml
init_config:

instances:
  - min_collection_interval: 45
```
* [x] Screenshots  
  ![comment](screenshots/1-install-db.png)  

### Configure the Agent check's interval without modifying the Python check file. (Bonus)
* [x] Agent check config : [test_check.yaml](datadog/conf.d/test_check.yaml)  
```yaml
init_config:

instances:
  - min_collection_interval: 45
```
* [x] Screenshots  
  ![comment](screenshots/1-install-db.png)  

---
# 2. Visualizing Data:
###  To create a Timeboard that contains:
* [x] My custom metric scoped over your host.  
  ```python
  #YOUR CODE HERE
  ```  
  ![comment](screenshots/1-install-db.png)  

* [x] The metric from the Integration on Database with the anomaly function applied.  
  ```python
  #YOUR CODE HERE
  ```  
  ![comment](screenshots/1-install-db.png)  

* [x] My custom metric with the rollup function applied to sum up all the points for the past hour into one bucket  
  ```python
  #YOUR CODE HERE
  ```  
* [x] The whole script to create the Timeboard  
  [create_timeboard,py](datadog/scripts/create_timeboard.py) 

### Dashboard screenshots
* [x] Set the Timeboard's timeframe to the past 5 minutes  
  ![comment](screenshots/1-install-db.png)  

* [x] A snapshot of the graph  that mentions myself.  
  ![comment](screenshots/1-install-db.png)  

* [x] What is the Anomaly graph displaying? (Bonus)  
  ```text
  #YOUR CODE HERE
  ```  

---
# 3. Monitoring Data
### Metric Monitor settings for my custom metric.
* [x] Notify as "Warning" with threshold of 500 over the past 5 minutes  
  ![comment](screenshots/1-install-db.png)  
* [x] Notify as "Alert" with threshold of 800 over the past 5 minutes  
  ![comment](screenshots/1-install-db.png)  
* [x] Notify myself if there is No Data for this query over the past 10m  
  ![comment](screenshots/1-install-db.png)  

### Metric Monitor message for my custom metric.

* [x] Send you an email whenever the monitor triggers.  
  ![comment](screenshots/1-install-db.png)  
  
* [x] Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.  
  ![comment](screenshots/1-install-db.png)  

* [x] The metric value and the host ip in the Alert message.  
  ![metric valu](screenshots/1-install-db.png)  
  ![host ip](screenshots/1-install-db.png)  

* [x] A screenshot of the email notification.  
  ![warning](screenshots/1-install-db.png)  
  ![alert](screenshots/1-install-db.png)  
  ![nodata](screenshots/1-install-db.png)  

###  Two scheduled downtimes for this monitor: (Bonus)
* [x] One that silences it from 7pm to 9am daily on M-F.  
  ![comment](screenshots/1-install-db.png)  
* [x] The other that silences it all day on Sat-Sun.  
  ![comment](screenshots/1-install-db.png)  
* [x] A screenshot of the email notification.   
  ![comment](screenshots/1-install-db.png)  

---
# 4. Collecting APM Data:
### My application settings for APM
```python
#Your code here
```
```python
#Your code here
```
### Fully instrumented application 
  [Application](screenshots/1-install-db.png)  
  [Dockerfile](screenshots/1-install-db.png)  

### Difference between a Service and a Resource (Bonus)
```text

```
### A screenshot of a Dashboard with both APM and Infrastructure Metrics.
* [x] Screenshots  
  ![comment](screenshots/1-install-db.png)  

---
# 5. Final Question:
### Is there anything creative you would use Datadog for?
```python
#Your code here
```
  [comment](screenshots/1-install-db.png)  

---
# Extra. Various Integrations:
I have implemented the following integrations to show my interest for Datadog.  
* [x] AWS  
  ![comment](screenshots/1-install-db.png)  
* [x] Nginx  
  ![comment](screenshots/1-install-db.png)  
* [x] Slack  
  ![comment](screenshots/1-install-db.png)  
* [x] Jira  
  ![comment](screenshots/1-install-db.png)  
* [x] Docker  
  ![comment](screenshots/1-install-db.png)  


Happy when you could vote Yes for me.
