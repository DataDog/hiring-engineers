<h2>Dipankar Barua DataDog Techncial Assignment</h2>
<h3>Spin up a fresh Ubuntu VM via Vagrant</h3>

<h4>1 Let’s Setup Vagrant:</h4>

Before going to setup Vagrant  we have to install some prerequisites such as :

<h4>1.1.Windows Terminal / Mac Terminal / Gitbash Terminal (Recommended For Windows users).</h4>

You can Download Those Terminal Following below Links:

Gitbash- - https://git-scm.com/downloads For Windows.

let's Install Gitbash For Windows Users:

<img src ="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/Gitbash%20Terminal.png" alt="Gitbash Terminal">


Iterm2 - https://www.iterm2.com/ For Mac 

<img src="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/Iterm2%20for%20Mac%20Users.PNG" alt="Iterm2 Terminal ">


<h4>1.2.Virtual Box /VMware Etc.</h4>

Download the  VirtualBox  Tool – To download this tool visit the website https://www.virtualbox.org/

<img src ="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/Virtualbox%20after%20install.PNG" alt="Virtualbox After Installed">

<h3>1.3. Now we are going to setup Fresh Ubuntu Platform using in Virtual Box tools via Vagrant.</h3>

Download Vagrant and Install it on your system-  https://www.vagrantup.com/

<img src ="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/vagrant%20Website.PNG">

#### Is vagrant installed or not you can check it by the following command on your Terminal

#### Vagrant -v 

<img src="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/Vagrant%20Version.PNG">

 ###### Let’s create a folder on Desktop using Terminal  and Run below command on Terminal

User@Dipankar-Barua MINGW64 ~/Desktop

$ mkdir SetupVagrant

User@Dipankar-Barua MINGW64 ~/Desktop
$

<img src="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/Vagrant%20Folder%20On%20Desktop.PNG">

<img src ="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/VM%20and%20Terminal.PNG">


####### To find out the vagrant box visit https://app.vagrantup.com/boxes/search

We are going to select the Ubuntu 16.04 Vagrant Box for the Virtual Box


<img src ="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/vagrant%20box%20Ubuntu.PNG">


<h5>vagrant init ubuntu/xenial64</h5>

<h5>vagrant up<h5>
    

Then Next I run the Command vagrant up inside the Vagrant Folder


<img src ="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/Ubuntu%20install.PNG">


<h5>Following logs after Running the Vagrant up command inside the Vgarant Setup Folder Using Terminal</h5>

###### Here is the link of Logs Info 


https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/File%20Folder/vagrantup%20log



<h4>Below are the steps How to do configurations of Vagrant Setup</h4>

<code>
    
config.vm.box - operating system

config.vm.provider - Virtualbox

config.vm.network - How your host sees your box

config.vm.synced -  how you access files from your computer 

config.vm.provision - what want to setup

</code>



<img src ="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/vagrant%20box%20configure%20image.png">

Here is the Configurations File URL - https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/File%20Folder/vagrant%20File

##### some important command of Vagrant 

Some Important command For Vagrant

For Destroying- vagrant destroy

For suspend- vagrant suspend

For resuming – vagrant resume 

##### We can change VB Internal base Memory 

<h6> We can also change VM base memory and ram </h6>

vb.memory=2048
    vb.cpus =4
    
    
<h4>in the vagrant file </h4>

    
after saving the file we can reload vagrant -- reload then it will change

<img src ="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/vagrant%20reload.png">


Now we gonna install vagrant ssh using command vagrant ssh 


###### Logs below

###### $ vagrant ssh

<img src="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/vagrant%20ssh.png">


<h3>Here is the Vgarant ssh Logs File </h3>


https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/File%20Folder/vagrant%20ssh%20logs

######  Before Installing Apache 2

###### If we search now var /www we will not find for that we have to install apache2 


###### Lets Run the below command

Sudo apt-get update

Sudo apt-get install –y  git  (for git)

Sudo apt-get install –y  apache2 (for apache 2)


