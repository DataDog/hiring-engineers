Prerequisites - Setup the environment
You can utilize any OS/host that you would like to complete this exercise. However, we recommend one of the following approaches:
You can spin up a fresh linux VM via Vagrant or other tools so that you don’t run into any OS or dependency issues. Here are instructions for setting up a Vagrant Ubuntu VM. We strongly recommend using minimum v. 16.04 to avoid dependency issues.
You can utilize a Containerized approach with Docker for Linux and our dockerized Datadog Agent image.
Then, sign up for Datadog (use “Datadog Recruiting Candidate” in the “Company” field), get the Agent reporting metrics from your local machine.

I set up VirtualBox
www.virtualbox.org
I downloaded a vmdk image with CentOS 8
https://www.osboxes.org/centos/
I signed up for a Datadog account and followed the instructions to set up the Agent, by running:

DD_AGENT_MAJOR_VERSION=7 DD_API_KEY=fc215eb4da6720b7acb1538134aff790 DD_SITE="datadoghq.eu" bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"

Once the install was successful, at the end of the webpage I saw the “Finish” button had gone from being greyed out to blue.

Images:
01_agent_successful_install.png
02_agent_successful_install.png


Collecting Metrics:
Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.


I logged into the server, went to 
/etc/datadog-agent
Then edited the file datadog.yaml
by going to the “tags” section and add the tags

tags:
- "region:eu"
- "function:dev1"
- "user:database"
Then I restarted the agent:
# systemctl stop datadog-agent
# systemctl start datadog-agent

Images:
03_adding_tags_to_host.png

Scripts:
datadog.yaml


Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.


I decided to instal a MySQL 8.0 database.
Once installed,  I ran the following commands as specified in the documentation:

# mysql -u root -p
mysql> CREATE USER 'datadog'@'localhost' IDENTIFIED WITH mysql_native_password by 'MyD0gP3t#';

Then, to verify the user was created correctly I ran:

# mysql -u datadog --password=MyD0gP3t# -e "show status" | grep Uptime && echo -e "\033[0;32mMySQL user - OK\033[0m" || echo -e "\033[0;31mCannot connect to MySQL\033[0m"
mysql: [Warning] Using a password on the command line interface can be insecure.
Uptime  3095
Uptime_since_flush_status       3095
MySQL user - OK

I also ran the following commands in MySQL database:

mysql> ALTER USER 'datadog'@'localhost' WITH MAX_USER_CONNECTIONS 5;
mysql> GRANT PROCESS ON *.* TO 'datadog'@'localhost';
mysql> GRANT SELECT ON performance_schema.* TO 'datadog'@'localhost';


Next I modified the conf.yaml file.
In folder
/etc/datadog-agent/conf.d/mysql.d/ 
I copied the file conf.yaml.example and called it conf.yaml
I edited the conf.yaml file with the following parameters:

init_config:

instances:
- server: 127.0.0.1
  user: datadog
  pass: "MyD0gP3t#" 
  port: "3306"
  options:
    replication: false
    galera_cluster: true
    extra_status_metrics: true
    extra_innodb_metrics: true
    extra_performance_metrics: true
    schema_size_metrics: false
    disable_innodb_metrics: false


Scripts:
conf.yaml

Then I restarted the agent:
# systemctl stop datadog-agent
# systemctl start datadog-agent


In the UI I went to the Datadog Dashboards -> Dashboard List -> Install
I selected the MySQL interface.
(Note: When I created my Datadog account I already selected on MySQL interface)

Images:
04_mysql_integration.png
05_mysql_integration.png
06_mysql_integration.png




Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.


In folder /etc/datadog-agent/checks.d  I created file custom_random.py containing:

import random
from checks import AgentCheck
class RandomCheck(AgentCheck):
 def check(self, instance):
   self.gauge('my_metric', random.randint(0, 1000))


Also, in folder /etc/datadog-agent/conf.d  I created file  custom_random.yaml containing:

init_config:

instances: [{}]


