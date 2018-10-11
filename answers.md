Your answers to the questions go here.

# 0 - Prereqs (setup vm)
- setup vagrant box to perform tests from:
```
vagrant@ubuntu-xenial:~$ sudo systemctl status datadog-agent
● datadog-agent.service - "Datadog Agent"
   Loaded: loaded (/lib/systemd/system/datadog-agent.service; enabled; vendor preset: enabled)
   Active: active (running) since Thu 2018-10-11 05:54:15 UTC; 2min 56s ago
 Main PID: 15590 (agent)
    Tasks: 11
   Memory: 30.2M
      CPU: 1.305s
   CGroup: /system.slice/datadog-agent.service
           └─15590 /opt/datadog-agent/bin/agent/agent run -p /opt/datadog-agent/run/agent.pid
```

# 1 - Collecting Metrics
- Screenshot to agent host config with tags:

    - ![Screenshot Host config w/tags](/homework-assets/images/screenshot1.png)

    ![alt text][screenshot1]

     https://www.dropbox.com/s/dvvc65ywnpp21gj/Screenshot%202018-10-10%2022.55.47.png?dl=0
- Screenshot of postgresql integration enabled and collecting metrics automatically:
    - https://www.dropbox.com/s/40cbmpafrh970u7/Screenshot%202018-10-10%2023.53.47.png?dl=0
- Custom Agent Check - Created "allthethings_random_checker.py" (and allthethings_random_checker.yaml in conf.d directory) with the following code/configuration:

Check code:
```
root@ubuntu-xenial:/home/vagrant# cat /etc/datadog-agent/checks.d/allthethings_random_checker.py
import random
from checks import AgentCheck
class AllTheThingsRandomChecker(AgentCheck):
    def check(self, instance):
        self.gauge('allthethings.checker.random', random.randrange(0, 1000))
```
Check Config:
```
root@ubuntu-xenial:/home/vagrant# cat /etc/datadog-agent/conf.d/allthethings_random_checker.yaml
init_config:
    default_timeout: 5
instances:
    [{}]
```
Check Config (Bonus Question) - changed to 45s interval via config file:
```
root@ubuntu-xenial:/home/vagrant# cat /etc/datadog-agent/conf.d/allthethings_random_checker.yaml
init_config:
    default_timeout: 5
instances:
    - min_collection_interval: 45
```
- Screenshot of reported "allthethings_random_checker" metric:
    - https://www.dropbox.com/s/xtuyz7vgych1glr/Screenshot%202018-10-11%2000.47.08.png?dl=0
- Screenshot of timeboard created via API:
    - https://www.dropbox.com/s/ovvvz5qzkhu6zzl/Screenshot%202018-10-11%2001.34.08.png?dl=0
- Code to create the timeboard:
```python
from datadog import initialize, api

options = {
    'api_key': '[REDACTED]',
    'app_key': '[REDACTED]'
}

initialize(**options)

title = "AllTheThings Metric Timeboard"
description = "Displays AllTheThings metrics"
graphs = [{
    "definition": {
        "requests": [
            {"q": "sum:allthethings.checker.random{host:ubuntu-xenial}"},
        ],
        "viz": "timeseries"
    },
    "title": "allthethings.checker.random"
},
{
    "definition" : {
        "requests": [
            {"q": "anomalies(avg:system.load.1{host:ubuntu-xenial}, 'basic', 2)"},
            {"q": "anomalies(avg:system.load.5{host:ubuntu-xenial}, 'basic', 2)"},
            {"q": "anomalies(avg:system.load.15{host:ubuntu-xenial}, 'basic', 2)"},
            {"q": "anomalies(avg:postgresql.percent_usage_connections{host:ubuntu-xenial}, 'basic', 2)"}
        ],
        "viz": "timeseries"
    },
    "title": "Postgresql System Load and Percent usage connections"
},
{
    "definition": {
        "requests": [
            {"q": "avg:allthethings.checker.random{host:ubuntu-xenial}.rollup(sum, 3600)"}
        ],
        "viz": "timeseries"
    },
    "title": "allthethings.checker.random with rollup applied"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     read_only=read_only)
```
- Screenshot of timeboard set to recent 5min:
    - https://www.dropbox.com/s/3z3wl5rfdweznnh/Screenshot%202018-10-11%2001.39.17.png?dl=0