# --------------------------
vagrant@vagrant-ubuntu-trusty-64:~$ ls /var/www
html
vagrant@vagrant-ubuntu-trusty-64:~$ ls /var/www/html
index.html
vagrant@vagrant-ubuntu-trusty-64:~$


# ----------------------
For networking localhost has setup in vagrant file  and saved the file 

   config.vm.network "forwarded_port", guest: 80, host: 8080


# ----------------------
>h4>logs info  –</h4>

Setting up ssl-cert (1.0.33) ...
Processing triggers for libc-bin (2.19-0ubuntu6.14) ...
Processing triggers for ufw (0.34~rc-0ubuntu2) ...
Processing triggers for ureadahead (0.100.0-16) ...
vagrant@vagrant-ubuntu-trusty-64:~$ ls var/www/html
ls: cannot access var/www/html: No such file or directory
vagrant@vagrant-ubuntu-trusty-64:~$ clear
vagrant@vagrant-ubuntu-trusty-64:~$ ls /var/www
vagrant@vagrant-ubuntu-trusty-64:~$ cd html
-bash: cd: html: No such file or directory
vagrant@vagrant-ubuntu-trusty-64:~$ ls /var/www/html
index.html
vagrant@vagrant-ubuntu-trusty-64:~$ exit
logout
Connection to 127.0.0.1 closed.


User@Dipankar-Barua MINGW64 ~/Desktop/SetupVagrant
# -----

$ vagrant reload
==> default: Attempting graceful shutdown of VM...


<img src ="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/Apache2%20run.png">

# --------------
Apache setup 

http://localhost:8080/

<img src ="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/apache%20working%20local%208080.png">


# ------------------------
We can also use local private network using vagrant file network setting config.vm.network "private_network", ip: "192.168.33.10"

http://192.168.33.10/


<img src ="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/image16.png">


# -------------

#Folder setting 
  config.vm.synced_folder ".", "/var/www/html"



# -----------

<h4>config file sync</h4>

<img src="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/apache%20server%20file.png">



# ----------
Sign up for Data dog:

<img src ="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/Datadog%20Signup.png">


# ------------------------

1,2.Containerized approach with Docker for Linux and our dockerized Datadog Agent image

The Datadog agent was successfully installed via the following:

We can install two ways: First one is recommended

Run Below command Inside your Ubuntu Server

DD_API_KEY=610080f148d9e4d47efed7c611e64d7d bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"

<img src ="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/datadog%20agent%20install%20on%20Ubuntu.png">

Step by Step Installation:

Run these commands step by step to install the Datadog Agent in your Server.

<img src ="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/Datadog%20agent%20step%20by%20step.png">


1.3   Datadog Container Docker Install by following command 


docker run -d --name dd-agent -v /var/run/docker.sock:/var/run/docker.sock:ro -v /proc/:/host/proc/:ro -v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro -e DD_API_KEY=610080f148d9e4d47efed7c611e64d7d datadog/agent:latest


<img src ="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/Docker%20install%20on%20Ubuntu%20.png">


Docker installtion logs:

vagrant@ubuntu-xenial:~$ sudo docker run -d --name dd-agent -v /var/run/docker.sock:/var/run/docker.sock:ro -v /proc/:/host/proc/:ro -v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro -e DD_API_KEY=610080f148d9e4d47efed7c611e64d7d datadog/agent:latest
Unable to find image 'datadog/agent:latest' locally
latest: Pulling from datadog/agent
790c37dedd62: Pull complete
289cb409a94c: Pull complete
c8c8c4faaf9e: Pull complete
237fb89e1ed6: Pull complete
f57b386ca81e: Pull complete
847930fc0785: Pull complete
dc7a1564846a: Pull complete
2f9394a89b51: Pull complete
Digest: sha256:301adad25c80a2d976c47f77b5341479cf0e5f2f81db353c90568e8c42ab6576
Status: Downloaded newer image for datadog/agent:latest
6ee6039e47b205ea357fb9485ca04ddf99a48581b9c1dd7736cf59a56844a2bd
vagrant@ubuntu-xenial:~$


