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

We can change the collection interval without modifying the python check file we created by using the _min_collection_interval_ in the configuration file, _mycheck.yaml_, as referenced in the **Configuration** section from [https://docs.datadoghq.com/developers/agent_checks](url).  Be sure to restart the agent after any check file or configuration file updates!
# Visualizing Data
**Reference**: [https://docs.datadoghq.com/ja/api/#timeboards](url)

**Reference**: [https://docs.datadoghq.com/ja/api/#metrics](url)

**Reference**: [https://docs.datadoghq.com/monitors/monitor_types/anomaly](url)

**Reference**: [https://docs.datadoghq.com/graphing/miscellaneous/functions](url)

## Generate Application Key
To use the Datadog API, we need to have both our API key, as well as create an Application key.  We can both see our API key and create our App key from the Datadog UI -> Integrations -> APIs.  To create the App key, simply type in the _New application key_ field and click on the _Create Application Key_ button.
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

Following the Python _example request_ from the **Create a Timeboard** section, we can get a template for our Python script.  Our script will simply replace the existing example, as well as define more graphs, to accomplish the above three criteria.  Our _mytimeboard.py_ can be seen here:



# Monitoring Data
# Collecting APM Data
# Final Question
