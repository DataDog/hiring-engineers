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
NOTE: This section is intended to assist with setting up an environment to run Datadog.  This section can be skipped if you already have an environment with the Datadog Agent installed.

The Datadog agent can be installed on a variety of operating systems.  For this demo, we will be utilizing a Linux VM, courtesy of Vagrant, and viewing it through VirtualBox.  We will install the Datadog Agent to the Linux VM that we deploy in this section.  To view details of this content, click: <details><summary>**Expand**</summary>
## Installing and Configuring VirtualBox
You can download VirtualBox here:

[https://www.virtualbox.org/wiki/Downloads](url)

For this demo, we will download the VirtualBox 5.2.12 platform package for OS X hosts
![virtualbox](https://user-images.githubusercontent.com/39865915/41008653-f89df63a-68e0-11e8-9e1c-475b2a53c7d9.png)
Execute the VirtualBox.pkg and take all defaults through the installation
![virtualbox2](https://user-images.githubusercontent.com/39865915/41008714-5562d502-68e1-11e8-933b-0582ade8bef0.png)
## Installing and Configuring Vagrant
The "getting started" guide for Vagrant can be found here:

[https://www.vagrantup.com/intro/getting-started/index.html](url)

You can download Vagrant here:

[https://www.vagrantup.com/downloads.html](url)

For this demo, we will download the Mac OS 64-bit package
![vagrant](https://user-images.githubusercontent.com/39865915/41007786-5ba3f946-68dc-11e8-9f4f-135d38ede7b9.png)
Execute vagrant.pkg and take all defaults through the installation
![vagrant2](https://user-images.githubusercontent.com/39865915/41007954-30768710-68dd-11e8-94f4-fc8888c58ee3.png)
Now that we have Vagrant installed, we can create a directory for our Vagrant project by opening a terminal window and entering the following commands:
- _mkdir vagrant_dd_demo_
- _cd vagrant_dd_demo_

For this demo, we will use the official Ubuntu 16.04 LTS, from Vagrant's cloud box catalog found here:

[https://app.vagrantup.com/boxes/search](url)

In the terminal, enter the command to add the VM box:
- _vagrant box add ubuntu/xenial64_

To create and initialize the Vagrant configuration file to use the box we just added, enter the following command in the terminal:
- _vagrant init ubuntu/xenial64_

![vagrant3](https://user-images.githubusercontent.com/39865915/41010123-96679d18-68ea-11e8-8f02-f5933a79b6cf.png)

Finally, to launch our Vagrant VM via virtual box, enter the following command into the terminal:
- _vagrant up --provider=virtualbox_

Launch VirtualBox and you will see the Vagrant VM running
![virtualbox3](https://user-images.githubusercontent.com/39865915/41123326-235a2ace-6a53-11e8-8609-1c1cc9a06a04.png)

Login to the VM with the following:
- User: _vagrant_
- Password: _vagrant_
![virtualbox4](https://user-images.githubusercontent.com/39865915/41125387-2c7e557a-6a59-11e8-8742-97363391faad.png)
## Installing the Datadog Agent
Go to the Datadog website ([https://www.datadoghq.com](url)), click on the "FREE TRIAL" icon, and enter your information to begin your trial:
![datadog](https://user-images.githubusercontent.com/39865915/41126910-f92fa9bc-6a5d-11e8-8f36-93fc2330958f.png)

Since we are installing the agent to our VM that we just setup/configured, we will select "Ubuntu" from the menu run the installation script command from our VM command line interface:
- `_DD_UPGRADE=true bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"_`

The result should look similar to the following:
![virtualbox5](https://user-images.githubusercontent.com/39865915/41126935-0aacfc9e-6a5e-11e8-921f-cdddf2e0b3c0.png)
Once the installed agent is detected by Datadog, click "Finish" and you will be taken to the Datadog Events page
![datadog2](https://user-images.githubusercontent.com/39865915/41130524-06a7af46-6a6c-11e8-84f6-010901d5d043.png)

</details>

# Collecting Metrics
## Tags
**Reference**: [https://docs.datadoghq.com/getting_started/tagging](url)

Agent Tags are, essentially, a feature that allows a user to establish custom "filters" associated with each host that has the Datadog agent installed.  Agent tags are configured in the _datadog.yaml_ file.  It is recommended that tags be implemented with a **key:value** syntax for optimal functionality. For this exercise, we will edit the _datadog.yaml_ file to include the following tags:
- _env:test_
- _role:database_
- _region:west_

![vagrant4](https://user-images.githubusercontent.com/39865915/41140007-009677d4-6aa0-11e8-9052-0aab3e15cccc.png)
After making changes to _datadog.yaml_, restart the Datadog agent with the command:
- _sudo service datadog-agent restart_

The added tags can then be seen and available for use on Datadog's Host Map page:
![datadog3](https://user-images.githubusercontent.com/39865915/41140505-c2afa7c6-6aa2-11e8-8ef9-06028214b8ad.png)
## Install MySQL
**Reference**: [https://support.rackspace.com/how-to/installing-mysql-server-on-ubuntu](url)

Install MySQL to the VM via the package manager by running the following commands:
- _sudo apt-get update_
- _sudo apt-get install mysql-server_

When prompted, set the _root_ user password to a password of your choosing.  For this demonstration, we used _datadog_ as the password.
You can start the MySQL shell by executing the following command:
- _/usr/bin/mysql -u root -p_

To exit the shell, execute the command:
- _exit_

## Install Datadog MySQL Integration
**Reference**: [https://docs.datadoghq.com/integrations/mysql](url)

From the VM, make a copy of the MySQL _conf.yaml.example_ file, named _conf.yaml_, by executing the following commands:
- _cd /etc/datadog-agent/conf.d/mysql.d_
- _sudo cp conf.yaml.example conf.yaml_

Follow the directions from the **Metric Collection** section (from [https://docs.datadoghq.com/integrations/mysql](url)) to configure the MySQL integration for metric collection by editing the newly created _conf.yaml_ file.  To edit the file, execute the following commands:
- _cd /etc/datadog-agent/conf.d/mysql.d_
- _sudo vi conf.yaml_

Make the following changes:
- _server: 127.0.0.1_
- _user: datadog_
- _pass: 'datadog'_
- _replication: 0_
- _galera_cluster: 1_
- Uncomment the _user_, _pass_, _port_, _options_, _replication_, _galera_cluster_, _extra_status_metrics_, _extra_innodb_metrics_, _extra_performance_metrics_, _schema_size_metrics_, and _disable_innodb_metrics_ entries

The resulting _conf.yaml_ file should look similar to the following:

![vagrant5](https://user-images.githubusercontent.com/39865915/41173102-9e640aac-6b0a-11e8-8fc0-7cf756bde876.png)

Save and exit the VI editor.

On the VM,prepare MySQL by creating a Datadog user (with password) and granting appropriate permissions by executing the following commands:
- _/usr/bin/mysql -u root -p_ (enter password when prompted)
- _CREATE USER 'datadog'@'127.0.0.1' IDENTIFIED BY 'datadog';_
- _GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'127.0.0.1' WITH MAX_USER_CONNECTIONS 5;_
- _GRANT PROCESS ON *.* TO 'datadog'@'127.0.0.1';_
- _exit_

Using the _Integrations_ section of the Datadog UI, install the _MySQL_ integration:
![datadog4](https://user-images.githubusercontent.com/39865915/41144549-20871bf4-6ab2-11e8-9d11-40490b3c1a70.png)
## Create a Custom Agent Check
**Reference**: [https://docs.datadoghq.com/developers/agent_checks](url)

Agent checks are intended to allow a user to collect Datadog metrics from custom applications or unique systems, while metric collection from more common applications, public services or open source projects, are intended to be implemented via Datadog's Integrations.  Agent checks have two parts, the check file, written in python, and the configuration file.  
Both the check file and configuration must share the same name (ex. _mycheck.py_ and _mycheck.yaml_, respectively).  The check file resides in the Agent's _checks.d_ directory, and the configuration file resides in the Agent's _conf.d_ directory.  Both the _checks.d_ and _conf.d_ directories exist under the Agent's root directory, in our case, _/etc/datadog-agent_.

To show how a custom Agent check is implemented, we can create a custom Agent check that submits a metric named _my_metric_ with a random value between 1 and 1000.  We will also configure _my_metric_ check to have a collection interval that only submits once every 45 seconds.

The _mycheck.py_ check file is as follows:
![mycheck_py](https://user-images.githubusercontent.com/39865915/41180516-5432e07a-6b23-11e8-8881-0c9912966df0.png)

The _mycheck.yaml_ configuration file is as follows:
![mycheck_yaml](https://user-images.githubusercontent.com/39865915/41182984-fc5f9eba-6b2c-11e8-8007-add3578a0be0.png)

After creating _mycheck.py_ and _mycheck.yaml_, restart the Datadog agent with the command:
- _sudo service datadog-agent restart_

**Bonus**: We can change the collection interval without modifying the python check file we created by using the _min_collection_interval_ in the configuration file, _mycheck.yaml_, as referenced in the **Configuration** section from [https://docs.datadoghq.com/developers/agent_checks](url).  Be sure to restart the agent after any check file or configuration file updates!
# Visualizing Data
**Reference**: [https://docs.datadoghq.com/ja/api/#timeboards](url)

**Reference**: [https://docs.datadoghq.com/ja/api/#metrics](url)

**Reference**: [https://docs.datadoghq.com/monitors/monitor_types/anomaly](url)

**Reference**: [https://docs.datadoghq.com/graphing/miscellaneous/functions](url)

## Generate Application Key
To use the Datadog API, we need to have both our API key, as well as create an Application key.  We can both see our API key and create our App key from the Datadog UI by navigating to **Integrations -> APIs**.  To create the App key, simply type in the _New application key_ field and click on the _Create Application Key_ button.
## Install _pip_ and Datadog Module for Python
Before we can utilize the Datadog API, we need to install the _pip_ package mangement system, for software packages written in Python, onto our VM.  The Datadog Python module allows us to to use the Datadog API within our Python scripts, which among other things, allows us to implement Datadog Timeboards.  To do this we run the following commands:
- _sudo apt-get update && sudo apt-get -y upgrade_
- _sudo apt-get install python-pip_
- _pip install datadog_
_ _pip install --upgrade pip_

## Creating a Timeboard
One way we can leverage the Datadog API, is by using it to create Timeboards.  For this demo, we will create a Timeboard that contains:
- Our custom metric scoped over our host
- Any metric from the Integration on our database with the anomoly function applied
- Our custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

Following the Python _example request_ from the **Create a Timeboard** section, we can get a template for our Python script.  Our script will simply replace the existing example, as well as define two more graphs, to accomplish the above three criteria.  Our _mytimeboard.py_ was created in the _/vagrant_ directory of our VM and can be seen here:


We can initialize our newly created Timeboard in Datadog by executing our Python script.  To do this, run the following commands:
- _cd /vagrant_
- _python mytimeboard.py_

Once the script executes successfully, we can view our newly created Timeboard in the Datadog UI by navigating to the **Dashboards -> Dashboard List** section and selecting _My Timeboard_ under **All Dashboards**:
![timeboard](https://user-images.githubusercontent.com/39865915/41197001-1a56314a-6c04-11e8-8fe9-43d119d01324.png)

From the Timeboard scren in the Datadog UI, we can zoom in a a range by simply click-holding on a point on any graph and dragging it to the time interval desired.

We can also take snapshots of a particular graph and send them to any Datadog user using the **_@_** notation.

For this demo, we changed the timeframe to the past five minutes, and sent a snapshot of the _my_metric Random Number Generator_ graph to myself, as shown below:
![snap](https://user-images.githubusercontent.com/39865915/41197085-8aa63420-6c06-11e8-99a7-cd4025fc85e5.png)

**Bonus**: In this demo, our anomaly graph is displaying when the average percentage of CPU time spent in kernel space by _MySQL_ on our VM goes above or below three standard deviations away from the established range.

# Monitoring Data
**References**: [https://docs.datadoghq.com/monitors/](url)<br>
Monitoring is a key component of Datadog's software.  Monitor's allow Datadog's users to continuously check metrics, integration availibilty, network endpoints, (and more), and be notified by a variety of methods when established conditions are met. 

In this demonstration, we will create a new Metric Monitor that watches the average of custom metric, _my_metric_, that we created at the beginning of this demonstration.  This Metric Monitor will alert if it is above the following values over the past 5 minutes:
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
- Under ***Select a monitor type***, select ***Metric***<br>
   1. Choose detection method: ***Threshold Alert***<br>
   2. Define the metric: Metric: ***my_metric*** (you can leave remaining fields default)<br>
   3. Set alert conditions: Trigger when the metric is ***above*** the threshold ***on average*** during the last *** minutes***<br>
      Alert threshold: ***800***<br>
      Warning threshold: ***500***<br>
      Alert recovery threshold: **(default)***<br>
      Warning recovery threshold: ***(default)***<br>
      ***Do not require*** a full window of data for evaluation<br>
      ***Notify*** if data is missing for more than ***10 minutesv<br>
      ***Never*** automically resolve this event from a no data state<br>
      Delay evaluation by ***0*** seconds<br>
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
      ***Timothy Saleck***<br>
      ***Do not notify*** alert recipients when alert is modified<br>
      ***Do not restrict*** editing of this monitor to its creator or administrators<br>
- Click ***Save***<br>      

When the monitor triggers, an email is sent to the user:
![rng](https://user-images.githubusercontent.com/39865915/41198618-f273dadc-6c36-11e8-803e-093be10ca150.png)

**Bonus**:  We can also configure our monitor to only alert during in-office hours, so we are not alerted when we are out of the office.  For this demonstration, we will set up downtimes for our monitor as follows:
- Monitor will be off/silent from 7PM-9AM Mon-Fri
- Monitor will be silent all day Sat-Sun

To make these updates to our monitor, do the following:
- ***Datadog UI*** -> ***Monitors*** -> ***Manage Downtime***<br>
- Select ***Schedule Downtime***<br>
   1. Choose what to silence: ***Monitor: Random Number Generator***, ***host: ubuntu-xenial***<br>
   2. Schedule:<br> 
      ***Recurring***<br>
      Start Date: ***2018/06/11***, Time Zone: ***(default)***<br>
      Repeat every: ***1 days***<br>
      Beginning: ***7PM***<br>
      Duration: ***14 hours***<br>
      Repeat until: ***No end date***
   3. Add a message:
      ***Monday-Friday, 7PM-9AM off!***<br>
   4. Notify your team:<br>
      ***Timothy Saleck***<br>
- Click ***Save***<br> 
![monfri](https://user-images.githubusercontent.com/39865915/41198634-2664223e-6c37-11e8-8dcc-fa7d69d53b9d.png)<br>

And repeat for the weekend off!<br>
- ***Datadog UI*** -> ***Monitors*** -> ***Manage Downtime***<br>
- Select _Schedule Downtime_<br>
   1. Choose what to silence: ***Monitor: Random Number Generator***, ***host: ubuntu-xenial***<br>
   2. Schedule:<br> 
      _Recurring_<br>
      Start Date: ***2018/06/15***, Time Zone: ***(default)***<br>
      Repeat every: ***7 days***<br>
      Beginning: ***12PM***<br>
      Duration: ***2 days***<br>
      Repeat until: ***No end date***
   3. Add a message:
      ***Saturday and Sunday off!***<br>
   4. Notify your team:<br>
      ***Timothy Saleck***<br>
- Click ***Save***<br>  
![satsun](https://user-images.githubusercontent.com/39865915/41198637-3e542aa6-6c37-11e8-8d05-f83185c0620e.png)
# Collecting APM Data
# Final Question
Is there a creative way you would use Datadog for?<br>

Ever been to a big city, and never able to find parking?  I think a good application of Datadog would be for monitoring metered parking lots/sturctures, or even down to specific metered parking spaces. This would require a "smart" meter system that could support the Datadog Agent (if one doesnt already exist).  I know there are relatively low cost options for this, such as Raspberry Pi (mentioned in the Datadog blogs).  If each meter had the Datadog Agent, or if each "pay for parking" kiosk, had the Datadog Agent, you could monitor all kinds of data that would be useful real-time, or even for predicting future availability.  You could use Datadog's monitoring capabilities to report everything about the meter, from simply "available" or "occupied", to even "how long is the spot paid for/when will it be available" types of things.  I was thinking if you could project the real-time monitoring to some sort of app for a smartphone, one may have more success trying to find an available parking spot, or soon to be available parking spot.  While this may not be an application that shows off all of Datadog's capabilities, if implemented thoughtlfully, I think it would practical to use regularly.
