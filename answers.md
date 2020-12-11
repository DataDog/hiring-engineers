## Setup the environment
1. First, let's install Vagrant which would help you build and manage virtual machines easily.
2. On your computer, download and install the [appropriate package](https://www.vagrantup.com/downloads) of Vagrant for your opearting system.
3. Launch a command prompt or terminal, run the command ```vagrant``` to verify that Vagrant has been installed successfully. 
4. Next, we need to initialize a Vagrant project in order to build a Linux virtual machine, simply follow these [3 steps](https://learn.hashicorp.com/tutorials/vagrant/getting-started-project-setup?in=vagrant/getting-started), and then you will have a fully running virtual machine in VirtualBox running Ubuntu 18.04 LTS 64-bit.
5. After you initilize a Vagrant project, a box has been installed automatically to quickly clone a virtual machine, [configure the box](https://learn.hashicorp.com/tutorials/vagrant/getting-started-boxes?in=vagrant/getting-started#use-a-box) so it will be used as a base by your project.
6. Once the box is configured, you are ready to boot your very first Vagrant environment! :checkered_flag: Run the command ```vagrant up``` from your terminal.
7. Once the VM is booted, since there is no GUI, you can SSH into the VM to interact with it. Run ```vagrant ssh``` to start an SSH session, run ```logout``` to get out of the SSH session. 
8. Other things you can do with your VM: run ```vagrant suspend``` to suspend the machine, ```vagrant halt``` to gracefully shut down the machine, and ```vagrant destory``` to destory the machine which removes all traces.

How about that? Setting up a VM in less than 5 mins. Cool. 

9. Now we want to use Datadog to collect metrics from that VM, and you just need 2 things to make it happen:  
   a. Apply a Datadog trial account at https://www.datadoghq.com/, use "Datadog Recruiting Candidate" in the "Company" field so you can get approved right away and start using Datadog.  
   b. Install the Datadog Agent on your VM and it will automatically collect metrics and report events about your system.  
10. There are 2 ways to install the Datadog Agent, either install it directly or as a container version. We will walk through the first method (it only takes one step) here, but take a look at this [instruction](https://docs.datadoghq.com/agent/docker/?tab=standard) if you want to install the container version. 
11. Different platforms require different commands to run to install the Agent, since we are running Ubuntu, SSH into your VM and run the following command to install the Agent in one step.  
```DD_AGENT_MAJOR_VERSION=7 DD_API_KEY=<Your 32-digit API key> DD_SITE="datadoghq.com" bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_script.sh)"```  
   a. Find your API key by going to Datadog --> Integrations --> APIs --> API Keys 
   b. You will be asked to provide your Datadog account password after running the command  
12. The Datadog Agent has a configuration file that you can use to set properties and manipulate behaviors. There are two required parameters that need to be set before starting to use the Agent.  
   a. Run ```vagrant up``` to start your VM  
   b. Run ```vagrant ssh``` to enter an SSH session  
   c. Find the Datadog Agent confirmation file ```datadog.yaml``` under ```/etc/datadog-agent/```    
   d. Edit the file to include the following two parameters, they are used to associate your Agent’s data with your organization and the Datadog site.    
      1). ```api_key: <your API key>```  
      2). ```site: datadoghq.com```
12. Run this status command ```sudo service datadog-agent status``` to verify the Agent has been installed and is running properly.
13. If you go to Datadog --> Infrastructure --> Host Map, you should see your vagrant host show up as well. 

That's it! You now have successfully setup your enviornment and next we get to play around with the Agent so you can gain visibility and insights into your systems and applications.


## Collecting Metrics
1. When visualizing Datadog telemetries, you can use Tags to filter, aggregate, and compare them to gain better observations. Tags can be added in multiple ways, we will modify the Datadog Agent configuration file to add some host tags but check out these [other methods](https://docs.datadoghq.com/getting_started/tagging/assigning_tags?tab=noncontainerizedenvironments) if you are interested.  
   a. Edit the Datadog Agent confirmation file ```datadog.yaml``` to include:
      ```
      tags:  
           - "env:dev"
           - "service:hiring-exercise"
           - "version:1.0"
           - "region:us-east"
           - "project:trial"
      ``` 
   b. Now go to the Host Map page in Datadog and you should see the following screen which shows the host tags you just added.:v:    
![Alt text](https://github.com/yangli3/hiring-engineers/blob/master/Host-Map-Datadog.png "Host Map with Tags")

2. Datadog can not only collect metrics about your host system but can also be used to monitor your infrastructure as a whole, for example Datadog can integrate with your database to collect metrics and logs so you can see how the database impacts the whole unified system. Let's install a MySQL database to your VM and connect Datadog with it to gain some more insight.   

   a. Install a MySQL database  
      1). Run ```sudo apt update``` to update the package index  
      2). Run ```sudo apt install mysql-server``` to install the default MySQL package  
      3). Run ```sudo mysql_secure_installation``` to configure MySQL, this will take you through a series of prompts where you can make some changes to your MySQL installation’s security options such as setting the password for the root user  
      4). Run ```mysql -u root -p``` and enter your password for the root user to enter the mysql console  
      
   b. Now you have MySQL installed, let's set up a MySQL integration with Datadog. Go to Datadog --> Integrations, find the MySQL integration, and follow the [instruction](https://app.datadoghq.com/account/settings#integrations/mysql) there to prepare MySQL and configure the integration.  

