Your answers to the questions go here.

### Prerequisites - Setup the environment
I am using macOS Sierra Version 10.12.6 for this Challenge. I installed and set up Vagrant with VirtualBox as provider, since the virtualization platform best suited for vagrant is VirtualBox.
Here are the steps of installing Vagrant and set up VirtualBox.

# Installation process
Vagrant uses Virtualbox to manage the virtual dependencies. You can directly download virtualbox and install or use homebrew for it.

$ brew cask install virtualbox
Now install Vagrant either from the website or use homebrew for installing it.
<img src="https://github.com/zhang587/datadog_screenshots/blob/master/Virtual_Box_install.png" />
<img src="https://github.com/zhang587/datadog_screenshots/blob/master/virtual_box_manager.png" />
$ brew cask install vagrant
Vagrant-Manager helps you manage all your virtual machines in one place directly from the menubar.

$ brew cask install vagrant-manager

Now start the machine using the following command.
$ vagrant up

The datadog can be installed on OS X as:

```
DD_API_KEY=63ab065b2982aed65fff538ba18a93ba bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/dd-agent/master/packaging/osx/install.sh)"
```

# Sign up for Datadog
Use “Datadog Recruiting Candidate” in the “Company” field.

### Collecting Metrics

# Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

Change direction by type 'cd ~/.datadog-agent' in terminal, then type 'vim datadog.conf' to open and edit the configuration file.
<img src="https://github.com/zhang587/datadog_screenshots/blob/master/add_tags.png" />

After a few minutes refresh the Datadog, go to [_Infrastructure - Host Map_], the tags are now shown in there.
<img src="https://github.com/zhang587/datadog_screenshots/blob/master/tag_host_map.png" />

