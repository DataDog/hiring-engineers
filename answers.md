### Environment Setup

**Host OS:** Mac OS X

Installed Vagrant & VirtualBox

**Vagrant OS:** ubuntu/xenial64
  
# Collecting Metrics
  
##  Install Datadog Agent

SSH into the vagrant ubuntu host and run below command

```
DD_API_KEY=<<API_KEY>> bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```

##  Adding Tags

The configuration files and folders for the Agent are located in:

/etc/datadog-agent/datadog.yaml

1. Edit datadog.yaml
2. Add tags

```
tags:
    - env:trial
    - type:vagrant
    - role:dd_challenge
```
3. Restart datadog agent
```
$sudo service datadog-agent restart
```
4. Host Map in action

 ![Host Map](/img/Host_Map.png)


##  Integration with Postgres

1. Install Postgres

2. Add integration in Datadog GUI (follow steps on UI)

3. Create user with proper access to your PostgreSQL server

```
sudo psql
postgres=# create user datadog with password '<PASSWORD>';
postgres=# grant pg_monitor to datadog;
```
4. Create & configure postgres.d/conf.yaml file to point to your server, port etc.

```
sudo $vi /etc/datadog-agent/conf.d/postgres.d/config.yaml 
```

change below parameters -

```
    host: localhost
    port: 5432
    username: datadog
    password: <PASSWORD>
```


5. Restart Agent

```
$sudo service datadog-agent restart
```
6. Postgres on Host Map

 ![Host Map_Postgres](/img/host_map_postgres.png)

##  Random number generator Custom Check

1. Install python
```
$ sudo apt install python3
```
2. Python code to generate random number
[Code](/files/custom_random_check.py)

```python
from random import *
# the following try/except block will make the custom check compatible with any Agent version

try:
    # first, try to import the base class from old versions of the Agent...

    from checks import AgentCheck
except ImportError:
    # ...if the above failed, the check is running in Agent version 6 or later

    from datadog_checks.checks import AgentChecks

# content of the special variable __version__ will be shown in the Agent status page

__version__ = '1.0.0'

class RandomCheck(AgentCheck):
    def check(self, instance):
        value = randint(0,1000)
        self.gauge('my_metric', value)
```

3. Configuration file to configure collection interval to 45 seconds
[Yaml config](/files/custom_random_check.yaml)
```yaml
init_config:

instances:
  - min_collection_interval: 45
```

4. Copy python script to `/etc/datadog-agent/checks.d`
5. Copy yaml config to `/etc/datadog-agent/conf.d`
6. Restart Agent
7. Verify custom check is working
```
$sudo -u dd-agent -- datadog-agent check custom_random_check
```
8. Custom metric can be seen in Dashboard

 ![custom_metric](/img/custom_metric.png)



#### Bonus Question
Can you change the collection interval without modifying the Python check file you created?

> Yes, collection interval can be changed by changing the yaml configuration file as above.

# Visualizing Data:

1. Install datadog python lib
```
pip install datadog
```
2. Python code to create a timeboard 
[code](/files/create_timeboard.py)

```python
from datadog import initialize, api

options = {
  'api_key': '<<>>',
  'app_key': '<<>>'
}

initialize( ** options)

title = 'Hiring Challenge Timeboard'
widgets = [{
    'definition': {
      'type': 'timeseries',
      'requests': [{
        "q": "avg:my_metric{host:ubuntu-xenial}"
      }],
      'title': 'Random number metric over host'
    }
  },
  {
    'definition': {
      'type': 'timeseries',
      'requests': [{
        "q": "anomalies(avg:postgresql.bgwriter.checkpoints_timed{host:ubuntu-xenial}, 'basic', 6)"

      }],
      'title': 'Anamloy detection on checkpoints timed in postgresql'
    }
  },
  {
    'definition': {
      'type': 'query_value',
      'requests': [{
        "q": "sum:my_metric{host:ubuntu-xenial}.rollup(sum, 3600)"
      }],
      'title': 'Random number metric rollup over last 1 hour'
    }
  }
]
layout_type = 'ordered'
description = 'Hiring challenge dashboard showcasing different metrics.'
is_read_only = True
notify_list = ['user@domain.com']
template_variables = [{
  'name': 'host1',
  'prefix': 'host',
  'default': 'ubuntu-xenial'
}]
api.Dashboard.create(title = title,
  widgets = widgets,
  layout_type = layout_type,
  description = description,
  is_read_only = is_read_only,
  notify_list = notify_list,
  template_variables = template_variables)

```