3. The Agent automatically collects many metrics from your host and any integrated systems, however you can also write custom Agent checks to collect metrics from custom applications or unique systems. For example, we can write a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.  
   a. In the vagrant SSH session, change directory to ```/etc/datadog-agent/checks.d```  
   b. Run ``` touch my_metric.py``` to create a python file, use the vi editor to write the following code to the python file 
   ```
   import random

   try:
       from datadog_checks.base import AgentCheck
   except ImportError:
       from checks import AgentCheck

   __version__ = "1.0.0"

   class MyMetricCheck(AgentCheck):
       def check(self, instance):
           num = random.randint(0, 1000)
           self.gauge("my_metric", num, tags=['TAG_KEY:TAG_VALUE'])
   ```
   c. Change directory to ```/etc/datadog-agent/config.d```  
   d. Run ```touch my_metric.yaml``` to create a configuration file for the check you just created, use the vi editor to write the following code to the yaml file  
   ```instances: [{}]```  
   e. Note the names of the configuration and check files must match  
   f. Now if you go to Datadog --> Metrics --> Explorer, and search for "my_metric" in the Graph field, you should be able to see a graph of the custom check you just created. :heart_eyes_cat:   
   g. By default, the Datadog Agent collects metrics every 15 seconds, you can easily change the time interval for collecting the custom check my_metric. For example, to have the Agent submits the metric every 45 seconds, edit the ```my_metric.yaml``` configuration file to include the following code  
   ```
   init_config:

   instances:
     - min_collection_interval: 45
   ```
   
## Visualizing Data
Datadog offers many ways to visualize your data, on the dashboard level, you can use Timeboards or Screenboards. Timeboards are commonly used for troubleshooting, correlation, and general data exploration, while Screenboards are commonly used as status boards or storytelling views that update in real-time or represent fixed points in the past.

Datadog has an extensive API set that can be used to access the Datadog platform programmatically. Let's call an API to create a cool Timeboard so you can show off the custom metric you just created. :sunglasses:  

