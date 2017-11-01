# Table of contents
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Tagging](#tagging)
4. [Collecting](#collecting)
5. [Custom Agent Check](#custom_agent_check)
6. [Monitoring](#monitoring)
7. [Dashboard](#dashboard)

## Introduction  
For this technical exercise, I was tasked with spinning up a Linux VM, deploying the DataDog agent and configuring it to monitor on a variety of metrics. Afterwards, then configure the DataDog dashboard to display some of these results, and set several alerts to notify me once they have reached the desired threshold. The following will be the results of my activities in this exercise and will be accompanied by various screenshots of my steps along the way.

## Installation  
First, we need to install the datadog agent on our intended host. You can either install from source or use the one-step install format that uses curl to install on your target system
```
DD_API_KEY="Your API Key" bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/dd-agent/master/packaging/datadog-agent/source/install_agent.sh)"
```
Then we need to start the agent and check the status to ensure it was installed properly. Do so by running the following commands
```
sudo /etc/init.d/datadog-agent start then sudo /etc/init.d/datadog-agent status
```
Now that you have installed the agent successfully and verified that it is running using the status command, you can move on to the next step of configuring tags for monitoring.

## Tagging  
After installing the DataDog agent we then need to configure several tags for monitoring. First, navigate to the DataDog config file located in /etc/dd-agent/datadog.conf and un-comment the tags line and add the tags you would like in the following format separated by comma's for more than one tag "a:1, b:2". Then if you wish to assign tags in the UI of DataDog start this by going to the Infrastructure List page. Click on any host and then click the Update Host Tags button. In the host overlay that appears, click Edit Tags and make the changes or additions that you would like.  

![DataDog Agent Tagging](https://github.com/Pilotreborn/hiring-engineers/blob/master/Screenshots/Agent_Tag_Config.PNG?raw=true)  

### And here we can see the tagging being done via the UI.

![DataDog Tagging via UI](https://github.com/Pilotreborn/hiring-engineers/blob/master/Screenshots/Tags%20Host%20Map.PNG?raw=true)  


## Collecting  
Next, we need to install a DB and perform the the configuration/integration to allow DataDog to monitor it appropriately. I chose to install MySQL and integrate it with DataDog. Once your desired DB is installed you will then need to navigate to the integrations page in DataDog and enable your DB specific integration. Once this has been done you then need to create a user for the agent via the following commands  
```
sudo mysql -e "CREATE USER 'datadog'@'localhost' password';"
sudo mysql -e "GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'localhost' WITH MAX_USER_CONNECTIONS 5;
```

Next, we need to make a copy of our example YAML file and rename it to mysql.yaml and make the necessary edits to complete the integration.
```
instances:
  - server: localhost
    user: datadog
    pass: password
    tags:
        - optional_tag1
        - optional_tag2
```  


Keep in mind YAML files use spaces, not tabs. I recommend you run the YAML config file through a validator like this one http://www.yamllint.com/ before saving to ensure the formatting is correct. I ran into a few issues with formatting on a couple occasions and this helped me identify and correct the mistake. Once you have configured the YAML file next we need to restart the agent and run the check command to verify that it is working as expected.  

```
sudo /etc/init.d/datadog-agent restart 
sudo /etc/init.d/datadog-agent check  
```  
You should see something similar to the following or similar to the screenshot below.  

```
Checks
======

  [...]

  mysql
  -----
      - instance #0 [OK]
      - Collected 8 metrics & 0 events
```  

![DataDog Check](https://github.com/Pilotreborn/hiring-engineers/blob/master/Screenshots/my_metric%20check%201.PNG?raw=true)  

## Custom_Agent_Check

Datadog allows for custom agent checks which enables you to send custom application metrics via multiple methods with StatsD being the most common format. For this exercise, I made a simple python application check file in the checks.d directory /etc/dd-agent/checks.d  

```
from checks import AgentCheck
import random
class HelloCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric.king', random.randint(1,1000))
```  
![my_metric.py](https://github.com/Pilotreborn/hiring-engineers/blob/master/Screenshots/my_metric_py.PNG?raw=true)  

This generates a random integer from 1-1000. An important step is to ensure you have a YAML config file with the exact same name in your DataDog conf.d directory/etc/dd-agent/conf.d. In the image below we can see the python file and the corresponding YAML config file which has the minimum collection interval set for every 45 seconds.  

![](https://github.com/Pilotreborn/hiring-engineers/blob/master/Screenshots/my_metric_collection_interval.PNG?raw=true)  

And here we can see this custom check being monitored in DataDog.   

![Custom Metric](https://github.com/Pilotreborn/hiring-engineers/blob/master/Screenshots/Timeboard%20Snapshot.PNG?raw=true)  

## Monitoring  
Now that we have configured our custom metric and are able to visualize our data we want to configure some monitors to be notified if certain criteria or thresholds have been reached. We start by navigating to the Monitors tab in the DataDog UI and selecting a new monitor. We then need to decide what we are going to be monitoring, and in this scenario we select metric. Now that we are on the edit screen for monitoring a metric select from the drop down which specific metric we want to set an alert or monitor for, and in this case we choose my_metric.king. You then need to select your host or tag you want to monitor this metric from. Now that the metric and host or tag has been selected we need to set our thresholds which will trigger these monitors, and in this case, we set our alert threshold at 800 and our warning threshold at 500, and now we are almost done. The last two steps are to craft our messaging based on what is happening and how those users or groups will be notified.  

You can use variables and markdown to craft custom and dynamic messaging based on what threshold have been reached. For example  

```
{{#is_alert}} my_metric.king alert threshold has been exceeded. Please check with the Ops team for a resolution {{/is_alert}}
```  
DataDog can integrate with various platforms to send your custom alerts and monitors including Slack, and Pagerduty, but for this exercise, we are going to have it notify us via email as seen below.  

![Monitor](https://github.com/Pilotreborn/hiring-engineers/blob/master/Screenshots/Managed_Downtime.PNG?raw=true)  
![Email Alert](https://github.com/Pilotreborn/hiring-engineers/blob/master/Screenshots/Email%20Notification%20Monitor.PNG?raw=true)  

## Dashboard  
Now that we have deployed and installed the agent, set some custom metrics, and configured some custom monitors to alert us of various thresholds that are reached, we will now create a custom Timeboard to visualize some of our data. To begin you will select dashboards from the menu on the left and select new dashboard. Then you will give your dashboard a name and choose between a time series and screen board dashboard. For this exercise, I went with a time series dashboard. Now that you have your initial dashboard created you can begin selecting various graphs you would like displayed here.  
#### Metric Over Host  
Let's begin by selecting the time series graph and dragging it to an open spot on our dashboard this will open an editor for us to select and apply some parameters for our graph. Next, select from the first drop-down and choose our custom metric we created earlier. Then choose our primary host from the next drop down then click the save button. Your graph should resemble something similar to the following.  

![](https://github.com/Pilotreborn/hiring-engineers/blob/master/Screenshots/metric%20over%20host%20edit.PNG)  

#### Applying the Anomaly Function  
Now we are going to follow the same steps above to add another time series graph to our dashboard, but with the anomaly function applied. Once your graph editor is open select a metric from your MySQL DB then click the plus sign on the right-hand side and under algorithms in the drop-down appears select anomaly. Your settings should look like something similar to the following.  

![](https://github.com/Pilotreborn/hiring-engineers/blob/master/Screenshots/Anomaly%20Graph.PNG)  

#### Applying the Rollup Function  
Just like the last example we will follow the same steps to add another graph to our dashboard. Once your editor is open select your custom metric you previously setup and map it over your host. then click the plus sign to the right and from the drop down that loads we will select Rollup and then average in the right list. Your settings should look something similar to the following.  

![](https://github.com/Pilotreborn/hiring-engineers/blob/master/Screenshots/Rollup.PNG)  

