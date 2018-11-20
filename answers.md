# Setting up the Environment
## Step 1
Download Vagrant [here](www.vagrantup.com/downloads.html). Make sure to choose the correct operating system

When it's been downloaded and installed, verify the installation by going into the terminal and typing **vagrant** as per Vagrant's [documentation](https://www.vagrantup.com/intro/getting-started/install.html).

If you don't already have [VirtualBox](www.virtualbox.org/wiki/Downloads) downloaded and installed, please do that now. Also be sure to download and install the correct one for your computer.

## Step 2

Let's create a directory, or folder, where we want to keep our virtual machine and it's related files. In the terminal, once you've navigated to the right location you want the folder in create the new folder with **mkdir test-vm**.

Let's move inside the newly created folder and start creating this virtual machine--**cd test-vm**.

We have to first initialize the virtual machine with this command: **vagrant init**--this creates a Vagrantfile, which is the equivalent of a Dockerfile if you're more familiar with Docker, where you can define the environment and setup for this virtual machine we want to create.

Before we start editing the Vagrantfile, let's get an image, or a box as they call it with Vagrant for our virtual machine. You can find various public boxes shared on the internet for your convenience [here](https://app.vagrantup.com/boxes/search). The Vagrant tutorial/documentation uses a different box, but we will be using the [Ubuntu/Xenail box](https://app.vagrantup.com/ubuntu/boxes/xenial64). You can do this with **vagrant box add ubuntu/xenial64**. This command will download the "box" for you to use for any virtual machine you create going forward.

## Step 3

Once the box has finished downloading--or if you want to do this while it is downloading--let's configure the Vagrantfile to include this ubuntu or linux box for this virtual machine. You can do this with any text editor--for example if you like Atom you can open it in the terminal with **atom Vagrantfile**, and the same with VSCode but with **code Vagrantfile** instead.

Add the following inside:

```shell
Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/xenial64"
end
```

And that's all we need to configure our virtual machine environment to get it up and running!

Let's start this virtual machine with **vagrant up**! It will run in the background and you'll still be able to use the terminal without opening a new one or a new tab.

To interact with this virtual machine, use the command **vagrant ssh** which will use a secure protocol. And if you want to exit from interacting with the VM, just press CTRL + D.

## Step 4

Create a [Datadog account](https://app.datadoghq.com/signup) if you already haven't as you'll need it next!

Follow the instructions Datadog gives you after registering an account and ensure you're running the scripts provided in the **vagrant ssh** environment. You can tell if you're already inside said environment if you see *vagrant@ubuntu-xenial:* on the left-hand side of the terminal by the blinking cursor.

![alt text][vagrant-ssh]

There are a couple of different pages referring to agent commands but I found [this one](https://docs.datadoghq.com/agent/basic_agent_usage/ubuntu/?tab=agentv6) to be accurate and work for me.

Go ahead and use the start command **sudo service datadog-agent start** to start the Datadog agent--it will run in the background. 

# Collecting Metrics

Let's add a tag to our host representing our VM. In order to do so let's navigate to the agent config file at */etc/datadog-agent*--you can do so with command **cd /etc/datadog-agent**. This will only work if you were in the root folder to start with--to go back to the root place **cd ~**.

Let's edit the *datadog.yaml* file to add the tags with **sudo vim datadog.yaml**. Scroll down to where they have *tags* in the file, should be starting on line 49--you can identify which line/row you're on by looking at the bottom-right hand side, the first number represents the row/line. 

Press *i* to allow yourself to edit and make changes to this file.

![alt text][host-tags]

Delete the *#* which comments out the line so it isn't run or interpreted by the computer. Then edit the sample tag to whatever you want to call it. They provide good examples of what you may want to name it among all your VMs and applications. This will allow you to keep track of everything without confusion--you could essentially have 10-100 of these VMs with the same environment, so referring to this VM as Ubuntu/Xenial will simply not do.

Save the file when you're done by first pressing "Esc", and then by pressing **:wq** and then *Enter* to save and close out of the file.

Restart the agent with **sudo service datadog-agent restart**.

You'll be able to see it on Datadog's platform once it updates:
![alt text][host-map]

## Step 1

Now we will install a MySQL database in the virtual machine and connect it with Datadog's agent to collect metrics. 

Download and install MySQL into the VM with **sudo apt-get install mysql-server** and when it ask for a password just press *Enter*--you can always go back and update it.

Once that has been completed, you can enter the MySQL environment where you can communicate with its server and setup databases and whatnot with **sudo mysql**. You can exit by simply typing **exit**, and you'll know if you're in this environment by looking at the left-hand side--it should say *mysql>*.

![alt text][mysql]

## Step 2

![alt text][integrations]

Go to your account on the Datadog platform at www.datadoghq.com and click on *Integrations*. 

![alt text][mysql-integration]

Find MySQL, or search for it in the above search bar and follow the instructions for *step 1* on how to integrate or configure MySQL in the VM to talk with the Datadog Agent so that you can collect certain metrics to be displayed in interactive and informative graphs. *Note that the scripts provided already take into consideration the mysql environment and so you shouldn't be in the mysql environment.*

![alt text][mysql-config]

For the second step where you are configuring the mysql.yaml file, if you're lost as to where you are in the folder structure, go back to the root with **cd ~** and then navigate to the proper location with **cd /etc/datadog-agent/conf.d/mysql.d/**. Once there, you will have to create a new file--**sudo touch mysql.yaml**. Open up this file in your text editor--I used Vim instead, so I opened it up with **sudo vim mysql.yaml**. Then you can copy and paste the script they gave you in there.

In addition, you can also add the following for extra metrics at the end:

```yaml
extra_status_metrics: true
extra_innodb_metrics: true
extra_performance_metrics: true
schema_size_metrics: false
```

I copied the example provided and edited, but it looks as follows:
![alt text][mysql-yaml]

Restart the agent with **sudo service datadog-agent restart**. Then check to see how it is with **sudo service datadog-agent check mysql**.

## Step 3

In this step we will see how we can create custom checks that can submit metrics through the agent to your dashboard view. 

You should currently be in */etc/datadog-agent/checks.d*, so just **cd checks.d** to get to the right directory. Here we will create a Python file to code out our custom check--**sudo touch my_metric.py** will do just that. 

Let's hop inside this new Python file with **sudo vim my_metric.py**. Copy and paste the following inside:

```python
try: 
  from checks import AgentCheck
except ImportError:
  from datadog_checls.checks import AgentCheck

__version = "1.0.0"

import random

class MyMetricCheck(AgentCheck):
  def check(self, instance):
   self.gauge('my_metric', random.randint(0, 1000))
```

It would look as follows:
![alt text][check-config]

When you're finished pasting that in, press **:wq** to save and close out of the file.

This will send a random number from 0 - 1000 with the check every time.

By default this check is done in intervals of 30 seconds according to the [docs here](https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6). If we want to adjust it, then we can!

Let's move from this *checks.d* directory back to the *conf.d* directory with **cd ../conf.d**. 

Here let's follow the more recent file structure and create a folder that will match our newly created custom check with **mkdir my_metric.d**. 

Navigate to it--**cd my_metric.d**. And then create a *yaml* file for this custom check with **sudo touch my_metric.yaml**.

Open it up with Vim **sudo vim my_metric.yaml** and copy and paste the following inside:

```yaml
init config:

instances:
  - min_collection_interval: 45
```

*remmber you have to press **i** in order to edit inside Vim.*

It's as simple at that:
![alt text][metric-interval]

Then save and close by once again pressing *Esc*, *:wq*, and then *Enter*. That's how you can create custom agent checks! 

### Bonus
But let's say you don't want intervals of 45 seconds always, and instead you want to delay a check--you can do so without having to edit the file. Just add **-d** and a number when you run a check (sudo datadog-agent check mysql -d 10).

# Visualizing Data

Let's create a timeboard and some graphs for some metrics using Datadog's API instead of doing it online with their Graphical User Interface (GUI). 

## Step 1

Create a file somewhere inside the vagrant ssh environment--I chose to do it in */etc/datadog-agent*. I did so with the following command: **sudo touch test-timeboard.sh**. Let's jump inside and edit it to do just what we want then--**sudo vim test-timeboard.sh**. *Feel free to name it what you like, but be sure to keep the extension as "sh"*.

Remember you need to press *i* to edit inside Vim.

Start off by typing the following:

```shell
api_key=
app_key=
```

You're declaring two variables to be used later on. Go to the Datadog GUI in the browser and go to *Integrations* which depending your view could be at the top or left-hand side. Then click on the *APIs* tab at the top (it may be in a different location based on your screen size and resolution).

![alt text][keys]

Copy and paste the respective keys into the file--you may have to create a key and you can do so by clicking the buttons there on the webpage. 

Continue on and copy and paste the following inside the same file:

```shell
curl -X POST -H "Content-type: application/json" -d '{
  "graphs":[{
    "title": "My Metric Graph",
    "definition": {
      "events": [],
      "requests": [
        {"q": "sum:my_metric{host:ubuntu-xenial}.rollup(sum, 60)"}
      ],
      "viz": "timeseries"
    }
  }],
  "title": "Test Timeboard",
  "description": "A dashboard showing my_metric totals for each hour",
  "template_variables": [{
    "name": "host1",
    "prefix": "host",
    "default": "host:ubuntu-xenial"
  }],
  "read-only": "True"
}' "https://api.datadoghq.com/api/v1/dash?api_key=${api_key}&application_key=${app_key}"
```

Remember to save and close out of the file inside Vim is to press *Esc*, *:wq* and then *Enter*.

Now to run this script we can simply enter **./test-timeboard.sh**. 

If you run into a permissions error, do this **chmod +x /test-timeboard.sh**. And then try running the script above again.

## Step 2

We want to be able to detect anomalies right? We would like our systems and apps to be monitored and notify or alert us in case something is a bit unusual so we can come in, analyze and resolve the issue if there is one. Let's see how we can do this.

![alt text][monitors]

On the Datadog GUI in the browser, go to the Monitor section and click on a New Monitor for a metric.
1. Choose the detection method--Anomaly Detection
2. Define the metric--metric: *mysql.performance.qcache_free_memory*, from *mysqldb_test* (this is the tag you created when configuring MySQL)
3. Set alert conditions--Change the info as you see fit
4. Say what's happenening--A concise message about the error
5. Notify your team--include everyone who should be alerted

*make sure to give this monitor or anomaly detection monitor a name, otherwise you won't be able to save it

Click save and you have a new monitor! 

How can we create a graph for this metric which we created a monitor for just like we did with the other metric in Step 1? In the first section, we'll basically copy and paste it and edit it for the new metric is all. 

Navigate to where you saved the shell script, test-timeboard.sh, I saved mine at */etc/datadog-agent*. Let's open it up in Vim to edit, and be sure to open it up with **sudo** so you may edit the file.

After you edit it, it should more or less look like the following:

```shell
api_key=asdfJAHFn7492ASfkn4552
app_key=ASdj8fi4921knfnasdf45231

curl -X POST -H "Content-type: application/json" -d '{
  "graphs":[
    {
      "title": "My Metric Graph",
      "definition": {
        "events": [],
        "requests": [
          {"q": "sum:my_metric{host:ubuntu-xenial}.rollup(sum, 60)"}
        ],
        "viz": "timeseries"
      }
    },
    {
      "title": "Anomaly Graph",
      "definition": {
        "events": [],
        "requests": [
          {"q": "avg:mysql.performance.qcache_free_memory{*}"}
        ],
        "viz": "timeseries"
      }
    },
  ],
  "title": "Test Timeboard",
  "description": "A dashboard showing my_metric totals for each hour",
  "template_variables": [{
    "name": "host1",
    "prefix": "host",
    "default": "host:ubuntu-xenial"
  }],
  "read-only": "True"
}' "https://api.datadoghq.com/api/v1/dash?api_key=${api_key}&application_key=${app_key}"
```

![alt text][timeboard]

You already have this timeboard created, so go ahead and delete it in the browser and then run this script again and you'll find you have a timeboard with 2 graphs now.

### Bonus
The Anomaly graph shows us over time the average amount of free memory there is in the cache for our database on our virtual machine.

# Monitoring Data

## Step 1
We have an anomaly detection monitor, but what other monitors can we have? Let's setup one for our my_metric metric and alert us if it sees its metrics going above or below a certain threshold. Go back to where we create a monitor and create a new one for our my_metric.

## Step 2
Let's do a warning threshold of 500 (it's in yellow). And an alerting threshold of 800 (in red). We can keep the rest of the default settings as is, but let's be notified if there's been no data for more than 10 minutes (3rd step, 3rd from the 4th step).

![alt text][monitor1]

## Step 3
Just like we did with the previous monitor, edit the message to fit this monitor and you can include the metric name and the metric values with 2 pairs of curly braces {{}}. *You can search for what you can use when you start with the opening curly brace {*.

![alt text][monitor2]

### Bonus
These monitors will constantly be running and warning and alerting all the time. If we don't want to be notified during certain hours or time frames, we can schedule downtimes specifically to avoid this scenario and live life with more peace.

You can do so by going to Monitor and then to Manage Downtime, or go towards the top and you'll see the tab for it since we're already on the Monitor page.

Click on *Schedule Downtime*. Find a metric you'd like to avoid hearing about during the evenings on weekdays. Select it and choose the start date to continue on forever. Let's say the evenings start at 7PM and it will go on till the following morning at 9am. Do this daily and that will work for us! 

![alt text][downtime2]

Let's also schedule another downtime for the weekends. You can do this by selecting to repeat every 1 week and check off Saturday and Sunday. And if you select a duration of 1 day, that should do the trick!

![alt text][downtime1]

# Collecting APM Data

APM stands for Application Performance Management and it is just so, this allows you to track the performance or key metrics of your applications. Thereby allowing you to have a single souce to check all your systems and applications to debug, fix or pinpoint areas needing improvemnt.

![alt text][apm]

Go to the APM section on Datadog's platform in the browser. If you already have one setup, go to the docs section inside APM. Otherwise it will bring you to the docs page automatically as you need instructions to get started.

![alt text][apm-docs]

We'll be using Python but they have other docs available for other languages too.

## Step 1
But before we do anything with Python, we have to ensure our datadog agent is configured properly! 

You can do so by opening up the *datadog.yaml* file in */etc/datadog-agent* and editing it with Vim. Towards the bottom you will see at the very bottom of the file a section called *Trace Agent Specific Settings*. Underneath it you'll see the following commented out. 

```yaml
apm_config:
  enabled: true
```

Mine looks like this:
![alt text][apm-config]

Uncomment these two lines out by deleting the *#*'s. Then save and close out of the file.

Restart the datadog agent, and now you're ready to move forward because the agent is setup to collect APM data!

## Step 2
Here let's ensure we have everything prepared by checking our environment and respective and necessary packages and installations.

If you go to the terminal (inside the vagrant virtual machine) and check if you have pip installed with **pip --version**. If you get a version response back then you already have pip installed otherwise you can install it with **sudo apt-get install pip**.

Once you have pip installed then you can install ddtrace with the command they give you **pip install ddtrace**. You will need Flask for this, so let's install that now too with **sudo apt-get install flask**. And while we're at it, check your python version with **python --version**. If it's 2.7 or higher then I think you'll be fine, otherwise **sudo apt-get install python3**.

## Step 3
Create a python file with **sudo touch app.py**. I created it inside the */etc/datadog-agent* folder. Then let's edit it with Vim and copy and paste the following inside it:

```python
from flask import Flask
import logging
import sys

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

Should look like this:
![alt text][python-app]

Save and close out of the file.

Now you can test the tracing with the agent and this file with **ddtrace-run python app.py**. 

If you get the following error, don't panic:

```shell
ERROR:ddtrace.writer:failed_to_send services to Agent: HTTP error status 400, reason Bad Request, message Content-Type: text/plain; charset=utf-8...
```

Let's just go ahead and manually test it ourselves and we'll see that it is working! *Don't cancel the python application--keep it running*.

Open up another terminal, or a new tab. If you're on a Mac then go to the top bar and click on Shell-->New Tab. 

This new tab is another terminal but you won't automatically be inside the virtual machine. Go to the folder where you have the vagrant VM and get inside it with **vagrant ssh**.

Now let's send some requests to our python application to test if the agent is truly tracing it or not. Type **curl localhost:5050/api/trace** and then press *Enter*. Move to the other terminal with the python server running and see if you get a message. 

It might look something like this:

```shell
INFO:wekzeug:127.0.0.1 - - [20/Nov/2018 00:18:24] "GET /api/trace HTTP/1.1" 200...
```

If you see this message with the status of 200 then you're in good shape. Let's send a few more requests in the other terminal to get more info to work with. Also sent it to endpoint */api/apm* too--**curl localhost:5050/api/apm** in other words.

It might take a few minutes to update on the Datadog platform in the browser so don't be surprised if you go back to the APM section and still see the docs!

You may also configure the python file slightly differently to avoid having to use *ddtrace-run*. If you'd rather do this, copy and paste the following inside the python file towards the top:

```python
from ddtrace import patch_all
patch_all()
```

Then when you run the python file, you can just use **python app.py** instead. You may run into issues if you try using both, so try to use only one method. 

### Bonus
If the application has routes/URLs or endpoints then those would be its resources--like /users and /products. But if it is a database, then a resource would refer to the queries themselves, like SELECT * from Users.

Whereas a service is defined by the user/admin or person in charge of setting it up. It's a collection of processes that work together for a single purpose. For a single application, you can have many parts that work together and you may want to track them separately. It makes sense to separate your database from the application. And perhaps if you have a backend application that works as an API included, you can separate that as its own service as well.

# Final Question

I think the hospitality industry could easily benefit from Datadog's product. Whether it comes to reservations, inventory, seating availability, ticket availability or managing all the applications, services, and infrastructure to keep it running efficiently and effectively.


[vagrant-ssh]: ./snapshots/vagrant-ssh-snapshot.png "how to know you're in a SSH environment in a Vagrant VM"
[python-app]: ./snapshots/apm-python-app-snapshot.png "view of basic python app to get APM working with Datadog"
[timeboard]: ./snapshots/create-timeboard-scripts-snapshot.png "view of syntax of writing a post curl request to create a timeboard with Datadog's API"
[check-config]: ./snapshots/custom-check-config-snapshot.png "custom datadog agent check sending a random number from 0 - 1000"
[metric-interval]: ./snapshots/custom-metric-config-snapshot.png "config setup for custom metric changing default collection interval from 30 to 45 seconds"
[downtime1]: ./snapshots/custom-metric-monitor-downtime-snapshot.png "steps 1-2 preview on how I created my monitor downtime for the weekends"
[downtime2]: ./snapshots/custom-metric-monitor-downtime-snapshot2.png "steps 1-2 preview on how I created my monitor downtime for weeknights"
[monitor1]: ./snapshots/custom-metric-monitor-snapshot.png "metric monitor for thresholds to alert team in cases of potential threats or concerns"
[monitor2]: ./snapshots/custom-metric-monitor-snapshot2.png "metric monitor syntax for including data in alerting email to team members"
[apm-config]: ./snapshots/dd-agent-apm-config-snapshot.png "datadog.yaml datadog agent config file change to account for APM"
[host-tags]: ./snapshots/dd-agent-tags-snapshot.png "virtual machine datadog agent config file host's tags"
[keys]: ./snapshots/dd-api-keys-snapshot.png "datadog platform location for getting personal key information for the API and applications"
[apm-docs]: ./snapshots/dd-apm-docs-snapshot.png "datadog apm python instructions to install agent package and connect the application with the agent configs"
[apm]: ./snapshots/dd-apm-snapshot.png "datadog platform apm location"
[mysql-integration]: ./snapshots/dd-integrations-mysql-snapshot.png "datadog platform integrations area for mysql"
[integrations]: ./snapshots/dd-integrations-snapshot.png "datadog platform integration icon on navbar"
[monitors]: ./snapshots/dd-monitors-snapshot.png "datadog platform monitors icon on navbar"
[mysql-config]: ./snapshots/dd-mysql-integration-config-snapshot.png "mysql integration configuration to allow datadog to gain access and collect metrics"
[host-map]: ./snapshots/host-map-tags-snapshot.png "datadog platform view of hosts and specific host's tags"
[mysql-yaml]: ./snapshots/mysql-integration-config-snapshot.png "yaml file for mysql configuration to connect to datadog's agent"
[mysql]: ./snapshots/mysql-snapshot.png "how the terminal will look when you type sudo mysql and you enter into a shell to communicate with its server"