Is Datadog is running or not  to know I run the command below
sudo datadog-agent status

Here is the Datadog running status Logs:

https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/File%20Folder/datadog_running_statusd_log



To get the related info of Datadog agent we can use below command 

DESCRIPTION	COMMAND
Start Agent as a service	sudo service datadog-agent start

Stop Agent running as a service	sudo service datadog-agent stop

Restart Agent running as a service	sudo service datadog-agent restart

Status of Agent service	sudo service datadog-agent status

Status page of running Agent	sudo datadog-agent status

Send flare	sudo datadog-agent flare

Display command usage	sudo datadog-agent --help

Run a check	sudo -u dd-agent -- datadog-agent check <check_name>


I have already installed all the necessary packages those are all in vagrant provision shell script.

To get the MySQL config file change the directory 

<img src ="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/Datadog%20metric.png">






vagrant@vagrant-ubuntu-trusty-64:/etc/datadog-agent/conf.d$

<img src ="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/Datadog%20metric.png">

And also install manually MySQL integrations.
After installing the MySQL integration I restart my datadog agent

by following command 

sudo service datadog-agent restart

logs

vagrant@vagrant-ubuntu-trusty-64:/etc/datadog-agent/conf.d/mysql.d$ cd

vagrant@vagrant-ubuntu-trusty-64:~$ sudo service datadog-agent restart

datadog-agent stop/waiting

datadog-agent start/running, process 9504

vagrant@vagrant-ubuntu-trusty-64:~$




vagrant@vagrant-ubuntu-trusty-64:~$ sudo service datadog-agent restart

datadog-agent stop/waiting

datadog-agent start/running, process 9712


# Collecting Metrics:

Mysql 
sudo mysql -u root -p



I used this Documents to create new user with password;
https://docs.datadoghq.com/integrations/mysql/

Configuration

Edit conf.d/mysql.d/conf.yaml in the root of your Agent’s configuration directory in order to connect the Agent to your MySQL server. You will begin collecting your MySQL metrics and logs right away. See the sample configuration filefor all available configuration options.

PREPARE MYSQL
On each MySQL server, create a database user for the Datadog Agent:
mysql> CREATE USER 'datadog'@'localhost' IDENTIFIED BY '<UNIQUEPASSWORD>';
    
Query OK, 0 rows affected (0.00 sec)

For mySQL 8.0+ create the datadog user with the native password hashing method:
mysql> CREATE USER 'datadog'@'localhost' IDENTIFIED WITH mysql_native_password by '<UNIQUEPASSWORD>';
Query OK, 0 rows affected (0.00 sec)


sudo mysql -e "CREATE USER 'datadog'@'localhost' IDENTIFIED BY 'datadog';"

CREATE USER 'datadog'@'localhost' IDENTIFIED BY 'datadog';

GRANT PROCESS ON *.* TO 'datadog'@'localhost';

I gave user is datadog and password also datadog

# Images:

<img src="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/mysql%20configurations%20for%20tags.png">




 
 mysql config file 

vagrant@ubuntu-xenial:/etc/datadog-agent/conf.d/mysql.d$

conf.yaml.example

<img src="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/Datadog%20tags.png">



I Copied the example yaml file and as well create new file by following command

Sudo cp conf.yaml.example mysql.yaml




I took a lot of time because I was doing mistake 
I was creating a file inside the mysql. d directory 

/etc/datadog-agent/conf.d/mysql.d


But I had to create file inside the conf.d


dd tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog




<img src ="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/mysql%20is%20running%20in%20Datadog.png">

<img src ="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/datadog%20agent%20UI.png">

<img src ="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/datadog%20Integration.png">

<img src ="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/datadog%20mysql%20Integrations%20tags.png">

Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.


<img src ="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/mysql%20integration%20manully.png">

Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000

<img src ="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/customs%20metrics.png">


I created a Python file my_metric.py  inside the checks.d directory 