1. Following the "Setup" secion of this [instruction](https://docs.datadoghq.com/getting_started/api/) to set up Postman, import the Datadog API collection and configure the Datadog Authentication. 
2. Once you have the Postman environment setup, we can work with the Datadog API collection  
   a. In Postman, on the left hand side, under the ```Datadog API collection```, find ```Dashboards``` and click ```Create a new dashboard```  
   b. Use ```POST``` with ```https://api.datadoghq.com/api/v1/dashboard```  
   c. Enter the following JSON for ```body``` and hit ```Send```  
   ```
   {
     "description": "string",
     "is_read_only": false,
     "layout_type": "ordered",
     "notify_list": [],
     "template_variable_presets": [
       {
         "name": "string",
         "template_variables": [
           {
             "name": "string",
             "value": "string"
           }
         ]
       }
     ],
     "template_variables": [
       {
         "default": "my-host",
         "name": "host1",
         "prefix": "host"
       }
     ],
     "title": "Yang First Timeboard",
     "widgets": [
       {
         "definition": {
             "title": "Custom Metric",
             "type": "timeseries",
             "requests": [
                 {
                     "q": "my_metric{host:vagrant}"
                 }
             ],
             "yaxis": {
                 "scale": "linear",
                 "min": "0",
                 "max": "1000",
                 "include_zero": true
             }
         },
         "id": 1,
         "layout": {
           "height": 0,
           "width": 0,
           "x": 0,
           "y": 0
         }
       },
       {
         "definition": {
             "title": "MySQL Performance CPU Time",
             "type": "timeseries",
             "requests": [
                 {
                     "q": "anomalies(mysql.performance.cpu_time{host:vagrant}, 'basic', 3)"
                 }
             ],
             "yaxis": {
                 "scale": "linear",
                 "min": "0",
                 "max": "1.5e-3",
                 "include_zero": true
             }
         },
         "id": 2,
         "layout": {
           "height": 0,
           "width": 0,
           "x": 0,
           "y": 0
         }
       },
       {
         "definition": {
             "title": "Custom Metric with Rollup Function",
             "type": "timeseries",
             "requests": [
                 {
                     "q": "my_metric{host:vagrant}.rollup(sum, 3600)"
                 }
             ],
             "yaxis": {
                 "scale": "linear",
                 "min": "0",
                 "max": "80000",
                 "include_zero": true
             }
         },
         "id": 3,
         "layout": {
           "height": 0,
           "width": 0,
           "x": 0,
           "y": 0
         }
       }
     ]
   }
   ```
   d. Now you've successfully created a Timeboard using API. Go to Datadog --> Dashboards --> Dashboard List, and find the Timeboard with the title ```Yang First Timeboard```, it should look like the following screenshot. Also, here is a public link to that Timeboard. https://p.datadoghq.com/sb/912oapovcm9ys7nf-6d2ff9da5161f89c0f8772071c07b87f
![Alt text](https://github.com/yangli3/hiring-engineers/blob/solutions-engineer/Yang-First-Timeboard-Datadog.png "Timeboard Created from API")

   e. You notice that the Timeboard has 3 graphs in it, let's take a look at what these 3 graphs are, as they were defined in the above script.  
      1). We created the first widget that shows the custom metric scoped over the host, the definition is ```"q":"my_metric{host:vagrant}"```  
      2). The second widget shows the ```mysql.performance.cpu_time``` metric from the MySQL Integration with the anomaly function applied. The definition is ```"q": "anomalies(mysql.performance.cpu_time{host:vagrant}, 'basic', 3)"```. What this Anomaly graph displays is the blue part means the data fall into its normal range and is expected, the red part means the data is anomalous and have gone beyond the expected behavior based on the past data, the gray band represents the upper bound and lower bound of the data in order to be considered as normal and not anomalous.  
      3). The third widget shows the custom metric with the rollup function applied to sum up all the points for the past hour into one bucket. The definition is ```"q": "my_metric{host:vagrant}.rollup(sum, 3600)"```.

## Monitoring Data
What is the point of collecting data if we don't monitor its behavior to gain insight or be notified whenever something happened unexpectedly? Now that we have been collecting data from our custom metric that randomly generates a number between 1 and 1000 for every 45 seconds, let's monitor it and get alerted whenver the number goes above 800.   

Let's say we want to have a monitor that watches the average of your custom metric (my_metric) and will alert you if it’s above the following values over the past 5 minutes:    
- Warning threshold of 500
- Alerting threshold of 800
- And also ensure that it will notify you if there is No Data for this query over the past 10m.

