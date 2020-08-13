
Early stage notes:

I am using a MacOSx operating system, hardware overview:

Model Name: MacBook Pro
Model Identifier: MacBookPro15,
Processor Name: Quad-Core Intel Core i
Processor Speed: 1.4 GHz
Number of Processors: 1

Total Number of Cores: 4

L2 Cache (per Core): 256 KB
L3 Cache: 6 MB
Hyper-Threading Technology: Enabled
Memory: 8 GB
Boot ROM Version: 1037.80.53.0.0 (iBridge: 17.16.13050.0.0,0)
Activation Lock Status: Enabled

Prerequisites - Setup the environment

In this section, I will spin up a fresh linux VM via Vagrant by using VirtualBox. I will also make
sure to use a minimum v. of 16.04 to make sure that I don’t have any dependency issues.

1- Download the open-source software Vagrant to be able to build and maintain portable virtual
software development environment.
Location: https://www.vagrantup.com/downloads.html
2- Download VirtualBox. Make sure that the version is compatible with the latest Vagrant
updates.
Location: https://www.virtualbox.org/wiki/Downloads
3- Create a directory anywhere on your machine to be able to hold the Vagrant files in the
future. (Make sure there is no space, could cause issues in the future)
4- Open your terminal, go to your file location. (Here mine is located in my Desktop):
code:
cd desktop
cd vagrant_vm
5- Initialize your linux VM:
code:
vagrant init bento/ubuntu-16.
6- Bring up the machine, start running it:
code:
vagrant up
7- To do any SSH (secure shell) commands:
code:
vagrant ssh
8- To make sure the VM has been carefully created:
code:
unman -a
Resulting in the following line:
Linux vagrant 4.4.0-185-generic #215-Ubuntu SMP Mon Jun 8 21:53:19 UTC 2020 x86_
x86_64 x86_64 GNU/Linux

9- Exit the SSH session and proceed to halt or terminate your VM, in this case, the VM will be
kept running.
Code:
exit -> to exit your SSH session
vagrant halt -> to halt, temporally disable your VM
vagrant destroy -> to fully destroy you VM

I will also create an account using “Datadog Recruiting Candidate” for the Company field.
Account: tony_bh@live.com

Here we can see that VirtualBox UI will display the linux VM just created with
all of the system specifications and if it is running or not.
Collecting Metrics:

The first point on the agenda for this section is to be able to add tags from the Agent config file
directly.

The agent that has been downloaded directly via the DataDog platform is Mac OS X with the
following command line:
DD_AGENT_MAJOR_VERSION=7 DD_API_KEY=822c3c10f88c65b74efed9f3934f9af
DD_SITE="datadoghq.com" bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/
install_mac_os.sh)"
(Via the terminal)

I was able to find the Agent config file by going trough the following address for the directory:
~/.datadog-agent/datadog.yaml\