vagrant@ubuntu-xenial:/etc/datadog-agent$ cd checks.d

vagrant@ubuntu-xenial:/etc/datadog-agent/checks.d$ ls
dashboard-via-script.py  flask-app.py  my_metric.py  my_metric.pyc

my_metric.py:

# the following try/except block will make the custom check compatible with any Agent version
try:
    # first, try to import the base class from old versions of the Agent...
    from checks import AgentCheck
except ImportError:
    # ...if the above failed, the check is running in Agent version 6 or later
    from datadog_checks.checks import AgentCheck

# content of the special variable __version__ will be shown in the Agent status page
__version__ = "1.0.0"

import random

class MyMetricCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', random.randint(1,1001))


vagrant@ubuntu-xenial:/etc/datadog-agent/checks.d$





and as well yaml file  a yaml file  my_metric.yaml inside conf.d directory
vagrant@ubuntu-xenial:/etc/datadog-agent/conf.d$

my_metric.yaml:






init_config:

instances:
  - min_collection_interval : 45





Bonus Question Can you change the collection interval without modifying the Python check file you created?

my_metric.yaml:

yes without changing Python file we can change interval inside the yaml file.






init_config:

instances:
  - min_collection_interval : 45

Like instead of 45 we can setup 30 





datadog-agent.service - "Datadog Agent"
   Loaded: loaded (/lib/systemd/system/datadog-agent.service; enabled; vendor preset: enabled)
   Active: active (running) since Sat 2018-12-29 02:47:08 UTC; 10s ago
 Main PID: 9295 (agent)
    Tasks: 11
   Memory: 29.5M
      CPU: 1.762s
   CGroup: /system.slice/datadog-agent.service
           └─9295 /opt/datadog-agent/bin/agent/agent run -p /opt/datadog-agent/run/agent.pid

Dec 29 02:47:13 ubuntu-xenial agent[9295]: 2018-12-29 02:47:13 UTC | INFO | (runner.go:324 in work) | Done running check uptime
Dec 29 02:47:14 ubuntu-xenial agent[9295]: 2018-12-29 02:47:14 UTC | INFO | (runner.go:258 in work) | Running check network
Dec 29 02:47:14 ubuntu-xenial agent[9295]: 2018-12-29 02:47:14 UTC | WARN | (datadog_agent.go:149 in LogMessage) | (base.py:228) | DEPRECATION NOTICE: `device_name` is deprecated, please use a `device:` tag in the
Dec 29 02:47:14 ubuntu-xenial agent[9295]: 2018-12-29 02:47:14 UTC | INFO | (runner.go:324 in work) | Done running check network
Dec 29 02:47:15 ubuntu-xenial agent[9295]: 2018-12-29 02:47:15 UTC | INFO | (runner.go:258 in work) | Running check load
Dec 29 02:47:15 ubuntu-xenial agent[9295]: 2018-12-29 02:47:15 UTC | INFO | (runner.go:324 in work) | Done running check load
Dec 29 02:47:16 ubuntu-xenial agent[9295]: 2018-12-29 02:47:16 UTC | INFO | (runner.go:258 in work) | Running check file_handle
Dec 29 02:47:16 ubuntu-xenial agent[9295]: 2018-12-29 02:47:16 UTC | INFO | (runner.go:324 in work) | Done running check file_handle
Dec 29 02:47:17 ubuntu-xenial agent[9295]: 2018-12-29 02:47:17 UTC | INFO | (runner.go:258 in work) | Running check cpu
Dec 29 02:47:17 ubuntu-xenial agent[9295]: 2018-12-29 02:47:17 UTC | INFO | (runner.go:324 in work) | Done running check cpu
lines 1-20/20 (END)










After running the check my_metric I got the Below logs:


vagrant@ubuntu-xenial:/etc/datadog-agent/checks.d$ sudo -u dd-agent -- datadog-agent check my_metric
=== Series ===
{
  "series": [
    {
      "metric": "my_metric",
      "points": [
        [
          1546105749,
          615
        ]
      ],
      "tags": null,
      "host": "ubuntu-xenial",
      "type": "gauge",
      "interval": 0,
      "source_type_name": "System"
    }
  ]
}
=========
Collector
=========

  Running Checks
  ==============

    my_metric (1.0.0)
    -----------------
      Instance ID: my_metric:5bbfe9f3938f1c8d [OK]
      Total Runs: 1
      Metric Samples: Last Run: 1, Total: 1
      Events: Last Run: 0, Total: 0
      Service Checks: Last Run: 0, Total: 0
      Average Execution Time : 0s


Check has run only once, if some metrics are missing you can try again with --check-rate to see any other metric if available.

<img src ="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/custom%20%20metrcis%20ouput%20logs.png">


agent check my_metric
=== Series ===
{
  "series": [
    {
      "metric": "my_metric",
      "points": [
        [
          1546106211,
          394
        ]
      ],
      "tags": null,
      "host": "ubuntu-xenial",
      "type": "gauge",
      "interval": 0,
      "source_type_name": "System"
    }
  ]
}
=========
Collector
=========

  Running Checks
  ==============

    my_metric (1.0.0)
    -----------------
      Instance ID: my_metric:5ba864f3937b5bad [OK]
      Total Runs: 1
      Metric Samples: Last Run: 1, Total: 1
      Events: Last Run: 0, Total: 0
      Service Checks: Last Run: 0, Total: 0
      Average Execution Time : 0s


Check has run only once, if some metrics are missing you can try again with --check-rate to see any other metric if available.
vagrant@ubuntu-xenial:/etc/datadog-agent/checks.d$


Yes we can change the interval without modifying python file  

init_config:

instances:
  - min_collection_interval : 45

Here is yaml file into conf.d Directory





# Visualizing Data:


https://docs.datadoghq.com/api/?lang=python#create-a-timeboard

Utilize the Datadog API to create a Timeboard that contains


<img src ="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/dashboard%20via%20script.png">



vagrant@ubuntu-xenial:/etc/datadog-agent$ cd checks.d
vagrant@ubuntu-xenial:/etc/datadog-agent/checks.d$ ls
dashboard-via-script.py  flask-app.py  my_metric.py  my_metric.pyc
vagrant@ubuntu-xenial:/etc/datadog-agent/checks.d$

Inside the checks.d directory I created a python file name is dashboard-via-script.py  



dashboard-via-script.py  :

Notes:
Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboar

initialize(**options)

title = "Dipankar Barua Time Board"
description = "An informative timeboard."
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:system.mem.free{*}"}
        ],
        "viz": "timeseries"
    },
    "title": "Average Memory Free"
}]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:my-host"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)


I Have given the name  Dipankar Barua Time Board"



<img src ="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/dashboard%20listed.png">



Once this is created, access the Dashboard from your Dashboard List in the UI:

<img src ="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/dashbboard%20garphg.png">




•	Set the Timeboard's timeframe to the past 5 minutes
•	Take a snapshot of this graph and use the @ notation to send it to yourself.

<img src ="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/annotate%20dashboard.png">

<img src ="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/monitor%20schedule%20downtime.png">


•	Bonus Question: What is the Anomaly graph displaying?
The anomaly diagram is designed to show any variations in the data points from normal leaning. If the data point is outside of what is predicted, it's going to an anomaly.





# Monitoring

<img src ="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/datadog%20monitor.png">

<img src ="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/metric%20monitorr.png">

<img src ="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/metric%20monitor%20notified.png">


<img src ="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/monitor%20check%20mail%20send%20to%20me.png">



<img src ="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/monitor%20schedule%20downtime.png">

<img src ="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/mail%20send%20to%20me.png">

<img src ="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/datadog%20monitor%20schedule.png">


# ollecting APM Data

<img src ="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/pip%20install.png">


I installed all python flask related packages in to the server
Then later I created a file inside the agent checks.d foder 
# vagrant@ubuntu-xenial:/etc/datadog-agent/checks.d$ ls
dashboard-via-script.py  flask-app.py  my_metric.py  my_metric.pyc