Then I restarted the agent:
# systemctl stop datadog-agent
# systemctl start datadog-agent

Change your check's collection interval so that it only submits the metric once every 45 seconds.

In edited the file custom_random.yaml and added:

init_config:

instances:
  -  min_collection_interval: 45


Then I restarted the agent:
# systemctl stop datadog-agent
# systemctl start datadog-agent


Images:
07_my_metric.png

Scripts:
custom_random.yaml
custom_random.py

Bonus Question Can you change the collection interval without modifying the Python check file you created?

To change the collection interval, you can edit the .yaml file and change the value of min_collection_interval (in seconds).


Visualizing Data:
Utilize the Datadog API to create a Timeboard that contains:
Your custom metric scoped over your host.
Any metric from the Integration on your Database with the anomaly function applied.
Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.


First I went to Integrations -> APIs to find out the API keys and the Application keys:
API keys = fc215eb4da6720b7acb1538134aff790
Application keys = 4e95a7285207d4a24fb15089ad565eace5099222 

I tested connectivity:

# curl "https://api.datadoghq.eu/api/v1/validate" -H "DD-API-KEY: fc215eb4da6720b7acb1538134aff790" -H "DD-APPLICATION-KEY: 4e95a7285207d4a24fb15089ad565eace5099222"
{"valid":true}[root@osboxes local]#

Then I ran the following command to create the timeboard:

# curl -X POST https://api.datadoghq.eu/api/v1/dashboard \
-H "Content-Type: application/json" \
-H "DD-API-KEY: fc215eb4da6720b7acb1538134aff790" \
-H "DD-APPLICATION-KEY: 4e95a7285207d4a24fb15089ad565eace5099222" \
-d @- << EOF
{
    "title": "API Data Visualization Timeboard",
    "widgets": [
        {
            "definition": {
                "type": "timeseries",
                "requests": [
                    {
                        "q": "avg:my_metric{*}"
                    }
                ],
                "title": "Custom metric my_metric"
            }
        },
		{
            "definition": {
                "type": "timeseries",
                "requests": [
                    {
                        "q": "anomalies(avg:mysql.performance.cpu_time{host:osboxes}, 'basic', 2)"
                    }
                ],
                "title": "Anomalies: CPU load is very high on MySQL"
            }
        },
		{
            "definition": {
                "type": "timeseries",
                "requests": [
                    {
                        "q":"sum:my_metric{*}.rollup(sum,3600)"
					}
                ],
                "title": "Custom metric my_metric Rollup by hour Timeline"
            }
        },
		{
            "definition": {
                "type": "distribution",
                "requests": [
                    {
                        "q":"sum:my_metric{*}.rollup(sum,3600)"
					}
                ],
                "title": "Custom metric my_metric Rollup by hour Distribution"
            }
        }
	],
    "layout_type": "ordered",
    "description": "API Data Visualization",
    "is_read_only": false,
    "notify_list": []
}
EOF


Scripts:
API_Data_Visualization_Timeboard.json


Once this is created, access the Dashboard from your Dashboard List in the UI:
Set the Timeboard's timeframe to the past 5 minutes
Take a snapshot of this graph and use the @ notation to send it to yourself.


To change the timeframe window, I went to Dashboard -> Dashboard List
On the “API Data Visualization Timeboard”, on the top right of the screen, I clicked inside the timeframe window, typed “5 min”, but it was not a valid option.
I could, however, change the timeframe window on the individual graphs.

Please note on the Datadog documentation:
https://docs.datadoghq.com/dashboards/guide/custom_time_frames/ 

It states “entering custom timeframes is in beta”
One way to do it is to make every custom graph to show a 5-minute interval.

Images:
08_timeboard.png
09_graph_sent_by_email.png
10_email_with_graph.png


Public URL:
https://p.datadoghq.eu/sb/16w6rsrm921tgxht-95f79c0fba426030dd5069179331d93b 

Bonus Question: What is the Anomaly graph displaying?

