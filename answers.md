# Solutions Engineer Exercise - Shuo Jin


## Setting up the Environment

This exercise was done using a flavor of Ubuntu 18.04 called Linux Mint. I went with VirtualBox instead of Vagrant because I am more familiar with this software. 

![](img/1_1.PNG?raw=true)

As I am on Ubuntu, I used this command to install the agent. 
```
DD_API_KEY=API_KEY bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```
This message shows that the installation was successful. 

![](img/1_2.PNG?raw=true)

This can be verified by visiting the DataDog welcome screen.

![](img/1_3.PNG?raw=true)

## Collecting Metrics
### Addings tags
The agent config file was accessed with the command:
```
sudo nano /etc/datadog-agent/datadog.yaml
```

I added two tags within this file. 

![](img/2_1.PNG?raw=true)

Here's those same tags displayed on the website. 

![](img/2_3.PNG?raw=true)

### Installing a database

The database I went with was MySQL using [this resource](https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-18-04) to assist me.

The next step was creating a mysql.yaml file in the /etc/datadog-agent/conf.d folder. Per instructions, here's what that file contained.
```
init_config:

instances:
  - server: localhost
    user: datadog
    pass: password
    tags:
        - optional_tag1
        - optional_tag2
    options:
        replication: 0
        galera_cluster: 1
```

Checking the status with the command:
```
sudo datadog-agent status
```
should show this after a successful integration. 

![](img/2_2.PNG?raw=true)

A similar verification can be found on the Integrations page along with some metrics that have been gathered. 

![](img/2_4.PNG?raw=true)

![](img/2_5.PNG?raw=true)

### Creating a custom agent check
Most of this section was done by referencing this [page](https://docs.datadoghq.com/developers/agent_checks/).

Here's the code used to submit my_metric with the assistance of the random standard library. The check file can be found in /etc/datadog-agent/checks.d. 

![](img/2_6.PNG?raw=true)

For the .yaml file, this was what I used to change the check's collection interval so that I would not need to edit the Python file anymore. The .yaml file can be found in /etc/datadog-agent/conf.d. Make sure the name of hte .yaml is the same as the check.  

![](img/2_7.PNG?raw=true)

Restart the agent with:
```
sudo service datadog-agent restart
```

Run the check with:
```
sudo -u dd-agent -- datadog-agent check my_check
```

![](img/2_8.PNG?raw=true)

Here's what the check looked like plotted on a graph. 

![](img/2_9.PNG?raw=true)

## Visualizing Data

In trying to create my script, I had to install the datadog Python library with pip on my VM. These were the commands to do that:
```
sudo apt install python-pip
pip install datadog
```

I got a setuptools error during this section so I used this command after installing pip:
```
pip install --upgrade setuptools
```

Through referencing the API documentation, I created a script called create_timeboard.py that has been included in this repository. Replace '<YOUR_API_KEY>' and '<YOUR_APP_KEY>' in lines 4 and 5 of the script with the corresponding api and app keys respectively.

Run with:
```
python create_timeboard.py
```

Here's that timeboard produced on the site.

![](img/3_1.PNG?raw=true)

The time dropdowns does not include an option for the past five minutes but it can still be done by highlighting the graph so that it only shows data from the last five minutes. 

![](img/3_2.PNG?raw=true)

Using the @ notation gave me an email that looked like this.

![](img/3_4.PNG?raw=true)

The anomaly graph uses an algorithm that compares the past behavior of a metric to its present behavior. For instance, if the database was growing in size by a constant rate, and that rate dropped off or fell unexpectedly, the anomaly monitor would alert.

## Monitoring Data
I created a monitor by navigating the sidebar like this: Monitors -> New Monitor. 

These were my options for setting up a monitor to notify if my_metric has exceeded 500 (warning), 800 (alert), or has no data for the past 10 minutes (no data). 

![](img/4_1.PNG?raw=true)

I used these lines for the "Say what's happening" section.

```
{{#is_warning}}
Warning: my_metric at {{value}} has registered over the warning threshold of {{warn_threshold}}  on IP {{host.ip}} for {{host.name}}!
{{/is_warning}}

{{#is_alert}}
Alert: my_metric at {{value}} has registered over the alert threshold of {{threshold}}  on IP {{host.ip}} for {{host.name}}!
{{/is_alert}}

{{#is_no_data}}
No Data: my_metric has not registered a value for the last 10 minutes on IP {{host.ip}} for {{host.name}}!
{{/is_no_data}} 

@email@provider.com
```

Here was an email alerting me that my_metric has exceeded the warning threshold. 

![](img/4_2.PNG?raw=true)

Downtime can be setup by navigating the sidebar like this: Monitors -> Manage Downtime. 
These were my options for setting up a monitor to mute alerts from 7 PM to 9 AM. 

![](img/4_3.PNG?raw=true)

Here was an email for that.

![](img/4_4.PNG?raw=true)

These were my options for setting up a monitor to mute alerts on weekends.

![](img/4_5.PNG?raw=true)

Here was an email for that. 

![](img/4_6.PNG?raw=true)

## Collecting APM Data

As per the documentation, the first step was enabling trace collection for the DataDog agent. This was done by accessing the datadog.yaml file from the adding tags section with the addition of two lines at the bottom like this.

Next, I used pip to install ddtrace and blinker as per instructions from [this resource](http://pypi.datadoghq.com/trace/docs/web_integrations.html#flask). 

```
pip install ddtrace
pip install blinker
```

A service consists of a collection of methods that together form a feature. An example of a service is a database for a web application. A resource is a data access mechanism for a service. These serve as a form of input and can be defined by a URL or a handler function. 
 
## Final Question

In many competitive online games, patches can shift the metagame allowing what was weak a chance to become strong. Using DataDog to access the APIs of many of these games, I can generate data on shifts in power so that I can stay ahead of the curve. 
