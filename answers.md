Prerequisites - Setup the Environment

Downloaded Ubuntu, Downloaded DD Agent

<img width="572" alt="ubuntudownload" src="https://user-images.githubusercontent.com/26099421/45600855-bc1b2880-b9d1-11e8-96cc-61c9eeec7f55.png">
<img width="1024" alt="ubuntudownload1" src="https://user-images.githubusercontent.com/26099421/45600862-d35a1600-b9d1-11e8-8bfd-0d15266f7921.png">

The datadog agent is an application that will collect metrics of the applications running on your computer, send those metrics todatadog, and then will display them in charts on a website that you can look at and monitor. 
To install the agent on your computer (we will use Ubuntu for this example), run this script in your terminal, which has the api key included in it that you received when you signed up for datadog:
    - API key "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
This will install the (APT) packages for the Datadog agent
Note: If you want to install the Agent and not have it start up automatically, add this before the script above:
    - DD_INSTALL_ONLY=true 
Once you have the Datadog Agent up and running, you should be able to see your computer pop up on the datadog website  within a
few moments.
You can also launch the website (GUI) through this command in your terminal:
    - datadog-agent launch-gui 

A few good commands to know once you get the Datadog Agent up and running:
    - Start agent as a service                 sudo service datadog-agent start
    - Stop agent as a serivce                  sudo service datadog-agent stop
    - Restart agent running as a service       sudo service datadog-agent restart
    - Status of agent service                  sudo dagadog-agent status
    - Send flare			       sudo datadog-agent flare
    - Display command usage		       sudo datadog-agent help
    - Run a check			       sudo -u dd-agent -- datadog agent check <check_name>

All of the configuration files and folders for the Agent are located in /etc/datadog-agent/datadog.yaml
The Configuration files for integrations are located in /etc/datadog-agent/conf.d/

The link for the commands is https://docs.datadoghq.com/agent/basic_agent_usage/ubuntu/
The link for the datadog agent is https://app.datadoghq.com/account/settings#agent/ubuntu

Once you get your Datadog Agent up and running, you will want to see where your computer is on the website. If you go to the 
website, under the Infrastructure dropdown, and click on Host Map, you should see your machine pop up (mine is trusty64).
After you see your computer show up, click on the dashboard link (located to the right of your computer name), which will then
take you to a breakdown of what is on your computer. There will be a chart that names all of the current processes running
(example: agent, puppet, Mysql, ruby, etc).

<img width="1024" alt="agentsetup3" src="https://user-images.githubusercontent.com/26099421/45601039-57150200-b9d4-11e8-9dc5-68941c9b7baa.png">

You can also navigate around your host map to see the CPU usage, load averages, memory breakdown, available swap, disk usage by device, disk latency, network traffic, and other programs you are running (example being Mysql) 

<img width="1024" alt="dashboard host map" src="https://user-images.githubusercontent.com/26099421/45600911-7ca10c00-b9d2-11e8-8836-0faccaf177c6.png">
<img width="1024" alt="dashboard host map1" src="https://user-images.githubusercontent.com/26099421/45600917-a35f4280-b9d2-11e8-839e-0281f0d42cba.png">
<img width="1024" alt="dashboard host map2" src="https://user-images.githubusercontent.com/26099421/45600925-b540e580-b9d2-11e8-81c8-d9b092cbd265.png">


Added tags in the .yaml file.
https://docs.datadoghq.com/tagging/
https://docs.datadoghq.com/graphing/infrastructure/hostmap/  
This page includes an example on tags for hostmap aws

Once you have looked around your Host Map, you may want to add agent tags to make it easier to look at containers the processes
that are running. Tagging is a method to help you look at specific individual processes you choose as a whole.
"Tags are key to  modern monitoring because they allow you to aggregate metrics across your infrastructure at any level you
choose" 
This example is for adding tags to the host map.
https://www.datadoghq.com/blog/the-power-of-tagged-metrics/
One way to add tags into your host map is to edit the datadog.yaml file, which is located at /etc/datadog-agent/datadog.yaml
Editing this specific part of the datadog.yaml file is under #set up the hosts tags (optional).

<img width="1024" alt="tagsetup1" src="https://user-images.githubusercontent.com/26099421/45600977-5b8ceb00-b9d3-11e8-84c4-881ab06e07a8.png">
 