flask-app.py  





vagrant@ubuntu-xenial:/etc$ pip install datadog
Collecting datadog
  Downloading https://files.pythonhosted.org/packages/17/dd/a7bbb33427f853f82b36356286fb922ef976bf18e78dbb76ac43b8c50e26/datadog-0.26.0.tar.gz (154kB)
    100% |████████████████████████████████| 163kB 1.2MB/s
Collecting decorator>=3.3.2 (from datadog)
  Downloading https://files.pythonhosted.org/packages/bc/bb/a24838832ba35baf52f32ab1a49b906b5f82fb7c76b2f6a7e35e140bac30/decorator-4.3.0-py2.py3-none-any.whl
Collecting requests>=2.6.0 (from datadog)
  Downloading https://files.pythonhosted.org/packages/7d/e3/20f3d364d6c8e5d2353c72a67778eb189176f08e873c9900e10c0287b84b/requests-2.21.0-py2.py3-none-any.whl (57kB)
    100% |████████████████████████████████| 61kB 2.1MB/s
Collecting certifi>=2017.4.17 (from requests>=2.6.0->datadog)
  Downloading https://files.pythonhosted.org/packages/9f/e0/accfc1b56b57e9750eba272e24c4dddeac86852c2bebd1236674d7887e8a/certifi-2018.11.29-py2.py3-none-any.whl (154kB)
    100% |████████████████████████████████| 163kB 1.4MB/s
Collecting chardet<3.1.0,>=3.0.2 (from requests>=2.6.0->datadog)
  Downloading https://files.pythonhosted.org/packages/bc/a9/01ffebfb562e4274b6487b4bb1ddec7ca55ec7510b22e4c51f14098443b8/chardet-3.0.4-py2.py3-none-any.whl (133kB)
    100% |████████████████████████████████| 143kB 1.1MB/s
Collecting idna<2.9,>=2.5 (from requests>=2.6.0->datadog)
  Downloading https://files.pythonhosted.org/packages/14/2c/cd551d81dbe15200be1cf41cd03869a46fe7226e7450af7a6545bfc474c9/idna-2.8-py2.py3-none-any.whl (58kB)
    100% |████████████████████████████████| 61kB 1.1MB/s
Collecting urllib3<1.25,>=1.21.1 (from requests>=2.6.0->datadog)
  Downloading https://files.pythonhosted.org/packages/62/00/ee1d7de624db8ba7090d1226aebefab96a2c71cd5cfa7629d6ad3f61b79e/urllib3-1.24.1-py2.py3-none-any.whl (118kB)
    100% |████████████████████████████████| 122kB 1.4MB/s
Building wheels for collected packages: datadog
  Running setup.py bdist_wheel for datadog ... done
  Stored in directory: /home/vagrant/.cache/pip/wheels/83/ad/89/ffe24c194922e51d6ce237e44b469d30d80fbeaf30e327aa30
Successfully built datadog
Installing collected packages: decorator, certifi, chardet, idna, urllib3, requests, datadog
Successfully installed certifi chardet datadog decorator idna requests urllib3
You are using pip version 8.1.1, however version 18.1 is available.
You should consider upgrading via the 'pip install --upgrade pip' command


<img src ="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/pip%20install%20menthod.png">


I run the flask app via ddtrace-run python flask-app.py

Then got the below logs:



INFO:werkzeug: * Running on http://0.0.0.0:5050/ (Press CTRL+C to quit)



<img src ="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/run%20flask%20app.png">

#  Apm is running dashboard

<img src ="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/complete%20datadog%20Graph.png">


Another way I tried to run the flask app using virtutalenv and gurnicorn 



<img src ="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/flask%20app%20run%20another%20way.png">


Anomaly detection is an algorithmic feature that allows you to identify when a metric is behaving differently than it has in the past, taking into account trends, seasonal day-of-week, and time-of-day patterns. It is well-suited for metrics with strong trends and recurring patterns that are hard or impossible to monitor with threshold-based alerting





