#
# Prerequisites - Setup the environment

You can utilize any OS/host that you would like to complete this exercise. However, we recommend one of the following approaches:

* You can spin up a fresh linux VM via Vagrant or other tools so that you don’t run into any OS or dependency issues. [Here are instructions](https://github.com/DataDog/hiring-engineers/blob/solutions-engineer/README.md#vagrant) for setting up a Vagrant Ubuntu VM. We strongly recommend using minimum `v. 16.04` to avoid dependency issues.
* You can utilize a Containerized approach with Docker for Linux and our dockerized Datadog Agent image.

Then, sign up for Datadog (use “Datadog Recruiting Candidate” in the “Company” field), get the Agent reporting metrics from your local machine.

__Fork DataDog/hiring-engineers Repo__
 * Goto Master Repo and Click Fork https://github.com/DataDog/hiring-engineers
 * mkdir ~/Documents/Datadog
 * cd ~/Documents/Datadog
 * git clone https://github.com/paterrell/hiring-engineers.git

__Checkout solution-engineer branch__
* cd ~/Documents/Datadog/hiring-engineers
* git branch -a (list all branches in DataDog Repo)
* git checkout remotes/origin/solutions-engineer

__Installed VirtualBox on macOS__   
* [Download VirtualBox](https://download.virtualbox.org/virtualbox/6.0.4/VirtualBox-6.0.4-128413-OSX.dmg)

__Installed Vagrant on macOS__  
* [Download Vagrant](https://releases.hashicorp.com/vagrant/2.2.4/vagrant_2.2.4_x86_64.dmg)

__Spin up and update VM__
* mkdir vagrant
* vagrant init ubuntu/xenial64
* Edit the Vagrantfile
![Vagrantfile Edit](/images/edit1.png)
* vagrant up

__Sign up for Datatdog__
* [Sign up for Datadog - Yeah](https://app.datadoghq.com/signup/agent#ubuntu)
* vagrant ssh
* Run the provided install_script.sh with DD_API_KEY

# Collecting Metrics

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
__Add Tags__

  * cd /etc/datadog-agent
  * sudo vim datadog.yaml
  * uncomment tags: and make additions
  __datadog-agent/datadog.yaml__
  ![Added Host Tags](/images/hosttags.png)
  * sudo service datadog-agent restart
  * Check UI to see newly added Host Tags
  __Added Host Tags Shown__
  ![Added Host Tags](/images/hosttagsui.png)


* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
  __Install Postgresql Database__
  * Edit Vagrantfile and Update Shell Adding Database Scripts
  * vagrant up --provision

  __Install Database Integration__
  * vagrant ssh
  * sudo -i -u postgres
  * psql
  ```create user datadog with password 'password';```
  ```grant SELECT ON pg_stat_database to datadog;```
  * Check Installation Integration
  ```psql -h localhost -U datadog postgres -c "select * from pg_stat_database LIMIT(1);" && \```
  ```echo -e "\e[0;32mPostgres connection - OK\e[0m" || \```
  ```echo -e "\e[0;31mCannot connect to Postgres\e[0m"```
  * enter password

  __Configure the Agent to connect to the Postgresql server__
  * cd /etc/datadog-agent/conf.d/postgres.d
  * sudo cp conf.yaml.example conf.yaml
  * sudo vim conf.yaml (add datadog user password)
  * sudo service datadog-agent restart
  * sudo service datadog-agent status (check for postgres)

* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
 __Create Custom Agent Check that submits random Metric__
 * sudo vim /etc/datadog-agent/conf.d/custom_my_metric.yaml
 * set the instance sequence
 * sudo vim /etc/datadog-agent/checks.d/custom_my_metric.py
 * add random int class in code
 * sudo service datadog-agent restart
 * sudo -u dd-agent -- datadog-agent check custom_my_metric


* Change your check's collection interval so that it only submits the metric once every 45 seconds.

 __Change the Agent Check interval to 45 seconds__
 * sudo vim /etc/datadog-agent/conf.d/custom_my_metric.yaml
 * add sequence min_collection_interval
 * sudo service datadog-agent restart
 * sudo -u dd-agent -- datadog-agent check custom_my_metric


* Can you change the collection interval without modifying the Python check file you created?

 __Bonus Question__
 * you could use [datadog-agent](https://github.com/DataDog/datadog-agent/blob/master/pkg/collector/check/check.go) DefaultCheckInterval
  * you could use the default metric limit using datadog api class AgentCheckPy2

# Visualizing Data
__Create a Timeboard__
Utilize the Datadog API to create a Timeboard that contains:

* Create and tag a new api key
[Manage your account’s API and application keys.](https://app.datadoghq.com/account/settings#api)
* add the custom metric scoped over your host
 * create my_timeboard.json
 * add my_metric scope
 * execute curl -X POST listed below
* add any metric from the Integration on your Database with the anomaly function applied
 * edit my_timeboard.json
 * add postgres metric system.net.bytes_rcvd for anomaly detection
 * execute curl -X POST again
* add rollup function applied to sum up all the points for the past hour into one bucket for my_metric
 * edit my_timeboard.json
 * add sum rollup funciton to my_metric
 * execute curl -X POST again
__my_timeboard.json code__
 ```
 {
   "title": "My Timeboard",
   "widgets": [{
     "definition": {
       "type": "timeseries",
       "requests": [{
           "q": "avg:my_metric{host:terrellea}"
         },
         {
           "q": "anomalies(avg:system.net.bytes_rcvd{*}, 'basic', 1)"
         },
         {
           "q": "sum:my_metric{host:terrellea}.rollup(sum, 3600)"
         }
       ],
       "title": "My Metric scope over my host"
     }
   }],
   "layout_type": "ordered",
   "description": "A dashboard with My Random Metric and Postgres Network Bytes Received",
   "is_read_only": true,
   "notify_list": ["mordac@domain.com"],
   "template_variables": [{
     "name": "terrellea",
     "prefix": "exercise-host",
     "default": "my-future-job"
   }]
 }
```
__CURL API CALL__
```
curl -X POST -H "Content-type: application/json" -d /
"@my_timeboard.json" "https://api.datadoghq.com/api/v1/dashboard?api_key= /
${DD_API_KEY}&application_key=${DD_APP_KEY}"
```
* Set the Timeboard's timeframe to the past 5 minutes
* Take a snapshot of this graph and use the @ notation to send it to yourself.
* **Bonus Question**: What is the Anomaly graph displaying?
![Notification1](/images/notification1.png)

# Monitoring Data
Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

* Warning threshold of 500
* Alerting threshold of 800
* And also ensure that it will notify you if there is No Data for this query over the past 10m.

Please configure the monitor’s message so that it will:

* Send you an email whenever the monitor triggers.
* Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
* Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
* When this monitor sends you an email notification, take a screenshot of the email that it sends you.
![FirstAlert](/images/notification2.png)

* **Bonus Question**: Set up two scheduled downtimes for this monitor:
  * One that silences it from 7pm to 9am daily on M-F,
  * And one that silences it all day on Sat-Sun.
  * email scheduled downtime to team

![FirstDowntime](/images/notification3.png)

![SecondDowntime](/images/notification4.png)

## Collecting APM Data:

* Install Flask app using Python and instrument this using Datadog’s APM solution
* Edit the Vagrantfile
* Install python
* Install pip
* pip install Flask
* Enable logging in the agents configuration by uncommenting logs_enabled: true
* mkdir /etc/datadog-agent/conf.d/python.d
* cd /etc/datadog-agent/conf.d/python.d
* vim conf.yaml
* chown -R dd-agent:dd-agent conf.d/python.d/
* touch /var/log/my-log.json
* chown dd-agent:dd-agent /var/log/my-log.json
* pip install ddtrace
* pip install json_log_formatter


* **Bonus Question**: What is the difference between a Service and a Resource?
  * "service" is the top level application or microservice
  * "resource" is a specific quantifiable component of that service.

* Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.
 * [Flask APM and Infrastructure Timeboard](https://app.datadoghq.com/dashboard/65t-3qc-2jk?tile_size=l&page=0&is_auto=false&from_ts=1552788615000&to_ts=1552789515000&live=true)

 * ![apminfra](/images/apminfra.png)

## Final Question:
Is there anything creative you would use Datadog for?
__Event Correlation__

# APM References
* [Quick Start](http://pypi.datadoghq.com/trace/docs/installation_quickstart.html)
* [Monitoring Flask](https://www.datadoghq.com/blog/monitoring-flask-apps-with-datadog/)
* [Tracing Flask Code](https://www.datadoghq.com/blog/monitoring-flask-apps-with-datadog/#tracing-your-code)
* [Log Collection](https://docs.datadoghq.com/logs/log_collection/python/?tab=json_logformatter)