- Screenshot of screenshot (screenshot inception!) of the 5min timeframe, annotated and emailed to myself:
    - https://www.dropbox.com/s/3dba631ydq058zt/Screenshot%202018-10-11%2001.41.05.png?dl=0
## Bonus Question: What is the Anomaly graph displaying?
- Anomaly detection is used to identify variances (anomalies) in a given metric over the timeperiod in question. By applying it to the given series, it will display the actual results along with the expected results to help identify said anomalies.
- Screenshot below shows how the Evaluation period is displayed along with actual results:
https://www.dropbox.com/s/lw5igcph2mm3hnl/Screenshot%202018-10-11%2001.47.06.png?dl=0

# Monitoring Data
- Screenshot of notification that the monitor was created to handle the following thresholds: Alert >800, Warn >500
    - https://www.dropbox.com/s/ixgsqnaljl3emwa/Screenshot%202018-10-11%2002.15.08.png?dl=0
- Screenshot of Monitor being triggered based on warn and alert thresholds above 500 & 800 respectively:
    - https://www.dropbox.com/s/ez5vfl2fxlcusjk/Screenshot%202018-10-11%2002.17.04.png?dl=0

## Bonus Question: Create downtime for monitor beteen 7pm-9am M-F, and all day Saturday and Sunday
- Screenshot showing monitor downtime created for 7pm-9am M-F:
    - https://www.dropbox.com/s/4f42b6brs6jstak/Screenshot%202018-10-11%2002.13.16.png?dl=0
- Screenshot showing monitor downtime created for 9am-9am Saturday & Sunday:
    - https://www.dropbox.com/s/cnhzuhqpq344hvy/Screenshot%202018-10-11%2002.16.14.png?dl=0

# Collecting APM Data: Given the following app, instrument via APM
Application: (opted to use the provided app)
note: I am entering the application via the `ddtrace-run python apm_flask_app.py` command
```python
"""This application has a basic hello World response
    as well as handles monitoring components"""
from flask import Flask
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
main_logger.addHandler(c)

app = Flask(__name__)
traced_app = TraceMiddleware(app, tracer, service="apm_flask_app", distributed_tracing=True)

@app.route('/')
def api_entry():
    return 'Entrypoint to the Application \n Hello, World!'

@app.route('/api/apm')
def apm_endpoint():
    return 'Getting APM Started'

@app.route('/api/trace')
def trace_endpoint():
    return 'Posting Traces'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5050')
```
- Screenshot to the APM Services page, showing traces being collected:
    - https://www.dropbox.com/s/bjdzazmudjfu8ku/Screenshot%202018-10-11%2002.39.13.png?dl=0
- Dashboard with infrastructure and APM metrics, as well as my custom metric:
    - https://app.datadoghq.com/dash/944046/allthethings-metric-timeboard?live=true&page=0&is_auto=false&from_ts=1539247476797&to_ts=1539251076797&tile_size=m
    - Screenshot of the same: https://www.dropbox.com/s/3fypovfvv9sdvan/Screenshot%202018-10-11%2002.48.42.png?dl=0

# Final bonus question: What is the difference between a Service and a Resource
- A Service is a higher level construct identifying the combination of a number of Resources (Applications, Databases, etc...).
- A Resource is a lower level construct such as a web app request path (e.g. `/api/trace`), or a SQL query or similar.



-----
Assets:
[screenshot1]: /homework-assets/images/screenshot1 "Screenshot1"
[screenshot2]: https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 2"
[screenshot3]: https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 2"
[screenshot4]: https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 2"
[screenshot5]: https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 2"
[screenshot6]: https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 2"
[screenshot7]: https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 2"
[screenshot8]: https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 2"
[screenshot9]: https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 2"
[screenshot10]: https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 2"
[screenshot11]: https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 2"
[screenshot12]: https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 2"
[screenshot13]: https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 2"
[screenshot14]: https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 2"
[screenshot15]: https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 2"