I will go into the datadog.yaml file and make sure to the add the tags I have created there:
(Under @param tags)
![Tags%20added%20to%20Agent%20config%20file..png](https://github.com/tonybh1991/hiring-engineers/blob/master/Tags%20added%20to%20Agent%20config%20file..png)

And now I demonstrate these tags being displayed right below the Tags section on the right of
the Agent section.

![Tags%20displayed%20in%20platform..png](https://github.com/tonybh1991/hiring-engineers/blob/master/Tags%20displayed%20in%20platform..png)

For the next step, I will have to download a database on my machine. My database of choice
will be MongoDB.
Link to download the DB: https://docs.mongodb.com/manual/tutorial/install-mongodb-on-os-
x/
I will also make sure to run my MongoDB as a macOS Service.
Code: brew services start mongodb-community@4.4 (In terminal.)

![MongoDB%20started%20on%20machine..png](https://github.com/tonybh1991/hiring-engineers/blob/master/MongoDB%20started%20on%20machine..png)

I will then install the respective Datadog integration for that database.

![Extension%20installed..png](https://github.com/tonybh1991/hiring-engineers/blob/master/Extension%20installed..png)

I make sure to create the proper user into the shell of MongoDB.
Code:
db.createUser({
"user": "datadog",
"pwd": "Scuderia11",
"roles": [
{ role: "read", db: "admin" },
{ role: "clusterMonitor", db: "admin" },
{ role: "read", db: "local" }
]
})

And then modify the mondo.d/conf.yaml life to make sure it holds all the proper information.
Code:
init_config:

instances:

@param hosts - list of strings - required
Hosts to collect metrics from, as is appropriate for your deployment topology.
E.g. for a standalone deployment, specify the hostname and port of the mongod
instance.

For replica sets or sharded clusters, see instructions in the sample conf.yaml.
hosts:
MacBook-Pro-de-Tony.local: 27017
@param username - string - optional
The username to use for authentication.
username: datadog

@param password - string - optional
The password to use for authentication.
password: Scuderia

@param database - string - optional
The database to collect metrics from.
database: datadog_example

@param options - mapping - optional
Connection options. For a complete list, see:
https://docs.mongodb.com/manual/reference/connection-string/#connections-
connection-options

options:
authSource: admin

@param replica_check - boolean - optional - default: true
Whether or not to read from available replicas.
Disable this if any replicas are inaccessible to the Agent.
replica_check: true

We can now see the following confirmation that the integration for MongoDB has been
successfully installed and is properly working.

![MongoDB%20success.](https://github.com/tonybh1991/hiring-engineers/blob/master/MongoDB%20success..png)

Also, we can see in the dashboard section that a new dashboard has been found for the
MongoDB overview.

Now for the following part, we will be creating a Custom Agent Check. Basically, we need to
modify the minimum collection interval by writing the proper script. The proper collection
interval is usually set at 15 seconds.

First I need to create the custom agent check with a random value between 0 and 1000. I will
create a my_metric.py file located in check.d file directory and import the random package
from the basic Python library to be able to do so.

![my_metric.py%20.png](https://github.com/tonybh1991/hiring-engineers/blob/master/my_metric.py%20.png)

And then I set the collection interval to 45 seconds by implementing the following code in the
my_metric.yaml located in the conf.d file directory. I have to make sure that this file name
corresponds to the same file name as the one given for my python script.

![my_metric.yaml%20.png](https://github.com/tonybh1991/hiring-engineers/blob/master/my_metric.yaml%20.png)

I will also go a step further to verify that my_metric works using terminal verification.
code: datadog-agent check my_metric

![Making%20sure%20that%20my_metric%20has%20been%20properly%20initialized..png](https://github.com/tonybh1991/hiring-engineers/blob/master/Making%20sure%20that%20my_metric%20has%20been%20properly%20initialized..png)

Bonus question:

The collection interval can be modified also from the Agent config file. So you can modify this
value in the jmx_check_period section in the datadog.yaml file. (Be careful to make sure to
modify the value according to the fact that the measure presented in the file is in milliseconds.)

![Bonus%20question%20for%20check%20period..png](https://github.com/tonybh1991/hiring-engineers/blob/master/Bonus%20question%20for%20check%20period..png)

Visualizing Data:

For this section I first need to get the API Key and the Application Key from the following link:
https://app.datadoghq.com/account/settings#api

Then I need to create an application key, from the same link.

Then I need to write the API python calls script, which will also be included in my submission.
(File included in the submission)

Here are the following graphs produced in the UI for the past 4 hours:

![Dashbaord%20from%20API%20Datadog..png](https://github.com/tonybh1991/hiring-engineers/blob/master/Dashbaord%20from%20API%20Datadog..png)

Then after I set the timeframe to the past 5 mins and send it to myself via the @ notation.

![Sending%20a%20screenshot%20via%20email..png](https://github.com/tonybh1991/hiring-engineers/blob/master/Sending%20a%20screenshot%20via%20email..png)

Bonus question:

The Anomaly graph will measure and adapt to new behaviours and provide alerts when the
there is a significant change in the behaviour from its previous pattern.

Monitoring Data

For the next part, I will be creating a new monitor that will watch the overage of my average
metric (my_metric).

Here are screenshots of the monitor created that respects the conditions given by the
instructions.

![Configure%20monitor%20part%201.png](https://github.com/tonybh1991/hiring-engineers/blob/master/Configure%20monitor%20part%201.png)
![Configure%20monitor%20part%202.png](https://github.com/tonybh1991/hiring-engineers/blob/master/Configure%20monitor%20part%202.png)

Here is the template email notification received:

![Alert%20for%20monitor%20via%20email.png](https://github.com/tonybh1991/hiring-engineers/blob/master/Alert%20for%20monitor%20via%20email.png)

Bonus question:
![Downtime%20weekday..png](https://github.com/tonybh1991/hiring-engineers/blob/master/Downtime%20weekday..png)
![Downtime%20weekend..png](https://github.com/tonybh1991/hiring-engineers/blob/master/Downtime%20weekend..png)

Here is the email notification sent:

![Scheduled%20downtime%20email%20notification..png](https://github.com/tonybh1991/hiring-engineers/blob/master/Scheduled%20downtime%20email%20notification..png)

(With a test time applied.)

Collecting APM Data:

For this next session, I will be using dtrace-run only.

After importing the dtrace package and also enabling the app analytics (via code:
ddtrace.config.analytics_enabled = True), I am able to view the trace and app analytics on the
platform directly.

![Traces%20for%20APM..png](https://github.com/tonybh1991/hiring-engineers/blob/master/Traces%20for%20APM..png)

A fully instrumented app will be provided in the submission as well.

Here is a screenshot for the dashboard including APM and Infrastructure Metrics.

![Dashbaord%20with%20APM%20and%20Infrastructure%20Metrics..png](https://github.com/tonybh1991/hiring-engineers/blob/master/Dashbaord%20with%20APM%20and%20Infrastructure%20Metrics..png)

Also, here is the link to this dashboard:
https://p.datadoghq.com/sb/v5wjp7nuo1ht9332-f9b61aa87c32930f9959ec64223bfd

Bonus question:
A service is a process in the system, like an API call or a trace call, and a resource is an
endpoint itself.

Final Question:

Medical drone monitoring for all special cases and emergencies for countries equipped of
such technology.
Amperage and Voltage level measurement and monitoring to be able to sustain the green
practices for many federal and provincial buildings.
General view for oncologists monitoring white cells by use of a pacer for patients treated for
cancer.
Monitoring of torque produced by sports cars on corners to be able to elevate the the
stickiness of tires and increase the car’s downforce.
