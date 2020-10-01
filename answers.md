# Datadog Enterprise Sales Engineer Assignment - Los Angeles
**Prerequisites - Setup the environment**

You can utilize any OS/host that you would like to complete this exercise. However, we recommend one of the following approaches:

I downloaded Vagrant 2.2.10 for Mac OSX 64-bit. Added Vagrant Box xenial64 to utilize Ubuntu 16.04.
Installed the agent with the documentation provided [here.](https://app.datadoghq.com/signup/agent#ubuntu)

You can spin up a fresh linux VM via Vagrant or other tools so that you don’t run into any OS or dependency issues. Here are instructions for setting up a Vagrant Ubuntu VM. We strongly recommend using minimum v. 16.04 to avoid dependency issues.
You can utilize a Containerized approach with Docker for Linux and our dockerized Datadog Agent image.
Then, sign up for Datadog (use “Datadog Recruiting Candidate” in the “Company” field), get the Agent reporting metrics from your local machine.

```
$ datadog-agent version
Agent 7.22.1 - Commit: 6f0f0d5 - Serialization version: v4.40.0 - Go version: go1.13.11

```

**Collecting Metrics**

Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
The documentation I followed for this section can be found [here](https://docs.datadoghq.com/getting_started/tagging/)
I navigated to ```/etc/datadog-agent/datadog.yaml``` and navigated to @param tags and added the following:
```

#tags:
# -environment:dev
# -project:solutionsengineerassignment

```
I restarted Agent running as a service ```sudo service datadog-agent restart``` For agent usage specific to Ubuntu, I followed the documentation [here](https://docs.datadoghq.com/agent/basic_agent_usage/ubuntu/?tab=agentv6v7)

 ![Tags](https://github.com/jasondunlap/hiring-engineers/blob/master/DD_tags.png) 

   
Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
I chose to install MySQL database with the following steps
```
$ sudo apt-get update
$ sudo apt-get install mysql-server
$ mysql_secure_installation

```
I followed [these](https://docs.datadoghq.com/integrations/mysql/?tab=host) steps in regards to the Datadog integration.
```

mysql> CREATE USER 'datadog'@'localhost' IDENTIFIED BY 'JasonPW;

mysql -u datadog --password=JASONPW -e "show status" | \
grep Uptime && echo -e "\033[0;32mMySQL user - OK\033[0m" || \
echo -e "\033[0;31mCannot connect to MySQL\033[0m"
# The Agent needs a few privileges to collect metrics. Grant the user the following limited privileges ONLY:
mysql> GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'localhost' WITH MAX_USER_CONNECTIONS 5;
Query OK, 0 rows affected, 1 warning (0.00 sec)

mysql> GRANT PROCESS ON *.* TO 'datadog'@'localhost';
Query OK, 0 rows affected (0.00 sec)

```
After that I updated the configuration file located at ```/etc/datadog-agent/conf.d/mysql.d/conf.yaml```

```

init_config:

instances:
- host: localhost
  user: datadog
  pass: "JasonPW" # replace and update with your password
  port:  3306
  options:
    replication: false
    galera_cluster: true
    extra_status_metrics: true
    extra_innodb_metrics: true
    extra_performance_metrics: true
    schema_size_metrics: false
    disable_innodb_metrics: false

   ```

 Restart the agent and you can go to Metrics Explorer to view MySQL

   ![MySQL](https://github.com/jasondunlap/hiring-engineers/blob/master/mysql.png)
   ![Metrics Explorer](https://github.com/jasondunlap/hiring-engineers/blob/master/metricsexplorer_mysql.png)


Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
Change your check's collection interval so that it only submits the metric once every 45 seconds.

I went to ```/etc/datadod-agent/checks.d/``` and create the file ```my_metric.py``` which you can see below. 

```

#!/usr/bin/python

import random

from datadog_checks.base import AgentCheck

__version__ = '1.0.0'


class My_Metric(AgentCheck):

    def check(self, instance):
       self.gauge('my_metric', random.randrange(0, 1000),
        tags = ['TAG_KEY:TAG_VALUE'])

```
```/etc/datadog/conf.d/my_metric.yaml```
```

init_config:

instances:
  - min_collection_interval: 45

  ```
I found this [tutorial](https://docs.datadoghq.com/developers/metrics/agent_metrics_submission/?tab=count) and this [one.](https://datadoghq.dev/summit-training-session/handson/customagentcheck/)
[Writing a Custom Agent Check](https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7) has everything you need to help with the python script. 

Finally, to double check everything is working ok, run ```sudo -u dd-agent -- datadog-agent check my_metric```

```

    Running Checks
    ==============
    
    my_metric (1.0.0)
    -----------------
      Instance ID: my_metric:5ba864f3937b5bad [OK]
      Configuration Source: file:/etc/datadog-agent/conf.d/my_metric.yaml
      Total Runs: 1
      Metric Samples: Last Run: 1, Total: 1
      Events: Last Run: 0, Total: 0
      Service Checks: Last Run: 0, Total: 0
      Average Execution Time : 0s
      Last Execution Date : 2020-09-30 23:51:30.000000 UTC
      Last Successful Execution Date : 2020-09-30 23:51:30.000000 UTC

      And you can go to Metrics > Explore in the Datadog Dashboard and see it works

      ```


   ![My_Metric](https://github.com/jasondunlap/hiring-engineers/blob/master/my_metric.png)

Bonus Question Can you change the collection interval without modifying the Python check file you created?

**Visualizing Data**
Utilize the Datadog API to create a Timeboard that contains:

Your custom metric scoped over your host.
Any metric from the Integration on your Database with the anomaly function applied.
I found MySQL integrations in Python [here.](https://github.com/DataDog/integrations-core/blob/master/mysql/datadog_checks/mysql/mysql.py) [This](https://www.datadoghq.com/blog/monitoring-mysql-performance-metrics/) blog post was very helpful as well. 
Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard. 

Prior to running the Python script, you need to complete a few steps to setup your environment on your Vagrant box. 
1. ```apt-get update```
2. ```curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"```
3. ```python get-pip.py```
4. Verify pip is installed correctly ```pip --version``` ```pip 20.2.3 from /home/vagrant/.local/lib/python3.5/site-packages/pip (python 3.5)```
5. ```pip install datadog```

Once all the above is setup, you execute the Python script ```python3 datadogdashboard.py```
```

from datadog import initialize, api

options = {
    'api_key': 'API Key Hidden',
    'app_key': 'App Key Hidden'
}
initialize(**options)

title= "Visualizing Data"
widgets= [
{
  "definition":{
      "type":"timeseries",
      "requests": [
          {
      
              "q":"avg:my_metric{*}"
          }
      ],
      "title":"my_metric_average"
  }
},
{
    "definition":{
        "type":"timeseries",
        "requests":[
            {
       
        # change this 
                "q":"anomalies(avg:mysql.performance.cpu_time{*},'basic',2)"
            }
        ],
        "title":"anomolies cpu function"
    }
},
{
    "definition":{
        "type":"timeseries",
        "requests":[
            {
       
                "q":"avg:my_metric{*}.rollup(sum,3600)"
            }
        ],
        "title":"my_metric rollup"
    }
}
]

layout_type = 'ordered'
description = 'the dashboard exercise'
is_read_only = True
notify_list = ['dunlap.jason@gmail.com']


api.Dashboard.create(title=title,
                     widgets=widgets,
                     layout_type=layout_type,
                     description=description,
                     is_read_only=is_read_only,
                     notify_list=notify_list) 

                     ```
The code example for the Python script is located [here](https://docs.datadoghq.com/api/v1/dashboards/)

I created my Application and API keys from the Datadog dashboard, Under Integrations > [API's.](https://app.datadoghq.com/account/settings#api)

Once this is created, access the Dashboard from your Dashboard List in the UI:

![Dashboard List](https://github.com/jasondunlap/hiring-engineers/blob/master/data.png)

Set the Timeboard's timeframe to the past 5 minutes
Take a snapshot of this graph and use the @ notation to send it to yourself.
Bonus Question: What is the Anomaly graph displaying?
Monitoring Data
Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

Warning threshold of 500
Alerting threshold of 800
And also ensure that it will notify you if there is No Data for this query over the past 10m.
Please configure the monitor’s message so that it will:

Send you an email whenever the monitor triggers.

Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.

Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.

When this monitor sends you an email notification, take a screenshot of the email that it sends you.

Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

One that silences it from 7pm to 9am daily on M-F,
And one that silences it all day on Sat-Sun.
Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.
**Collecting APM Data**
Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:

```from flask import Flask
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

Note: Using both ddtrace-run and manually inserting the Middleware has been known to cause issues. Please only use one or the other.
I used ddtrace-run

Bonus Question: What is the difference between a Service and a Resource?

Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

Please include your fully instrumented app in your submission, as well.

**Final Question**
Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?

Instructions
If you have a question, create an issue in this repository.

To submit your answers:

Fork this repo.
Answer the questions in answers.md
Commit as much code as you need to support your answers.
Submit a pull request.
Don't forget to include links to your dashboard(s), even better links and screenshots. We recommend that you include your screenshots inline with your answers.


