## Andrew Kang - Sales Engineer - Technical Exercise

**Table of Contents

1- Prerequisites - Setup the environment
2- Collecting Metrics
3- Visualizing Data
4- Monitoring Data
5- Collecting APM Data
6- Final Question

[TechnicalExerciseReference](https://github.com/DataDog/hiring-engineers/tree/solutions-engineer)

## Prerequisites - Setup the environment

For the environment, I setup a Vagrant Ubuntu VM.
[Vagrant Reference](https://learn.hashicorp.com/collections/vagrant/getting-started)

Download & Install Vagrant & VirtualBox
'''
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
sudo apt-get update && sudo apt-get install vagrant
vagrant init hashicorp/bionic64
vagrant up
vagrant ssh
'''

Next we signed up for a trial Datadog account at https://www.datadoghq.com/, using “Datadog Recruiting Candidate” in the “Company” field.

Finally we installed and configured the Agent and APT packages to get the reporting metrics from our local machine.

DD_AGENT_MAJOR_VERSION=7 DD_API_KEY=310b7c445032127de65454610fdcf581 DD_SITE="datadoghq.com" bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_script.sh)"

[AgentReference](https://app.datadoghq.com/signup/agent)

![agent](photos/agent.png)

## Collecting Metrics:

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

'''
sudo vim /etc/datadog-agent/datadog.yaml

tags:
    -name:Andrew
    -born:1989
    -goodcandidate:yes
    -hair:no
    
sudo systemctl restart datadog-agent.service
'''

![tags1](photos/tags1.png)    
![tags](photos/tags.png)

* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

For the Database, I setup MySQL for Ubuntu on Vagrant. The MySQL check is included in the Datadog Agent package, no additional installation was needed on our MySQL server. We started out by creating a database user for the Datadog Agent and granted the permissions.

'''
sudo mysql
mysql> CREATE USER 'datadog'@'127.0.0.1' IDENTIFIED with mysql_native_password BY 'datadawg';
mysql> GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'127.0.0.1' WITH MAX_USER_CONNECTIONS 5;
mysql> GRANT PROCESS ON *.* TO 'datadog'@'127.0.0.1';
mysql> show databases like 'performance_schema';
mysql> GRANT SELECT ON performance_schema.* TO 'datadog'@'127.0.0.1';
'''

[MySQLReference](https://docs.datadoghq.com/integrations/mysql)

Next we created the configuration file, /etc/datadog-agent/conf.d/mysql.d/conf.yaml.

'''
sudo vim /etc/datadog-agent/conf.d/mysql.d/conf.yaml

init_config:

instances:
  - server: 127.0.0.1
    user: datadog
    pass: "datadawg" # from the CREATE USER step earlier
    port: "3306" # e.g. 3306
    options:
      replication: false
      galera_cluster: true
      extra_status_metrics: true
      extra_innodb_metrics: true
      extra_performance_metrics: true
      schema_size_metrics: false
      disable_innodb_metrics: false

logs:
  - type: file
    path: "<ERROR_LOG_FILE_PATH>"
    source: mysql
    service: "<SERVICE_NAME>"

  - type: file
    path: "<SLOW_QUERY_LOG_FILE_PATH>"
    source: mysql
    service: "<SERVICE_NAME>"
    log_processing_rules:
      - type: multi_line
        name: new_slow_query_log_entry
        pattern: "# Time:"
        # If mysqld was started with `--log-short-format`, use:
        # pattern: "# Query_time:"
        # If using mysql version <5.7, use the following rules instead:
        # - type: multi_line
        #   name: new_slow_query_log_entry
        #   pattern: "# Time|# User@Host"
        # - type: exclude_at_match
        #   name: exclude_timestamp_only_line
        #   pattern: "# Time:"
  - type: file
    path: "<GENERAL_LOG_FILE_PATH>"
    source: mysql
    service: "<SERVICE_NAME>"
    # For multiline logs, if they start by the date with the format yyyy-mm-dd uncomment the following processing rule
    # log_processing_rules:
    #   - type: multi_line
    #     name: new_log_start_with_date
    #     pattern: \d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])
    # If the logs start with a date with the format yymmdd but include a timestamp with each new second, rather than with each log, uncomment the following processing rule
    # log_processing_rules:
    #   - type: multi_line
    #     name: new_logs_do_not_always_start_with_timestamp
    #     pattern: \t\t\s*\d+\s+|\d{6}\s+\d{,2}:\d{2}:\d{2}\t\s*\d+\s+
'''

![mysql](photos/mysql.png)

* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

'''
sudo -u dd-agent vim /etc/datadog-agent/checks.d/my_metric.py

import random
from datadog_checks.base import AgentCheck
__version__ = "1.0.0"
class RandomCheck(AgentCheck):
 def check(self, instance):
   self.gauge('my_metric', random.randint(0, 1001))
'''

![mymetric](photos/mymetric.png)


* Change your check's collection interval so that it only submits the metric once every 45 seconds.

'''
sudo vim /etc/datadog-agent/conf.d/my_metric.yaml

init_config:

instances:
        - min_collection_interval: 45
'''

* **Bonus Question** Can you change the collection interval without modifying the Python check file you created?

We can change the collection interval in another file, specifically /etc/datadog-agent/conf.d/my_metric.yaml.

## Visualizing Data:

Utilize the Datadog API to create a Timeboard that contains:

* Your custom metric scoped over your host.
* Any metric from the Integration on your Database with the anomaly function applied.
* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

'''
pip3 install datadog-api-client
import datadog_api_client
'''

'''
sudo vim my_timeboard.py
'''

'''
{"title":"Timeboard","description":"## Title\n\nDescribe this dashboard. Add links to other dashboards, monitors, wikis,  and docs to help your teammates. Markdown is supported.\n\n- [This might link to a dashboard](#)\n- [This might link to a wiki](#)","widgets":[{"id":3820757399904548,"definition":{"title":"my_metric","title_size":"16","title_align":"left","show_legend":true,"legend_layout":"auto","legend_columns":["avg","min","max","value","sum"],"time":{},"type":"timeseries","requests":[{"formulas":[{"formula":"query1"}],"queries":[{"name":"query1","data_source":"metrics","query":"avg:my_metric{host:andrew-740U5L}"}],"response_format":"timeseries","style":{"palette":"dog_classic","line_type":"solid","line_width":"normal"},"display_type":"line"}]}},{"id":7417595625295712,"definition":{"title":"Rollup","title_size":"16","title_align":"left","show_legend":true,"legend_layout":"auto","legend_columns":["avg","min","max","value","sum"],"time":{},"type":"timeseries","requests":[{"formulas":[{"formula":"query1"}],"queries":[{"name":"query1","data_source":"metrics","query":"avg:my_metric{*}.rollup(sum, 3600)"}],"response_format":"timeseries","style":{"palette":"dog_classic","line_type":"solid","line_width":"normal"},"display_type":"line"}]}},{"id":377970506678784,"definition":{"title":"Anomalies","title_size":"16","title_align":"left","show_legend":true,"legend_layout":"auto","legend_columns":["avg","min","max","value","sum"],"time":{},"type":"timeseries","requests":[{"formulas":[{"formula":"anomalies(query1, 'basic', 2)"}],"queries":[{"name":"query1","data_source":"metrics","query":"avg:my_metric{*}"}],"response_format":"timeseries","style":{"palette":"dog_classic","line_type":"solid","line_width":"normal"},"display_type":"line"}]}}],"template_variables":[],"layout_type":"ordered","is_read_only":false,"notify_list":[],"reflow_type":"auto","id":"4hb-vyh-m2d"}
'''

'''
DD_SITE="datadoghq.com" DD_API_KEY="310b7c445032127de65454610fdcf581" DD_APP_KEY="9d422bc984b309f817b59ff45dc97309f83593cb" python3 "my_timeboard.py"
'''

Once this is created, access the Dashboard from your Dashboard List in the UI:

[Dashboard](https://docs.datadoghq.com/api/latest/dashboards/#create-a-new-dashboard)

![timeboard](photos/timeboard.png)

* Set the Timeboard's timeframe to the past 5 minutes
![timeboard5min](photos/timeboard5min.png)

* Take a snapshot of this graph and use the @ notation to send it to yourself.

![anomaly](photos/anomaly.png)

shareable link
https://p.datadoghq.com/sb/357452ce-a4a2-11ec-878a-da7ad0900002-575aecb61518c9b9da9e76ee20a62fd5

* **Bonus Question**: What is the Anomaly graph displaying?

The anomaly graph is displaying when a metric is behaving differently than it has in the past, taking into account trends, seasonal day-of-week, and time-of-day patterns. It identifies any metrics with strong trends and recurring patterns that are hard to monitor with threshold-based alerting.

[APIReference](https://docs.datadoghq.com/api/latest/dashboards/)

## Monitoring Data

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

* Warning threshold of 500
* Alerting threshold of 800
* And also ensure that it will notify you if there is No Data for this query over the past 10m.

Please configure the monitor’s message so that it will:

* Send you an email whenever the monitor triggers.
* Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
* Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
* When this monitor sends you an email notification, take a screenshot of the email that it sends you.

![metricalert2](photos/metricalert2.png)
![metricalert1](photos/metricalert1.png)
![metricalert](photos/metricalert.png)
![metricalert3](photos/metricalert2.png)

![nodata](photos/nodata.png)


* **Bonus Question**: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

  * One that silences it from 7pm to 9am daily on M-F,
  * And one that silences it all day on Sat-Sun.
  * Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

![weekday2](photos/weekday2.png)
![weekday1](photos/weekday1.png)
![weekday](photos/weekday.png)

![weekend2](photos/weekend2.png)
![weekend1](photos/weekend1.png)
![weekend](photos/weekend.png)


## Collecting APM Data:

Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:

'''
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
'''


* **Note**: Using both ddtrace-run and manually inserting the Middleware has been known to cause issues. Please only use one or the other.

'''
sudo vim /etc/datadog-agent/datadog.yaml

pip3 install flask
sudo vim app.py

DD_SERVICE="custom_service" DD_ENV="custom_env" DD_LOGS_INJECTION=true ddtrace-run python app.py
'''

![custom_service](photos/custom_service.png)
![custom_service2](photos/custom_service2.png)
![custom_service3](photos/custom_service3.png)

* **Bonus Question**: What is the difference between a Service and a Resource?

Resources represent a particular domain of a customer application. They could typically be an instrumented web endpoint, database query, or background job. 

A service groups together endpoints, queries, or jobs for the purposes of scaling instances. Some examples:
A group of URL endpoints may be grouped together under an API service.
A group of DB queries that are grouped together within one database service.
A group of periodic jobs configured in the crond service.

link https://p.datadoghq.com/sb/357452ce-a4a2-11ec-878a-da7ad0900002-d8df023abc4147b3a3288caa3df24f4f

![APMIM1](photos/APMIM1.png)

## Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability! Is there anything creative you would use Datadog for?

Datadog could be used in a variety of scenarios, it was difficult to choose just one. I figured we'd look at the area with the most impact, medical science. As biotech and medtech companies continue to innovate in patient monitoring and wearables, Datadog could be used to track and monitor patients vital signs from a far more in depth and accurate internal body outlook. As companies like Neuralink continue to push the boundaries of what humans know about the human brain, the data obtained will only continue to refine human exploration of the microscopic world insides our bodies. We'd be able to make better decisions on how to treat 

![oj](photos/oj.png)