3. Execute python script

4. Dashboard in action

 ![timeboard_api](/img/timeboard_with_api.png)

5. Timeboard with 5 min timeframt

 ![timeboard_5_min](/img/timeboard_5_min.png)

6. Snapshot notification with comments

 ![timeboard_notification](/img/timeboard_notification.png)

#### Bonus Question
What is the Anomaly graph displaying?

> By analyzing a metric’s historical behavior, anomaly detection distinguishes between normal and abnormal metric trends
In this case, the anamoly graph is displayed on postgres bgwriter checkpoint function. The graph displays deviation of the metric from the normal average.


# Monitoring Data

1. Create Monitor : set alert conditions to configure warning,alert & no data notifications

 ![monitor config](/img/monitor_config.png)

2. Create Monitor : conditional notification message template

 ![monitor message](/img/monitor_message.png)

3. Email : Alert

 ![email alert](/img/monitor_alert.png)

4. Email : Warning

 ![email warning](/img/monitor_warning.png)

5. Email : No Data

 ![email no data](/img/monitor_no_data.png)

#### Bonus Question

6. Schedule weekday downtime configuration

 ![monitor_downtown_weekday_config](/img/monitor_downtime_weekday_config.png)

7. Schedule weekday downtime notification email

 ![monitor_downtown_weekday_email](/img/monitor_downtime_weekday_mail.png)

8. Schedule weekend downtime configuration

 ![monitor_downtown_weekday_config](/img/monitor_downtime_weekend_config.png)

9. Schedule weekend downtimee notification email

 ![monitor_downtown_weekday_email](/img/monitor_downtime_weekend_mail.png)


# Collecting APM Data:


1. Install ddtrace python client

```
pip install ddtrace
```


2. Flask App [code](/files/dd_flask_app.py)

```python
from flask import Flask
import logging
import sys
from random import randint

# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

app = Flask(__name__)

@app.route('/')
def api_entry():
    return 'Entrypoint to the Application'

@app.route('/api/apm')
def apm_endpoint():
    return 'Getting APM Started'

@app.route('/api/trace')
def trace_endpoint():
    return 'Posting Traces'

@app.route('/api/hello')
def hello():
    return 'Hello World! '


@app.route('/api/random')
def random():
    return "Random number {}\n".format(randint(1,1000))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5050')
```

3. Instrument above flask application

```
ddtrace-run python3 dd_flask_app.py
```

4. Hit app endpoints to simulate traces

```
curl localhost:5050/api/random
```

```
curl localhost:5050/api/hello
```

5. Traces Datadog dashboard

 ![apm_dd_trace](/img/apm_dd_trace.png)

6. Trace list

 ![trace_list](/img/trace_list.png)

7. Final timeboard with APM & Infra metrics
 ![apm_infra_final_dashboard](/img/apm_infra_final_dashboard.png)

8. Final screenboard with APM & Infra metrics (for Public sharing)

 [Screenboard link](https://p.datadoghq.com/sb/op0jcrfv5cfk07tu-d634974855064ab8bb11daab4820e41f)

 ![apm_infra_final_dashboard](/img/final_public_screenboard.png)


#### Bonus Question

9. What is the difference between a Service and a Resource?

> A service is a set of processes that do the same job. 
> In above example, service is the flask webapp which is sending traces to datadog.
> A Resource is a particular action for a service.
> In above example, '/api/hello' and '/api/random' are resources which accepts requests to the flask app service.


# Final Question

Is there anything creative you would use Datadog for?


I think with the proliferation of IoT devices, the need for monitoring and alerting sensors is imminent. 
As the latest Datadog agent is written in Go,and go has an extremely light memory/cpu footprint, running the datadog agents even on small sensors is possible. I could think of numerous IoT usecases wherein datadog can be used.

**Monitoring shipping containers:**  Tracking shipping containers by monitoring data such as temperature, pressure, GPS, container opened/closed etc . Let's say a container is carrying fishes, then detecting and alerting anamolies on container's temperature data can save the fishes from going bad and potentially save some losses. Datadog can continuously monitor container data and alert in case of anamolies

**Employee Happiness Index:**  Employees everyday can choose to answer "How was your day?" question by pressing one of the two buttons (Happy, Sad) attached to a Raspberry Pi. Datadog dashboard displaying the overall happiness index can be projected on a big screen in office to boost employee satisfaction.

