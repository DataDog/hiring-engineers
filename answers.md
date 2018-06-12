# Welcome
Welcome to the Datadog product demonstration!
# Agenda
- Prerequisites - Setup the environment (optional content)
   - Installing and Configuring VirtualBox
   - Installing and Configuring Vagrant
   - Installing the Datadog Agent
- Collecting Metrics
- Visualizing Data
- Monitoring Data
- Collecting APM Data
- Final Question
# Prerequisites - Setup the environment
NOTE: This section is intended to assist with setting up an environment to run Datadog.  This section can be skipped if you already have an environment with the Datadog Agent installed.<br>

The Datadog agent can be installed on a variety of operating systems.  For this demo, we will be utilizing a Linux VM, courtesy of Vagrant, and viewing it through VirtualBox.  We will install the Datadog Agent to the Linux VM that we deploy in this section.  To view details of this content, click: <details><summary>**Expand**</summary>

## Installing and Configuring VirtualBox
You can download VirtualBox here:<br>
[https://www.virtualbox.org/wiki/Downloads](url)<br>
   
For this demo, we will download the VirtualBox 5.2.12 platform package for OS X hosts
![virtualbox](https://user-images.githubusercontent.com/39865915/41008653-f89df63a-68e0-11e8-9e1c-475b2a53c7d9.png)<br>
Execute the VirtualBox.pkg and take all defaults through the installation
![virtualbox2](https://user-images.githubusercontent.com/39865915/41008714-5562d502-68e1-11e8-933b-0582ade8bef0.png)<br>
## Installing and Configuring Vagrant
The "getting started" guide for Vagrant can be found here:<br>
[https://www.vagrantup.com/intro/getting-started/index.html](url)<br>

You can download Vagrant here:<br>
[https://www.vagrantup.com/downloads.html](url)<br>

For this demo, we will download the Mac OS 64-bit package<br>
![vagrant](https://user-images.githubusercontent.com/39865915/41007786-5ba3f946-68dc-11e8-9f4f-135d38ede7b9.png)
Execute _vagrant.pkg_ and take all defaults through the installation
![vagrant2](https://user-images.githubusercontent.com/39865915/41007954-30768710-68dd-11e8-94f4-fc8888c58ee3.png)<br>
Now that we have Vagrant installed, we can create a directory for our Vagrant project by opening a terminal window and entering the following commands:<br>
```
mkdir vagrant_dd_demo
cd vagrant_dd_demo
```
For this demo, we will use the official Ubuntu 16.04 LTS, from Vagrant's cloud box catalog found here:<br>
[https://app.vagrantup.com/boxes/search](url)<br>
In the terminal, enter the command to add the VM box:<br>
``` 
vagrant box add ubuntu/xenial64
```
To create and initialize the Vagrant configuration file to use the box we just added, enter the following command in the terminal:<br>
```
vagrant init ubuntu/xenial64
```
![vagrant3](https://user-images.githubusercontent.com/39865915/41010123-96679d18-68ea-11e8-8f02-f5933a79b6cf.png)<br>
Finally, to launch our Vagrant VM via virtual box, enter the following command into the terminal:<br>
```
vagrant up --provider=virtualbox
```
Launch VirtualBox and you will see the Vagrant VM in a _Running_ state.  We need to configure the Network adaptor for our machine to _Bridged Adaptor_ so that our VM will connect to whatever default network device is allocating IP addresses for our physical network, allowing for a _bridge_ between the physical and virtual networks.  To do this from VirtualBox:
- Click on the _Settings_ -> _Network_ -> _Adaptor 1_<br>
- Select Attached to: _Bridged Adaptor_, Name: _en1: WiFi (AirPort)_<br>
![netadapt](https://user-images.githubusercontent.com/39865915/41270431-061273ca-6dc0-11e8-8f49-5360e00b0c5b.png)<br>
Restart the VM to make the changes take effect.  Right-click on the Click the _Show_ button to bring up the VM's virtual UI<br>
![virtualbox3](https://user-images.githubusercontent.com/39865915/41123326-235a2ace-6a53-11e8-8609-1c1cc9a06a04.png)
Login to the VM with the following:<br>
```
User: vagrant
Password: vagrant
```
![virtualbox4](https://user-images.githubusercontent.com/39865915/41125387-2c7e557a-6a59-11e8-8742-97363391faad.png)<br>
## Installing the Datadog Agent
Go to the Datadog website ([https://www.datadoghq.com](url)), click on the _FREE TRIAL_ icon, and enter your information to begin your trial:<br>
![datadog](https://user-images.githubusercontent.com/39865915/41126910-f92fa9bc-6a5d-11e8-8f36-93fc2330958f.png)<br>
Since we are installing the agent to our VM that we just setup/configured, we will select "Ubuntu" from the menu run the installation script command from our VM command line interface:<br>
```
DD_UPGRADE=true bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```
If successful, the result should look similar to the following:<br>
![virtualbox5](https://user-images.githubusercontent.com/39865915/41126935-0aacfc9e-6a5e-11e8-921f-cdddf2e0b3c0.png)<br>
Once the installed agent is detected by Datadog, click "Finish" and you will be taken to the Datadog Events page<br>
![datadog2](https://user-images.githubusercontent.com/39865915/41130524-06a7af46-6a6c-11e8-84f6-010901d5d043.png)<br>
</details>

# Collecting Metrics
## Tags
**Reference**: [https://docs.datadoghq.com/getting_started/tagging](url)<br>
Agent Tags are, essentially, a feature that allows a user to establish custom "filters" associated with each host that has the Datadog Agent installed.  Agent tags are configured in the _datadog.yaml_ file.  It is recommended that tags be implemented with a _key:value_ syntax for optimal functionality. For this exercise, we will edit the _datadog.yaml_ file to include the following tags:
```
env:test
role:database
region:west
```
![vagrant4](https://user-images.githubusercontent.com/39865915/41140007-009677d4-6aa0-11e8-9052-0aab3e15cccc.png)<br>
After making changes to _datadog.yaml_, restart the Datadog agent with the command:<br>
```
sudo service datadog-agent restart
```
The added tags can then be seen and available for use on Datadog's Host Map page:<br>
![datadog3](https://user-images.githubusercontent.com/39865915/41140505-c2afa7c6-6aa2-11e8-8ef9-06028214b8ad.png)<br>
## Install MySQL
**Reference**: [https://support.rackspace.com/how-to/installing-mysql-server-on-ubuntu](url)<br>
Install MySQL to the VM via the package manager by running the following commands:<br>
```
sudo apt-get update
sudo apt-get install mysql-server
```
When prompted, set the _root_ user password to a password of your choosing.  For this demonstration, we used _datadog_ as the password.<br>
You can start the MySQL shell by executing the following command:<br>
```
/usr/bin/mysql -u root -p
```
To exit the _MySQL_ shell, execute the command:<br>
```
exit
```
## Install Datadog MySQL Integration
**Reference**: [https://docs.datadoghq.com/integrations/mysql](url)<br>
From the VM, make a copy of the MySQL _conf.yaml.example_ file, named _conf.yaml_, by executing the following commands:<br>
```
cd /etc/datadog-agent/conf.d/mysql.d
sudo cp conf.yaml.example conf.yaml
```
Follow the directions from the _Metric Collection_ section (from [https://docs.datadoghq.com/integrations/mysql](url)) to configure the MySQL integration for metric collection by editing the newly created _conf.yaml_ file.  To edit the file, execute the following commands:<br>
```
cd /etc/datadog-agent/conf.d/mysql.d
sudo vi conf.yaml
```
Make the following changes:<br>
```server: 127.0.0.1
user: datadog
pass: 'datadog'
replication: 0
galera_cluster: 1
```
Uncomment the _user_, _pass_, _port_, _options_, _replication_, _galera_cluster_, _extra_status_metrics_, _extra_innodb_metrics_, _extra_performance_metrics_, _schema_size_metrics_, and _disable_innodb_metrics_ entries<br>
The resulting _conf.yaml_ file should look similar to the following:<br>
![vagrant5](https://user-images.githubusercontent.com/39865915/41173102-9e640aac-6b0a-11e8-8fc0-7cf756bde876.png)<br>
Save and exit the VI editor<br>
On the VM,prepare MySQL by creating a Datadog user (with password) and granting appropriate permissions by executing the following commands:<br>
```
/usr/bin/mysql -u root -p (enter password when prompted)
CREATE USER 'datadog'@'127.0.0.1' IDENTIFIED BY 'datadog';
GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'127.0.0.1' WITH MAX_USER_CONNECTIONS 5;
GRANT PROCESS ON *.* TO 'datadog'@'127.0.0.1';
exit
```
Using the _Integrations_ section of the Datadog UI, install the _MySQL_ integration:<br>
![datadog4](https://user-images.githubusercontent.com/39865915/41144549-20871bf4-6ab2-11e8-9d11-40490b3c1a70.png)<br>
## Create a Custom Agent Check
**Reference**: [https://docs.datadoghq.com/developers/agent_checks](url)<br>
Agent checks are intended to allow a user to collect Datadog metrics from custom applications or unique systems, while metric collection from more common applications, public services or open source projects, are intended to be implemented via Datadog's Integrations.  Agent checks have two parts, the check file, written in Python, and the configuration file.  
Both the check file and configuration must share the same name (ex. _mycheck.py_ and _mycheck.yaml_, respectively).  The check file resides in the Agent's _checks.d_ directory, and the configuration file resides in the Agent's _conf.d_ directory.  Both the _checks.d_ and _conf.d_ directories exist under the Agent's root directory, in our case, _/etc/datadog-agent_.<br>
To show how a custom Agent check is implemented, we can create a custom Agent check that submits a metric named _my_metric_ with a random value between 1 and 1000.  We will also configure _my_metric_ check to have a collection interval that only submits once every 45 seconds.<br>

The _mycheck.py_ check file is as follows:<br>
![mycheck_py](https://user-images.githubusercontent.com/39865915/41180516-5432e07a-6b23-11e8-8881-0c9912966df0.png)<br>
The _mycheck.yaml_ configuration file is as follows:<br>
![mycheck_yaml](https://user-images.githubusercontent.com/39865915/41182984-fc5f9eba-6b2c-11e8-8007-add3578a0be0.png)<br>
After creating _mycheck.py_ and _mycheck.yaml_, restart the Datadog agent with the command:<br>
```
sudo service datadog-agent restart
```
**Bonus**: We can change the collection interval without modifying the python check file we created by using the _min_collection_interval_ in the configuration file, _mycheck.yaml_, as referenced in the _Configuration_ section from [https://docs.datadoghq.com/developers/agent_checks](url).  Be sure to restart the agent after any check file or configuration file updates!
# Visualizing Data
**Reference**: [https://docs.datadoghq.com/ja/api/#timeboards](url)<br>
**Reference**: [https://docs.datadoghq.com/ja/api/#metrics](url)<br>
**Reference**: [https://docs.datadoghq.com/monitors/monitor_types/anomaly](url)<br>
**Reference**: [https://docs.datadoghq.com/graphing/miscellaneous/functions](url)<br>
## Generate Application Key
To use the Datadog API, we need to have both our API key, as well as create an Application key.  We can both see our API key and create our App key from the Datadog UI by navigating to **Integrations -> APIs**.  To create the App key, simply type in the _New application key_ field and click on the _Create Application Key_ button.<br>
## Install _pip_ and Datadog Module for Python
Before we can utilize the Datadog API, we need to install the _pip_ package management system, for software packages written in Python, onto our VM.  The Datadog Python module allows us to to use the Datadog API within our Python scripts, which among other things, allows us to implement Datadog Timeboards.  To do this we run the following commands:<br>
```
_sudo apt-get update && sudo apt-get -y upgrade_
_sudo apt-get install python-pip_
_pip install datadog_
_pip install --upgrade pip_
```
## Creating a Timeboard
One way we can leverage the Datadog API, is by using it to create Timeboards.  For this demo, we will create a Timeboard that contains:
- Our custom metric scoped over our host
- Any metric from the Integration on our database with the anomoly function applied
- Our custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

Following the Python _example request_ from the _Create a Timeboard_ section, we can get a template for our Python script.  Our script will simply replace the existing example, as well as define two more graphs, to accomplish the above three criteria.  Our _mytimeboard.py_ was created in the _/vagrant_ directory of our VM and can be seen here:<br>
```
from datadog import initialize, api

options = {
	'api_key': 'c1a1bf2d95c1258d546019cfc7d1edae',
	'app_key': '2cde06fd67efc07965f3b57b32679c5a557f96ac'
}

initialize(**options)

title = "My Timeboard"
description = "An informative timeboard"
graphs = [{
	"definition": {
		"events": [],
		"requests": [
			{"q": "my_metric{*}"}
		],
	"viz": "timeseries"
	},
	"title": "my_metric Random Number Generator"
},
{
	"definition": {
		"events": [],
		"requests": [
			{"q": "anomalies(avg:mysql.performance.kernel_time{*}, 'basic', 3)"}
		],
	"viz": "timeseries"
	},
	"title": "% of CPU Time in kernal space by MySQL with Anomoly Function" 
},
{
	"definition": {
		"events": [],
		"requests": [
			{"q": "my_metric{*}.rollup(sum, 3600)"}
		],
	"viz": "timeseries"
	},
	"title": "my_metric Sum Using Rollup"
}]

template_variables = [{
	"name": "host1",
	"prefix": "host",
	"default": "host:my-host"
}]

read_only = True

api.Timeboard.create(title=title, description=description, graphs=graphs, template_variables=template_variables, read_only=read_only)
```
We can initialize our newly created Timeboard in Datadog by executing our Python script.  To do this, run the following commands:<br>
```
cd /vagrant
python mytimeboard.py
```
Once the script executes successfully, we can view our newly created Timeboard in the Datadog UI by navigating to the **Dashboards -> Dashboard List** section and selecting _My Timeboard_ under **All Dashboards**:<br>
![timeboard](https://user-images.githubusercontent.com/39865915/41197001-1a56314a-6c04-11e8-8fe9-43d119d01324.png)<br>
From the Timeboard scren in the Datadog UI, we can zoom in a a range by simply click-holding on a point on any graph and dragging it to the time interval desired.<br>

We can also take snapshots of a particular graph and send them to any Datadog user using the _@_ notation.<br>

For this demo, we changed the timeframe to the past five minutes, and sent a snapshot of the _my_metric Random Number Generator_ graph to myself, as shown below:<br>
![snap](https://user-images.githubusercontent.com/39865915/41197085-8aa63420-6c06-11e8-99a7-cd4025fc85e5.png)<br>

**Bonus**: In this demo, the anomaly function was defined in _mytimeboard.py_, in the line:<br>
```
{"q": "anomalies(avg:mysql.performance.kernel_time{*}, 'basic', 3)"}
```
Our anomaly graph is displaying when the average percentage of CPU time spent in kernel space by _MySQL_ on our VM goes above or below three standard deviations away from the established range.<br>
# Monitoring Data
**References**: [https://docs.datadoghq.com/monitors/](url)<br>
Monitoring is a key component of Datadog's software.  Monitor's allow Datadog's users to continuously check metrics, integration availibilty, network endpoints, (and more), and be notified by a variety of methods when established conditions are met.<br>

In this demonstration, we will create a new Metric Monitor that watches the average of custom metric, _my_metric_, that we created at the beginning of this demonstration.  This Metric Monitor will alert if it is above the following values over the past 5 minutes:<br>
- _Warning_ threshold of 500<br>
- _Alert_ threshold of 800<br>
- Ensure that it will notify us if there is No Data for this query over the past 10 minutes<br>

We will configure the monitor message so that it will:<br>
- Send us an email whenever the monitor triggers<br>
- Create different messages bases on whether the monitor is an _Alert_, _Warning_, or _No Data_ state<br>
- Include the metric value that caused the monitor to trigger, as well as a host IP when the monitor triggers an _Alert_ state<br>
## Create and Configure a Custom Monitor
To create a cutom monitor to satisfy the above criteria:<br>
- ***Datadog UI*** -> ***Monitors*** -> ***New Monitor***<br>
- Under _Select a monitor type_, select _Metric_<br>
   1. Choose detection method: _Threshold Alert_<br>
   2. Define the metric: Metric: _my_metric_ (you can leave remaining fields default)<br>
   3. Set alert conditions: Trigger when the metric is _above_ the threshold _on average_ during the last _5 minutes_<br>
      Alert threshold: _800_<br>
      Warning threshold: _500_<br>
      Alert recovery threshold: _(default)_<br>
      Warning recovery threshold: _(default)_<br>
      _Do not require_ a full window of data for evaluation<br>
      _Notify_ if data is missing for more than _10 minutes_<br>
      _Never_ automically resolve this event from a no data state<br>
      Delay evaluation by _0_ seconds<br>
   4. Say what's happening:<br>
      _Random Number Generator_<br>
     
      _{{#is_alert}}_<br>
      _Monitor is reporting above established threshold of 800!_<br>
      _{{/is_alert}}_<br>

      _{{#is_warning}}_<br> 
      _Monitor is reporting above established threshold of 500!_<br>
      _{{/is_warning}}_<br>
      
      _{{#is_no_data}}_<br>
      _Monitor is reporting no data!_<br>
      _{{/is_no_data}}_<br>
   5. Notify your team:<br>
      _Timothy Saleck_<br>
      _Do not notify_ alert recipients when alert is modified<br>
      _Do not restrict_ editing of this monitor to its creator or administrators<br>
- Click _Save_<br>      

When the monitor triggers, an email is sent to the user:<br>
![rng](https://user-images.githubusercontent.com/39865915/41198618-f273dadc-6c36-11e8-803e-093be10ca150.png)<br>

**Bonus**:  We can also configure our monitor to only alert during in-office hours, so we are not alerted when we are out of the office.  For this demonstration, we will set up downtimes for our monitor as follows:<br>
- Monitor will be off/silent from 7PM-9AM Mon-Fri<br>
- Monitor will be silent all day Sat-Sun<br>

To make these updates to our monitor, do the following:<br>
- ***Datadog UI*** -> ***Monitors*** -> ***Manage Downtime***<br>
- Select _Schedule Downtime_<br>
   1. Choose what to silence: _Monitor: Random Number Generator_, _host: ubuntu-xenial_<br>
   2. Schedule:<br> 
      _Recurring_<br>
      Start Date: _2018/06/11_, Time Zone: _(default)_<br>
      Repeat every: _1 days_<br>
      Beginning: _7PM_<br>
      Duration: _14 hours_<br>
      Repeat until: _No end date_<br>
   3. Add a message:
      _Monday-Friday, 7PM-9AM off!_<br>
   4. Notify your team:<br>
      _Timothy Saleck_<br>
- Click _Save_<br> 
![monfri](https://user-images.githubusercontent.com/39865915/41198634-2664223e-6c37-11e8-8dcc-fa7d69d53b9d.png)<br>

And repeat for the weekend off!<br>
- ***Datadog UI*** -> ***Monitors*** -> ***Manage Downtime***<br>
- Select _Schedule Downtime_<br>
   1. Choose what to silence: _Monitor: Random Number Generator_, _host: ubuntu-xenial_<br>
   2. Schedule:<br> 
      _Recurring_<br>
      Start Date: _2018/06/15_, Time Zone: _(default)_<br>
      Repeat every: _7 days_<br>
      Beginning: _12PM_<br>
      Duration: _2 days_<br>
      Repeat until: _No end date_
   3. Add a message:
      _Saturday and Sunday off!_<br>
   4. Notify your team:<br>
      _Timothy Saleck_<br>
- Click _Save_<br>  
![satsun](https://user-images.githubusercontent.com/39865915/41198637-3e542aa6-6c37-11e8-8d05-f83185c0620e.png)<br>
# Collecting APM Data
**Reference**: [https://docs.datadoghq.com/tracing/setup](url)<br>
## Enable APM
In the VM, update the Datadog Agent configuration file, at _/etc/datadog-agent/datadog.yaml_, to uncomment the following:
```
apm_config:
     enabled: true
```
Restart the Agent, with the command:
```
sudo service datadog-agent restart
```
## Install Virtual Environment-- then Flask, Blinker, and ddtrace
**Reference**: [http://flask.pocoo.org/docs/1.0/installation/](url)<br>
**Reference**: [https://docs.datadoghq.com/tracing/setup/python](url)<br>
Datadog's Tracing library, _ddtrace_, allows us to begin 

From the VM, execute the following commands:<br>
```
sudo apt-get install python-virtualenv
cd /vagrant
virtualenv venv
. venv/bin/activate
```
You should see a _(venv)_ preceding the command line interface in the VM, indicating the activated environment
```
cd venv
pip install flask
pip install blinker
pip install ddtrace
```
We then copy the provided flask app into a newly created _my_app.py_ file located in our virtual environment folder _/vagrant/venv_<br>

Execute the code with the following command:<br>
```
ddtrace-run python my_app.py
```
The code for our _my_app.py_ was used as provided, but is also shown below:<br>
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
While the web application is running, open an Internet browser window on the host machine and enter the following addresses:<br>
[http://ubuntu-xenial:5050/](url)<br>
![entry](https://user-images.githubusercontent.com/39865915/41271040-28514b52-6dc3-11e8-90a7-321a587f30f4.png)<br>
- [http://ubuntu-xenial:5050/api/apm](url)<br>
![apm](https://user-images.githubusercontent.com/39865915/41271053-38d87a7c-6dc3-11e8-8771-e06df6e1d59c.png)<br>
- [http://ubuntu-xenial:5050/api/trace](url)<br>
![trace](https://user-images.githubusercontent.com/39865915/41271071-492d942a-6dc3-11e8-8e2c-ea0f53a8f705.png)<br>
Navigate between the above addresses a few times each to create traces to each defined route (_/_, _/api/apm_, and _/api/trace_) defined in _my_app.py_.<br>

After a few moments you can check the Datadog application's _APM_ -> _Services_ menu, select _env:test_, and you will see the _flask_:
![flask](https://user-images.githubusercontent.com/39865915/41271186-f38d12a6-6dc3-11e8-8a48-6aa518e5fd1d.png)<br>
Click on the _flask_ to bring up the trace data.  Export each graph to the timeboard created earlier in this exercise by clicking on the _Share_ icon, _Export to Timeboard_, leaving the graph name default, and selecting _My Timeboard_:<br>
![exporttotime](https://user-images.githubusercontent.com/39865915/41271235-4283fe92-6dc4-11e8-802f-4ce27f1f0389.png)<br>
The updated _My_Timeboard_ is shown below:<br>
![uptimeboard](https://user-images.githubusercontent.com/39865915/41271352-ed6eee34-6dc4-11e8-9c6e-1873729edaf6.png)<br>
[https://app.datadoghq.com/dash/831616/my-timeboard?live=true&page=0&is_auto=false&from_ts=1528776840274&to_ts=1528780440274&tile_size=m](url)<br>

**Bonus**: What is the difference between a Service and a Resource?
**Reference**: [https://docs.datadoghq.com/tracing/visualization](url)<br>
A service is a set of processes that do the same job, while a resource is a particular action for a service.  In the case of our example, the _my_app.py_ web application is the service, while the resources would be the routes _/_, _/api/apm_, and _api/traces_<br>
# Final Question
Is there a creative way you would use Datadog for?<br>

Have you ever lived in, or been to, a big city, and always have trouble finding parking?  I think a good application of Datadog would be for monitoring metered parking lots/sturctures, or even down to specific metered parking spaces. This would require a "smart" meter system that could support the Datadog Agent (if one doesnt already exist).  I know there are relatively low cost options for this, such as Raspberry Pi (mentioned in the Datadog blogs).  If each meter had the Datadog Agent, or if each "pay for parking" kiosk, had the Datadog Agent, you could monitor all kinds of data that would be useful real-time, or even for predicting future availability.  You could use Datadog's monitoring capabilities to report everything about the meter, from simply "available" or "occupied", to even "how long is the spot paid for/when will it be available" types of things.  I was thinking if you could project the real-time monitoring to a smartphone (via app , or otherwise), one may have more success trying to find an available parking spot, or soon to be available parking spot.  While this may not be an application that shows off all of Datadog's capabilities, if implemented thoughtfully, I think it would be in high demand!
