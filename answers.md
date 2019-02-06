# Answers 

Thank you for the oppportunity to apply for the position as Solutions Engineer at Datadog. I have very much enjoyed working with and seeing the various aspects of the Datadog solution. 

I have included the question list from [README.md](/README.md) to ensure everything is logically arranged. All the questions are highlighted as headings with my answers clearly described underneath with screenshots, code snippets and commands run. 

## Prerequisites - Setup the environment

Clone the repo to your PC, check out the correct branch and setup the vagrant host.
```bash
git clone https://github.com/daclutter/hiring-engineers.git
cd hiring-engineers
git checkout solutions-engineer
vagrant init hasicorp/precise64
vagrant up
```

Log in and ensure everything is up to date.
```bash
sudo apt-get update
sudo apt-get upgrade -y
sudo reboot
```

Install the Agent on the host using the install command, including the API KEY is desplayed on the Datadog getting started page.

![Agent](/images/00-Ubuntu-agent.PNG)

```bash
sudo apt-get install -y curl
DD_API_KEY=<API_KEY> bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```
*curl not included on the base vagrant image*

## Collecting Metrics:

Default vagrant install is missing vim, install it. Alternatively you can install and use the text editor of your choice.
```bash
sudo apt-get install -y vim
```

### Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

Add the following lines into the config file
```bash
sudo vim /etc/datadog-agent/datadog.yaml
```
```yaml
# Set the host's tags (optional)
tags:
   - interview
   - home:desktop
   - role:testing
```

Restart the datadog-agent
```bash
sudo service datadog-agent restart
```