You can add any tags you need based on your system and which metrics are needed to be monitored.
Here are a few ideas for creating tags:
    - Tags must start with a letter, and after that they can contain: alphanumerics, underscores, minuses, colons, periods, and        slashes. Any other special characters will be converted into an underscore. Please note, that a tag cannot end with a 
      colon (ex. tag:)
    - Tags can be up to 200 characters long and support unicode
    - A tag can have a value or a key:value syntax. It is recommended to use the key:value syntax for better functionality
        - Some examples that are frequently used are env, instance, name, and role
        - role:database:mysql is an example where role is parsed as key and database:mysql as value
        - role_database:mysql is an example where role_database is parsed as key, and mysql as value

Tags that I inputted  are christinastahovec, env:prod, mysql, role:database, host:vagrant-ubuntu-trusty64

<img width="1024" alt="tagsetup5" src="https://user-images.githubusercontent.com/26099421/45601008-b0306600-b9d3-11e8-8032-dac547984f41.png">



To integrate datadog with mysql - this example will be from MySQL
Navigate to the conf.yaml file in your terminal which is found in /etc/datadog-agent/ conf.d/mysql/conf.d.
Here you will want to make some changes that will allow Datadog to help with your database.
Then, under options (also in the conf.yaml file) you will want to edit as so:
    - replication:0
    - galera_cluster: 1
    - extra_status_metrics: true
    - extra_innodb_metrics: true
    - extra_performance_metrics: true
    - schema_size_metrics: false
    - disable_innodb_metrics: false

<img width="914" alt="sqlsetup4" src="https://user-images.githubusercontent.com/26099421/45601076-de627580-b9d4-11e8-995b-b913ef1632bc.png">

The MySQL metrics and logs will start to be collected within a few minutes of editing the conf.yaml file.
The instructions to prepare MySQL for DataDog if you are not familiar can be found here:
https://docs.datadoghq.com/integrations/mysql/ 
Also, a screenshot of this process

<img width="1023" alt="sqlsetup3" src="https://user-images.githubusercontent.com/26099421/45601106-94c65a80-b9d5-11e8-841e-28de786d181d.png">


Create a custom agent check that submits a metric named my_metric with a random value between 0 and 1000. 
Change checks collection interval so that it only submits the metric once every 45 seconds.

This example is to create a metric that records a value generated by a custom application. 
These metrics will be submitted to Datadog.
Note: you will have two new files for a custom agent check.
Suppose you want this to happen. Follow these steps:
Navigate to your conf.d directory. For this example it is located in etc/datadog-agent/conf.d
Create a new configuration file for the agent check. Name the file checkvalue.yaml.
Input this script:

<code>
init_config:

instances:
    -  check_name: 'checkvalue'
       min_collection_interval: 45
</code>

Then navigate to the checks.d directory, which is located at /etc/datadog-agent/checks.d
Create a new file called checkvalue.py, and insert the following:

 <code>
from checks import AgentCheck
import random

class HelloCheck(AgentCheck):
  def check(self, instance):
    instance['check_name']
    self.gauge('my_metric', random.randint(1,1000))
</code>

Another reference: https://datadog.github.io/summit-training-session/handson/customagentcheck/

Within a few minutes, there should be a new metric in the metric summary called my_metric. This is located in the DataDog 
website under metrics. Then click on summary and search for my_metric.
Collection intervals can be specified for each instance using a min_collection_interval
(In datadog prior to this release, min_collection_interval was a global)

<img width="953" alt="mymetric" src="https://user-images.githubusercontent.com/26099421/45601178-d4da0d00-b9d6-11e8-92f1-bf29ba2187bd.png">


Creating a datadog timeboard

Create a custom timeboard that uses datadogs API. The API makes it easy to get data in and out of Datadog

For this example we will create a timeboard with the  new metric we set up called my_metric.  
Depending on what you need or which visualization you would like to have, you can choose from: 
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

<img width="1024" alt="timeboardsetup2" src="https://user-images.githubusercontent.com/26099421/45601226-a14bb280-b9d7-11e8-84eb-2fc552a2ac58.png">
<img width="1024" alt="timeboardsetup" src="https://user-images.githubusercontent.com/26099421/45601235-c5a78f00-b9d7-11e8-8ad4-5c973b3c4ff4.png">

I used the directions located here: https://docs.datadoghq.com/api/?lang=python

Bonus: the anomaly graph is displaying the results along with the expected normal range



Creating a new metric monitor

Suppose you want to be alerted if your new timeboard is too high, too low, or not responding. For this example we will create a 
new metric monitor that watches the average of my_metric, and will alert if it is above the following values over the past five
minutes:
    - Warning threshold of 500, alerting threshold of 800, and to also notify if there is no data over the past 10 minutes.
