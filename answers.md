# Answer for Recuiting Challenge
I took the docker-containerized approach to complete the Challenge.  
You can reproduce the environment by docker-compose with a deploy script.  

```DD_API_KEY="<DatadogAPIKEY>" YOUR_LOCAL_IP="<LOCAL_HOST_IP>" sh deploy_local.sh```  

The [deploy_local.sh](deploy_local.sh) launches four containers (web, app, db, and datadog-agent), which work with all the configs mentioned in the answer.  

After launching, access http://localhost to see the app working.   
  ** Containers cannot cooperate if`YOUR_LOCAL_IP` = 127.0.0.1. It should be your real private IP like 192.168.0.5 or 10.4.167.168.  
  ** Docker host ip for APM is configured to 172.17.0.1 as default. Export `DOCK_DEFAULT_GW` if needed.  

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
  ![Host Map](screenshots/1-host-map-1.png)  
  ![Host Map](screenshots/1-host-map-2.png)  

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
* [x] Datadog-agent status
```text
postgres (2.2.2)
----------------
    Instance ID: postgres:de2362ecea868019 [OK]
    Total Runs: 28
    Metric Samples: 29, Total: 377
    Events: 0, Total: 0
    Service Checks: 1, Total: 28
    Average Execution Time : 15ms
```

* [x] Postgresql integration on the Integration Page  
  ![postgres Integration 2](screenshots/1-postgres-integration.png)


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

### Configure Agent check's interval to 45 seconds 
* [x] Agent check config : [test_check.yaml](datadog/conf.d/test_check.yaml)  
```yaml
init_config:

instances:
  - min_collection_interval: 45
```
```text
2018-10-19 04:46:11 UTC | INFO | (scheduler.go:63 in Schedule) | Scheduling check test_check
2018-10-19 04:46:11 UTC | INFO | (scheduler.go:76 in Enter) | Scheduling check test_check with an interval of 45s
2018-10-19 04:46:12 UTC | INFO | (runner.go:258 in work) | Running check test_check
2018-10-19 04:46:12 UTC | INFO | (runner.go:324 in work) | Done running check test_check
2018-10-19 04:46:57 UTC | INFO | (runner.go:258 in work) | Running check test_check
2018-10-19 04:46:57 UTC | INFO | (runner.go:324 in work) | Done running check test_check
```
### Configure Agent check's interval to 45 seconds without modifying the Python check file (Bonus)
* [x] Achieved in the question right before this one
---
# 2. Visualizing Data:
###  To create a Timeboard that contains:
* [x] My custom metric scoped over host.  
  ```json
  { "definition": {
        "events": [],
        "requests": [
            {"q": "top(max:my_metric{*} by {host}, 10, 'last', 'desc'), top(max:my_metric{*} by {host}, 10, 'max', 'desc'), top(max:my_metric{*} by {host}, 10, 'min', 'desc'), top(max:my_metric{*} by {host}, 10, 'mean', 'desc')"}
        ],
        "viz": "timeseries"
    },
    "title": "Data for my_metric over host."
  }
  ```  
  ![metric_byhost](screenshots/2-metric-byhost.png)  

* [x] The metric from the Integration on Database with the anomaly function applied.  
  ```json
  { "definition": { 
        "events": [],
        "requests": [
            {"q": "anomalies(avg:postgresql.buffer_hit{*}, 'basic', 2)"}
        ],
        "viz": "timeseries"
    },
    "title": "Avg of postgresql.buffer_hit w/ anomaly function applied"
  }
  ```  
  ![metric_anomaly](screenshots/2-metric-anomaly.png)  

* [x] My custom metric with the rollup function applied to sum up all the points for the past hour into one bucket  
  ```json
  { "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{*}.rollup(sum, 3600)"}
        ],
        "viz": "timeseries"
    },
    "title": "Rollup of my_metric for past hour"
  }
  ```  
  ![metric_rolledup](screenshots/2-metric-rolledup.png)  
  
* [x] The whole script to create the Timeboard  
  [create_my_custom_timeboard,py](datadog/scripts/create_my_custom_timeboard.py) 

### Dashboard screenshots
* [x] Set the Timeboard's timeframe to the past 5 minutes  
  ![timeframe](screenshots/2-timeframed-dashboard.png)  