Bonus Question: What is the difference between a Service and a Resource? 

A "Service" is the name of a set of processes that work together to provide a feature set. For instance, a simple web application may consist of two services: a single webappservice and a single database service, while a more complex environment may break it out into 6 services: 3 separate webapp, admin, and query services, along with a master-db, a replica-db, and a yelp-api external service.
These services are defined by the user when instrumenting their application with Datadog. This field is helpful to quickly distinguish between your different processes.
In the Datadog UI, this is the "Name" field in the above image.  An example of setting a custom Service using Python: 



<img src ="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/image53.png">


Resource
A particular query to a service. For a web application, some examples might be a canonical URL like /user/home or a handler function like
web.user.home (often referred to as "routes" in MVC frameworks). For a SQL database, a resource would be the SQL of the query itself like select * from users where id = ?
The Tracing backend can track thousands (not millions or billions) of unique resources per service, so resources should be grouped together under a canonical name, like /user/home rather than have /user/home?id=100 and /user/home?id=200 as separate resources.
These resources can be found after clicking on a particular service. 
 
<img src ="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/image54.png">


Fianl Question 

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability! 
Is there anything creative you would use Datadog for? 




I would like to integrate data dog with Health Industry. In the hospitals, there are a lot of patients with having different illnesses. we know that all the hospitals they have all the tools I mean the difference application to checkup the patient's conditions.in Realtime how patience health is improving we can know by using datadog and as well Hospitals authorisation can also confirm how can they improve patients health for future patients.





Notes: sorry to say that I didn’t submit on deadline due to some personal reasons I needed some times to complete the task and Finally I would like to tell that I am  really interested for this positions.





#  All events of data dogdog agents




Now5 events1:004:007:0010:0013:0016:0019:0022:00
28 matching events from Dec 29, 12:00AM - Dec 30, 12:00AM  Aggregate related events
 
 
Post
 
Dipankar Barua started scheduled downtime on Metric Monitor #audit #downtime #downtime_id:443823653 #monitor#monitor_id:7757433
Scheduled downtime on Metric Monitor has started. 
Alerting on Metric Monitor will be silenced until 8:53PM UTC on December 30.
@barua.dipankar04@gmail.com
Sat Dec 29 2018 21:54:53 GMT+0100 (Central European Standard Time) • Add comment • Lower priority
 
Dipankar Barua started scheduled downtime on Metric Monitor #audit #downtime #downtime_id:443823435 #monitor#monitor_id:7757433
Scheduled downtime on Metric Monitor has started. 
Alerting on Metric Monitor will be silenced until 8:52AM UTC on December 30.
@barua.dipankar04@gmail.com
Sat Dec 29 2018 21:53:15 GMT+0100 (Central European Standard Time) • Add comment • Lower priority
 
[Monitor Created] Metric Monitor #audit #monitor #monitor_id:7757433
Dipankar Barua created Metric Monitor.

The monitor:
•	is named: Metric Monitor.
•	has the query avg(last_5m):avg:my_metric{*} > 800.
•	notifies if the metric has been missing data for the last 10m.
•	does not automatically resolve.
•	includes the message: "@barua.dipankar04@gmail.com"
•	does not renotify.
•	notifies recipients when the definition is modified.
•	requires a full window of data - includes triggering tags in notification title.
•	does not evaluate with a delay.
Sat Dec 29 2018 21:39:35 GMT+0100 (Central European Standard Time) • Add comment • Lower priority
 
Average Memory Free 

Average Memory Free
 
@barua.dipankar04@gmail.com
Sat Dec 29 2018 21:25:42 GMT+0100 (Central European Standard Time) • View • Add comment • Lower priority • Edit
 
A new application key has been created. #account #audit
Application key mrbarua created by barua.dipankar04@gmail.com in org Datadog Recruiting Candidate
Sat Dec 29 2018 19:30:55 GMT+0100 (Central European Standard Time) • Add comment • Lower priority
 
