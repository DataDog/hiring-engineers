# Sales Engineer Hiring Exercise
#### Michelle Bray January/February 2021

## Initial Setup
#### Install the VM (Ubuntu >= 16.04)
- Download & install Vagrant (64-bit MacOS)
    - https://www.vagrantup.com/downloads
    - Install using downloaded dmg
- Update my current install of VirtualBox (from 5.0 to 6.1)
    - https://www.virtualbox.org/wiki/Downloads
    - Install using downloaded dmg
- Ensure it is installed and recognized by your system
    - `which vagrant`
- Initialize virtual machine
    - `vagrant init ubuntu/xenial64`
- Ensure Vagrantfile at root of base specifies box to use
    - `config.vm.box = "ubuntu/xenial64"`
- Start the VM
    - `vagrant up`
- SSH into the VM (there is no GUI)
    - `vagrant ssh`
#### Sign up for DataDog trial
- Use Datadog Recruiting Candidate in Company field
- Install Ubuntu DataDog Agent
    - https://app.datadoghq.com/signup/agent#ubuntu
- Copy and paste the provided command into VM
    - Ubuntu agent commands, for reference:
        - https://docs.datadoghq.com/agent/basic_agent_usage/ubuntu/?tab=agentv6v7

## Collecting Metrics
#### Add tags to the config file
- Docs: https://docs.datadoghq.com/getting_started/tagging/
- Navigate to the datadog-agent directory and open the datadog.yaml file for editing
    - `cd /etc/datadog-agent`
    - `sudo vim datadog.yaml`
- Uncomment and add to `tags` parameter
```
## @param tags  - list of key:value elements - optional
## List of host tags. Attached in-app to every metric, event, log, trace, and service check emitted by this Agent.
##
## Learn more about tagging: https://docs.datadoghq.com/tagging/
#
tags:
#   - <TAG_KEY>:<TAG_VALUE>
  - hostname:michelle_vm
  - environment:dev
  - version:0.0.1
 ```
- Restart the agent
    - `sudo service datadog-agent restart`
- Check the agent’s status
    - `sudo service datadog-agent status`
#### Install database and respective DataDog integration
- Docs: https://docs.datadoghq.com/integrations/mysql/?tab=host
- MySQL:
    - `sudo apt-get install mysql-server`
    - Set root username and password when prompted
    - Start up MySQL:
        - `sudo /etc/init.d/mysql start`
- Add new datadog user
    - `CREATE USER 'datadog'@'localhost' IDENTIFIED WITH mysql_native_password by 'datadog';`
- Check user was created
    - `SELECT User, Host FROM mysql.user;`
- Grant user privileges
    - `ALTER USER 'datadog'@'localhost' WITH MAX_USER_CONNECTIONS 5;`
    - `GRANT PROCESS ON *.* TO 'datadog'@'localhost';`
- Add configuration to sudo vim mysql.d/conf.yaml
    - See screenshot
- Restart the agent
#### Custom agent check
- Docs: https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7
- `my_metric.py` at `/etc/datadog-agent/checks.d`
    - Modify classname, return, and tags
#### Update collection interval
- NOTE: The names of the configuration and check files must match. If your check is called mycheck.py, your configuration file must be named mycheck.yaml
- Create/edit my_metric.yaml at /etc/datadog-agent/conf.d
- Restart the agent
    - `sudo service datadog-agent restart`
- Verify my_metric check is running properly
    - `sudo -u dd-agent -- datadog-agent check my_metric`
#### Bonus
*Can you change the collection interval without modifying the Python check file you created?*

Yes, via the `min_collection_interval` parameter
```
## @param min_collection_interval - number - optional - default: 15
## This changes the collection interval of the check. For more information, see:
## https://docs.datadoghq.com/developers/write_agent_check/#collection-interval

min_collection_interval: 45
```

## Visualizing Data
#### Create a Timeboard
- Prep for DataDog package installation
    - Docs: https://docs.datadoghq.com/dashboards/timeboards/
    - By default, Ubuntu 16.04 ships in with Python 2.7 and Python 3.5
    - Install pip (Python package management system)
        - `sudo apt install python3-pip`
    - Check that it is installed
        - `pip3 --version`
    - Install Python DataDog package
        - `sudo python3 -m pip install datadog`
    - Create Application and API keys
        - Docs: https://docs.datadoghq.com/account_management/api-app-keys/
    - Create timeboard.py file for creating a new dashboard
        - Docs: https://docs.datadoghq.com/api/latest/dashboards/
    - Run the file
        - `python3 timeboard.py`
    - Update the dashboard's timeline in the upper right dropdown by selecting `Past 5 Minutes`
    - Send a notification by clicking the share icon in the upper right of the desired graph
#### My Dashboard
https://p.datadoghq.com/sb/o9xxm85zlcw7frpa-3c525608fec23e6bd3970ee99f450856
#### Bonus
*What is the Anomaly graph displaying?*

As per DataDog’s docs: https://docs.datadoghq.com/monitors/monitor_types/anomaly/
> Anomaly detection is an algorithmic feature that identifies when a metric is behaving differently than it has in the past, taking into account trends, seasonal day-of-week, and time-of-day patterns. It is well-suited for metrics with strong trends and recurring patterns that are hard to monitor with threshold-based alerting.

