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

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/xenial64"
end

And that's all we need to configure our virtual machine environment to get it up and running!

Let's start this virtual machine with **vagrant up**! It will run in the background and you'll still be able to use the terminal without opening a new one or a new tab.

To interact with this virtual machine, use the command **vagrant ssh** which will use a secure protocol. And if you want to exit from interacting with the VM, just press CTRL + D.

## Step 4

Create a [Datadog account](https://app.datadoghq.com/signup) if you already haven't as you'll need it next!

Follow the instructions Datadog gives you after registering an account and ensure you're running the scripts provided in the **vagrant ssh** environment. You can tell if you're already inside said environment if you see *vagrant@ubuntu-xenial:* on the left-hand side of the terminal by the blinking cursor.

There are a couple of different pages referring to agent commands but I found [this one](https://docs.datadoghq.com/agent/basic_agent_usage/ubuntu/?tab=agentv6) to be accurate and work for me.

Go ahead and use the start command **sudo service datadog-agent start** to start the Datadog agent--it will run in the background. 

# Collecting Metrics

Let's add a tag to our host representing our VM. In order to do so let's navigate to the agent config file at */etc/datadog-agent*--you can do so with command **cd /etc/datadog-agent**. This will only work if you were in the root folder to start with--to go back to the root place **cd ~**.

Let's edit the *datadog.yaml* file to add the tags with **sudo vim datadog.yaml**. Scroll down to where they have *tags* in the file, should be starting on line 49--you can identify which line/row you're on by looking at the bottom-right hand side, the first number represents the row/line. 

Press *i* to allow yourself to edit and make changes to this file.

Delete the *#* which comments out the line so it isn't run or interpreted by the computer. Then edit the sample tag to whatever you want to call it. They provide good examples of what you may want to name it among all your VMs and applications. This will allow you to keep track of everything without confusion--you could essentially have 10-100 of these VMs with the same environment, so referring to this VM as Ubuntu/Xenial will simply not do.

Save the file when you're done by first pressing "Esc", and then by pressing **:wq** and then *Enter* to save and close out of the file.

Restart the agent with **sudo service datadog-agent restart**.

## Step 1

Now we will install a MySQL database in the virtual machine and connect it with Datadog's agent to collect metrics. 

Download and install MySQL into the VM with **sudo apt-get install mysql-server** and when it ask for a password just press *Enter*--you can always go back and update it.

Once that has been completed, you can enter the MySQL environment where you can communicate with its server and setup databases and whatnot with **sudo mysql**. You can exit by simply typing **exit**, and you'll know if you're in this environment by looking at the left-hand side--it should say *mysql>*.

## Step 2

Go to your account on the Datadog platform at www.datadoghq.com and click on *Integrations*. Find MySQL, or search for it in the above search bar and follow the instructions for *step 1* on how to integrate or configure MySQL in the VM to talk with the Datadog Agent so that you can collect certain metrics to be displayed in interactive and informative graphs. *Note that the scripts provided already take into consideration the mysql environment and so you shouldn't be in the mysql environment.*

For the second step where you are configuring the mysql.yaml file, if you're lost as to where you are in the folder structure, go back to the root with **cd ~** and then navigate to the proper location with **cd /etc/datadog-agent/conf.d/mysql.d/**. Once there, you will have to create a new file--**sudo touch mysql.yaml**. Open up this file in your text editor--I used Vim instead, so I opened it up with **sudo vim mysql.yaml**. Then you can copy and paste the script they gave you in there.

In addition, you can also add the following for extra metrics at the end:
extra_status_metrics: true
extra_innodb_metrics: true
extra_performance_metrics: true
schema_size_metrics: false

Restart the agent with **sudo service datadog-agent restart**. Then check to see how it is with **sudo service datadog-agent check mysql**.

## Step 3

In this step we will see how we can create custom checks that can submit metrics through the agent to your dashboard view. 

You should currently be in */etc/datadog-agent/checks.d*, so just **cd checks.d** to get to the right directory. Here we will create a Python file to code out our custom check--**sudo touch my_metric.py** will do just that. 

Let's hop inside this new Python file with **sudo vim my_metric.py**. Copy and paste the following inside:

try: 
  from checks import AgentCheck
except ImportError:
  from datadog_checls.checks import AgentCheck

__version = "1.0.0"

import random

class MyMetricCheck(AgentCheck):
  def check(self, instance):
    self.gauge('my_metric', random.randint(0, 1000))

When you're finished pasting that in, press **:wq** to save and close out of the file.

This will send a random number from 0 - 1000 with the check every time.

By default this check is done in intervals of 30 seconds according to the [docs here](https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6). If we want to adjust it, then we can!

Let's move from this *checks.d* directory back to the *conf.d* directory with **cd ../conf.d**. 

Here let's follow the more recent file structure and create a folder that will match our newly created custom check with **mkdir my_metric.d**. 

Navigate to it--**cd my_metric.d**. And then create a *yaml* file for this custom check with **sudo touch my_metric.yaml**.

Open it up with Vim **sudo vim my_metric.yaml** and copy and paste the following inside:

init config:

instances:
  - min_collection_interval: 45
  
*remmber you have to press **i** in order to edit inside Vim.*

Then save and close by once again pressing *Esc*, *:wq*, and then *Enter*.

That's how you can create custom agent checks! But let's say you don't want intervals of 45 seconds always, and instead you want to delay a check--you can do so without having to edit the file. Just add **-d** and a number when you run a check (sudo datadog-agent check mysql -d 10).

# Visualizing Data

Let's create a timeboard and some graphs for some metrics using Datadog's API instead of doing it online with their Graphical User Interface (GUI). 

## Step 1

Create a file somewhere inside the vagrant ssh environment--I chose to do it in */etc/datadog-agent*. I did so with the following command: **sudo touch test-timeboard.sh**. Let's jump inside and edit it to do just what we want then--**sudo vim test-timeboard.sh**. *Feel free to name it what you like, but be sure to keep the extension as "sh"*.

Remember you need to press *i* to edit inside Vim.

Start off by typing the following:

api_key=
app_key=

You're declaring two variables to be used later on. Go to the Datadog GUI in the browser and go to *Integrations* which depending your view could be at the top or left-hand side. Then click on the *APIs* tab at the top (it may be in a different location based on your screen size and resolution).

Copy and paste the respective keys into the file--you may have to create a key and you can do so by clicking the buttons there on the webpage. 

Continue on and copy and paste the following inside the same file:

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

Remember to save and close out of the file inside Vim is to press *Esc*, *:wq* and then *Enter*.

Now to run this script we can simply enter **./test-timeboard.sh**. 

If you run into a permissions error, do this **chmod +x /test-timeboard.sh**. And then try running the script above again.

## Step 2











