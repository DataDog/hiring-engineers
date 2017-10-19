# The Challenge
#####  Datadog Candidate: Pamela Chow
------

The system that I used for this challenge had the following:

Windows 10

Oracle VirtualBox 5.1.28

Git Bash for Windows

### Level 0 (optional) - Setup an Ubuntu VM

With my Windows background, I initially started with a Windows 2008R2 Server virtual machine, installed an agent, MySQL, the MySQL integration, and realized that I was spending more time working on various framework dependencies, so I setup an Ubuntu box with Vagrant with the command below from bash for Windows which was already on my machine.
```
vagrant up
```
My initial attempt resulted in the error below. I had installed VirtualBox back in 2014 and even though I upgraded to the latest version, the version of Guest Additions did not update properly. I tried reinstalling again, but received the same error below stating a mismatch of Guest additions 4.2.0 to VirtualBox 5.1 as shown.
![VirtualBox version mismatch error](http://farm5.staticflickr.com/4450/37677477326_e9657abb1c_b.jpg)
 
To resolve this problem I tried a Google search for `VirtualBox Guest Additions downloads` to look for specific versions, but didn’t see a sufficient answer.

I decided to go to the source and navigated to the location of the `Guest Additions` in the `Oracle\VirtualBox` directory to see if it had been updated when I upgraded.
![Finding the VirtualBox Guest Additions ISO](http://farm5.staticflickr.com/4513/37055430223_6ebe9a0854_b.jpg)
 
The date was current, but the issue persisted. I did a Google search for `VBoxGuestAdditions.iso` which resulted in a link that had various versions available for [download](http://download.virtualbox.org/virtualbox/) I chose the `VBoxGuestAdditions_5.1.0.iso` and replaced the old version (renaming it to match). I ran `vagrant up` again with success and connected to the box!
Connecting to my new virtual machine:
```
vagrant ssh
```
I’m in!

![Vagrant box](http://farm5.staticflickr.com/4474/23915872618_a51406a148_b.jpg)

Reflecting on this initial setup, the challenge that I had from my mouse bound Windows background was understanding that I wouldn’t be working with an OS with a graphical UI. I was trying to create a new Ubuntu box from an ISO in VirtualBox with a mouse friendly interface before understanding how Vagrant makes life simple.
### Level 1 - Collecting your Data
From the Datadog [website](https://www.datadoghq.com), it was simple to sign up for an account and get started.
![Sign up for Datadog](http://farm5.staticflickr.com/4498/37056282993_d06e25cf5c_b.jpg)

The new Ubuntu system needed a few updates and applications to continue with the changes that I planned to implement, so I installed a few tools, curl for receiving files by URL and nano for text editing.
```
sudo apt-get install update
sudo apt-get install curl
sudo apt-get install nano
```
To install the agent, I found instructions to install the Ubuntu Agent from the `Integrations>Agent>Ubuntu` page.
![Ubuntu Agent installation instructions](http://farm5.staticflickr.com/4472/37727425311_621a71ed9a_b.jpg)
A quick and easy install with a single line:
```
DD_API_KEY=b01a83b64ead45bef96965119825cd76 bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/dd-agent/master/packaging/datadog-agent/source/install_agent.sh)"
```
To rename the host and add tags, the config file needed modification. I referenced the [Basic Agent Usage for Ubuntu]( https://docs.datadoghq.com/guides/basic_agent_usage/ubuntu/#configuration) to find that the config file for the Agent lives here: `/etc/dd-agent/datadog.conf`.
```
cd etc/dd-agent
sudo nano datadog.conf
```
I then removed the comments # to rename the host and add tags for my two kittens, `Cooper` and `Rio`.

![Updating the config](http://farm5.staticflickr.com/4455/37677477146_228d8c58b7_b.jpg )
 
```Kitten tags: Cooper and Rio```

![Kitten Tags](http://farm5.staticflickr.com/4492/37017067434_1947a7dc0b_b.jpg)

My little helpers.

In order for the Agent to recognize config changes, it needs to be restarted. To restart the agent, I referenced the help section of the DataDog Docs for [Basic Agent Usage for Ubuntu]( https://docs.datadoghq.com/guides/basic_agent_usage/ubuntu/#starting-and-stopping-the-agent)
```
sudo /etc/init.d/datadog-agent restart
```
I could see on the Events board that the host was renamed and contained my updated kitten tags 
![Renamed host and kitten tags](http://farm5.staticflickr.com/4463/37677476846_b27a4d1636_b.jpg)

 
## Installing a database
MySQL was my database of choice and from the Datadog website, found the instructions for the MySQL Integration under [Integrations](https://app.datadoghq.com/account/settings#integrations/mysql)
![MySQL Integration Instructions](http://farm5.staticflickr.com/4475/37055864283_971274fbdc_b.jpg)
Being new to this database management system, I referenced resources from [Linode]( https://www.linode.com/docs/databases/mysql/install-mysql-on-ubuntu-14-04)  for instructions on how to install and connect to MySQL.
```
sudo apt-get install mysql-server
```
I then connected to MySQL
```
sudo mysql -u root –p
```
Per the integration configuration instructions, I created a user, datadog, granted replication and other necessary privileges.

![MySQL Grants](http://farm5.staticflickr.com/4452/23872802088_f72c5c6686_b.jpg )
 
I created the ‘/etc/dd-agent/conf.d/mysql.yaml’ file with the content below in order to configure the Agent to connect to MySQL.
```
init_config:

instances:
  - server: localhost
    user: datadog
    pass: yjyaweevrTZ/KVnm02tv1gUj
    tags:
        - boxer
        - pug
    options:
        replication: 0
        galera_cluster: 1
```
I restarted the agent and ran an info check on the agent.
```
sudo /etc/init.d/datadog-agent restart
sudo /etc/init.d/datadog-agent info
```
![Agent Info](http://farm5.staticflickr.com/4448/37677476686_8331021641_b.jpg )
 
![Agent Info](http://farm5.staticflickr.com/4473/37677478526_75810fc9ff_b.jpg)
 
### Writing an Agent Check
An Agent Check is a way to collect metrics for applications for custom applications.
In order to gain a basic understanding of how to create one, I started with the simple example from [Your First Check]( https://docs.datadoghq.com/guides/agent_checks/#your-first-check).

I created the Agent config file `/etc/dd-agent/conf.d/hello.yaml`
```
init_config:

instances:
    [{}]
```
And also the Python file with the custom check at the Agent root location `/etc/dd-agent/checks.d/hello.py`
```
from checks import AgentCheck
class HelloCheck(AgentCheck):
    def check(self, instance):
        self.gauge('hello.world', 1)
```
To run the new metric, I then ran the command.
```
sudo -u dd-agent dd-agent check hello
```
The results show the new `hello.world` metric.
![Test check Hello](http://farm5.staticflickr.com/4491/37677478386_a53fc6c43a_b.jpg)
 

To create a new custom metric that samples a random value, I created a file with the contents below at the location `/etc/dd-agent/conf.d/test.yaml`
```
init_config:

instances:
    [{}]
```

To generate the random values, I created a python file with the contents below at the location `/etc/dd-agent/checks.d/test.py`
```
from random import random
from checks import AgentCheck
class HelloCheck(AgentCheck):
    def check(self, instance):
        self.gauge('test.support.random', random())
```
I ran the Agent Check and also checked the Agent info which shows the custom check `test` with 1 metric
```
sudo -u dd-agent dd-agent check test
```
![Test.support.random metric](http://farm5.staticflickr.com/4460/37677478196_b4cbfefe67_b.jpg)
 
```
sudo /etc/init.d/datadog-agent info
```
The results show both the `hello` and `test` metrics.

![New metrics](http://farm5.staticflickr.com/4491/37055430693_ecfbd1d283_b.jpg)
  
After creating these new custom metrics, I needed to send the data that they generated to Datadog. In order for my newly created metrics to talk to Datadog, the information needed to be sent with [StatsD]( https://docs.datadoghq.com/guides/metrics/) which requires some setup.
StatsD is a client/server model which is included with Datadog Agents (version 3+).
In order to use the module, I first needed to install Python-PIP for package management and then the Datadog module.
```
sudo apt-get install python-pip
sudo pip install datadog
```
After running the installing the module I created the python file `datadogstatsd.py`

```
sudo nano datadogstatsd.py
```
Content for `datadogstatsd.py`:
```
#!/usr/bin/env python
from datadog import statsd
```

And then ran the file

```
python datadogstatsd.py
```

StatsD is now communicating and sending data from the new metrics to Datadog.
### Level 2 - Visualizing your Data
Next, I wanted to clone my database integration dashboard and add additional database metrics to it as well as my new `test.support.random` metric.
In order to do so, I opened the MySQL dashboard from the `Integration Dashboards` from my Dashboard and chose `Clone Dashboard` from the Settings cog in the upper left corner.

![Cloning a dashboard](http://farm5.staticflickr.com/4477/23874155308_d504cac937_b.jpg)

The new dashboard is visible under `Your Custom Dashboards` of the Dashboard section.

![Newly cloned dashboard](http://farm5.staticflickr.com/4494/37070133343_784649662c_b.jpg)

To [view the new metrics](https://docs.datadoghq.com/guides/metrics/#seeing-your-custom-metrics), I navigated to the Metric Explorer on the Metrics page, I chose `test.support.random` as the custom metric to graph on my new dashboard.

![Adding metrics](http://farm5.staticflickr.com/4446/37055430543_f729b46909_b.jpg) 

The metrics displayed on the cloned dashboard.

![Adding Metrics]( http://farm5.staticflickr.com/4505/37470328310_2411a8be22_b.jpg)
### What is the Agent?
An agent is an application that is installed onto a host to monitor stats of a machine or application. Agents can monitor a machine or some are created to monitor integrated applications. They collect data, or metrics, and send them to Datadog so that they can evaluate the performance of a host or application that is being monitored. They can be used to ensure that operations are running smoothly and send notifications when they are not, or warn that there may be issues with operations by monitoring metrics.

### What is the difference between a [timeboard and a screenboard?]( https://help.datadoghq.com/hc/en-us/articles/204580349-What-is-the-difference-between-a-ScreenBoard-and-a-TimeBoard-)
A timeboard is designed primarily to collect data to be used for troubleshooting and correlation whereas the purpose of a screenboard is the view the status of a machine or application and relevant data. The layout of a timeboard is a simple grid that is not customizable, in contrast  a screenboard has the ability to add various widgets in a layout that the user chooses. Using a screenboard, you have the ability to view data from different timeframes by widget, but the timeboard is restricted to the same time for each graph.
 
### Creating a snapshot
Referencing the Blog article [Real-time graph annotations](https://www.datadoghq.com/blog/real-time-graph-annotations/)  I created a graph annotation.

From the Dashboard page, I first zoomed into a timeframe, highlighted a snapshot with the camera, and added a message that would display as an event. 

![Adding Annotations](http://farm5.staticflickr.com/4469/37073111163_8e4a74fdc4_b.jpg) 

 
 
 

The snapshot notification as shown on the Event page.

![Event page snapshot](http://farm5.staticflickr.com/4474/23927792028_90cf72e7d1_b.jpg)
 
### Level 3 - Alerting on your Data
If you’ve ever wanted to stay informed about the health of a host or application, receiving alerts from a Monitor is a simple and easy way to do so. The purpose of a Monitor is to send notifications to check the status, threshold of a metric, or other conditions.

To create a [Monitor](https://docs.datadoghq.com/guides/monitors/), from the Monitors page I chose to create a `New Monitor` for metrics. This specific monitor was for detecting the threshold for the `test.support.random` metric, on the host sashimi. I specified that the alert should only trigger when the value exceeded 0.9.

![New Monitor](http://farm5.staticflickr.com/4494/37677478056_3fedee4e41_b.jpg)
 

The content of the alert includes the value of the metric as a template variable that exceeds the threshold. Since alerts support markdown, I added a link to the dashboard for easier troubleshooting.

```
{{#is_alert}} Database performance has reached {{value}} {{/is_alert}}. View [dashboard](https://app.datadoghq.com/dash/376395/mysql---overview-cloned) @pamela______@gmail.com
```

The email that I received including the alert notification and link to the dashboard.

![Email alert](https://c1.staticflickr.com/5/4494/37069033823_fe1455e48a_b.jpg)
 


To schedule downtime, from the Monitors Manage Downtime page, I created a recurring period of downtime. For the purpose of this example the monitor is checking a non production, test environment so alerts regarding performance will be silenced outside of the typical production hours.

![Scheduling downtime](http://farm5.staticflickr.com/4483/37768172691_8e073b8f4b_b.jpg)
 

Note: One important thing to take into account in regards to scheduling downtime is that the notification email will show the time in UTC. The example email below shows that the notifications will be silenced until 4:00pm UTC which corresponds to 9:00am PST.

The email notification for the scheduled downtime.

![Downtime alert](http://farm5.staticflickr.com/4458/37482951900_ba83ff11dc_b.jpg)
 
