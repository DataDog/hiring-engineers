## Datadog Solution Engineer - Technical Exercise
The documented steps below are designed to provide an introduction to the Datadog monitoring service to a prospective solution engineer.   By executing on the below items an engineer can gain a basic understanding of how the Datadog monitoring service can collect, report and notify based on metrics.  Installation of agents on multiple platforms, configuring of collectors for multiple products, and configuring items within the Datadog web based console are all documented in the items listed in the table of contents below.
## Table of Contents
- [Setup an Ubuntu VM](#setup-an-ubuntu-vm)
  - [Installing Oracle VirtualBox on Windows](#installing-oracle-virtualbox-on-windows)
  - [Installing Vagrant on Windows](#installing-vagrant-on-windows)
  - [Configuring Vagrantfile](#configuring-vagrantfile)
  - [Starting the Ubuntu VM](#starting-the-ubuntu-vm)
- [Collecting Your Data](#collecting-your-data)
  - [Installing the Datadog Agent on Ubuntu](#installing-the-datadog-agent-on-ubuntu)
  - [Adding Tags to the agentconfig file](#adding-tags-to-the-agentconfig-file)
  - [Restart the Datadog Agent](#restart-the-datadog-agent)
  - [Group the Infrastructure by Tag](#group-the-infrastructure-by-tag)
  - [Installing PostgreSQL on Ubuntu](#installing-postgresql-on-ubuntu)
  - [Adding User Account in PostgreSQL for Datadog](#adding-user-account-in-postgres-for-datadog)
  - [Collect PostgreSQL Metrics in Datadog](#collect-postgresql-metrics-in-datadog)
  - [Install the PostgreSQL Integration into Datadog Console](#install-the-postgresql-integration-into-datadog)
  - [Verify PostgreSQL Metric Collection](#verify-postgresql-metric-collection)
  - [Configure the Agent to Sample Random Data](#configure-the-agent-to-sample-random-data)
 - [Visualizing Your Data](#visualizing-your-data)
  - [Adding the PostgreSQL and Random Metrics to a Dashboard](#adding-the-postgresql-and-random-metrics-to-a-dashboard)
  - [Snapshot and Notify Based on Threshold](#snapshot-and-notify-based-on-threshold)
 - [Alerting on Your Data](#alerting-on-your-data)
  - [Configure a Monitor Based on Threshold](#configure-a-monitor-based-on-threshold)
  - [Re-Configure the Monitor for Multi-Alert](#re-configure-the-monitor-for-multi-alert)  
  - [Configure Downtime for Monitor](#configure-downtime-for-monitor)
 - [Extended Use Cases](#extended-use-cases)
  - [Collecting Metrics from Docker](#collecting-metrics-from-docker)
    - [Installing the Datadog Agent on RHEL](#installing-the-datadog-agent-on-rhel)
    - [Collect Docker Metrics in Datadog](#collect-docker-metrics-in-datadog)
    - [Verify Docker Metric Collection](#verify-docker-metric-collection)
  - [Collecting Metrics from VMWare VSphere](#collecting-metrics-from-vmware-vsphere)
    - [Installing the Datadog Agent on Windows](#installing-the-datadog-agent-on-windows)
    - [Collect VSphere Metrics in Datadog](#collect-vsphere-metrics-in-datadog)
    - [Verify VSphere Metric Collection](#verify-vsphere-metric-collection)

## Setup an Ubuntu VM
### Installing Oracle VirtualBox on Windows
VirtualBox is a general-purpose full virtualizer for x86 hardware, targeted at server, desktop and embedded use. 

Version 5.1.26 for Windows can be downloaded [here](http://download.virtualbox.org/virtualbox/5.1.26/VirtualBox-5.1.26-117224-Win.exe)

Download, run the installer and referance the wiki [here](https://www.virtualbox.org/manual/ch02.html#installation_windows) for the specific installation directions for Windows

### Installing Vagrant on Windows
Vagrant is a tool for building and managing virtual machine environments in a single workflow. With an easy-to-use workflow and focus on automation, Vagrant lowers development environment setup time, increases production parity, and makes the "works on my machine" excuse a relic of the past.

The 64-bit download for Windows is available [here](https://releases.hashicorp.com/vagrant/1.9.7/vagrant_1.9.7_x86_64.msi)

The installation instruction for Vagrant is available from HashiCorp's wiki located [here](https://www.vagrantup.com/docs/installation/)

### Configuring Vagrantfile
There are several configuration steps neccessary to configure vagrant to startup an Ubuntu 12.5 virtual machine in VirtualBox.

  - Start a windows command prompt and change to the path you want the vagrant configuration to be stored
  - Execute vagrant with the initialization parameter from the command line: `vagrant init`
  - A configuration called `Vagrantfile` will be placed in the current directory, open it with a text editor
  - Update the parameter `config.vm.box = "base"` to be `config.vm.box = "hashicorp/precise64"`
  - Save and close the `Vagrantfile`
### Starting the Ubuntu VM
From the Windows command prompt issue the command: `vagrant start`

Output from the command should be something like below
![vm startup screenshot](screenshots\vm-startup.PNG)

## Collecting Your Data
`Bonus question: In your own words, what is the Agent?`
The agent is a piece of communication software that is installed on a host. The agent is responsible for securely reporting whatever metrics is required of it to the datadog platform. The agent allows for full customization in that it can grab information from a script (in the case of the random number exercise) or from a multitude of supported integrated products. In the example I used for this exercise, I setup postgresql on the server, a user for Datadog within the instance and the correct grants for access. Once the yaml for that specific monitor was activated with the correct configuration, a variety of different postgresql specific metrics were available in the datadog platform.

### Installing the Datadog Agent on Ubuntu
The following steps are required to install the agent on Ubuntu and send the basic metrics  to your Datadog account.

- From the windows command prompt in the directory where your vagrant file was located ssh to the Ubuntu: `vagrant ssh`
- Update repositories for apt-get by running: `sudo apt-get update`
- Install the binaries for curl from apt-get: `sudo apt-get install curl` 
- Open a browser and navigate to [https://www.datadoghq.com/](https://www.datadoghq.com/)
- Login to your Datadog account
- Click the Agent tab on the left under integrations as shown below
![agent tab screenshot](screenshots\agent-tab.PNG)
- Click the tab for Ubuntu
- Copy the installation command for the one-step install to the clipboard, it should look like:

```bash
`DD_API_KEY=e628d674717c2be4bb030c701a746656 bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/dd-agent/master/packaging/datadog-agent/source/install_agent.sh)"`
```

- In the command prompt window, paste the string and press enter
- The datadog agent will download from their website and install using apt-get a successful install will look like below
![ddagent install screenshot](screenshots\ddagent-install.PNG)

### Adding Tags to the agentconfig file
Tagging allows for grouping of infrastructure and application objects within the Datadog monitoring service.  They can be added to the agent configuration file or within the infrastructure host map on their site.  The steps for updating the agent configuration are below.

- Change to root access: `sudo su -`
- Change to the Datadog configuration directory: `cd /etc/dd-agent`
- Open the datadog.conf file in vi: `vi datadog.conf`
- find the tags parameter in the file uncomment it: `tags: mytag, env:prod, role:database`
- save and close the file

### Restart the Datadog Agent
After configuration changes to the Datadog agent, it needs to be restarted in order for the new configuration to take affect.

From the root shell prompt execute: `service datadog-agent restart`

Successful agent restart will have output like below.
![ddagent restart screenshot](screenshots\datadog-agent-restart.PNG)

### Group the Infrastructure by Tag
Now that the installed agent has a few tags associated with it, you can utilize those tags to group within the infrastructure host map view.

- Log into [https://www.datadoghq.com/](https://www.datadoghq.com/)
- Click on the Host Map tab under Infrastructure on the left menu bar
![hostmap tab](screenshots\host-map-tab.PNG)
- Click the group by tag drop down on the top/center of the panel
![hostmap tab](screenshots\group-by-tag.PNG)
- Select env or role - host map is now grouped by that tag
![hostmap tab](screenshots\group-by-env-tag.PNG)

### Installing PostgreSQL on Ubuntu
PostgreSQL, often simply Postgres, is an object-relational database management system (ORDBMS) with an emphasis on extensibility and standards compliance. As a database server, its primary functions are to store data securely and return that data in response to requests from other software applications.

To install PostgreSQL:

- Connect to the Ubuntu VM through ssh at the windows command prompt: `vagrant ssh`
- Change to root access: `sudo su -`
- Initiate the download and install through apt-get: `apt-get-install postgresql`
- A successful install will look like:
![postgresql install](screenshots\install-postgresql.PNG)

### Adding User Account in PostgreSQL for Datadog
In order for the Datadog agent to collect metrics on the default instance of postgreSQL it will need read only user access.

To setup the Datadog user:

- From the vagrant ssh session at a root prompt, switch to the postgres user: `su postgres`
- Add the user using pgsql: `psql -c "create user datadog with password 'k2a93rA4T7V8zTrpNvijeQHs'; grant SELECT ON pg_stat_database to datadog;"`

Run this query to allow collection of metrics by the Datadog user:
 `psql -h localhost -U datadog postgres -c "select * from pg_stat_database LIMIT(1);"  
 && echo -e "\e[0;32mPostgres connection - OK\e[0m" || \ ||  
echo -e "\e[0;31mCannot connect to Postgres\e[0m"`

When prompted for the password enter: `k2a93rA4T7V8zTrpNvijeQHs`

A successful query will output:
![query output](screenshots\query-output.PNG)

Exit psql with the `\q` command.

### Collect PostgreSQL Metrics in Datadog
The Datadog agent uses yaml based configuration files to determine what applications to collect metrics from.

Collecting metrics for PostgreSQL:

- From a root prompt on the VM change to the dd-agent user: `su - dd-agent`
- Change to bash shell: `bash`
- Change directory to the agent configuration directory: `cd /etc/dd-agent/conf.d`
- Copy the example yaml file so it will be active: `cp postgres.yaml.example postgres.yaml`
- Modify the postgres yaml with the datadog account info: `vi postgres.yaml` with below snippet
```yaml
init_config:

instances:
  - host: localhost
    port: 5432
    username: datadog
    password: k2a93rA4T7V8zTrpNvijeQHs
#    dbname: db_name
#    ssl: False
```
- Restart the Datadog agent from a root prompt: `service datadog-agent restart`
### Install the PostgreSQL Integration into Datadog Console
Once the agent is collecting the postgres metrics, we can now install the integration into the console so Datadog knows what to do with them.

- Log into [https://www.datadoghq.com/](https://www.datadoghq.com/)
- Click on the Integrations tab under Integrations on the left:        
![integrations tab](screenshots\integrations-tab.PNG)
- Scroll down to the PostgreSQL tile and click install

### Verify PostgreSQL Metric Collection
There are two areas to verify metric collection for an activated integration

To verify from the command prompt as root: `service datadog info`

Output should look like below under checks for posgres:
![postgres check info](screenshots\postgres-check-info.PNG)

To verify from the Datadog console:

- Log into [https://www.datadoghq.com/](https://www.datadoghq.com/)
- Click on the host map tab under infrastructure     
![hostmap tab](screenshots\host-map-tab.PNG)
- Click on postgres on the host which has the agent installed     
![postgres host](screenshots\postgres-host.PNG)
- Several metrics from postgres will be displayed in graphs
![postgres metrics](screenshots\postgres-metrics.PNG)

### Configure the Agent to Sample Random Data
The Datadog agent is extensible via script the below steps will collect a random number into Datadog from the agent using a python script.

- From a root prompt su to dd-agent user: `su dd-agent`
- Execute a bash shell: `bash`
- Open a yaml file with vi for the random data in the datadog configuration directory: `vi /etc/dd-agent/conf.d/random.yaml`
- Edit the file with the below snippet: 
```yaml
init_config:

instances:
	[{}]
```
- Open a python script for random with vi: `vi /etc/dd-agent/checks.d/random.py`
- Edit the file with the below snippet:
```python
import random
from checks import AgentCheck
class RandomCheck(AgentCheck):
	def check(self, instance):
		self.gauge('test.support.random', random.random())
```
- Exit to a root prompt and restart the agent: `service datadog-agent restart`
- Run info for the Datadog service and ensure that the check is being run: `service datadog-agent info` output should look like:
![random check info](screenshots\random-check-info.PNG)

## Visualizing Your Data
### Adding the PostgreSQL and Random Metrics to a Dashboard
### Snapshot and Notify Based on Threshold
## Alerting on Your Data
### Configure a Monitor Based on Threshold
### Re-Configure the Monitor for Multi-Alert
### Configure Downtime for Monitor
## Extended Use Cases
### Collecting Metrics from Docker
#### Installing the Datadog Agent on RHEL
#### Collect Docker Metrics in Datadog
#### Verify Docker Metric Collection
### Collecting Metrics from VMWare VSphere
#### Installing the Datadog Agent on Windows
#### Collect VSphere Metrics in Datadog
#### Verify VSphere Metric Collection

