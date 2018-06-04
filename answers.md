Your answers to the questions go here.
<h1>Solutions Engineer Technical Challenge</h1>
<h2>Prerequisites - Setup the environment</h2>

1) Install VirtualBox and Vagrant (this was already preinstalled on my laptop).
2) Create an folder for your VirtualBox machine. In my case *mkdir dd*.
3) Change in the folder *cd dd* and create Vagrantfile *vagrant init*. For more detailes see here - https://www.vagrantup.com/intro/getting-started/ 
4) I used Ubuntu 16.04.3 LTS and therefore you need to modify *Vagrantfile* file with appropriate vm.box.

    ![Alt Text](https://raw.github.com/AndyL77/hiring-engineers/solutions-engineer/img/VagrantBox.png)
5) Now you need to start the VM and ssh to it
    + a) *vagrant up*
    + b) *vagrant ssh*
6) As a next step you need to install the Datadog software (agent) on your Ubuntu VM.
    + a) Got to Datadog's website at www.datadoghq.com and click the "GET STARTED FOR FREE" button. Fill out the form and sign up.
    + b) After submission, select your operating system and install the Datadog agent. In my case *Ubuntu*. 
        
        ![Alt Text](https://raw.github.com/AndyL77/hiring-engineers/solutions-engineer/img/InstallDDAgent.png)

        ![Alt Text](https://raw.github.com/AndyL77/hiring-engineers/solutions-engineer/img/InstallDDAgentonOS.png)
    Hint: API Key hidden
    + c) The installation process may look like this at the end.

        ![Alt Text](https://raw.github.com/AndyL77/hiring-engineers/solutions-engineer/img/InstallDDAgentFinal.png)
    + d) Upon completion, go back to the Datadog installation page and there will be a notification that the Datadog agent is now collecting metrics. 
7) In Datadog UI navigation bar go to *Dashboard* tab and select dashboard *System Overview* to get the metrics collected by the agent.

    ![Alt Text](https://raw.github.com/AndyL77/hiring-engineers/solutions-engineer/img/Dashbaord-Systemoverview.png)
    
    ![Alt Text](https://raw.github.com/AndyL77/hiring-engineers/solutions-engineer/img/Dashbaord-Systemoverview2.png)
<h2> Technical Challenge - Collecting Metrics </h2>

***Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.***

1) Open the agent configuration file: */etc/datadog-agent/datadog.yaml* with a text editor like *vim*, scroll down to *Set host's tag optional' and add the tag. In my case *os:ubuntu*.
The configuration file for the agent tagging documentantion and  can be found here https://docs.datadoghq.com/agent/basic_agent_usage/#configuration-file and here
https://docs.datadoghq.com/getting_started/tagging/.

    ![Alt Text](https://raw.github.com/AndyL77/hiring-engineers/solutions-engineer/img/hosttag.png)

2) To see the tag in the Datadog UI go to the Infrastructure tab, click on Host Map and then on your host. The specified tag will appier unter Tags, like depicted below.

    ![Alt Text](https://raw.github.com/AndyL77/hiring-engineers/solutions-engineer/img/Infrastructure-Tag.png)

***Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.***

1) Install MySQL on your ubuntu machine. Instructions can be found here (I skiped the *mysql_secure_installation* part): https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-16-04.

2) Once completed, install the integration for MySQL. To do this, go to the Integrations Tab on the navigation bar and search for MySQL. Click on it and follow instructions provided in this wizzard. Here is an example:

    ![Alt Text](https://raw.github.com/AndyL77/hiring-engineers/solutions-engineer/img/MySQLIntegration.png)

**Hint**: In case you get an "Access denied for user 'root@localhost' (using password: NO)" mysql command error - add a *-p* switch to the command and provide the password.  

3) Create *mysql.yaml* file inside */etc/datadog-agent/conf.d* folder. 
    + a) Create a copy from the example file and it *mysql.yaml*: *cp /etc/datadog-agent/conf.d/mysql.d/conf.yaml.example /etc/datadog-agent/conf.d/mysql.yaml*
    + b) Add configuration info as descibed in the instruction.

        ![Alt Text](https://raw.github.com/AndyL77/hiring-engineers/solutions-engineer/img/mysqlyaml.png)
    + c) Once completed go to the Dashboard Tab on the navigation bar and select MySQL Overview dashboard. It will show you MySQL metric like here:

        ![Alt Text](https://raw.github.com/AndyL77/hiring-engineers/solutions-engineer/img/MySQLDashboard.png)

***Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.***

1) First you need to create a YAML file, in my case *my_metric.yaml*, in agent's directory at */etc/datadog-agent/conf.d*. The agent check documentation for reference: https://docs.datadoghq.com/agent/agent_checks/. Here my example:

    ![Alt Text](https://raw.github.com/AndyL77/hiring-engineers/solutions-engineer/img/my_metricyaml.png)

2) Second you need to create the check itself. Create a separate file in */etc/datadog-agent/checks.d* directory with exactly the same name as the configuration file. In my case  *my_metric.py*. Add the code (see below), saved it and restart the agent *sudo service datadog-agent restart*. For more details see - https://docs.datadoghq.com/agent/basic_agent_usage/ubuntu/.

    ![Alt Text](https://raw.github.com/AndyL77/hiring-engineers/solutions-engineer/img/my_metricpy.png)

3) Go to the *Metrics* Tab on the navigation bar, click on *Exploerer* and search for *my_metric*.

    ![Alt Text](https://raw.github.com/AndyL77/hiring-engineers/solutions-engineer/img/my_metricoverview.png)

***Change your check's collection interval so that it only submits the metric once every 45 seconds.***

1) I added the following line of code to my *my_metric.yaml* file to change the default check of every 15 seconds to 45 seconds.

            init_config:
                min_collection_interval: 45

