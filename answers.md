# Solutions Engineer Exercise - Shuo Jin


## Setting up the Environment

This exercise was done using a flavor of Ubuntu 18.04 called Linux Mint. My computer already had VirtualBox installed so that was what I used to complete this exercise. The download for VirtualBox can be found [here](https://www.virtualbox.org/wiki/Downloads). 

![](img/1_1.PNG?raw=true)

I followed the install instructions for Ubuntu which resulting in pasting this command into the terminal:
```
DD_API_KEY=API_KEY bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```
Here was a confirmation that the installation was successful.  

![](img/1_2.PNG?raw=true)

Further verification could be found on the DataDog welcome screen which now showed a hexagon with my host. 

![](img/1_3.PNG?raw=true)

## Collecting Metrics
### Addings tags

The agent config file was accessed with the command:
```
sudo nano /etc/datadog-agent/datadog.yaml
```

I added two tags to the file. Make sure to scroll to the bottom past the comments to write the tags. 

![](img/2_1.PNG?raw=true)

Here are those same tags displayed on the website. 

![](img/2_3.PNG?raw=true)

### Installing a database

The database I went with was MySQL using [this resource](https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-18-04) as a reference. 

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

Checking the status with the command
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

Here was the code used to submit my_metric with the assistance of Python's random standard library. The check file was created and stored in /etc/datadog-agent/checks.d. 

![](img/2_6.PNG?raw=true)

For the .yaml file, this was what I used to change the collection interval so that I would not need to edit the Python file anymore. The .yaml file is located in /etc/datadog-agent/conf.d. Make sure the name of the .yaml is the same as the check.  

![](img/2_7.PNG?raw=true)

I restarted the agent with
```
sudo service datadog-agent restart
```

And ran the check with
```
sudo -u dd-agent -- datadog-agent check my_check
```

![](img/2_8.PNG?raw=true)

Here's what that check looked like plotted on a graph. 

![](img/2_9.PNG?raw=true)

## Visualizing Data

In trying to create my script, I had to install pip and then install the datadog Python library. These were the commands used to accomplish that:

```
sudo apt install python-pip
pip install datadog
```

I got a setuptools error during installation so I used this command after installing pip to resolve the issue:

```
pip install --upgrade setuptools
```

Through referencing the API documentation, I created a script called create_timeboard.py that has been included in this repository. Of course, I replaced '<YOUR_API_KEY>' and '<YOUR_APP_KEY>' in lines 4 and 5 of the script with the corresponding api and app keys respectively.

I ran the timeboard with this command:
```
python create_timeboard.py
```

Here's that same timeboard produced on the website. 

![](img/3_1.PNG?raw=true)

The time dropdowns in the menu bar did not include an option for the past five minutes but I was able to get this portion of the data by highlighting the last five minutes on the graph manually. 

![](img/3_2.PNG?raw=true)

Using the @ notation gave me an email that looked like this.

![](img/3_4.PNG?raw=true)

The anomaly graph uses an algorithm that compares the past behavior of a metric to its present behavior. For instance, if the database was growing in size by a constant rate, and that rate dropped off or fell unexpectedly, the anomaly monitor would alert.

## Monitoring Data
I created a monitor by navigating the sidebar like this: Monitors -> New Monitor. 

These were my options for setting up a monitor to notify if my_metric has exceeded 500 (warning), 800 (alert), or has no data for the past 10 minutes (no data). 

![](img/4_1.PNG?raw=true)

I used these lines to fill out the "Say what's happening" section.

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

Downtime can be set up by navigating the sidebar like this: Monitors -> Manage Downtime. 
These were my options for setting up a monitor to mute alerts from 7 PM to 9 AM. 

![](img/4_3.PNG?raw=true)

Here was an email for the weekday downtime. 

![](img/4_4.PNG?raw=true)

These were my options for setting up a monitor to mute alerts on weekends.

![](img/4_5.PNG?raw=true)

Here was an email for the weekend downtime. 

![](img/4_6.PNG?raw=true)

## Collecting APM Data

As per the documentation, the first step was enabling trace collection for the DataDog agent. This was done by accessing the same datadog.yaml file from the adding tags section with the addition of two lines at the bottom like this:

![](img/5_1.PNG?raw=true)

Next, I used pip to install ddtrace with this command:

```
pip install ddtrace
```

Running the Flask app code from the technical exercise with the command

```
ddtrace-run python apm_collector.py
```

gave this result. 

![](img/5_2.PNG?raw=true)

As such, I was not able to view traces from the website. 

My next effort was to manually insert the Middleware as per instructions from [this resource](http://pypi.datadoghq.com/trace/docs/web_integrations.html#flask). I needed the blinker library which was installed with pip using this command:

```
pip install blinker
```

I made an updated script called apm_collector.py, which has been added to this respository, and ran it with these commands:

```
export FLASK_APP = apm_collector.py
flask run
```

Here was the output I recieved. 

![](img/5_3.PNG?raw=true)

Unfortunately, this created more questions than answers as I was given a long list of errors. I saw that I got a socket error saying the address was already in use which I troubleshooted with the following command to see if another process was listening on the port that I chose. 

```
lsof -i :5050
```

No process was shown. 

![](img/5_4.PNG?raw=true)

At this moment, I tried researching other solutions to fix possible errors and could not work towards a resolution. 

To close this section out, a service consists of a collection of methods that together form a feature. An example of a service is a database for a web application. A resource is a data access mechanism for a service. These serve as a form of input and can be defined by a URL or a handler function. 
 
## Final Question

In many competitive online games, patches can shift the metagame allowing what was weak a chance to become strong. One such game is League of Legends where players control one "champion" out of a roster of over 100. Using DataDog to access the API from League of Legends, I can see spikes in winrates of champions after a patch to see where shifts of power are occuring. The anomaly function from earlier can be a great application for this! This way I can pick the champions that are strong before other players know that they are strong allowing me to stay ahead of the curve. 