ubuntu-xenial's Datadog Agent has started #host:ubuntu-xenial
See ubuntu-xenial's dashboard
Updated Sat Dec 29 2018 19:02:36 GMT+0100 (Central European Standard Time) • Created Sat Dec 29 2018 18:14:55 GMT+0100 (Central European Standard Time) • Add comment • Lower priority
2 events
 
ubuntu-xenial's Datadog Agent has started #host:ubuntu-xenial
See ubuntu-xenial's dashboard
Sat Dec 29 2018 18:40:23 GMT+0100 (Central European Standard Time) • Add comment • Lower priority
 
[Auto] Clock in sync with NTP is ok on 1 over 1 host #host:ubuntu-xenial #monitor
ntp.in_sync recovered on host:ubuntu-xenial
Triggers if any host's clock goes out of sync with the time given by NTP. The offset threshold is configured in the Agent's ntp.yaml file.
Please read the KB article on NTP Offset issues for more details on cause and resolution.
________________________________________
[Monitor Status] • [Edit Monitor]
Updated Sat Dec 29 2018 18:16:11 GMT+0100 (Central European Standard Time) • Created Sat Dec 29 2018 16:39:10 GMT+0100 (Central European Standard Time) • Add comment • Lower priority
2 events
 
ubuntu-xenial's Datadog Agent has started #host:ubuntu-xenial
See ubuntu-xenial's dashboard
Updated Sat Dec 29 2018 15:32:14 GMT+0100 (Central European Standard Time) • Created Sat Dec 29 2018 14:54:20 GMT+0100 (Central European Standard Time) • Add comment • Lower priority
5 events
 
ubuntu-xenial's Datadog Agent has started #host:ubuntu-xenial
See ubuntu-xenial's dashboard
Sat Dec 29 2018 15:12:59 GMT+0100 (Central European Standard Time) • Add comment • Lower priority
 
ubuntu-xenial's Datadog Agent has started #host:ubuntu-xenial
See ubuntu-xenial's dashboard
Sat Dec 29 2018 14:44:46 GMT+0100 (Central European Standard Time) • Add comment • Lower priority
 
MySQL has been manually created. 
Integration configuration created by Dipankar Barua.
Sat Dec 29 2018 14:28:54 GMT+0100 (Central European Standard Time) • Add comment • Lower priority
 
MySQL has been manually deleted. 
Integration configuration deleted by Dipankar Barua.
The integration dashboards have been removed, but you also need to manually change the agent configuration to stop metric collection.
Sat Dec 29 2018 14:25:54 GMT+0100 (Central European Standard Time) • Add comment • Lower priority
 
ubuntu-xenial's Datadog Agent has started #host:ubuntu-xenial
See ubuntu-xenial's dashboard
Sat Dec 29 2018 13:31:27 GMT+0100 (Central European Standard Time) • Add comment • Lower priority
 
ubuntu-xenial's Datadog Agent has started #host:ubuntu-xenial
See ubuntu-xenial's dashboard
Sat Dec 29 2018 03:47:09 GMT+0100 (Central European Standard Time) • Add comment • Lower priority
 
MySQL has been manually created. 
Integration configuration created by Dipankar Barua.
Sat Dec 29 2018 03:44:21 GMT+0100 (Central European Standard Time) • Add comment • Lower priority
 
ubuntu-xenial's Datadog Agent has started #host:ubuntu-xenial
See ubuntu-xenial's dashboard
Sat Dec 29 2018 02:38:45 GMT+0100 (Central European Standard Time) • Add comment • Lower priority
 
ubuntu-xenial's Datadog Agent has started #host:ubuntu-xenial
See ubuntu-xenial's dashboard
Sat Dec 29 2018 02:31:45 GMT+0100 (Central European Standard Time) • Add comment • Lower priority


# recent datadog alert email

<img src ="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/2nd%20Janaury.png">

<img src ="https://github.com/mrbarua/hiring-engineers/blob/solutions-engineer/images/2nd%20January%20.png">




