***Bonus Question: Can you change the collection interval without modifying the Python Check file you created***

Yes. You can change thie collection interval in the corresponding configuration YAML file. Python Check file don't need to be modified. 


<h2> Visualizing Data</h2>

***Utilize the Datadog API to create a Timeboard that contains:***
+   ***Your custom metric scoped over your host.***
+   ***Any metric from the Integration on your Database with the anomaly function applied.***
+   ***Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket***

1) I found this article and followed the steps https://help.datadoghq.com/hc/en-us/articles/115002182863-Using-Postman-With-Datadog-APIs. 
    + a) Generate an application key.
    + b) Replace *api_key* and *application_key* infos with your own keys.
    + b) Importe the datadog collection
    + c) In Collections under Timeboards create a Timeboard file and click *Send*. See my example below (API and Application Keys hidden):

    ![Alt Text](https://raw.github.com/AndyL77/hiring-engineers/solutions-engineer/img/Timaboard.png)

References: 
https://docs.datadoghq.com/api/?lang=bash#create-a-timeboard
https://docs.datadoghq.com/monitors/monitor_types/anomaly/#anomaly-detection-algorithms
https://docs.datadoghq.com/graphing/#rollup-to-aggregate-over-time

***Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timemboard.***
```{
      "graphs" : [{
          "title": "Average My_metric over my host",
          "definition": {
              "requests": [
                  {"q": "avg:my_metric{host:ubuntu-xenial}"}
              ]
          },
          "viz": "timeseries"
      },
      {
          "title": "My_metric with Rollup sum over one hour Buckets",
          "definition": {
              "requests": [
                  {"q": "avg:my_metric{*}.rollup(sum, 3600)"}
              ]
          },
          "viz": "timeseries"
      },
      {
          "title": "MySQL Average mysql.performance.cpu_time Anomaly",
          "definition": {
              "requests": [
                  {"q": "anomalies(avg:mysql.performance.cpu_time{host:ubuntu-xenial}, 'basic', 2)"}
              ]
          },
          "viz": "timeseries"
      }
      ],
      "title" : "Andreas's TimeBoard",
      "description" : "A Timeboard of metric data from tech chellange.",
      "template_variables": [{
          "name": "host1",
          "prefix": "host",
          "default": "host:my-host"
      }],
      "read_only": "True"
    }

```

***Once this is created, access the Dashboard from your Dashboard List in the UI:***
***Set the Timeboard's timeframe to the past 5 minutes***
***Take a snapshot of this graph and use the @ notation to send it to yourself.***

1) Once the timeboard is created, go to the *Dashboard* Tab on the navigation bar, click on *Navigation List* and select the new TimeBoard, e.g. *"Andreas's TimeBoard"* . Zoom into one of the graphs to get a 5 minute timeframe. Here my example:

    ![Alt Text](https://raw.github.com/AndyL77/hiring-engineers/solutions-engineer/img/AndreasTimeboard.png)
    
    ![Alt Text](https://raw.github.com/AndyL77/hiring-engineers/solutions-engineer/img/AndreasTimeboard2.png)

**Note**: Rollup graph shows no data because it is summed over one hour but the praph is zoomed into five minutes.  

2) Click on each graph (snapshot icon) and comment the email address in each one. Here my examples (Email address hidden):

    ![Alt Text](https://raw.github.com/AndyL77/hiring-engineers/solutions-engineer/img/DashboardComment.png)
    
    ![Alt Text](https://raw.github.com/AndyL77/hiring-engineers/solutions-engineer/img/DashboardComment1.png)

***BONUS QUESTION: What is the Anomaly graph displaying?***

The [Anomaly graph](https://www.datadoghq.com/blog/introducing-anomaly-detection-datadog/) detects any unusual activity by analyzing the metrics's history behavior and by following the trends in some timeseries. If the graph goes above or below this threshold an alert is created.

<h2>Monitoring Data</h2>

***Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:***
+   ***Warning threshold of 500***
+   ***Alerting threshold of 800***
+   ***And also ensure that it will notify you if there is No Data for this query over the past 10m.***

***Please configure the monitor’s message so that it will:***
+   ***Send you an email whenever the monitor triggers.***
+   ***Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.***
+   ***Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.***
+   ***When this monitor sends you an email notification, take a screenshot of the email that it sends you.***

1) Go to the monitor tab in the navigation bar and click on New Monitor. Click on metric and fill out the form as needed. Examples are below (Email hidden):

    ![Alt Text](https://raw.github.com/AndyL77/hiring-engineers/solutions-engineer/img/Monitor.png)
    
    ![Alt Text](https://raw.github.com/AndyL77/hiring-engineers/solutions-engineer/img/Monitor2.png)

    Here are emails for an Alert, Warning, and No Data state (Email hidden):

    ![Alt Text](https://raw.github.com/AndyL77/hiring-engineers/solutions-engineer/img/AlertWarning.png)
    
    ![Alt Text](https://raw.github.com/AndyL77/hiring-engineers/solutions-engineer/img/Alertnodata.png)

***Hint:*** During the tech challenge my_metric wasn't above the alert threshold of 800, therefore there is no alert email notification for this alert.

***Bonus Question:***
***Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:***
+   ***One that silences it from 7pm to 9am daily on M-F,***
+   ***And one that silences it all day on Sat-Sun.***
+   ***Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.***

1) Gt to the monitor tab in the navigation bar and click on Manage Downtime. Click the yellow *Schedule Downtime* buttnn and fill out the fields for when notifications should be turned off.
Here the screenshot examples:

    ![Alt Text](https://raw.github.com/AndyL77/hiring-engineers/solutions-engineer/img/DowntimeWorkday.png)
    
    ![Alt Text](https://raw.github.com/AndyL77/hiring-engineers/solutions-engineer/img/DowntimeWeekend.png)
    
    ![Alt Text](https://raw.github.com/AndyL77/hiring-engineers/solutions-engineer/img/EmailWorkdayDowntime.png)

***Hint:*** The tech challenge was taken during the workdays, therefore there is no email notification for weekend downtime.

References:
https://docs.datadoghq.com/monitors/downtimes/
https://docs.datadoghq.com/monitors/notifications/#message-template-variables

<h2>Collecting APM Data </h2>

***Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution***

General documentation for reference: https://docs.datadoghq.com/tracing/setup/

1) Install Flask using this commands:

```
export LC_ALL="en_US.UTF-8"
export LC_CTYPE="en_US.UTF-8"
sudo pip install Flask
sudo pip install blinker
```

2) Install Datadog python APM tracer. For instructure go to the APM tab in the navigation bar and select Getting Started. Click python and install ddtrace.

```
pip install ddtrace
```
3) Create a file *my_app.py* and copy the provided code into it.

````
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
    app.run(host='0.0.0.0', port=8080)
````

**Hint**:  *app.run(host='0.0.0.0', port=8080)* the server is set to be publicly available on port 8080.

4) Open */etc/datadog-agent/datadog.yaml* and set *apm config: enabled true* as seen below:

    ![Alt Text](https://raw.github.com/AndyL77/hiring-engineers/solutions-engineer/img/apmconfig.png)

5) In the directory where your Flask file is located, run *ddtrace-run python my_app.py*.

    **Hint**: Add PortForwarding *8080* to the network configuration of your virtualbox VM.

    ![Alt Text](https://raw.github.com/AndyL77/hiring-engineers/solutions-engineer/img/PortForwarding.png)

6) Start a browser and enter http://localhost:8080 and http://localhost:8080/api/apm.

    ![Alt Text](https://raw.github.com/AndyL77/hiring-engineers/solutions-engineer/img/FlaskApp.png)
    
    ![Alt Text](https://raw.github.com/AndyL77/hiring-engineers/solutions-engineer/img/FlaskApp2.png)

7) Go to to the APM tab in the navigation bar and your service's metrics will soon be visible. Click on the Services sub-tab wthin APM tab and select flask. On each graph click on the *Export to Timeboard* button and choose your Timeboard. Once completed, got to Dashboard tab in the navigation click on *Dashboard List* and select the Timeboard. In my case "Andreas's TimeBoard.

    ![Alt Text](https://raw.github.com/AndyL77/hiring-engineers/solutions-engineer/img/FlaskinTimeBoard2.png)

    ![Alt Text](https://raw.github.com/AndyL77/hiring-engineers/solutions-engineer/img/FlaskinTimeBoard.png)

***Bonus Question: What's the difference between a Service and a Resource?***

1) A **service** is a set of processes that do the same job and work together to provide a feature set. This may entail a database, a web-application, queries, etc. A web application may have several services, depending on the complexity of the application. A **resource** is an action that is called with whatever the service provide - such as an endpoint or query. For example: */user/home*.
In the context of this exercise the web service would be the flask app. The resource would be some data, such as some information that the user has stored on a database that the flask app fetches and serves the user.

<h4>Final Question:</h4>

***Is there anything creative you would use Datadog for?***

Today I would think of two use cases.
+ One would be the monitoring capabilities of IoT devices. For instance monitoring of Raspberry Pi or any other devices with wide range of censors components (weather, paking lots etc.). 
+ Second would be the monitoring capabilities for serverless or FAAS technologies. The technology is evolving really fast and I think this is next big thing after container technology. But how do I know if my function performs as expected, e.g. startup and execution time?  