I initially ran into some issues with this. At first, I couldn't locate where the to add tags, since I was confused with what all the folders mean and what are the functionalities of each folder and it's files. To solve this issue, I double checked online documents about 'tagging'in the datadog website, [reference](https://docs.datadoghq.com/guides/tagging/), and was able to locate that tags exit in the conf file. The second issue I had was that the tags wouldn't display at first, the reason is that I didn't give it enough time for it to show up. I checked my host map right after I changed the config file. After I waited for a few minutes, it showed up.

# Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

I am using PostgreSQL for this part, for how to download and install the software PostgreSQL please refer to -> [Download PostgreSQL here](https://www.postgresql.org/download/)

Find the PostgreSQL API under [_Integrations-Integrations_](https://app.datadoghq.com/account/settings), click 'install', then click on 'Configuration' tab.
<img src="https://github.com/zhang587/datadog_screenshots/blob/master/integration.png" />

>Create a read-only datadog user with proper access to your PostgreSQL Server.
```
create user datadog with password 'password_for_datadog';
grant SELECT ON pg_stat_database to datadog;
```
I initially used MySQL, but I ran into issues about starting MySQL server. The error I got was 'Starting MySQL... ERROR! The server quit without updating PID file'. I searched this error message online, and found out the reason was that there were mysqld processes already before I tried starting the server, which means I need to use 'ps -ef|grep mysqld' to check if there are ongoing mysqld, and use 'kill -9 PID' to stop those ones, and then restart mysqld. 

However, there could be more errors once I solve this one, instead of keeping looking into it, I chose a rather more time efficient way: I switched to PostgresSQL.

I ran into some issues when I was trying to start the database server. 
<img src="https://github.com/zhang587/datadog_screenshots/blob/master/config_postgres.png" />
By searching error messages, I figured out how to configure my postgres to make the command lines provided in the Integration work.

To create a normal user and an associated database you need to type the following commands. The easiest way to use is to create a Linux / UNUX IDENT authentication i.e. add user tom to UNIX or Linux system first.
Type the following commands to create a UNIX/Linux user called tom:
# adduser tom
# passwd tom

You need to login as database super user under postgresql server. Again the simplest way to connect as the postgres user is to change to the postgres unix user on the database server using su command as follows:
# su - postgres

Type the following command
$ psql template1

OR
$ psql -d template1 -U postgres

After running all those commands, I was able to make the command lines provided in the Integration work.

>Configure the Agent to connect to the PostgreSQL server
>Edit `conf.d/postgres.yaml`
<img src="https://github.com/zhang587/datadog_screenshots/blob/master/postgres_yaml.png" />

>Restart the Agent

>Type `datadog-agent info` in Terminal to check states.
<img src="https://github.com/zhang587/datadog_screenshots/blob/master/postgres_checks.png" />

>Can also go to [_Dashboard-Dashboard List_](https://app.datadoghq.com/dash/list) to check whether it is working or not.

# Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

Here is `my_metric.py`:

```
from random import randint

from checks import AgentCheck

 class HelloCheck(AgentCheck):

    def check(self, instance):

        self.gauge('my_metric', randint(1,1000))
```
I ran into some problems at first, because I wasn't sure which folder should I put `my_metric.py` in. I put `my_metric.yaml` in the `/checks.d` folder instead of the `/conf.d` directory, and got the error message saying `Error: no valid check found`. I then realize that `/checks.d` was the wrong directory, and thus solved this issue.

# Change your check's collection interval so that it only submits the metric once every 45 seconds.

I did this by editing the `my_metric.yaml` file so that it specifies the collection interval:

```
init_config:
 instances:
    -   min_collection_interval: 45
```
If `min_collection_interval` is not specified, the check would run about every 15-20 seconds.

# Bonus Question Can you change the collection interval without modifying the Python check file you created?

Yes, the collection interval can be changed by changing the `min_collection_interval` in the `.yaml` configuration file.

### Visualizing Data

# Utilize the Datadog API to create a Timeboard

Here is my `timeboard.py`

```
from datadog import initialize, api
 
options = {"api_key": "76e7696c9a143d8f5111365fa4e61d26", "app_key":"21e7378eff399c099bc5da859a21df54962ac0a6" }
initialize(**options)
title = "Shay's Timeboard"
description = "Tracks my_metric"
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{*}"}
        ],
        "viz": "timeseries"
    },
    "title": "my_metric over time"
}, {
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:mongodb.database_size{role:database:mongodb}, 'basic', 3)"
             }],
        "viz": "timeseries"
    },
    "title": "Database size anomalies"
}, {
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{*}.rollup(sum, 3600)"}
        ],
        "viz": "timeseries"
    },
    "title": "Hourly Rollup Sum of my_metric"
}]

template_variables = [{
    "name": "i-0a9ff2c19f22d237a",
    "prefix": "host",
    "default": "host:i-0a9ff2c19f22d237a"
}]
 
read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)
```

Screenshot of timeboard:

<img src="https://github.com/zhang587/datadog_screenshots/blob/master/timeboard.png" />

# Bonus Question: What is the Anomaly graph displaying?

The anomaly graph uses an algorithm that compares the past behavior of a metric to its present behavior. For instance, if the database were growing in size by a constant rate, and that rate dropped off or fell unexpectedly, the anomaly monitor would alert.

### Monitoring Data

# Create a new monitor with Warning and Alerting threshold
<img src="https://github.com/zhang587/datadog_screenshots/blob/master/set_threshold.png" />

# Configure the monitor’s message
<img src="https://github.com/zhang587/datadog_screenshots/blob/master/configure_monitor_msg.png" />

To create and manage monitors, it's crucial to learn how to configure the monitor. Here is a useful reference: 
https://docs.datadoghq.com/monitors/notifications/?tab=is_alertis_warning.

# Screenshot of email notification
<img src="https://github.com/zhang587/datadog_screenshots/blob/master/trigger_notification.png" />

# Bonus Question: Scheduled downtime

Downtime hat silences it from 7pm to 9am daily on M-F: 
<img src= "https://github.com/zhang587/datadog_screenshots/blob/master/downtime_daily.png" />

Downtime hat silences it silences it all day on Sat-Sun: 
<img src= "https://github.com/zhang587/datadog_screenshots/blob/master/downtime_weekend.png" />

Screenshot of email: <img src= "https://github.com/zhang587/datadog_screenshots/blob/master/email_notification.png" />

### Collecting APM Data

To better understand how APM works, it's beneficial learn about flask and the Datadog tracing agent first. 

Here is the Dashboard screenshot:
<img src= "https://github.com/zhang587/datadog_screenshots/blob/master/dashboard.png" />

Here is the APM screenshot:
<img src= "https://github.com/zhang587/datadog_screenshots/blob/master/APM.png" />

Here is the instrumented app, 'apm_app.py'

```
import logging
import sys
import blinker as _
from ddtrace import tracer
from ddtrace.contrib.flask import TraceMiddleware
from flask import Flask

main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

app = Flask(__name__)
traced_app = TraceMiddleware(app, tracer, service="my-flask-app", distributed_tracing=False)

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
~                                                     
```
When I tried to run the flask application using my script, I got error message saying `ddtrace.writer - ERROR - cannot send services to localhost:8126: [Errno 111] Connection refused`. I then tried using the `dd-trace run command`, but it gave me the same error. I read about how to trouble shoot this error by reading https://docs.datadoghq.com/agent/troubleshooting/?tab=agentv6, and tailed the logs at /var/log/datadog/trace-agent.log. It gave me error saying `Error reading datadog.yaml: failed to parse yaml configuration: yaml: unmarshal errors: line 472: cannot unmarshal !!str 'enabled...' intconfig.traceAgent
`, I then figured that it's an error in datadog.yaml file. I fixed this issue in datadog.yaml file and it worked.


# Bonus Question: What is the difference between a Service and a Resource?

A service is a set of processes that work together to provide a feature set. For instance, a web application could consist of a webapp service and a database service. A resource is a particular action for a given service.


### Final Question

I like working out and being fit, and I think it would be very interesting to have Datadog to visualize various factors that might affect a person's fitness journey. Factors include:

-number of hours spent in the gym
-number of calories input
-metabolic rate
-magnesium intake
-vitamin D intake
-alcohol intake
-social media usage

It would be interesting to see those kinds of data display in the Datadog dashboard over years, and monitor changes in each factor, therefore people can have better sense of getting fit and healthy.
