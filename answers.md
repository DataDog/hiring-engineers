Prerequisites - Setup the Environment



<img width="1024" alt="flask" src="https://user-images.githubusercontent.com/26099421/45600589-3ac19700-b9cd-11e8-97a5-578b9e3cc5b0.png">




Downloaded Ubuntu, Downloaded DD Agent

I used vagrant. See Vagrantfile.

https://github.com/Stahovec29/hiring-engineers/blob/master/UbuntuDownload.png

https://github.com/Stahovec29/hiring-engineers/blob/master/UbuntuDownload1.png

The datadog agent is a piece of software that runs on your hosts, which in turn will display metrics and then you will be able to monitor everything you need. To install the agent on your machine (we will use Ubuntu for this example), simply run the script  on your machine, which has the api key included in it that you received when you signed up for datadog. 
- DD_API_KEY=5f2ec4a8761c36c75db5cb1a21eae420 bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
This will install the APT packages for the Datadog agent, and it will then ask you for your password. If you want to install the Agent and not have it start up automatically, prepend the script above with DD_INSTALL_ONLY=true. 
Once you have the Datadog Agent up and running, you should be able to see your machine pop up on the GUI within a few moments. 
A few good commands to know once you get the Datadog Agent up and running:
    - Start agent as a service                 sudo service datadog-agent start
    - Stop agent as a serivce                  sudo service datadog-agent stop
    - Restart agent running as a service       sudo service datadog-agent restart
    - Status of agent service                  sudo dagadog-agent status
    - Send flare			       sudo datadog-agent flare
    - Display command usage		       sudo datadog-agent help
    - Run a check			       sudo -u dd-agent -- datadog agent check <check_name>
All of the configuration files and folders for the Agent are located in /etc/datadog-agent/datadog.yaml
The Configuration files for integrations are located in 
    /etc/datadog-agent/conf.d/

The link for the commands is https://docs.datadoghq.com/agent/basic_agent_usage/ubuntu/
The link for the datadog agent is https://app.datadoghq.com/account/settings#agent/ubuntu

Once you get your Datadog Agent up and running, if you go to the GUI, under the Infrastructure dropdown, and click on Host Map,  you should see your machine pop up (with whatever the name is, mine is trusty64).
Once you click on your machine, click on the dashboard link, which will then take you to a breakdown of your machine. There will be a chart that names all of the current processes running (ex; agent, puppet, mysql, ruby, etc). You can also navigate around your host map to see the CPU usage, load averages, memory breakdown, available swap, disk usage by device, disk latency, network traffic, and other programs you are running (example being Mysql) (ADDED NEW 
SCREENSHOTS FOR THIS)

Added tags in the .yaml file, was able to get them up 
https://docs.datadoghq.com/tagging/
https://docs.datadoghq.com/graphing/infrastructure/hostmap/   This page includes an example on tags for hostmap aws



Once you have poked around your Host Map, you may want to add agent tags to make it easier to look at containers. "Tags are key to     modern monitoring because they allow you to aggregate metrics across your infrastructure at any level you choose" 
This example is for adding tags to the host map.
https://www.datadoghq.com/blog/the-power-of-tagged-metrics/
One  way to add tags into your host map is to edit the datadog.yaml file
This is under #set up the hosts tags (optional) 
 You can add any tags you need based on your system and which metrics are needed to be monitored. Here are a few ideas and best practices for creating tags.
    - Tags must start with a letter, and after that they can contain: alphanumerics, underscores, minuses, colons, periods, and        slashes. Any other special characters will be converted into an underscore. Please note, that a tag cannot end with a 
      colon (ex. tag:)
    - Tags can be up to 200 characters long and support unicode
    - A tag can have a value or a key:value syntax. It is recommended to use the key:value syntax for better functionality
        - Some examples that are frequently used are env, instance, name, and role
        - role:database:mysql is an example where role is parsed as key and database:mysql as value
        - role_database:mysql is an example where role_database is parsed as key, and mysql as value

Tags that I inputted  are christinastahovec, env:prod, mysql, role:database, host:vagrant-ubuntu-trusty64
https://github.com/Stahovec29/hiring-engineers/blob/master/TagSetup1.png
https://github.com/Stahovec29/hiring-engineers/blob/master/TagSetup5.png



To integrate datadog with mysql - this example will be from MySQL
Navigate to the conf.yaml file which is found in conf.d/mysql/conf.d. Here you will want to turn on instances, edit the server,  user, port, and pass. Then under options (also in the conf.yaml file) you will want to edit as so:
    - replication:0
    - galera_cluster: 1
    - extra_status_metrics: true
    - extra_innodb_metrics: true
    - extra_performance_metrics: true
    - schema_size_metrics: false
    - disable_innodb_metrics: false
(new screenshot of this)
The MySQL metrics and logs will start to be collected right away
The instructions to prepare MySQL for DataDog if you are not familiar can be found here:
https://docs.datadoghq.com/integrations/mysql/



Create a custom agent check that submits a metric named my_metric with a random value between 0 and 1000. 
Change checks collection interval so that it only submits the metric once every 45 seconds.

