This .md file contains the procedure [outlined](https://github.com/DataDog/hiring-engineers/tree/support-engineer) by [DataDog] (https://www.datadoghq.com/)

# Challenge Completion Overview
The completion of this exercise required me to download Vagrant for Windows (the system I am currently using) to create a linux instance that would be monitored by Datadog's agent. From ther, I installed the agent for the linux instance as well as for the mongodb instance that I also installed onto the server. 
## Level 0 - Installation of Vagrant on Windows 
* To complete Level 0, I downloaded [Vagrant](https://www.vagrantup.com/docs/installation/) for Windows
* From there, I installed a ubuntu environment that I could ssh into using Git
* I received assistance from [stackoverflow](http://stackoverflow.com/questions/27768821/ssh-executable-not-found-in-any-directories-in-the-path) which highlighted a common problem in which the console could not recognize the ssh command. The solution sets the path so that Git can be successfully using for SSHing
```
set PATH=%PATH%;C:\Program Files\Git\usr\bin
```

* [Install](https://app.datadoghq.com/account/settings#agent) the DataDog Agent onto the Ubuntu Interface
* Start the Agent using the code snippet provided by DataDog
```terminal
sudo /etc/init.d/datadog-agent start
```

## Level 1 - Collecting Data
#### getting agent reporting metrics 

* To get the agent working on vagrant's Ubuntu environment, I refered to the documentation [here](https://app.datadoghq.com/account/settings#agent)
* Basic agent interface commands such as starting, shutting down, and restarting were found [here](http://docs.datadoghq.com/guides/basic_agent_usage/ubuntu/)
* To get Agent Reporting on the default metrics for my local machine, I refered to [DataDog's Web Dashboard](https://app.datadoghq.com/dash/list)

<p align="center">
<img src="https://raw.githubusercontent.com/ziquanmiao/hiring-engineers/master/imgs/fig1.PNG" width="750" height="500" alt="ERROR">
</p>

#### In my own words, what is an Agent?
An agent is a software specific solution that is integrated into a web or infrastructure service tracking all the conceivable metrics produced. The agent interacts with Datadog's webservice allowing serviced members to determine the quality and health of their systems using DataDog's high level visualization tools. 

#### Adding tags to config file
* Use nano once again to edit the config file found in /etc/dd-agent/datadog.conf
```
	sudo nano /etc/dd-agent/datadog.conf 
```
Add the relevant tags code into the instances scope. For our purpose, we are tracking ziquanstag and the datadog suggest tags

<p align="center">
<img src="https://raw.githubusercontent.com/ziquanmiao/hiring-engineers/master/imgs/fig2.PNG" width="500" height="150" alt="_DSC4652">
</p>


* Below is a screenshot of my host containing the tags I initialized: #ziquanstag, env:prod, role:database

<p align="center">
<img src="https://raw.githubusercontent.com/ziquanmiao/hiring-engineers/master/imgs/fig3.PNG" width="750" height="500" alt="_DSC4652">
</p>

#### Connecting and Integrating MongoDB
* [Install](https://docs.mongodb.com/v3.0/tutorial/install-mongodb-on-ubuntu/) Mongodb v3 for ubuntu v12

* Integrated Mongodb following the instructions [here](https://app.datadoghq.com/account/settings#integrations/mongodb)

Successful integration allows datadog to showcase various metrics for mongodb
<p align="center">
<img src="https://raw.githubusercontent.com/ziquanmiao/hiring-engineers/master/imgs/fig4.PNG" width="750" height="500" alt="_DSC4652">
</p>

#### Custom Agent Check
* Add the following python agent check and yaml configuration files into the corresponding locations, to establish data transfer to datadog for the test.support.random metric

/etc/dd-agent/data.conf/firstCheck.py
```
from checks import AgentCheck
from random import random

class HelloCheck(AgentCheck):
	def check(self, instance):
		self.gauge('test.support.random', random.random())
```
/etc/dd-agent/conf.d/firstCheck.yaml
```
init_config:

instances:
	[{}]
```
<p align="center">
<img src="https://github.com/ziquanmiao/hiring-engineers/blob/master/imgs/fig5.PNG" width="750" height="500" alt="_DSC4652">
</p>

## Level 2 - Visualization of Data
I created a new dashboard, this dashboard tracks 3 metrics, the test.support.random metric is tracked as well as the system's uptime and the number of connections in mongodb. 
Below is a simple dashboard visualization tracking the test.support.random metric, the number of mongodb connections available and the system uptime

<p align="center">
<img src="https://github.com/ziquanmiao/hiring-engineers/blob/master/imgs/fig7.PNG" width="750" height="500" alt="_DSC4652">
</p>

#### What is the difference between a timeboard and a screenboard?

A timeboard has functionality that caters to all time series graphs available on the board. What this means is that when a user hovers over a specific time frame (denoted by the mouses position within that graphs frame), vertical lines will be drawn for all other time series graphs that reveals the corresponding values across other graphs at that time instance.
A screen board is more customizable and allows users to add basic functionalities like warnings, images and notes in addition to the graphing functionalities.

#### snapshot of test.support.random graph
<p align="center">
<img src="https://github.com/ziquanmiao/hiring-engineers/blob/master/imgs/fig8.PNG" width="750" height="500" alt="_DSC4652">
</p>

##Level 3 - Alerting Data

#### Setting up monitor with multihost
* Go to Monitors tab of Datadog's dashboard and click on New Monitor

<p align="center">
<img src="https://github.com/ziquanmiao/hiring-engineers/blob/master/imgs/fig10.PNG" width="750" height="500" alt="_DSC4652">
</p>

*Provide a descriptive monitor name, like: Randomly generated number exceeded .9

<p align="center">
<img src="https://github.com/ziquanmiao/hiring-engineers/blob/master/imgs/fig9.PNG" width="750" height="500" alt="_DSC4652">
</p>

*Schedule downtime using the "Manage Downtime" feature in the Monitors tab of the datadog web dashboard

<p align="center">
<img src="https://github.com/ziquanmiao/hiring-engineers/blob/master/imgs/fig13.PNG" width="400" height="700" alt="_DSC4652">
</p>

* below shows the two events, the trigger of when the test.support.random metric exceeds .90 and the initialization of the downtime disabling the agent check at night

<p align="center">
<img src="https://github.com/ziquanmiao/hiring-engineers/blob/master/imgs/fig12.PNG" width="750" height="450" alt="_DSC4652">
</p>

