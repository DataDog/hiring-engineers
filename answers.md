
## *Amrith's answers to the exercise*

*Please find below answers to the excercise*


# Setting up the environment

## Installing Vagrant and VirtualBox on a local machine

### Install Vagrant:


Download the proper package for your operating system and architecture from [Vagrant Download page](https://www.vagrantup.com/downloads). Additional instructions on installation if needed are available [here](https://www.vagrantup.com/docs/installation)


### Install VirtualBox:

VirtualBox is a free and open source virtualisation software. We will use VirtualBox to run Ubuntu 18.04 The latest version is available in the [VirtualBox Download page](https://www.virtualbox.org/wiki/Downloads)


## Configuring Vagrant and verifying the OS

The following command initialises Vagrant on your local machine and downloads the image of Ubuntu 18.04 also known as Bionic Beaver.
````
vagrant init hashicorp/bionic64
````


![Init vagrant](screenshots/1.1-init-vagrant.png)

### Launching the server

The following command would bring the server up. If this is the first time the command is run and if Vagrant cannot find the image it will attempt to find and install the OS on VirtualBox

````
vagrant up
````
![vagrant up](screenshots/1.2-bringing-vagrant-up.png)

### Connecting to the server

Once Vagrant has brought up the server you will need to connect to it by performing a Vagrant ssh. This simulates connecting to the server through Secure Socket Shell (SSH). The following command connects to the Ubuntu Bionic server that we just spun up:
````
vagrant ssh
````
![vagrant ssh](screenshots/1.3.vagrant-ssh-ubuntu.png)

### Verify the OS version by running the command
````
lsb_release -a
````
![verify-os](screenshots/1.4.verify-os-version.png)

### Change the hostname for better identification

The below screenshot confirms that the hostname has been changed.

![hostname](screenshots/1.5.change-hostname-vagrant.png)

### Create a new Datadog account.

* Use your browser and open https://www.datadoghq.com/ and create a new account
* After siging up, your new Datadog home page may appear like below:

![new-dd-account](screenshots/1.6.new.dd.account.png)

## Installing Datadog agent

### Agent Installation Instructions

Agent installations instructions are available in the following path:

Integrations ⇨ Agent ⇨ Ubuntu(choose based on the OS)  ⇨ Copy the instruction that matches the most suitable option. In our case, we will be performing a new installation.

The command would look similar to below.
Note: The API key will be associated to your account only and should not be shared.

````
DD_AGENT_MAJOR_VERSION=7 DD_API_KEY=███████████████████████████ DD_SITE="datadoghq.com" bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_script.sh)"
````

Copy and paste the command on the server and run it. You may have to enter your password if prompted.

### Verify the installation

The installation can be verified by checking the status of the Datadog service.

### Checking the status of the agent

````
sudo systemctl status datadog-agent
````
![datadog-agent-status](screenshots/1.7.datadog-agent-status.png)

Please note the following commands which will be used to stop, start or restart the agent.

The agents will need to be restarted whenever there is a change to the any configuration.

### Stopping the agent
````
sudo systemctl stop datadog-agent
````

### Starting the agent
````
sudo systemctl start datadog-agent
````

### Restarting the agent
````
sudo systemctl restart datadog-agent
````

## Confirming that the agent is reporting metrics:

Login to your Datadog account to verify that the agent is reporting metrics. This can be verified by any of the following options:

* Datadog event stream would indicate that the agent on the new host has been started. Datadog  ⇨ Events
![datadog-event](screenshots/1.8.datadoghq-event-stream.png)
* Datadog Infrastructure section would start reporting a new host. Datadog  ⇨ Infrastructure
![datadog-infra-host](screenshots/1.9.datadoghq-infra-host.png)
* Checking the home page as well where you would notice a new host has started to report
* Further, the default dashboard would start reporting metrics in graphs as well.

# Collecting Metrics

## Updating tags

Change the tags in the datadog_conf.yaml as per your requirement.

The datadog_conf.yaml is located in /etc/datadog for Ubuntu 18.04. The file location may vary depending on the platform. You can refer [this page](https://docs.datadoghq.com/agent/guide/agent-configuration-files/?tab=agentv6v7) for additional details
````
~
tags:
   - env:test
   - app:vagrant
   - owner:amrith
~
````


Verify that the tags are reporting in Datadog by navigating to
Infrastructure  ⇨ Host maps

![hostmap](screenshots/2.2.datadoghq-infra-hostmap-tags.png)

## Installing a Database

We will be installing MySQL as an example. Follow the below instructions to install MySQL on Ubuntu

Updating the OS
````
sudo apt update
````

Installing MySQL
````
sudo apt install mysql-server
````
![installing-mysql](screenshots/2.3.installing-mysql.png)

Enter the following commands and accept the defaults to configure the security settings of MySQL:
````
sudo mysql_secure_installation
````
![mysql-secure-installation](screenshots/2.4.mysql-secure-installation.png)

Verify that the installation is successful by entering the mysql command followed by performing a SELECT statement:
````
$ sudo mysql

mysql> SELECT user,authentication_strig,plugin,host FROM mysql.user;

````
If you see a table listed as shown in the screenshot below, you can be assured that the installation was successful.
![](screenshots/2.5.mysql-check-user.png)

### Create a datadog user and providing privilges to collect metrics

Enter the following command in mysql to create a new user named 'datadog' with a password
````
CREATE user 'datadog'@'localhost' IDENTIFIED BY '████████';
````

Verify that the user was created by running the previously run SELECT user command.
![verify-mysql-datadog-user](screenshots/2.6.mysql-verify-datadog-user.png)

The datadog agent needs a few privileges to collect metrics. Run the following commands to grant limited privileges only
````
mysql> GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'localhost' WITH MAX_USER_CONNECTIONS 5;
Query OK, 0 rows affected, 1 warning (0.01 sec)

mysql>
mysql>
mysql> GRANT PROCESS ON *.* TO 'datadog'@'localhost';
Query OK, 0 rows affected (0.00 sec)

mysql>
mysql>
mysql> ALTER USER 'datadog'@'localhost' WITH MAX_USER_CONNECTIONS 5;
Query OK, 0 rows affected (0.00 sec)

````
Verify that metrics can be collected from the performance_schema database and grant additional privilege by running the GRANT command

````
mysql>
mysql> show databases like 'performance_schema';
+-------------------------------+
| Database (performance_schema) |
+-------------------------------+
| performance_schema            |
+-------------------------------+
1 row in set (0.00 sec)

mysql>
mysql>


mysql> GRANT SELECT ON performance_schema.* TO 'datadog'@'localhost';
Query OK, 0 rows affected (0.02 sec)

````

### Configuration to collect MySQL metrics

Edit the mysql.d/conf.yaml file, in the conf.d/ folder at the root of your Agent’s configuration directory to start collecting your MySQL metrics and logs.

MySQL configuration for Datadog in our example is located in the following directory:
````
/etc/datadog-agent/conf.d/mysql.d
````
Modify the config file at these sections with the datadog username, password and other settings as shown below:
````
~
instances:
  - host: localhost
    user: datadog
    pass: ███████
    port: 3306
~
.
~

    options:
      replication: false
      galera_cluster: true
      extra_status_metrics: true
      extra_innodb_metrics: true
      extra_performance_metrics: true
      schema_size_metrics: false
      disable_innodb_metrics: false
````
Note: localhost may be replaced with 127.0.0.1 if needed. Also if you need to extract the database performance from a remote DB server

Additional details can be refered from the [MySQL Integration page](https://docs.datadoghq.com/integrations/mysql/?tab=host)

Save the conf.yaml in the mysql.d directory and restart the datadog agent.

### Verifying the integration check

Confirm that the mysql check is running correctly by running this specific agent subcommand:
````
sudo datadog-agent check mysql
````
Notice there are no warnings when you run this command:

![MySQL-agent-check](screenshots/2.8.datadog-agent-check-mysql-output.png)


### Verifying the metrics in Datadog
Navigate to Datadog  ⇨ Dashboards  ⇨ All Dashboards  ⇨ MySQL - Overview which is a preset dashboard for MySQL. Verify if you can see MySQL metrics as shown below:
![mysql-dashboard](screenshots/2.7.mysql-verify-metrics.png)

## Creating a Custom agent check

### Agent Check and config directory structure

The custom agent check would reside in a directory named ````checks.d```` while the corresponding configuration would reside in a directory in ````conf.d````

```
etc
|
└───
    datadog-agent
    |
    └───checks.d
    │   │   my_metric.py
    |
    └───conf.d
    │   │
    │   └───my_metric.d
    │       │   my_metric.yaml
    │   └───mysql.d
    │_______│   conf.yaml
```

Now that we understand where to place the files, lets create an agent check called ````my_metric.py```` in folder ````/etc/datadog-agent/checks.d/````

````my_metric.py:````

````
import random
    # first, try to import the base class from new versions of the Agent...
from datadog_checks.base import AgentCheck
    # content of the special variable __version__ will be shown in the Agent status page
__version__ = "1.0.0"

class MyCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric',random.randint(0,1000))
````

Lets update the configuration file which would go in conf.d/my_metric.yaml

````my_metric.yaml:````

````
init_config:

instances:
  - min_collection_interval: 45
````
Note: Leaving the configuration with no real information is acceptable but it would choose the default collection interval which is 15 seconds.

Restart the datadog-agent to use the latest configuration.

## Verify the agent check

Run the following command to verify if the agent is running normally:

````
sudo -u dd-agent -- datadog-agent check my_metric
````
or
````
sudo datadog-agent check my_metric
````

Notice that both the commands show the same output:

Output for ````sudo -u dd-agent -- datadog-agent check my_metric````

![dd-agent-check](screenshots/2.9.dd-agent-check-my_metric.png)

Output for ````sudo datadog-agent check my_metric````

![check-my_metric](screenshots/2.10.check-my_metric.png)

## View the Dashboard

You can also view the my_metric values in a Dashboard. Here is a sample below:
![my_metric Dashboard](screenshots/2.11.my_metric_graph.png)

### Bonus Question Can you change the collection interval without modifying the Python check file you created?

Yes. The collection interval can changed by changing the ````my_metric.yaml```` located in ````conf.d/my_metrid.d/```` folder

````
init_config:

instances:
  - min_collection_interval: 45
````
# Visualizing Data:

### Installing Postman

Datadog API can be used in variety of ways like writing a script or using commands like curl or wget.
In this example, Postman was used to create the dashboard.

After [downloading and installing postman](https://www.postman.com/downloads/), Import the Datadog collection into Postman by clicking the option to import [from this page](https://docs.datadoghq.com/getting_started/api/).

### Getting API and Application Keys

API and Applications keys are needed to authenticate against Datadog APIs. This can be obtained from the following locations in the Datadog UI:

API Key:

Integration ⇨ APIs  ⇨ API Keys
You can either create a new key or copy an existing key.

Application Key:

 Team ⇨ Application Keys  ⇨
 Click on ````New Key```` to create a new application key.

 ### Creating the Dashboard using the API

 Follow instructions in the [Using Postman with Datadog APIs](https://docs.datadoghq.com/getting_started/api/) article to add the keys into the Postman environment.

 Postman  ⇨ Collections  ⇨ Datadog API Collection  ⇨ Dashboards  ⇨  Create a new dashboard

 Update the POST URL to
 ````https://api.datadoghq.com/api/v1/dashboard````

 Update the Body to the following JSON document which includes the following

 * The custom metric (my_metric) scoped over the host.
 * MySQL CPU performance with the anomalies function applied
 * The custom metric (my_metric) applied to sum up all the points for the past hour into one bucket

````
{
    "title": "API-created-timeboard",
    "layout_type": "ordered",
    "notify_list": [],
    "widgets": [
        {
            "definition": {
                "type": "timeseries",
                "requests": [
                    {"q": "my_metric{host:vagrant-amrith}"}
                ],
                "title": "Custom my_metric on the Host",
                "title_align": "center"
            }
        },
        {
            "definition": {
                "type": "timeseries",
                "requests": [
                    {
                        "q": "anomalies(mysql.performance.cpu_time{host:vagrant-amrith}, 'basic', 3)"
                    }
                ],
                "title": "MySQL CPU Performance Anomalies",
                "title_align": "center"
            }
        },
        {
            "definition": {
                "type": "query_value",
                 "time": {
                    "live_span": "4h"
                },
                "requests": [
                    {
                        "q": "sum:my_metric{host:vagrant-amrith}.rollup(sum,3600)"
                    }
                ],
                "title": "Hourly roll-up for sum of my_metric over host ",
                "title_align": "center"


            }
        }
    ]
}
````

Ensure you receive a 200 OK to confirm that the POST was successfull.

### Access the Dashboard from the GUI:

![dashboard-created-by-api](screenshots/2.12.api-created-dashboard-in-ui.png)

### Setting the timeboards timeframe to the past 5 minutes

![dashboard-5-min](screenshots/2.12.api-created-dashboard-in-ui-5mins.png)

### Emailing the graph

Click the share icon, select the ````Send snapshot```` button and then enter the @ button and send it your intended recipient

![Sending-snapshot](screenshots/2.13.sending-snapshot.png)

Check the inbox if you have received the email:

![snapshot-email](screenshots/2.1.receiving-snapshot.png)

## Bonus Question: What is the Anomaly graph displaying?

In addition to the actual metric plotted over the graph, the anomaly graph has a gray band that shows the expected behaviour of the metric based on the historical data.

![anomaly-example](screenshots/2.14.anamoly.png)

Notice the above graph that shows the gray band which is the range the system expects the metric to stay within. The red spike is the anomaly detected based on historical data.

# Monitoring Data

Creating a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

* Warning threshold of 500
* Alerting threshold of 800
* And also ensure that it will notify you if there is No Data for this query over the past 10m.

### Creating the monitor:

To create a monitor, head to Datadog UI  ⇨ Monitors  ⇨ Manage Monitors  ⇨ Click on 'New Monitor'  ⇨ Select 'Metric' as the monitor type

* Select 'Threshold Alert' under 'Choose the detection method'
* Define the metric:
    * Select 'my_metric' from the drop down menu and leave the other options un changed. Those options can be confined to or restricted to certain resources.
* Select alert conditions
    * Set the Alert threshold to 800
    * Set the Warning threshold to 500
* Select the option to 'Notify' if the data is missing for '10' minutes.
* Enter text that shows the alert title and subject. An example is shown below:
* Finally, select the recipient of the email.


Screenshot of the screen to create a new monitor:
![create-monitor-metric](screenshots/3.1.create-monitor-metric.png)

### Configuring custom emails based on Alert, Warning or missing data:


### Title and Body of the notification


Notice the following aspects:
* Host IP is included in the body
* Custom messages has been incorporated depending on the alert condition: Alert, Warning or No Data


````
{{#is_alert}} My_Metric is {{value}} and above {{threshold}} on host {{host.ip}} {{/is_alert}} {{#is_warning}} My_Metric is {{value}} and above {{warn_threshold}} on host {{host.ip}} {{/is_warning}} {{#is_no_data}} My_Metric hasn't send any data for the past 10 mins {{host.ip}} {{/is_no_data}}

````

#### Body of the email.


````
{{#is_alert}}

Alert! My Metric is now {{value}} on host {{host.ip}} and thus has gone above defined {{threshold}} during the last 5 mins!

{{/is_alert}}

{{#is_warning}}

Warning! My metric is now {{value}} on host {{host.ip}} and thus has gone above defined {{threshold}} during the last 5 mins!

{{/is_warning}}

{{#is_no_data}}

No Data! My Metric has not sent any data yet. Are you sure the server is up and running?

{{/is_no_data}}

This message was sent by your friendly pup,

Datadog.

````

## Send you an email whenever the monitor triggers.

![notify-team](screenshots/3.2.monitor-notify-your-team.png)

### Verify you are receiving the notification in your email:
![email-alert](screenshots/3.4.monitor-email-sample.png)



Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

One that silences it from 7pm to 9am daily on M-F,
And one that silences it all day on Sat-Sun.
Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.


## Managing Downtime:

Navigate to Monitors  ⇨  Manage Downtime  ⇨ Schedule Downtime.

* Choose the monitor that you want to silence
* Select the schedule (recurring in this case)
* Add a message as required
* Add the email details to notify when the downtime begins.

Below is a screenshot of the downtime set for 7pm to 9am daily on M-F

![downtime-mon-fri](screenshots/3.5.downtime-mon-fri.png)

Below is a screenshot of the downtime set for the weekend:

![weekend-downtime](screenshots/3.6.weekend-downtime.png)
