Your answers to the questions go here.
Prerequisites - Setup the environment
You can utilize any OS/host that you would like to complete this exercise. However, we recommend one of the following approaches:

You can spin up a fresh linux VM via Vagrant or other tools so that you don’t run into any OS or dependency issues. Here are instructions for setting up a Vagrant Ubuntu VM. We strongly recommend using minimum v. 16.04 to avoid dependency issues.
You can utilize a Containerized approach with Docker for Linux and our dockerized Datadog Agent image.
Then, sign up for Datadog (use “Datadog Recruiting Candidate” in the “Company” field), get the Agent reporting metrics from your local machine.

ANSWERS 
Apache was successfully installed


I set up a vagrant Ubuntu server, I installed MySQL for the database. 

The Datadog agent was successfully installed via the following:

vagrant@precise64:~$ DD_API_KEY=65932bfeac0f4f4dfe626035439bcae2 bash -c "$(curl -L https://raw.githubusercontent.com/D
ataDog/datadog-agent/master/cmd/agent/install_script.sh)"

Returned the following message: Your Agent is running and functioning properly. It will continue to run in the
background and submit metrics to Datadog.


MySQL integration was set up.

create MYSQL USER
CREATE USER 'datadog'@'localhost' IDENTIFIED BY 'DGLu16DQ_ET2BT0vUrosxMMJ'

Collecting Metrics:


Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.



Tags field was added in the datadog/yaml file. Code is as follows

Set the host's tags (optional)
tags:
   - prodserverdb1
   - env:prod
   - role:database_servers


Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

I installed a MySQL server for this use case.

Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
Change your check's collection interval so that it only submits the metric once every 45 seconds.
I created a my_metric.py file in the /etc/datadog-agent/checks.d directory and added the following code.
from checks import AgentCheck
 
import random
 
class MyMetricCheck(AgentCheck):
 
     def check(self, instance):
 
         self.gauge('my_metric', random.randint(1,1001))

I then created a my_metric.yaml file in the /etc/datadog-agent/conf.d directory and added the following code.

init_config:

instances: [{}]

Instances:
    - min_collection_interval: 45

I then ran a sudo service datadog-agent restart to restart the agent.
I then ran the following command to ensure the custom metric was working. sudo -u dd-agent -- datadog-agent check my_metric

The following data was returned indicating that the custom metric was working properly.

=== Series ===
{
  "series": [
    {
      "metric": "my_metric",
      "points": [
        [
          1544564296,
          891
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

    my_metric (unversioned)
    -----------------------
        Instance ID: my_metric:d884b5186b651429 [OK]
        Total Runs: 1
        Metric Samples: 1, Total: 1
        Events: 0, Total: 0
        Service Checks: 0, Total: 0
        Average Execution Time : 0s


Check has run only once, if some metrics are missing you can try again with --check-rate to see any other metric if available.

Custom Metric is successfully reporting


Bonus Question Can you change the collection interval without modifying the Python check file you created?
Yes, the interval exists within the yaml file so it can be easily changed there.

Visualizing Data:
Utilize the Datadog API to create a Timeboard that contains:

Your custom metric scoped over your host.
Any metric from the Integration on your Database with the anomaly function applied.
Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.

I ran into some challenges in this exercise which I think is related to how my vagrant environment is set up.

It appears that there was an ssl issue within my vm. When I ran sudo -H pip install datadog I received the following output.

Collecting datadog
/usr/local/lib/python2.7/dist-packages/pip/_vendor/urllib3/util/ssl_.py:369: SNIMissingWarning: An HTTPS request has been made, but the SNI (Server Name Indication) extension to TLS is not available on this platform. This may cause the server to present an incorrect TLS certificate, which can cause validation failures. You can upgrade to a newer version of Python to solve this. For more information, see https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
  SNIMissingWarning
/usr/local/lib/python2.7/dist-packages/pip/_vendor/urllib3/util/ssl_.py:160: InsecurePlatformWarning: A true SSLContext object is not available. This prevents urllib3 from configuring SSL appropriately and may cause certain SSL connections to fail. You can upgrade to a newer version of Python to solve this. For more information, see https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
  InsecurePlatformWarning
  Using cached https://files.pythonhosted.org/packages/17/dd/a7bbb33427f853f82b36356286fb922ef976bf18e78dbb76ac43b8c50e26/datadog-0.26.0.tar.gz
Requirement already satisfied: decorator>=3.3.2 in /usr/local/lib/python2.7/dist-packages (from datadog) (4.3.0)
Collecting requests>=2.6.0 (from datadog)
  Using cached https://files.pythonhosted.org/packages/7d/e3/20f3d364d6c8e5d2353c72a67778eb189176f08e873c9900e10c0287b84b/requests-2.21.0-py2.py3-none-any.whl
Requirement already satisfied: urllib3<1.25,>=1.21.1 in /usr/local/lib/python2.7/dist-packages (from requests>=2.6.0->datadog) (1.24.1)
Requirement already satisfied: certifi>=2017.4.17 in /usr/local/lib/python2.7/dist-packages (from requests>=2.6.0->datadog) (2018.11.29)
Collecting chardet<3.1.0,>=3.0.2 (from requests>=2.6.0->datadog)
  Using cached https://files.pythonhosted.org/packages/bc/a9/01ffebfb562e4274b6487b4bb1ddec7ca55ec7510b22e4c51f14098443b8/chardet-3.0.4-py2.py3-none-any.whl
Requirement already satisfied: idna<2.9,>=2.5 in /usr/local/lib/python2.7/dist-packages (from requests>=2.6.0->datadog) (2.7)
Building wheels for collected packages: datadog
  Running setup.py bdist_wheel for datadog ... error
  Complete output from command /usr/bin/python -u -c "import setuptools, tokenize;__file__='/tmp/pip-install-RNVAgn/datadog/setup.py';f=getattr(tokenize, 'open', open)(__file__);code=f.read().replace('\r\n', '\n');f.close();exec(compile(code, __file__, 'exec'))" bdist_wheel -d /tmp/pip-wheel-1bXuZd --python-tag cp27:
  /usr/lib/python2.7/distutils/dist.py:267: UserWarning: Unknown distribution option: 'long_description_content_type'
    warnings.warn(msg)
  usage: -c [global_opts] cmd1 [cmd1_opts] [cmd2 [cmd2_opts] ...]
     or: -c --help [cmd1 cmd2 ...]
     or: -c --help-commands
     or: -c cmd --help

  error: invalid command 'bdist_wheel'

  ----------------------------------------
  Failed building wheel for datadog
  Running setup.py clean for datadog
Failed to build datadog
Installing collected packages: chardet, requests, datadog
  Found existing installation: chardet 2.0.1
Cannot uninstall 'chardet'. It is a distutils installed project and thus we cannot accurately determine which files belong to it which would lead to only a partial uninstall.

Basically the datadog module would not run so when I ran python timeboard.py, it would return that there was no module named datadog. my timeboard.py file was setup as follows.
#!/opt/datadog-agent/embedded/bin/python

from datadog import initialize, api

options = {
    'api_key': '53fa323e3493a54ee76356a4710187a3',
    'app_key': '3da12005766a4802b669bfd899962d56c1e728ce'
}
initialize(**options)
title = "Gregs Timeboard"
description = "Test Metric Timeboard."
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{*}"}
        ],
        "viz": "timeseries"
    },
    "title": "My_Metric"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:mysql.connections.current{*}, 'basic', 2)"}
        ],
        "viz": "timeseries"
    },
    "title": "MySQL Anomaly"
},
 {
 "definition": {
        "events": [],
        "requests": [
            {"q": "sum:my_metric{*}.rollup(sum,600)"}
        ],
        "viz": "timeseries"
    },
    "title": "My_Metric_1Hour_Rollup"
 }
 ]