* [x] A snapshot of the graph  that mentions myself.  
  ![mentioning_graph](screenshots/2-mentioning-graph.png)  

* [x] What is the Anomaly graph displaying? (Bonus)  
  ```text
  The anomaly graph displays two kinds of values; "natural" and "abnormal."
  "Natural" values fall within the usual range based on the culmitive data flow.
  "Abnormal" values are judged as warning because it doesn't fit in the routine data flow.
  In my case below, the anomaly graph displays when the postgres buffer hit is extremly high.
  ```  
  ![metric_anomaly_2](screenshots/2-anomaly-graph.png)  
---
# 3. Monitoring Data
### Metric Monitor settings for my custom metric.
* [x] "Alert" with threshold of 800 over the past 5 minutes.  
* [x] "Warning" with threshold of 500 over the past 5 minutes.  
  ![warning_alert](screenshots/3-monitor-alert-warning.png)  
* [x] Notify myself if there is No Data over the past 10 minutes.  
  ![nodata](screenshots/3-monitor-nodata.png)  

### Metric Monitor message for my custom metric.
* [x] Send you an email whenever the monitor triggers.    
  ![notify_team](screenshots/3-notify-team.png)  

* [x] Create different messages depending on the monitor status.  
  ![custom_messages](screenshots/3-status-messages.png)  

* [x] The metric value and the host ip in the Alert message.  
  ![value_ip](screenshots/3-value-ip.png)  
  
* [x] A screenshot of the email notification.
  (Alert, warning, nodata triggers)  
  ![alert](screenshots/3-notice-alert.png)  
  ![warning](screenshots/3-notice-warning.png)  
  ![nodata](screenshots/3-notice-nodata.png)  

###  Two scheduled downtimes for this monitor: (Bonus)
* [x] One that silences it from 7pm to 9am daily on M-F.  
  ![weekly_downtime](screenshots/3-weekly-downtime-1.png)  
  ![weekly_downtime_2](screenshots/3-weekly-downtime-2.png)  
* [x] The other that silences it all day on Sat-Sun.  
  ![weekend_downtime](screenshots/3-weekend-downtime-1.png)  
  ![weekend_downtime_2](screenshots/3-weekend-downtime-2.png)  
* [x] A screenshot of the email notification.   
  ![downtime_notice](screenshots/3-notice-downtime.png)  

---
# 4. Collecting APM Data:
### My application settings for APM
```Dockerfile
pip3 --no-cache-dir install mezzanine==4.3.1 psycopg2-binary==2.7.5 gunicorn==19.9.0 ddtrace setproctitle
```
```python
DATADOG_TRACE = {
    'AGENT_HOSTNAME': os.getenv('DOCK_DEFAULT_GW'),
    'DEFAULT_SERVICE': 'testweb',
    'TAGS': {'env': 'dev'},
}
```
### Fully instrumented application 
  [Dockerfile](Dockerfile)  
  [Application](app)  
  [docker-compose](docker-compose.yml)  

### Difference between a Service and a Resource (Bonus)
```text
A service is a cluster of processes that do the same task. A Resource is a particular action for a service.
For example, a typical web application consists of three services; web, application, SQL database.
A web/app service has resources such as a canonical URL and a handler function.
A SQL database service's resource is the query itself.
```
### A screenshot of a Dashboard with both APM and Infrastructure Metrics.
  ![APM_dashboard_1](screenshots/4-APM-infra-metrics.png)  

https://p.datadoghq.com/sb/dd9566751-7d9276b04920e50def2e02d7f7f25257

---
# 5. Final Question:
### Is there anything creative you would use Datadog for?
```text
#Your Sentence here
```

---
# Extra. Various Integrations:
I have implemented the following integrations for the extra work.  
* [x] AWS  
  ![aws_integration](screenshots/ex-monitor-aws.png)  
* [x] Nginx  
  ![nginx_integration](screenshots/ex-monitor-nginx.png)  
* [x] Slack  
  ![slack_integration](screenshots/ex-notify-slack.png)  
* [x] Jira  
  ![jira_integration](screenshots/ex-notify-jira.png)  
* [x] Docker  
  ![docker_integration](screenshots/ex-monitor-docker.png)  


Happy when you could vote Yes for me.
