# Answer for Recuiting Challenge
I took the docker-containerized approach to complete the Challenge.  
You can reproduce the environment by docker-compose with a deploy script.  
```DD_API_KEY="<DatadogAPIKEY>" YOUR_LOCAL_IP="<LOCAL_HOST_IP>" sh deploy_local.sh```  
The script launches four containers (web, app, db, and datadog-agent) in your computer with `YOUR_LOCAL IP`.  
Following is the flow for containers to launch.
```
1. Postgres db starts with datadog user.
2. Datadog agent starts with configured yaml files inside.
3. Django app starts as backend after database migration.
4. Nginx starts http web service as frontend.
```
---
# 1. Collecting Metrics
### Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
* [x] Agent cofing file: [datadog.yaml](datadog/datadog.yaml)  
```yaml
tags:
  - project:testweb
  - env:dev
```  
* [x]  Screenshots (Host Map)  
  ![Host Map](screenshots/1-hostmap.png)  
  ![Host Map 2](screenshots/1-config.png)

---
### Install a database on your machine and then install the Datadog integration for that database.

* [x] Integration file: [conf.d/postgres.d/conf.yaml](datadog/conf.d/postgres.d/conf.yaml)  
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
* [x] PostgresQL Integration  
  ![pSQL Integration](screenshots/1-install-db.png)  
  ![pSQL Integration 2](screenshots/1-postgres-integration.png)
  
### Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

* [x] Agentcheck for process: [checks.d/test_check.py](datadog/checks.d/test_check.py)  
```python
__version__ = "1.0.0"

from checks import AgentCheck
import random
class HelloCheck(AgentCheck):
    def check(self, instance):
        some_num = random.randint(1,1001)
        self.gauge('my_metric', some_num, tags=['test_check'])
```
* [x] Agentcheck for monitoring: [conf.d/test_check.yaml](datadog/conf.d/test_check.yaml)  
```yaml
init_config:

instances:
  - min_collection_interval: 45
```


### Question
* [x] Answer
```python
Your code here
```
* [x] Screenshots
  ![comment](screenshots/1-install-db.png)  

### Question