template_variables = [{
    "name": "ubuntu-xenial",
    "prefix": "host",
    "default": "host:ubuntu-xenial"
}]
read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)

Do to limited time to troubleshoot, I then attempted a bit of reverse engineering just to see how the timeboard creation is done in the UI:
What I learned is that you can pretty much build your timeboard using the JSON code that is in your script. I still would like to try and get this to work. But the process of running the python script is very useful and I fully understand the concept. One other thing I changed was that I set the rollup interval to 600 instead of 3600. It just gave me a little more data to view.

Screenshot for timeboard.


Once this is created, access the Dashboard from your Dashboard List in the UI:

Set the Timeboard's timeframe to the past 5 minutes


Take a snapshot of this graph and use the @ notation to send it to yourself.


Bonus Question: What is the Anomaly graph displaying?
The anomaly graph is designed to show any deviations in the data points from normal trends. If the data point is outside of what is predicted, it will be considered an anomaly.

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

I used the following
{{{{is_match "host.name" "<HOST_NAME>"}}}}
{{ .matched }} the host name
{{{{/is_match}}}}
I played around with the different parameters to see what output changes I would get.


When this monitor sends you an email notification, take a screenshot of the email that it sends you.

Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

One that silences it from 7pm to 9am daily on M-F,
And one that silences it all day on Sat-Sun.



Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.



Collecting APM Data:
Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:

I installed flask via sudo -H install flask
I then install ddtrace as follows sudo -H pip install ddtrace

I created a file called apm.py with the code below

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
Note: Using both ddtrace-run and manually inserting the Middleware has been known to cause issues. Please only use one or the other. I used ddtrace

I ran sudo ddtrace-run python apm.py to bring up the app



Bonus Question: What is the difference between a Service and a Resource?

Every Service being monitored by your application will be associated with a "Type". This Type can be "Web", "DB", "HTTP etc.
A Service is the name of a set of processes that work together to provide a feature set. For instance, a simple web application may consist of two or more services. 


Fianl Question

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?

I have worked in the Energy industry and Smart meter technology is becoming a standard. Getting the meter data can be very challenging as it is not a conventional approach. The Datadog API and custom integrations would allow for energy companies to monitor health and availability of smart meter technologies as well as the applications and infrastructures that support it. The ability to easily create timeboards would allow for a very intuitive view of the overall smart meter service from a business standpoint. Also, in traditional corporations, there is a increasing need to add business related metrics along with IT service metrics. This is another way the Datadog can add value to the line of business within and organization.