Suppose you want this to happen. Follow these steps
Navigate to your conf.d directory. For this example it is located in etc/datadog-agent/conf.d
Create a new config file for the agent check. Name the file checkvalue.yaml. Input this script (this is the one I created not 
the example located at https://datadog.github.io/summit-training-session/handson/customagentcheck/)

<code>
init_config:

instances:
    -  check_name: 'checkvalue'
       min_collection_interval: 45
</code>

Then navigate to the checks.d directory, which is located at /etc/datadog-agent/checks.d
Note: you will have two new files for a custom agent check
Create a new file called checkvalue.py, and insert the following:
Within a few minutes, there should be a new metric in the metric summary called my_metric. This is located in the DataDog GUI
 under metrics, and then click on summary

 <code>
from checks import AgentCheck
import random

class HelloCheck(AgentCheck):
  def check(self, instance):
    instance['check_name']
    self.gauge('my_metric', random.randint(1,1000))
</code>

Collection intervals can be specified for each instance using a min_collection_interval
(In datadog prior to this release, min_collection_interval was a global)



Creating a datadog timeboard

Suppose you want to create a custom timeboard that utilizes datadogs API. For this example we will create a timeboard with the   new metric we set up called my_metric.  
Depending on what you need or which visualization you would like to have, you can choose from 
    - Timeseries
    - Query Value
    - Heat Map
    - Distribution
    - Top List
    - Change
    - Host Map
You will have to give your timeboard a name, and input which metric you would like the timeboard to display (in this case we are
using my_metric) 
Please see attached screenshots and code for the timeboard reference
The timeboard.py file has the script for this particular timeboard

https://github.com/Stahovec29/hiring-engineers/blob/master/TimeboardSetup.png
https://github.com/Stahovec29/hiring-engineers/blob/master/TimeboardSetup1.png
https://github.com/Stahovec29/hiring-engineers/blob/master/TimeboardSetup2.png

I used the directions located here: https://docs.datadoghq.com/api/?lang=python

Bonus: the anomaly graph is displaying the results along with the expected normal range



Creating a new metric monitor
Suppose you want to be alerted if your new timeboard is too high, too low, or not responding. For this example we will create a 
new metric monitor that watches the average of my_metric, and will alert if it is above the following values over the past five
minutes:
    - Warning threshold of 500, alerting threshold of 800, and to also notify if there is no data over the past 10 minutes.
If you want to configure a new monitor, go under monitors, and new monitor. 
Step 1: specify what sort of detection method you want. For this example we are using the Threshold Alert, which means an alert
is triggered whenever a metric crosses a threshold
Step 2: Define the metric (in this case my_metric), and set it to simple alert, which means it triggers a single alert when your
metric satisfies your alert conditions
Step 3: Set your alert conditions
    - Trigger when the metric is above(dropdown) the threshold on average(dropdown) during the last 5 minutes(dropdown) 
    - (SEE SCREENSHOTS)
    - Type into the alert threshold box 800, and 500 in the warning threshold box
    - Select do not require in the full window for data evaluation field
    - Select notify(dropdown) if data is missing for more than 10(dropdown) minutes
Step 4: Say what is happening. For this we use markdown in this field. Here is the example used for what we need
<code>
{{#is_alert}} System is too high {{/is_alert}} 

{{#is_warning}} System is almost too high {{/is_warning}} 

{{#is_no_data}} There is nothing reporting {{/is_no_data}} 

Notify: @christina.stahovec@gmail.com
<code>

Step 5: If you wish to notify your team input their names in the notify box

https://github.com/Stahovec29/hiring-engineers/blob/master/MetricSetup.png
https://github.com/Stahovec29/hiring-engineers/blob/master/MetricSetup2.png
https://github.com/Stahovec29/hiring-engineers/blob/master/EmailMetricAlert.png
https://github.com/Stahovec29/hiring-engineers/blob/master/EmailMetricAlert1.png
https://github.com/Stahovec29/hiring-engineers/blob/master/EmailMetricAlert2.png
https://github.com/Stahovec29/hiring-engineers/blob/master/EmailMetricAlert3.png

https://docs.datadoghq.com/monitors/
Bonus: if you click the manage downtime button in the monitor drop down menu, select my metric, choose what to silence,
set the schedule for a specific time by selecting the recurring tab, set repeat every one week


Flask and APM

Suppose you want to integrate a Flask app to use DataDogs APM solution, which is found under APM in the gui. This will be an 
example of tracing applications written in Python.  
First you have to install the Datadog tracing library, ddtrace, using pip. 
    - pip install ddtrace
Then to instrument your Python application use the included ddtrace-run command.
To use it, prefix your Python entry-point command with ddtrace-run
    - ddtrace-run python app.py
After a few minutes your traces should start showing up

https://github.com/Stahovec29/hiring-engineers/blob/master/APM1.png

https://github.com/Stahovec29/hiring-engineers/blob/master/APM2.png

https://github.com/Stahovec29/hiring-engineers/blob/master/APM3.png

https://github.com/Stahovec29/hiring-engineers/blob/master/APM4.png


Bonus: Difference between a service and a resource

A service is the name of a set of processes that work together to provide a feature set, and a resource is a particular query to a service 

Final Question:

I would use datadog to monitor metrics so that I could forecast my server utilization

For example, comparing the load from black friday in a particular store from last year, to possibly see how many people came into the store, how many purchases were made, and how many items were purchased. This would be good to get ready for the sale coming up this year. Additionally, I could hook into the datadog api and trigger services to autoscale.

 