Look at the [host map](https://app.datadoghq.com/infrastructure/map?host=817478908&fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=availability-zone&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=true&palette=green_to_orange&paletteflip=false&node_type=host)

![Hostmap](/images/01-hostmap-tags.PNG)

### Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

Install MySQL, setting the MySQL root password in the install process (You will be prompted)
```bash
sudo apt-get install -y mysql-server 
```

Follow the [MySQL integration instructions](https://app.datadoghq.com/account/settings#integrations/mysql), [alternative instructions](https://docs.datadoghq.com/integrations/mysql/)

Integrations on the Datadog Web interface
![Integrations](/images/02-Integrations.png)
![MySQL Integrations](/images/03-mysql-integration.PNG)

Create a user for the datadog agent to use with replications rights:
```bash
sudo mysql -e "CREATE USER 'datadog'@'localhost' IDENTIFIED BY '<PASSWORD>';"
sudo mysql -e "GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'localhost' WITH MAX_USER_CONNECTIONS 5;"
```
If you created a password for the root user you will need to use the below commands and enter the password at the prompt:
```bash
sudo mysql -e "CREATE USER 'datadog'@'localhost' IDENTIFIED BY '<PASSWORD>';" -p 
sudo mysql -e "GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'localhost' WITH MAX_USER_CONNECTIONS 5;" -p
```

Grant additional privileges to get full metrics access
```bash
sudo mysql -e "GRANT PROCESS ON *.* TO 'datadog'@'localhost';" -p
sudo mysql -e "GRANT SELECT ON performance_schema.* TO 'datadog'@'localhost';" -p
```

Use the following commands to verify the above
```bash
$ mysql -u datadog --password='<PASSWORD>' -e "show status" | \
> grep Uptime && echo -e "\033[0;32mMySQL user - OK\033[0m" || \
> echo -e "\033[0;31mCannot connect to MySQL\033[0m"
Uptime  1191
Uptime_since_flush_status       1191
MySQL user - OK
$ mysql -u datadog --password='<PASSWORD>' -e "show slave status" && \
> echo -e "\033[0;32mMySQL grant - OK\033[0m" || \
> echo -e "\033[0;31mMissing REPLICATION CLIENT grant\033[0m"
MySQL grant - OK
```

Use the following commands to verify the additional privileges
```bash
$ mysql -u datadog --password='<PASSWORD>' -e "SELECT * FROM performance_schema.threads" && \
> echo -e "\033[0;32mMySQL SELECT grant - OK\033[0m" || \
> echo -e "\033[0;31mMissing SELECT grant\033[0m"
MySQL SELECT grant - OK
$ mysql -u datadog --password='<PASSWORD>' -e "SELECT * FROM INFORMATION_SCHEMA.PROCESSLIST" && \
> echo -e "\033[0;32mMySQL PROCESS grant - OK\033[0m" || \
> echo -e "\033[0;31mMissing PROCESS grant\033[0m"
+----+---------+-----------+------+---------+------+-----------+----------------------------------------------+
| ID | USER    | HOST      | DB   | COMMAND | TIME | STATE     | INFO                                         |
+----+---------+-----------+------+---------+------+-----------+----------------------------------------------+
| 50 | datadog | localhost | NULL | Query   |    0 | executing | SELECT * FROM INFORMATION_SCHEMA.PROCESSLIST |
+----+---------+-----------+------+---------+------+-----------+----------------------------------------------+
MySQL PROCESS grant - OK

```

Edit and setup the `/etc/datadog-agent/conf.d/mysql.d/conf.yaml` configuration file with the below configuration
```bash
sudo vim /etc/datadog-agent/conf.d/mysql.d/conf.yaml
```
```yaml
init_config:

instances:
  - server: 127.0.0.1
    user: datadog
    pass: <PASSWORD>
    tags:
        - interview_db
    options:
      replication: 0
      galera_cluster: 1
```

Restart the agent for the configuration changes to take effect
```bash
sudo service datadog-agent restart
```

Verify the changes using the status command
```bash
$ sudo datadog-agent status | grep -A 5 mysql
    mysql (1.5.0)
    -------------
      Instance ID: mysql:59e1aacfe586f820 [OK]
      Total Runs: 5
      Metric Samples: Last Run: 64, Total: 319
      Events: Last Run: 0, Total: 0
      Service Checks: Last Run: 1, Total: 5
      Average Execution Time : 76ms
```

Install the integration on the Datadog Web Interface
![Integrations](/images/04-mysql-integration-install.PNG)

Verify from the Hostmap that the App is installed
![MySQL Hostmap](/images/05-mysql-hostmap.PNG)

### Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

There will be 2 files that need to be created - a code file (python) and a configuration file (yaml). Both files **must** have the same name.

Create the configuration file with the below configuration
```bash
sudo vim /etc/datadog-agent/conf.d/my_metric.yaml
```
```yaml
instances: [{}]
```

Create the code file with the below code
```bash
sudo vim /etc/datadog-agent/checks.d/my_metric.py
```
```python
import random
# the following try/except block will make the custom check compatible with any Agent version
try:
    # first, try to import the base class from old versions of the Agent...
    from checks import AgentCheck
except ImportError:
    # ...if the above failed, the check is running in Agent version 6 or later
    from datadog_checks.checks import AgentCheck

# content of the special variable __version__ will be shown in the Agent status page
__version__ = "1.0.0"


class MyMetric(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', random.randint(0,1000))
```

Restart the datadog-agent
```bash
sudo service datadog-agent restart
```

Verify the check is working
```bash
$ sudo datadog-agent check my_metric
=== Series ===
{
  "series": [
    {
      "metric": "datadog.agent.check_ready",
      "points": [
        [
          1549385506,
          1
        ]
      ],
      "tags": [
        "agent_version_major:6",
        "agent_version_minor:9",
        "check_name:my_metric",
        "status:ready"
      ],
      "host": "precise64",
      "type": "gauge",
      "interval": 0,
      "source_type_name": "System"
    },
    {
      "metric": "my_metric",
      "points": [
        [
          1549385506,
          804
        ]
      ],
      "tags": null,
      "host": "precise64",
      "type": "gauge",
      "interval": 0,
      "source_type_name": "System"
    }
  ]
}
=========
Collector
=========

  Running Checks
  ==============

    my_metric (1.0.0)
    -----------------
      Instance ID: my_metric:d884b5186b651429 [OK]
      Total Runs: 1
      Metric Samples: Last Run: 1, Total: 1
      Events: Last Run: 0, Total: 0
      Service Checks: Last Run: 0, Total: 0
      Average Execution Time : 0s


Check has run only once, if some metrics are missing you can try again with --check-rate to see any other metric if available.
```

Also on the Datadog Web Interface
![my_metric](/images/06-my_metric.PNG)

### Change your check's collection interval so that it only submits the metric once every 45 seconds.

Modify the configuration file for the check to contain the following.
```bash
sudo vim /etc/datadog-agent/conf.d/my_metric.yaml
```
```yaml
init_config:

instances:
  - min_collection_interval: 45
```
*It is worth noting that the time put for `min_collection_interval` will be attempted, but if the agent is running many checks or the check takes more than 45 seconds to finish it will skip until the next interval.*

Restart the datadog-agent
```bash
sudo service datadog-agent restart
```

Verify the check is working
```bash
$ sudo datadog-agent check my_metric
=== Series ===
{
  "series": [
    {
      "metric": "datadog.agent.check_ready",
      "points": [
        [
          1549387187,
          1
        ]
      ],
      "tags": [
        "agent_version_major:6",
        "agent_version_minor:9",
        "check_name:my_metric",
        "status:ready"
      ],
      "host": "precise64",
      "type": "gauge",
      "interval": 0,
      "source_type_name": "System"
    },
    {
      "metric": "my_metric",
      "points": [
        [
          1549387187,
          251
        ]
      ],
      "tags": null,
      "host": "precise64",
      "type": "gauge",
      "interval": 0,
      "source_type_name": "System"
    }
  ]
}
=========
Collector
=========

  Running Checks
  ==============

    my_metric (1.0.0)
    -----------------
      Instance ID: my_metric:5ba864f3937b5bad [OK]
      Total Runs: 1
      Metric Samples: Last Run: 1, Total: 1
      Events: Last Run: 0, Total: 0
      Service Checks: Last Run: 0, Total: 0
      Average Execution Time : 0s


Check has run only once, if some metrics are missing you can try again with --check-rate to see any other metric if available.
```

Also on the Datadog Web Interface
![my_metric_45](/images/07-my_metric_45.PNG)

### **Bonus Question** Can you change the collection interval without modifying the Python check file you created?

The collection interval is controlled entirely by the configuration file (yaml) so there should be no need to modify the Python file. However if the check performed in the python file has a long execution time (e.g. greater than the interval desired) there may need to be changes made to the Python file.

## Visualizing Data:

### Utilize the Datadog API to create a Timeboard that contains:

* ***Your custom metric scoped over your host.***
* ***Any metric from the Integration on your Database with the anomaly function applied.***
* ***Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket***

Create an Application key on the [API page](https://app.datadoghq.com/account/settings#api) of the Datadog Web Interface
![App Key](/images/08-app-key.PNG)

Use the [API Reference](https://docs.datadoghq.com/api/?lang=python#timeboards)

Install the [Datadog Python SDK](https://github.com/DataDog/datadogpy)
```bash
sudo apt-get install python-pip -y
sudo pip install -i https://pypi.python.org/simple/ --upgrade pip
sudo apt-get remove python-chardet
sudo pip install datadog
```
*Note that the version of pip in the 16.04 repository is currently broken as it refers to the non-SSL version of the package index. The above forces the SSL version. Chardet also needs to be manually removed to allow pip to install datadog*

Create a Python script to create a timeseries/dashboard using the API and the following script
```bash
vim ~/create_timeboard.py
```
```python
from datadog import initialize, api

options = {
    'api_key': '<API KEY>',
    'app_key': '<APP KEY>'
}

initialize(**options)

title = "Dale's Metrics"
description = "A timeboard built for the Datadog interview process"
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{host:precise64}"}
        ],
        "viz": "timeseries"
    },
    "title": "My Metric"
},{
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:mysql.performance.queries{host:precise64}, 'basic', 2)"}
        ],
        "viz": "timeseries"
    },
    "title": "MySQL Metric"
},{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{host:precise64}.rollup(sum, 3600)",
            "type": "bars"}
        ],
        "viz": "timeseries"
    },
    "title": "My Metric Rollup"
}]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:my-host"
}]

read_only = True
result = api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)

print result
```

Execute the script and confirm the output from the script
```bash
$ python ~/create_timeboard.py
{u'dash': {u'read_only': True, u'description': u'A timeboard built for the Datadog interview process', u'created': u'2019-02-06T11:07:21.353611+00:00', u'title': u"Dale's Metrics", u'modified': u'2019-02-06T11:07:21.353611+00:00', u'created_by': {u'handle': u'daclutter@gmail.com', u'name': u'Dale Clutterbuck', u'access_role': u'adm', u'verified': True, u'disabled': False, u'is_admin': True, u'role': None, u'email': u'daclutter@gmail.com', u'icon': u'https://secure.gravatar.com/avatar/c3c51236610593c4fc3b677970e06c2c?s=48&d=retro'}, u'graphs': [{u'definition': {u'viz': u'timeseries', u'requests': [{u'q': u'avg:my_metric{host:precise64}'}], u'events': []}, u'title': u'My Metric'}, {u'definition': {u'viz': u'timeseries', u'requests': [{u'q': u"anomalies(avg:mysql.performance.queries{host:precise64}, 'basic', 2)"}], u'events': []}, u'title': u'MySQL Metric'}, {u'definition': {u'viz': u'timeseries', u'requests': [{u'q': u'avg:my_metric{host:precise64}.rollup(sum, 3600)', u'type': u'bars'}], u'events': []}, u'title': u'My Metric Rollup'}], u'template_variables': [{u'default': u'host:my-host', u'prefix': u'host', u'name': u'host1'}], u'id': 1068953}, u'url': u'/dash/1068953/dales-metrics', u'resource': u'/api/v1/dash/1068953'}
```

[The script used to create the timeboard can be found here.](/create_timeboard.py)

### Once this is created, access the Dashboard from your Dashboard List in the UI:

[Dashboard](https://app.datadoghq.com/dashboard/h5z-e46-t35/dales-metrics?tile_size=m&page=0&is_auto=false&from_ts=1549449300000&to_ts=1549452900000&live=true)
![Timeboard](/images/09-timeboard.PNG)

### Set the Timeboard's timeframe to the past 5 minutes

Use the key shortcut `alt + ]` to zoom in to 5 minutes.

[Dashboard 5m](https://app.datadoghq.com/dashboard/h5z-e46-t35/dales-metrics?tile_size=m&page=0&is_auto=false&from_ts=1549450950000&to_ts=1549451250000&live=false)
![Timeboard](/images/10-timeboard-5m.PNG)

### Take a snapshot of this graph and use the @ notation to send it to yourself.

Select the camera icon which is displayed when hovering over the graph to save a snapshot.

![Timeboard](/images/11-snapshot-email.PNG)

### **Bonus Question**: What is the Anomaly graph displaying?

The anomoly graph uses trends to understand expected metric values based on historical activity. It will highlight (in this case, in red) when a metric falls outside of expected values based on historical trends. The MySQL server is not hosting anything so is quiet, however I ran a series of blank queries to force an anomoly as you can see by the red spike below.

![Timeboard](/images/12-anomoly.PNG)

## Monitoring Data

### Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

* ***Warning threshold of 500***
* ***Alerting threshold of 800***
* ***And also ensure that it will notify you if there is No Data for this query over the past 10m.***

***Please configure the monitor’s message so that it will:***

* ***Send you an email whenever the monitor triggers.***
* ***Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.***
* ***Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.***
* ***When this monitor sends you an email notification, take a screenshot of the email that it sends you.***

Go to the [manage monitors page](https://app.datadoghq.com/monitors/manage) on the Datadog Web Interface and select "[New Monitor](https://app.datadoghq.com/monitors#/create)".

![New Monitor](/images/13-new-monitor-metric.PNG)

Configure the thresholds.

![Thresholds](/images/14-monitor-thresholds.PNG)

Configure the alert/warning/no data notification messages.

![Messages](/images/15-monitor-message.PNG)

Below are the warning and alert e-mail notifications.

![Warning](/images/16-warning.PNG)

![Alert](/images/17-alert.PNG)

### **Bonus Question**: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

  * ***One that silences it from 7pm to 9am daily on M-F,***
  * ***And one that silences it all day on Sat-Sun.***
  * ***Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.***

Go to the [manage downtime page](https://app.datadoghq.com/monitors#/downtime) on the Datadog Web Interface and select "Schedule Downtime"

Setup the nighttime downtime as per below.

![Night Downtime](/images/18-night-downtime.PNG)

Repeat to setup the weekend downtime as below.

![Weekend Downtime](/images/19-weekend-downtime.PNG)

The downtime list should look as follows.

![Downtime](/images/20-downtime.PNG)

The downtime messages.

![Downtime](/images/21-downtime-email.PNG)
![Downtime](/images/21-downtime-email2.PNG)

## Collecting APM Data:

### Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:

```python
from flask import Flask
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

Go to the [APM Intro page](https://app.datadoghq.com/apm/intro) and select [Get Started](https://app.datadoghq.com/apm/install)

Follow and select the appropriate language (in this case, Python) and follow the instructions.

![Python APM](/images/22-python-apm.PNG)

Install flask and ddtrace, then create the Python flask app using the provided script above, and finally launch the flask app using ddtrace.

*There was an issue with ddtrace being able to detect the 'six' package which was resolved by forcing an upgrade of the package 'setuptools'*
```bash
sudo apt-get remove python-setuptools -y
sudo pip install --upgrade setuptools
sudo pip install flask ddtrace
vim ~/flask_app.py
ddtrace-run python ~/flask_app.py
```

Then use curl to interact the with the flask app.
```bash
$ curl localhost:5050/
Entrypoint to the Application
$ curl localhost:5050/
Entrypoint to the Application
$ curl localhost:5050/api/apm
Getting APM Started
$ curl localhost:5050/api/trace
Posting Traces
$ curl localhost:5050/api/trace
Posting Traces
$ curl localhost:5050/api/trace
Posting Traces

```

Check the APM dashboard for the [Flask service](https://app.datadoghq.com/apm/service/flask/flask.request?end=1549464864418&env=none&paused=false&start=1549461264418)
![Flask APM](/images/23-flask-apm.PNG)


### **Bonus Question**: What is the difference between a Service and a Resource?

A service represents a whole application (e.g. the small Flask application used above) or a micro service (e.g. Auth service, tagging service, catalogue service). A resource is a component of a service, such as an api endpoint or a query (e.g. /api/trace in the above Flask app).

### Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

Below is a [dashboard](https://app.datadoghq.com/dashboard/yvj-byn-3in/infrastructure-and-apm-metrics?tile_size=m&page=0&is_auto=false&from_ts=1549461240000&to_ts=1549464840000&live=true) with some system metrics as well as APM metrics for the Flask service.

![Infrastructure and APM Dashboard](/images/24-apm-infrastructure.PNG)

Please include your fully instrumented app in your submission, as well.

[The app file is here.](/flask_app.py)

## Final Question:

### Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

***Is there anything creative you would use Datadog for?***

**There are a couple of creative uses I have for Datadog**

*The first would be to monitor and alert on the activity of our cats. We have two cats and a smart cat door. The cat door provides alerts when a cat goes in or out and if the cat looks out the door but doesn't go through. In the past I recognised a health issue with one of the cats when she started to spend less time outside than normal. I could see the anomoly engine being particularly useful as the cats have pretty typical schedules that they stick to. There could also be great opportunity to correlate the information against the other metrics such as the weather (temperature, rain, etc) and the internal environmental conditions of our house.*

*Another use would be for a computer game I play in my spare time, Elite: Dangerous (ED). ED has a very complex "background simulation" that constantly changes the the state of the populated systems. This covers numerous things such as factions, their influence in the system, the state of the system (Boom, Investment, War, etc). Lots of groups of players have their own faction in the game and use some 3rd party tools or complex spreadsheets to track the state of their faction. I could see lots of potential to use Datadog to provide dashboards and alerts to assist with the management of the background simulation for players of the game.*

