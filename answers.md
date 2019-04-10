## Environment Setup

Host OS: Mac OS X
Installed Vagrant
Vagrant OS: ubuntu/xenial64
  
  ## Collecting Metrics
  
##  Install Agent

```
  DD_API_KEY=<<API_KEY>> bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```

##  Adding Tags

The configuration files and folders for the Agent are located in:

/etc/datadog-agent/datadog.yaml

1. edit datadog.yaml
2. Add tags

```
tags:
    - env:trial
    - type:vagrant
    - role:dd_challenge
```
3. Restart datadog agent
```
$sudo service datadog-agent status
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

$vi /etc/datadog-agent/conf.d/postgres.d/config.yaml 

change below parameters -

```
    host: localhost
    port: 5432
    username: datadog
    password: <PASSWORD>
```


5. Restart Agent

```
$sudo service datadog-agent status
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



## Bonus Question
Can you change the collection interval without modifying the Python check file you created?

Yes, collection interval can be changed by changing the yaml configuration file as above.

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

# Bonus Question
What is the Anomaly graph displaying?
By analyzing a metric’s historical behavior, anomaly detection distinguishes between normal and abnormal metric trends
In this case, the anamoly graph is displayed on postgres bgwriter checkpoint function. The graph displays deviation of the metric from the normal average.


