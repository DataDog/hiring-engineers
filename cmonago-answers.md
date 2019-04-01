# Collecting Metrics:

## 1. Tags
<img src="https://raw.githubusercontent.com/cmonago/hiring-engineers/master/tags.png"/>

     
## 2. Postgres Integration
```
more /etc/datadog-agent/conf.d/postgres.yaml

init_config:

instances:

  - host: localhost
  
    port: 5432
    
    username: postgres
    
    password: postgres
    
    tags:
    
- optional_tag1
      
- optional_tag2
```

## 3. Custom Metrics
```
[root@datadogdemo conf.d]# more /etc/datadog-agent/checks.d/my_metric.py
import random
try:
    from checks import AgentCheck
except ImportError:
    from datadog_checks.checks import AgentCheck
__version__ = "1.0.0"

class My_MetricCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', random.randint(0,1000))


```
## 4. Collection Interval
```
[root@datadogdemo conf.d]# more /etc/datadog-agent/conf.d/my_metric.yaml

init_config:

instances:

  - min_collection_interval: 45

```
**Bonus Question:**

Yes, it is possible to change without modify python script. I have created configuration file my_metric.yaml in conf.d with the parameter min_collection_interval
      
# Visualizing Data:

## Timeboard 

<img src="https://raw.githubusercontent.com/cmonago/hiring-engineers/master/timeboard.png"/>

### Script 
```
api_key="c3053ab6854693b71140116aa25b6c0a"
app_key="3bda4f0edbd0b154e6e80ec92cfe2bc2f347e3a1"

curl  -X POST -H "Content-type: application/json" \
-d '{
      "title" : "DataDog Demo TimeBoard",
      "widgets" : [{
          "definition": {
              "type": "timeseries",
              "requests": [
                  {"q": "avg:my_metric{*}"}
              ],
              "title": "My Metric"
          }
      },
      {
          "definition": {
              "type": "query_value",
              "requests": [
                  {"q": "avg:my_metric{*}"}
              ],
              "title": "My Metric Aggregated"
          }
       }, {
          "definition": {
              "type": "alert_value",
              "alert_id": "9112171",
              "title": "Anomaly in connectios"
          }
       }],
      "layout_type": "ordered",
      "description" : "A dashboard for demo datadog",
      "is_read_only": false,
      "notify_list": ["c.monago@gmail.com"],
      "template_variables": [{
          "name": "host1",
          "prefix": "host",
          "default": "datadogdemo"
      }]
}' \
"https://api.datadoghq.com/api/v1/dashboard?api_key=${api_key}&application_key=${app_key}"

```
1. TimeBoard 5 min

<img src="https://raw.githubusercontent.com/cmonago/hiring-engineers/master/timeboard_last_5_min.png"/>

2. TimeBoard Snapshot notation

<img src="https://raw.githubusercontent.com/cmonago/hiring-engineers/master/send_snapshot.png"/>

**Bonus Question:**

Breaches of metric based in baseline calculated with all historical data.

## Monitoring Data

1. Alert

Configuration

<img src="https://raw.githubusercontent.com/cmonago/hiring-engineers/master/alert.png"/>

Alert text
```
My metric on {{host.name}} is {{threshold}}


{{#is_no_data}} My Metric is no data{{/is_no_data}}
{{#is_warning}}  Warning status because metric the value is {{value}} {{/is_warning}}
{{#is_alert}} Alert status because metric the value is {{value}} {{/is_alert}}

Alert in {{host.name}} with ip {{host.ip}}  

 @c.monago@gmail.com
```

Emails (no data, warning and alert)

<img src="https://raw.githubusercontent.com/cmonago/hiring-engineers/master/no_data_alert.JPG"/>
<img src="https://raw.githubusercontent.com/cmonago/hiring-engineers/master/warn_alert.JPG"/>
<img src="https://raw.githubusercontent.com/cmonago/hiring-engineers/master/email_alert.JPG"/>

**Bonus Question:**

- One that silences it from 7pm to 9am daily on M-F,
- And one that silences it all day on Sat-Sun.

## Collecting APM Data

https://app.datadoghq.com/dashboard/2b6-9sr-392/

Application instrumented

```
from flask import Flask
from ddtrace import config
from ddtrace import tracer
from ddtrace.contrib.flask import TraceMiddleware
import logging
import sys


# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)

# Enable distributed tracing
config.flask['distributed_tracing_enabled'] = True

# Override service name
config.flask['service_name'] = 'custom-service-name'

# Report 401, and 403 responses as errors
config.flask['extra_error_codes'] = [401, 403]

main_logger.addHandler(c)

app = Flask('thinker-app')
traced_app = TraceMiddleware(app, tracer, service='thinker-app')

@app.route('/')
def api_entry():
    return 'Entrypoint to the Application'

@app.route('/api/apm')
def apm_endpoint():
    return 'Getting APM Started'

@app.route('/api/trace')
def trace_endpoint():
    return 'Posting Traces'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5050')

```

## Final Question:

There are differents creative ways used in the past, an example:

- **Home Monitoring:**
 - Monitoring beedroom to slepp perfectly
 - Monitoring energy consumption
 - Monitoring water consumption