1. To create such monitor, go to Datadog --> Monitors --> New Monitor --> Metric, and make the following configurations  
![Alt text](https://github.com/yangli3/hiring-engineers/blob/solutions-engineer/monitor%20setting.png)

2. For the alert message title and body, you can create different messages by using message template variables. Following is the title and body of the message in the above screenshot.

```
{{#is_alert}} Test Metric is Above {{threshold}} on host {{host.ip}} {{/is_alert}} {{#is_warning}} Test Metric is Above {{warn_threshold}} on host {{host.ip}} {{/is_warning}} {{#is_no_data}} Test Metric is Missing Data on host {{host.ip}} {{/is_no_data}}
```

```
{{#is_alert}} You haven't gotten any alert messages recently, so here is a random one just to let you know that I haven't stopped caring.

Just kidding! The test metric on host {{host.ip}} has gone above {{threshold}} during the last 5 mins, good luck! 
{{/is_alert}}

{{#is_warning}} Don't panic, it's just a warning. 

The test metric on host {{host.ip}} has gone above {{warn_threshold}} during the last 5 mins, ignore it to get a heartwarming alert next time! 
{{/is_warning}}

{{#is_no_data}} I can't believe your test metric is ghosting me, I haven't heard anything from it for more than 10 mins. 10 mins! Jesus. UNBELIEVABLE. {{/is_no_data}} 

-- Your favorite Datadog agent

@liyangice@gmail.com
```

3. Now you have successfully set up 3 alerts on your custom metric, you should start receive alert emails like this one
![Alt text](https://github.com/yangli3/hiring-engineers/blob/solutions-engineer/Alert-Email-Monitor-500.png "Warn Email")

4. Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Let's set up two scheduled downtimes for this monitor.  
- One that silences it from 7pm to 9am daily on M-F,  
- And one that silences it all day on Sat-Sun.

Go to Datadog --> Monitors --> Manage Downtime --> Schedule Downtime    
   a. Following the configuration in this screenshot to shcedule the first downtime
   ![Alt text](https://github.com/yangli3/hiring-engineers/blob/solutions-engineer/Manage-Downtime-Datadog%201.png)
   
   b. Following the configuration in this screenshot to shcedule the second downtime
   ![Alt text](https://github.com/yangli3/hiring-engineers/blob/solutions-engineer/Manage-Downtime-Datadog%202.png)
   
Once these two downtimes are scheduled, you should receive the following email notifications
![Alt text](https://github.com/yangli3/hiring-engineers/blob/solutions-engineer/Downtime-Weekday.png "Downtime for Weekdays")
![Alt text](https://github.com/yangli3/hiring-engineers/blob/solutions-engineer/Downtime-Weekend.png "Downtime for weekend")

## Collecting APM Data
Now we have used Datadog to collect host metrics, database metrics, and a custom metric, do you know Datadog can also collect application performance metrics (APM)? We can use 1 minute to quickly build a Flask application and have the Agent collects performance metrics from it. The setup process is pretty much automated, so this will be easy peasy. 

1. Install Flask if you don't have it, following this [installation instruction](https://flask.palletsprojects.com/en/0.12.x/installation/#installation)  
2. In a vagrant SSH session, change directory to ```myproject``` (this is the directory you created when you setup the virtualenv in the above step)
3. Run ```touch datadog-hiring.py``` to create a Python file, use vi editor to write the following code to the Python file. (You can use other languages too, we are using Python for this example)  
```
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
```
4. Go to Datadog --> APM --> Setup & Configuration --> Service Setup --> Host-Based --> Python, following the [instruction](https://app.datadoghq.com/apm/docs?architecture=host-based&language=python) there to use ```ddtrace-run``` to automatically instrument your application.    
5. Once the application is instrumented and you have restarted your service, if you go back to Datadog --> APM, you should be able to see the Services/Traces/Profiles screen, like the following.
![Alt text](https://github.com/yangli3/hiring-engineers/blob/solutions-engineer/Service-List-env-dev-Datadog.png)
6. Do you know the difference between a Service and a Resource? A service is a building block of a modern microservice architecture, it groups together endpoints, queries, or jobs for the purposes of building an application. A resource represents a particular domain of a customer application, it is typically an instrumented web endpoint, database query, or background job.

Phew. You did it! So far you have successfully collected metrics from your host, your database, your custom check, and your application. Now it's that final moment that we get to put everything together into a beautiful dashboard so you can look at your infrastructure as a whole, this will be the fruit of your hard work.  

1. To build a dashboard that includes both APM and Infrastructure metrics, go to Datadog --> Dashboards --> Create Dashboard --> Create a Screenboard/Timeboard  
2. On the blank dashboard, click on "Edit Widgets" and start drag and drop widgets to the canvas and set them up with your APM and Infrastructure metrics  
3. At the end, you should have a dashboard like this one. Also, here is a public link to that dashboard. https://p.datadoghq.com/sb/912oapovcm9ys7nf-c75d97b6ab46ba4c6c4c40e7c3d0745b
![Alt text](https://github.com/yangli3/hiring-engineers/blob/solutions-engineer/APM-Dashboard.png "APM and Infrastructure Metrics Dashboard")

## Final Question
Considering the strange time we are all in this year, I would use Datadog to monitor COVID testing waiting time at different testing sites, allowing someone who wants to be tested to be able to check which testing site has a shorter waiting time, so they can go to the testing site that has the shortest waiting line and reduce the risk of getting affected while waiting at the testing site.

To get this idea implemented, Datadog needs to keep track of the number of people waiting in the line, and the average time it takes to test an individual, and use these data to calculate the real-time waiting time. The testing site needs to have a counting system that can count the number of people waiting in the line, like the one you may have seen in a bank or the DMV. The testing site needs to have a system that records the start time and end time of a test, Datadog can integrate with that system to get the average testing time per person. Once we have the real-time waiting time metric of each testing site, we can build a dashboard to show this information in one place so people can have a clear view of which testing site they want to go to. 