## Monitoring Data
#### Create a new Metric Monitor
- Docs: https://docs.datadoghq.com/monitors/monitor_types/metric/?tab=threshold
    - Warning threshold
        - Attach screenshot with markup
    - Alert threshold
        - Attach screenshot with markup
    - No Data window
        - Attach screenshot with markup
- Configure the monitor’s message
- Docs: https://docs.datadoghq.com/monitors/notifications/?tab=is_alert
```
@mbray1013@gmail.com

{{#is_alert}}
# **ALERT:** `my_metric` very high average for 5 minutes
## Reported average of {{value}} exceeds threshold of {{threshold}}

Click [here](https://app.datadoghq.com/dashboard/r6x-ckn-bay/mymetric-timeboard?from_ts=1612301431955&live=true&to_ts=1612301731955) for the relevant dashboard.
{{/is_alert}}

{{#is_warning}}
# **WARNING:** `my_metric` high average for 5 minutes
## Reported average of {{value}} exceeds threshold of {{warn_threshold}}

Click [here](https://app.datadoghq.com/dashboard/r6x-ckn-bay/mymetric-timeboard?from_ts=1612301431955&live=true&to_ts=1612301731955) for the relevant dashboard.
{{/is_warning}}

{{#is_no_data}}
# **No data** from `my_metric` for 10 minutes

Click [here](https://app.datadoghq.com/dashboard/r6x-ckn-bay/mymetric-timeboard?from_ts=1612301431955&live=true&to_ts=1612301731955) for the relevant dashboard.
{{/is_no_data}}
```
#### Bonus
*Set up two scheduled downtimes for this monitor.*
- 7 PM - 9AM every weekday
```
@mbray1013@gmail.com 

# DOWNTIME SCHEDULED: **7 PM - 9AM** ***M, T, W, Th, F***
## High Average Thresholds for Metric my_metric on Host michelle_vm

Your new downtime is scheduled for `High Average Thresholds for Metric my_metric on Host michelle_vm`.
This repeats weekly from 7 PM to 9AM every Monday, Tuesday, Wednesday, Thursday, and Friday.
```
- All day on weekends
```
@mbray1013@gmail.com 

# DOWNTIME SCHEDULED: **ALL DAY** ***Sat, Sun***
## High Average Thresholds for Metric my_metric on Host michelle_vm

Your new downtime is scheduled for `High Average Thresholds for Metric my_metric on Host michelle_vm`.
This repeats weekly every Saturday and Sunday.
```

## Collecting APM Data
- Docs: https://app.datadoghq.com/apm/docs?architecture=host-based&language=python
#### Install required packages and frameworks
- Upgrade pip (ensure you are on Python >= 3.6)
    - `pip3 install --upgrade pip`
- Install DataDog APM Package
    - `python3 -m pip install ddtrace`
- Install Flask (web framework)
    - `python3 -m pip install flask`
#### Create and run a simple Flask app
- Create `apm_flask_app.py` with provided script on host
- Run with the following command:
    - `DD_SERVICE="apm_flask_app" DD_ENV="dev" DD_LOGS_INJECTION=true DD_PROFILING_ENABLED=true ddtrace-run python3 apm_flask_app.py --port=5050`
#### Create traffic
- Hit each endpoint a handful of times to create traffic
    - `curl 0.0.0.0:5050`
    - `curl 0.0.0.0:5050/api/trace`
    - `curl 0.0.0.0:5050/api/apm`
#### My Dashboards
- Navigate to APM -> Services and update filter to search for `env:dev` (default is `env:none`)
- Continuous Profiler dashboard
    - https://p.datadoghq.com/sb/o9xxm85zlcw7frpa-f5c5f60de887d9451f4a8009bb027029
- Tracing Analytics dashboard
    - https://p.datadoghq.com/sb/o9xxm85zlcw7frpa-08b83e21d8beb6f5bb498717bba831cb
- Created a custom, cumulative dashboard as well
    - https://p.datadoghq.com/sb/o9xxm85zlcw7frpa-e97602418ef77ca26de0a4874038d7cf
#### Bonus
*What is the difference between a Service and a Resource?*

As per DataDog’s docs: https://docs.datadoghq.com/tracing/visualization/resource/
  https://docs.datadoghq.com/tracing/visualization/#services
> A resource is a particular action for a given service (typically an individual endpoint or query).
>
> Services are the building blocks of modern microservice architectures - broadly a service groups together endpoints, queries, or jobs for the purposes of scaling instances. Some examples:
> - A group of URL endpoints may be grouped together under an API service.
> - A group of DB queries that are grouped together within one database service.
> - A group of periodic jobs configured in the crond service.

## Final Question
*Is there anything creative you would use Datadog for?*

I think DataDog would prove as an ideal service when building a data pipeline.  More specifically, it would have proven 
invaluable when standing up a cryptocurrency market data pipeline at my last company.  As a startup, we implemented our 
own monitoring, alerting, and dashboard landing page, but pivoting to a solution like DataDog should have been on our 
road map.  Not only would it allow engineers to monitor the health of data streams, but customers could also ensure that
our SLA of near-real-time, accurate, and complete data is being met.  Data scientists could alert on the actual values 
coming through each stream if outliers are present, and even use patterns to predict future trends.  
It would also be interesting to leverage patterns and alert thresholds to auto size up or spin down machines as traffic 
spikes.  Oftentimes, when there is a big jump or fall in the price of an asset, exchanges will experience much higher traffic and
volume of trades.  This would ensure that infrastructure can keep up with demand when stressed, but also spin down 
unused resources and save money when under-utilized.
