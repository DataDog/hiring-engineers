# Edwin Zhou
Solutions Engineer

Technical Exercise

## Setting Up the Environment
I used Oracle's VirtualBox as my virtual machine environment, since it is already conveniently installed on my computer to complete previous projects.

[Click here to install Ubuntu v17.10.](http://releases.ubuntu.com/17.10/ubuntu-17.10.1-desktop-amd64.iso)

In VirtualBox, select *New*, set *Type* to 'Linux' and set *Version* to 'Ubuntu(64-bit)'. I recommend giving the virtual machine 2 GB RAM. 

![Virtual Box Create VM](/img/virtualbox-1.png)

Press *Create*.

If your computer specifications permits, I recommend adding additional threads to the VM, increasing video memory to 128 MB, and enabling 3D acceleration. This will greatly increase the performance of the virtual machine and alleviate much frustration due to frame drops and unresponsiveness. 

![More Cores](/img/more-cores.png)
![More Video](/img/more-video.png)

Launch your Ubuntu virtual machine. You will be prompted to select an Ubuntu image. Select `ubuntu-17.10.1-desktop-amd64.iso` in your downloads directory.

![Virtual Box Create VM](/img/virtualbox-2.png)

Select *Install Ubuntu*.

![Virtual Box Create VM](/img/virtualbox-3.png)


## Installing the Agent
The Datadog Agent is software that is active on a host, and its purpose is to collect metrics and data, and display them on Datadog for analysis.

Create your account on Datadog.

We must first install curl:
```
sudo apt install curl
```

In the Linux termnal, run:

```
DD_API_KEY=YOUR_API_KEY bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```

[Your API key can be found here](https://app.datadoghq.com/account/settings#api)

The Datadog agent should have started on its own, if not, run:
```
sudo service datadog-agent start  
```

## Collecting Metrics

### Adding Tags
In order add tags to your host we must access the `datadog.yaml` file under `/etc/datadog-agent/`. Inside this configuration file we may add tags under the `tag:` key beginning on line 35.

```yaml
/etc/datadog-agent/datadog.yaml

...
# Add new tags here
tags:
  - "custom-tag"
  - "custom-tag-2"
...
```
Host tags on host in host map:

![Host Tags](/img/host-tags.png)

#### Restarting your agent
After adding the tags here, restart the agent using:
```
sudo service datadog-agent restart
```
---
### Setting Up PostgreSQL on Ubuntu v17.10
PostgreSQL is an open source, relational database. We will be using Datadog to monitor the activity on our Postgres database.

**NOTE:** You may be prompted to install libicu55 when performing `apt-get install postgresql-10`. [Visit here to download libicu55 for Ubuntu v17.10.](https://packages.ubuntu.com/en/xenial/amd64/libicu55/download)

From the downloads directory, run:
```
sudo dpkg -i ./libicu55_55.1-7ubuntu0.4_amd64.deb
```
---
#### Installation
First we must update add the apt repository. To do that, create a file `/etc/apt/sources.list.d/pgdg.list` and add the following line:
```
deb http://apt.postgresql.org/pub/repos/apt/ xenial-pgdg main
```

Next, import the repository signing key and update the package lists.
```
> wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
> sudo apt-get update
```

To install PostgreSQL, run:
```
sudo apt-get install postgresql-10
```
**Note the above notice if you run into the `libicu55` error.**

Run the command:
```
sudo -u postgres -i psql
```

To create the `datadog` role, run:
```
create user datadog with password 'your_password';
grant SELECT ON pg_stat_database to datadog;
```


Now we must access our PostgreSQL `conf.d` file under `/etc/datadog-agent/conf.d/postgres.d/conf.yaml` and add the following lines:
```yaml
init_config:

instances:
   -   host: localhost
       port: 5432
       username: datadog
       password: your_password
       tags:
            - optional_tag1
            - optional_tag2
```

[Restart your agent.](#restarting-your-agent)

To verify that the database is integrated into Datadog, run `sudo -u dd-agent -- datadog-agent check postgres`.

You should receive the following snippet as the result if setup successfully:
```
  Running Checks
  ==============
    postgres
    --------
      Total Runs: 1
      Metrics: 14, Total Metrics: 14
      Events: 0, Total Events: 0
      Service Checks: 1, Total Service Checks: 1
      Average Execution Time : 110ms
```
---
### Creating a Custom Agent
Agent checks can be used to collect custom metrics from our own applications. If an integration doesn't exist for the application we wish to implement, then we must create our own agent.

To create a custom agent, make a new check `my_metric.py` in `/etc/datadog-agent/checks.d/`

In `my_metric.py`, insert the following code:
```python
from checks import AgentCheck
import random

class CustomCheck(AgentCheck):
  def check(self, instance):
    self.gauge('my_metric', random.randrange(1000), tags=['my_metric_tag'])

```
This check will submit a metric with a random value from 0 to 1000.

Then, make a new configuration directory for your new check. Note that the name of the new check must match the name of the new directory, in this case `my_metric`.
```
mkdir /etc/datadog-agent/conf.d/my_metric.d/
```
Create a new configuration file named `conf.yaml` in this folder.
In `conf.yaml`, insert the following:
```yaml
init_config:

instances:
  - min_collection_interval: 45
```
[Restart your agent.](#restarting-your-agent)

**Bonus Question** Can you change the collection interval without modifying the Python check file you created?

This configuration will change the collection interval of the check to occur once every 45 seconds.


## Visualizing Data
Timeboards are used to visualize metrics that are collected and displayed synchronously. Here, we will create several timeboards using the Datadog API. 

Using the Datadog API, we can send requests to create timeboards without needing to access the application itself.

First, we create a virtual environment in order to isolate our Python environment, and to prevent interference with other projects we may have.

We must install virtualenv,
```
sudo apt install virtualenv
```


Next, go to your desired directory of your project, and create the virtualenv.
```
virtualenv venv
```


Now activate the virtual environment
```
source venv/bin/activate
```



We can now install the Datadog package into our environment.
```
pip install datadog
```


[This Python script will create three custom metrics:](https://github.com/edzh/hiring-engineers/blob/Edwin-Zhou/scripts/visualizing.py)
* my_metric scoped over the host.
* A metric from PostgreSQL called postgres.bgwriter.checkpoints_timed with the anomaly function applied.
* my_metric with the rollup function applied that sums up all of the points for the hour into one bucket.
![New timeboards](/img/new-timeboards.png)

New timeboard of my_metric over 5 minutes created posted on the events page.
![Timeboard graph 5 minutes](/img/notified-to-events.png)

**Bonus Question**: What is the Anomaly graph displaying?

The anomaly graph displays the number of scheduled checkpoints called within the database, and indicates in red deviations from expected data with the anomaly algorithm.

![Postgres Anomaly Graph](/img/anomaly-graph.png)

## Monitoring Data
Monitors in Datadog allow us to keep active track of metrics provide alerts when the metrics provided reach a certain, user-determined criteria.

We will now create a new monitor that monitors the data from my_metric, and sends a warning when the average value exceeds 500, an alert when the average value exceeds 800, and notify us if no data is sent for 10 minutes.

To create a new monitor, in the Datadog application, go to Monitor->New Monitor and select 'Metric'.
![New Monitor Page](/img/new-metric-monitor-page.png)

1. Under 'metric', select 'my_metric'. Select your host. 
![New Metric 1](/img/new-monitor-1.png)
2. Set the *Alert Threshold* to '800'. 
3. Set the *Warn Threshold* to '500'. 
![New Metric 2](/img/new-monitor-2.png)
4. Change *Do not notify* to 'notify' if data is missing. It will notify every 10 minutes by default.
![New Metric 3](/img/new-monitor-3.png)
5. Type in your name in the *Notify your team* input bar.
6. Add the tags 'my_metric' and your host name to the tags bar.
![New Metric 4](/img/new-monitor-4.png)
7. Press save.


Here is an example email you will receive.

![Monitor Email](/img/monitor-email.png)
---
### Managing downtime - Bonus Question
We will create two schedule downtimes, one that silences the my_metric monitor from 7pm to 9am from Monday to Friday, and another that silences the my_metric monitor all day Saturday and Sunday.

First, go to Monitors->Manage Downtime and select *Schedule Downtime*.

Set both scheduled downtimes to monitor your newly created monitor under the monitor's host.

#### Weekday Schedule
Under *Schedule* click *Recurring* and set a schedule to repeat weekly. Check Monday to Friday. Begin the downtime at 7PM, and make the duration 14 hours. 
![Weekday monitor](/img/weekday-monitor.png)

Here is the email you will receive after setting up the downtime:
![Downtime Email](/img/downtime-email.png)

#### Weekend Schedule
Under *Schedule* click *Recurring* and set a schedule to repeat weekly. Check Saturday and Sunday Begin the downtime at 12AM, and make the duration 24 hours. 
![Weekend monitor](/img/weekend-monitor.png)

Here is the email you will receive after setting up the downtime:
![Downtime Email 2](/img/downtime-email-2.png)

## Collecting APM data
The Datadog APM allows us to collect insight on our applications performance. We can trace our application and monitor key metrics such as latency, request time, and request volume.

To collect data from a Flask application, we must install the middleware into the application `app.py`.

To install the middleware, we must add:
```python
from ddtrace import tracer
from ddtrace.contrib.flask import TraceMiddleware
import blinker as _
```
and create a TraceMiddleware object after initializing the app:
```
traced_app = TraceMiddleware(app, tracer, service="my-flask-app", distributed_tracing=False)
```
Next, we must install ddtrace using: `pip install ddtrace` and blinker using: `pip install blinker`.

Finally, run
```
python app.py
```
and return to your APM page on the Datadog application.

[Here is the application.](https://github.com/edzh/hiring-engineers/blob/Edwin-Zhou/scripts/app.py)

**Bonus Question**: What is the difference between a Service and a Resource?

A service is a set of processes that do the same job, such as a database, webapp, or an api. A resource is an action of a service. It can be an endpoint or a query.

Table of services:
![Services](/img/services.png)

Table of resources:
![Resources](/img/resources.png)

## Final Question:
*Is there anything creative you would use Datadog for?*

The Rubik's Cube competitive industry has been rapidly growing for the past decade. With a growing competitive body, the demand for competitions steadily increases, as does the demand for tools that simplify competitions. For a Rubik's Cube competition to be successfully run, competition organizers must be able to micromanage groups of people, the staff and volunteers, and the competitors. However, competitions often run behind schedule. We will provide organizers, staff, and competitors an application that will simplify the competing experience. The application will enhance their experience by providing powerful tools that automate tedious tasks, increase volunteer responsibility, and maintain communication between different roles. Across many competitions, we can use Datadog coupled with this application to collect metrics on each of these groups, and track when these groups are most inactive in given times. We can then develop solutions or improve tools to further mitigate downtime in order for competitions to coordinate more smoothly and on schedule.