If you want to configure a new monitor, go under monitors, and new monitor. 

Step 1: Specify what sort of detection method you want. For this example we are using the Threshold Alert, which means an alert
is triggered whenever a metric crosses a specified threshold.

<img width="1024" alt="metricsetup" src="https://user-images.githubusercontent.com/26099421/45601292-eae8cd00-b9d8-11e8-99ee-0c012e6e84e9.png">

Step 2: Define the metric (in this case my_metric), and set it to simple alert, which means it triggers a single alert when your
metric satisfies your alert conditions
Step 3: Set your alert conditions
    - Trigger when the metric is above(dropdown) the threshold on average(dropdown) during the last 5 minutes(dropdown) 
    - Type into the alert threshold box 800, and 500 in the warning threshold box
    - Select do not require in the full window for data evaluation field
    - Select notify(dropdown) if data is missing for more than 10(dropdown) minutes

<img width="953" alt="metricsetup5" src="https://user-images.githubusercontent.com/26099421/45601310-24b9d380-b9d9-11e8-9148-7546fe8800e1.png">

Step 4: Say what is happening. For this we use markdown in this field. Here is the example used for what we need

<code>
{{#is_alert}} System is too high {{/is_alert}} 

{{#is_warning}} System is almost too high {{/is_warning}} 

{{#is_no_data}} There is nothing reporting {{/is_no_data}} 

Notify: @christina.stahovec@gmail.com
<code>

<img width="1024" alt="metricsetup2" src="https://user-images.githubusercontent.com/26099421/45601254-2040eb00-b9d8-11e8-8ba8-e4c06b1717da.png">

Step 5: If you wish to notify your team input their names in the notify box. Here are some screenshots of threshold emails

<img width="1024" alt="emailmetricalert1" src="https://user-images.githubusercontent.com/26099421/45601349-81b58980-b9d9-11e8-9953-4d73b60699ce.png">
<img width="1024" alt="emailmetricalert" src="https://user-images.githubusercontent.com/26099421/45601355-9265ff80-b9d9-11e8-80a6-a9860d9a4f8c.png">
<img width="1024" alt="emailmetricalert3" src="https://user-images.githubusercontent.com/26099421/45601361-a7db2980-b9d9-11e8-9d7e-41ac3968fad1.png">
<img width="1024" alt="emailmetricalert2" src="https://user-images.githubusercontent.com/26099421/45601362-b88b9f80-b9d9-11e8-8bed-c680e79cbee4.png">

https://docs.datadoghq.com/monitors/
Bonus: if you click the manage downtime button in the monitor drop down menu, select my metric, choose what to silence,
set the schedule for a specific time by selecting the recurring tab, set repeat every one week


Flask and APM

Suppose you want to integrate a Flask app to use DataDogs APM solution, which is found under APM tab in the website.
This will be an example of tracing applications written in Python.  
First you have to install the Datadog tracing library, ddtrace, using pip. 
    - pip install ddtrace
Then to instrument your Python application use the included ddtrace-run command.
To use it, prefix your Python entry-point command with ddtrace-run
    - ddtrace-run python app.py
After a few minutes your traces should start showing up

<img width="1024" alt="apm1" src="https://user-images.githubusercontent.com/26099421/45601391-26d06200-b9da-11e8-9d79-5a111e1b64fd.png">
<img width="1024" alt="flask" src="https://user-images.githubusercontent.com/26099421/45601397-394a9b80-b9da-11e8-9504-d17fc515362f.png">
<img width="1024" alt="apm3" src="https://user-images.githubusercontent.com/26099421/45601403-48c9e480-b9da-11e8-9189-3412b825991a.png">
<img width="1024" alt="apm2" src="https://user-images.githubusercontent.com/26099421/45601414-5da67800-b9da-11e8-854c-cf5df4165107.png">
<img width="1024" alt="apm4" src="https://user-images.githubusercontent.com/26099421/45601419-68f9a380-b9da-11e8-98d4-12568ad90969.png">

Bonus: Difference between a service and a resource

A service is the name of a set of processes that work together to provide a feature set, and a resource is a particular query to a service 

Final Question:

I would use datadog to monitor metrics so that I could forecast my server utilization

For example, comparing the load from black friday in a particular store from last year, to possibly see how many people came into the store, how many purchases were made, and how many items were purchased. This would be good to get ready for the sale coming up this year. Additionally, I could hook into the datadog api and trigger services to autoscale.

 