The activity on MySQL is minimal, so the graph is showing very little variation on the metric “CPU usage”. As long as there is enough historical data, the algorithm would be able to calculate the deviation.




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


To create a new monitoring metric on the UI, I clicked on Manage Monitor -> New Monitor -> Metric

Images:
11_monitoring_metric_1.png
12_monitoring_metric_2.png
13_email_with_monitoring_metric.png

Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:
One that silences it from 7pm to 9am daily on M-F,
And one that silences it all day on Sat-Sun.
Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.



I went to Monitor -> Manage monitors  page
I clicked on “Manage Downtime” section on the top of the page, and then “Schedule Downtime”

Images:
14_schedule_downtime_1.png
15_schedule_downtime_2.png
16_email_schedule_downtime_1.png
17_email_schedule_downtime_2.png




Collecting APM Data:
Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:

Note: Using both ddtrace-run and manually inserting the Middleware has been known to cause issues. Please only use one or the other.
Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.
Please include your fully instrumented app in your submission, as well.




I went to the APM link, clicked on “Host-Based”, and followed the instructions for Phyton.
In my putty session I ran:

# pip3 install ddtrace


Then I created the file flask_app.py in directory /opt/datadog-agent/scripts

The file flask_app.py contains:



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






Scripts:
flask_app.py


Then I modified the datadog.yaml file by specifying the name of the server (see “env”):


# apm_config:

  ## @param enabled - boolean - optional - default: true
  ## Set to true to enable the APM Agent.
  #
  # enabled: true

  ## @param env - string - optional - default: none
  ## The environment tag that Traces should be tagged with.
  ## If not set the value will be inherited, in order, from the top level
  ## "env" config option if set and then from the 'env:' tag if present in the
  ## 'tags' top level config option.
  #
  # env: osboxes





At this point I opened a second putty session. On the first session I ran the tracing:


[root@osboxes datadog-agent]# ddtrace-run python3 /opt/datadog-agent/scripts/flask_app.py
 * Serving Flask app "flask_app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
2020-05-10 09:04:48,014 DEBUG [ddtrace.internal.import_hooks] [import_hooks.py:136] - No hooks registered for module 'stringprep'
2020-05-10 09:04:48,014 - ddtrace.internal.import_hooks - DEBUG - No hooks registered for module 'stringprep'
2020-05-10 09:04:48,092 INFO [werkzeug] [_internal.py:113] -  * Running on http://0.0.0.0:5050/ (Press CTRL+C to quit)
2020-05-10 09:04:48,092 - werkzeug - INFO -  * Running on http://0.0.0.0:5050/ (Press CTRL+C to quit)


And on the second putty session I generated HTTP traffic:

[root@osboxes datadog-agent]# netstat -an | grep 5050
tcp        0      0 0.0.0.0:5050            0.0.0.0:*               LISTEN
[root@osboxes datadog-agent]# curl http://0.0.0.0:5050/
Entrypoint to the Application[root@osboxes datadog-agent]# curl http://0.0.0.0:5050/api/apm
Getting APM Started[root@osboxes datadog-agent]# curl http://0.0.0.0:5050/api/trace

To review the tracing information in the UI, I clicked on  APM -> Traces -> Search your traces



Images:
18_flask_tracing.png
19_APM_Infra_dashboard.png



This is the URL Link for my Dashboard:
https://p.datadoghq.eu/sb/16w6rsrm921tgxht-f5e4116ff6a703511c383dd3f223893b 


Bonus Question: What is the difference between a Service and a Resource?


A service is a set of processes that do the same job - for example a database.
A resource is a particular action for a given service, for instance an SQL query ran against that database.



Final Question:
Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!
Is there anything creative you would use Datadog for?


It would be interesting to use Datadog to analyse queue lenghts in supermarkets, and the average queuing times throuout the day, especially int the current climate (Covid-19) health regulations.
Using this data, customers could simply check queue lenght using an app, or checking the supermarket website.
It could also be useful to collate the queuing info from local businesses and put in a dashboard, for the general public to consume. Same could apply in a shopping center.

