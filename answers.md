# Solutions Engineer Exercise - Shuo Jin

## Setting up the Environment

This exercise was done using a virtual machine. A virtual machine is defined as "a software computer that, like a physical computer, runs an operating system and applications." For this exercise, I used an application called VirtualBox to set up my virtual machine. The download for VirtualBox can be found [here](https://www.virtualbox.org/wiki/Downloads). The operating system I used was Linux Mint, a flavor of Ubuntu 18.04. 

I created my machine with these settings:

![](img/1_0.PNG?raw=true)

Here was my virtual machine after installation of Linux Mint. 

![](img/1_1.PNG?raw=true)

After installation, I updated the repositories on my Linux machine so that all the current software was up to date. This was done by entering these commands into the terminal:

```
sudo apt update
sudo apt upgrade
```

Note that throughout this exercise, I will evoke "sudo" to obtain root privileges which are necessary for things to work. I followed the install instructions for Ubuntu on the DataDog installation page which resulting involved pasting this command into the terminal:

```
DD_API_KEY=API_KEY bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```

Here was a confirmation that the installation of the agent was successful.  

![](img/1_2.PNG?raw=true)

Further verification could be found on the DataDog welcome screen which now showed a hexagon with my host. 

![](img/1_3.PNG?raw=true)

## Collecting Metrics
### Addings tags

The agent config file is located in /etc/datadog-agent. I accessed this directory with the command:

```
cd /etc/datadog-agent/
```

Due to permission errors, the datadog.yaml file cannot be opened in a regular text editor. Instead, elevated privileges are required to open this file and that was done with this command:

```
sudo nano datadog.yaml
```

Nano was the text editor I used, although vim works as well. I added the tags at the bottom of the file past all of the comments. I saved the file with CTRL+X and restarted the agent with the command:

```
sudo service datadog-agent restart
```

This is what the datadog.yaml file looked like after adding two tags. 

![](img/2_1.PNG?raw=true)

After the agent restart, I navigated to the Host Map page (Infrastructure -> Host Map) to see if my tags were there and here was what that looked like. 

![](img/2_3.PNG?raw=true)

### Installing a database

The database I went with was MySQL using [this resource](https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-18-04) as a reference. MySQL is the database I am most familiar with and is very popular so it is easy to find documentation online for any problems that may occur. For an installation TLDR:

```
sudo apt install mysql-server
sudo mysql_secure_installation
```

I followed the onscreen prompts and then added a datadog user onto my MySQL server. I used these commands:

```
sudo mysql -e "CREATE USER 'datadog'@'localhost' IDENTIFIED BY 'DZIGDtX2FsbFMQU0oY,vCUAf';"
sudo mysql -e "GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'localhost' WITH MAX_USER_CONNECTIONS 5;"
```

The next step was creating a mysql.yaml file in the /etc/datadog-agent/conf.d folder. To speed things up, I skipped the cd command to access the directory and created the file with one line:

```
sudo nano /etc/datadog-agent/conf.d/mysql.yaml
```

The instructions for installing the DataDog MySQL integration involved copying these lines into the mysql.yaml. CTRL+X to save.

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

Checking the status of the agent with the command

```
sudo datadog-agent status
```

should show this after a successful integration. 

![](img/2_2.PNG?raw=true)

A similar verification can be found on the Integrations page (Integrations -> Integrations) along with some metrics that have been gathered. 

![](img/2_4.PNG?raw=true)

![](img/2_5.PNG?raw=true)

### Creating a custom agent check
Most of this section was done by referencing this [page](https://docs.datadoghq.com/developers/agent_checks/).

A custom agent check requires a Python .py file and a .yaml file. The .py file needs to be placed in the directory /etc/datadog-agent/checks.d and the .yaml file needs to be placed in the directory /etc/datadog-agent/conf.d. I created the Python file my_check.py with the command:

```
sudo nano /etc/datadog-agent/checks.d/my_check.py
```

Here was the code used to submit my_metric with the assistance of Python's random standard library.

![](img/2_6.PNG?raw=true)

I created the .yaml file with the command:

```
sudo nano /etc/datadog-agent/conf.d/my_check.yaml
```

It is imperative for both the .py and .yaml files to have the same name for the check to work. Here was my initial code for the .yaml file.

![](img/2_10.PNG?raw=true)

The problem here was that I did not specifiy a collection interval. Therefore, I removed the last line "[{}]" and added a line to specify a collection interval of 45 seconds. Every 45 seconds a new value for my_metric would be sent to DataDog. Here was how I did that along with the full .yaml file. 

![](img/2_7.PNG?raw=true)

I restarted the agent with:

```
sudo service datadog-agent restart
```

And ran the check with:

```
sudo -u dd-agent -- datadog-agent check my_check
```

![](img/2_8.PNG?raw=true)

I created a timeboard on the website to view the results of my check on a graph. This was done by accessing the Dashboards tab and then New Dashboard. Here's what that check looked like plotted on a graph. 

![](img/2_9.PNG?raw=true)

## Visualizing Data
### Preliminary actions
A timeboard is useful for displaying metrics in an easy to read way. I needed a timeboard that showed the values of my_metric, a metric of the MySQL integration with the anomaly function applied, and my_metric with the rollup function applied to sum up all the points for the past hour. Before writing any code, I had to obtain my API and APP keys. I did this on the DataDog website by navigating to the Integrations tab and then APIs. I had an API key but not an APP Key so I clicked Create Application Key. The next step was installing pip, a package manager for Python. Pip was necessary for installing the datadog Python library to allow my script to function. These were the commands used to accomplish that:

```
sudo apt install python-pip
pip install datadog
```

I got hit with a setuptools error when trying to install datadog so I used this command to resolve the issue before installing datadog again:

```
pip install --upgrade setuptools
```

### Putting it together

Through referencing the [API documentation](https://docs.datadoghq.com/api/?lang=python#create-a-timeboard), I created a script called create_timeboard.py that has been included in this repository. I replaced '<YOUR_API_KEY>' and '<YOUR_APP_KEY>' in lines 4 and 5 of the script with the corresponding API and APP keys obtained earlier respectively. 

I ran the timeboard with this command:
```
python create_timeboard.py
```

Here was my custom timeboard shown on the website. 

![](img/3_1.PNG?raw=true)

I clicked the first graph to get a set of points from the last five minutes. The time dropdowns in the menu bar did not include an option for the past five minutes but I was able to circumvent this by highlighting the last five minutes on the graph manually. Here was what that looked like. 

![](img/3_2.PNG?raw=true)

Using the @ notation in the comments box and tagging myself gave me this email shortly afterwards.

![](img/3_3.PNG?raw=true)

### Bonus
The anomaly graph uses an algorithm that compares the past behavior of a metric to its present behavior. For instance, if the database was growing in size by a constant rate, and that rate dropped off or fell unexpectedly, the anomaly monitor would alert. Any deviance from normality will be alerted by the anomaly function. 

## Monitoring Data
I created a monitor by navigating the sidebar like this: Monitors -> New Monitor. 

These were my options for setting up a monitor to notify if my_metric has exceeded 500 (warning), 800 (alert), or has no data for the past 10 minutes (no data). 

![](img/4_1.PNG?raw=true)

I used these lines to fill out the "Say what's happening" section. I wanted the message to be different depending on the type of alert and intuitive enough to tell me the host and ip on the problem. Note the @email at the bottom tells DataDog to send me an email when any of these alerts happen. 

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

Downtime was set up by navigating the sidebar to Monitors and then Manage Downtime. 
These were my options for setting up a monitor to mute alerts from 7 PM to 9 AM. I added a message at the bottom reminding me of the downtime schedule. 

![](img/4_3.PNG?raw=true)

Here was an email for the weekday downtime along with my message that I added. 

![](img/4_4.PNG?raw=true)

These were my options for setting up a monitor to mute alerts on weekends.

![](img/4_5.PNG?raw=true)

Here was an email for the weekend downtime. As before, make sure to add a message along with the corresponding emails to notify them. 

![](img/4_6.PNG?raw=true)

## Collecting APM Data

As per the documentation, the first step was enabling trace collection for the DataDog agent. This was done by accessing the same datadog.yaml file from the adding tags section with the addition of two lines at the bottom like this:

![](img/5_1.PNG?raw=true)

Next, I used pip to install flask and then ddtrace with these commands:

```
pip install flask
pip install ddtrace
```

Running the Flask app code from the technical exercise with the command

```
ddtrace-run python apm_collector.py
```

gave this result. 

![](img/5_2.PNG?raw=true)

As such, I was not able to view traces from the website. 

My next effort was to manually insert the Middleware as per instructions from [this resource](http://pypi.datadoghq.com/trace/docs/web_integrations.html#flask). I needed the blinker library which once again called upon pip with this command:

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

Unfortunately, this created more questions than answers as I was given a long list of errors. I saw that I got a socket error number 98 saying the address was already in use which I troubleshooted with the following command to see if another process was listening on the port that I chose. 

```
lsof -i :5050
```

No process was shown. I experimented with more ports and other host addresses but I got the same error still. Hosts that I tried: localhost, 0.0.0.0, 127.0.0.1. Ports that I tried: 8000, 8080, 5050, 8126 (apm listener port)

![](img/5_4.PNG?raw=true)

Another thing I tried was looking at active processes and killing any that used Python. 

```
ps -fA | grep python
sudo kill -9 pid
```

However, this did nothing as the socket error remained. At this moment, I ran out of options as I could not get past this error so that the following screen could display something other than "Once you’ve completed this step, return to this page. Your traces should be available shortly." With more time, I would have liked to try this in another language. 

![](img/5_5.PNG?raw=true)

To close this section out, a service consists of a collection of methods that together form a feature. An example of a service is a database for a web application. A resource is a data access mechanism for a service. These serve as a form of input and can be defined by a URL or a handler function. 
 
## Final Question

In many competitive online games, patches can shift the metagame allowing what was weak a chance to become strong. One such game is League of Legends where players control one "champion" out of a roster of over 100. Using DataDog to access the API from League of Legends, I can see spikes in winrates of champions after a patch to see where shifts of power are occuring. The anomaly function from earlier can be a great application for this! This way I can pick the champions that are strong before other players know that they are strong allowing me to stay ahead of the curve. 
