# Level 0 (optional) - Setup an Ubuntu VM
## Q1:While it is not required, we recommend that you spin up a fresh linux VM via Vagrant or other tools so that you don't run into any OS or dependency issues. Here are instructions for setting up a Vagrant Ubuntu 12.04 VM.
## Answer: 

### Step1: Download Vagrant 
Download and install the Universal (64-bit) package for window 10.
[Link to Download Vagrant](https://www.vagrantup.com/downloads.html)

<img src="https://c1.staticflickr.com/5/4218/35349974342_746f911afb_b.jpg" width="1024" height="399" alt="L0-S1">

### Step2 :Download & Install Virtual Box 
Download the Windows hosts installation file from below link.

[Link to Download windows hosts](https://www.virtualbox.org/wiki/Downloads)

### Step3：Init the vagrant

1.Create a vagrant_getting_started folder as below. 

    mkdir C:\IT\vagrant_getting_started
    cd C:\IT\vagrant_getting_started

2.Run below command in the created folder as below.   

    vagrant init hashicorp/precise64

<img src="https://c1.staticflickr.com/5/4279/35130747840_611c11d908_b.jpg" width="923" height="124" alt="L0-S2">

HashiCorp (the makers of Vagrant) publish a basic Ubuntu 12.04 (32 and 64-bit) box that is available for minimal use cases. It is highly optimized, small in size, and includes support for Virtualbox and VMware.

    vagrant up

<img src="https://c1.staticflickr.com/5/4207/34707521423_cdca1ddc75_b.jpg" width="923" height="594" alt="L0-S3">

3.Confirm the VM machine and Run the Ubuntu in Virtual Box

Confirm the vagrant machine as below. 

<img src="https://c1.staticflickr.com/5/4282/35130836440_c225807241_b.jpg" width="843" height="484" alt="L0-S4">


Login in with below information:
* user: vagrant
* password: vagrant

<img src="https://c1.staticflickr.com/5/4234/35130836160_5c877f39bf_b.jpg" width="854" height="414" alt="L0-S5">




# Level 1  Collecting your Data

## L1-Q1: Sign up for Datadog (use "Datadog Recruiting Candidate" in the "Company" field), get the Agent reporting metrics from your local machine.
## Answer:
### Step1: Sign up for Datadog 
Access to https://www.datadoghq.com/. Fill in the detail and sign up as below.

<img src="https://c1.staticflickr.com/5/4278/35517660485_4d902e16a0.jpg" width="374" height="437" alt="L1-S1">

### Step2: Install the Agent reporting metrics from my local machine.
Use easy one-step install.

    DD_API_KEY=ed18fe469bf81acc242a9bb146d966f9 bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/dd-agent/master/packaging/datadog-agent/source/install_agent.sh)"

<img src="https://c1.staticflickr.com/5/4264/35387006121_7de23a34eb_b.jpg" width="938" height="150" alt="L0-S2">

### Step3: Install curl 

    sudo apt-get install curl

<img src="https://c1.staticflickr.com/5/4234/35517623555_b0be6501be_b.jpg" width="921" height="509" alt="L1-S3">

### Step4: Reinstall the Agent reporting metrics from my local machine.
Use easy one-step install.

    DD_API_KEY=ed18fe469bf81acc242a9bb146d966f9 bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/dd-agent/master/packaging/datadog-agent/source/install_agent.sh)"

<img src="https://c1.staticflickr.com/5/4215/35131279710_15661aa88e_b.jpg" width="922" height="494" alt="L1-S4">


## L1-Q2: Bonus question: In your own words, what is the Agent?
## Answer: A person or process that takes an action or responses for a particular action.


## L1-Q3: Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
## Answer:
### Step1: Add tags in the Agent config file

Backup config file

    cd /etc/dd-agent
    sudo cp -p datadog.conf datadog.conf_bk_20170623
    ls -ltr 

Add tags into config file
   
    sudo vi datadog.conf
    // add the below line into datadog.conf
    tags: mytag, env:prod, role:database, location:home


### Step2: Restart the Agent and confirm the tags on the Host Map page in Datadog

Restart the Agent and to reload the configuration files:

    sudo /etc/init.d/datadog-agent restart


Confirm the tags at event page

<img src="https://c1.staticflickr.com/5/4240/34677285434_d26409e62d.jpg" width="500" height="52" alt="L1-Q3-S3">

Confirm the tags on the Host Map page in Datadog

<p align="center"> 
<img src="https://c1.staticflickr.com/5/4216/35352213432_6fbdd1dd83.jpg" width="500" height="297" alt="L1-Q4-S2">
</p> 


## L1-Q4: Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
## Answer:

### Step1 Install MongoDB on Ubuntu

#### 1.Import the public key used by the package management system.

    sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10

#### 2.Create a list file for MongoDB.
  
   Create the /etc/apt/sources.list.d/mongodb-org-3.0.list list file using the command appropriate for your version of Ubuntu:

	echo "deb http://repo.mongodb.org/apt/ubuntu precise/mongodb-org/3.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.0.list

#### 3.Reload local package database.
Issue the following command to reload the local package database:

    sudo apt-get update

#### 4.Install the MongoDB packages.

    sudo apt-get install -y mongodb-org

#### 5.Start MongoDB.

    sudo service mongod start


### Step2 Install the Datadog-MongoDB Integration for database

Create a read-only admin user for Datadog 
   
    Authenticate as the admin user.
    use admin
    db.createUser({
    "user":"datadog",
    "pwd": "test123",
    "roles" : [
    {role: 'read', db: 'admin' },
    {role: 'clusterMonitor', db: 'admin'},
    {role: 'read', db: 'local' }
     ]
    })

### Step3 Configuration Datadog Integration

Create mongo.yaml file

    cd /etc/dd-agent/conf.d
    sudo cp -p mongo.yaml.example mongo.yaml
    ls -ltr 

Edit your instance information in conf.d/mongo.yaml file as below:
    
    instances:
     The format for the server entry below is:
     -server: mongodb://datadog:test123@localhost:27017/admin

### Step4 Restart the Agent

Restart the Agent and to reload the configuration files:

    sudo /etc/init.d/datadog-agent restart

### Step5 Execute the info command and verify that the integration check has passed. 

    sudo /etc/init.d/datadog-agent info

Check the information as below

<p align="center"> 
<img src="https://c1.staticflickr.com/5/4234/34677502844_496260cbe2.jpg" width="500" height="298" alt="L1-Q4-S5">
</p>


## L1-Q5: Write a custom Agent check that samples a random value. Call this new metric: test.support.random
Here is a snippet that prints a random value in python:

    import random
    print(random.random())
## Answer:
 
### Step1 Configruation test yaml file

Create conf.d/test.yaml as below 

    init_config:

    instances:
    [{}]

<img src="https://c1.staticflickr.com/5/4264/34677819294_d7df074a72.jpg" width="500" height="80" alt="L1-Q5-S1">

### Step2 Code the test Checker


Create checks.d/test.py as below 


    import random

    from checks import AgentCheck

    class TestCheck(AgentCheck):
     def check(self,instance):
        self.gauge('test.support.random',random.random(),tags=['support_random'])

<img src="https://c1.staticflickr.com/5/4217/35132641460_866511dbc5.jpg" width="500" height="125" alt="L1-Q5-S2">

### Step3 Restart the Agent

To restart the Agent and to reload the configuration files:

    sudo /etc/init.d/datadog-agent restart


To receive information about the Agent’s state:

    sudo /etc/init.d/datadog-agent info


### Step4 Check new metric from Datadog

<img src="https://c1.staticflickr.com/5/4285/35519004395_0defa890ff.jpg" width="500" height="323" alt="L1-Q5-S3">



# Level 2 - Visualizing your Data

## L2-Q1: Since your database integration is reporting now, clone your database integration dashboard and add additional database metrics to it as well as your test.support.random metric from the custom Agent check.
## Answer:

### Step1 Clone mongo database intergation as below 
<img src="https://c1.staticflickr.com/5/4216/35132805920_1b899242a3.jpg" width="500" height="242" alt="L2-Q1-S1">

<img src="https://c1.staticflickr.com/5/4279/34677979694_869f2c0236.jpg" width="500" height="217" alt="L2-Q1-S2">

### Step2 Add additional database metrics (included test.support.random metric )

Drag graph on to board. 

<img src="https://c1.staticflickr.com/5/4230/35133009350_a7535619a3.jpg" width="500" height="61" alt="L2-Q1-S3">

Define the new metrics (test.support.random) as below 

<img src="https://c1.staticflickr.com/5/4231/35480198616_89085a6aac.jpg" width="500" height="424" alt="L2-Q1-S4">

Define the new metrics (mongodb.dbs: count the number of database in mongodb) as below 

<img src="https://c1.staticflickr.com/5/4215/35133010760_2ca13205d0.jpg" width="500" height="425" alt="L2-Q1-S5">

New customized Clone mongo database is as below 

<img src="https://c1.staticflickr.com/5/4233/35352404572_178ee7bfe9.jpg" width="500" height="255" alt="L2-Q1-S6">


## L2-Q2:Bonus question: What is the difference between a timeboard and a screenboard?
## Answer: The difference is as below

* Screenboard: 

  - ScreenBoards can be shared as live and as a read-only entity, whereas TimeBoards cannot
	
  - These are flexible, far more customizable and are great for getting a high-level look into a system. They are created with drag-and-drop widgets, which can each have a different time frame.


* Timeboard：

  - All graphs are always scoped to the same time.

  - Graphs will always appear in a grid-like fashion. This makes them generally better for troubleshooting and correlation. Graphs from a TimeBoard can be shared individually



## L2-Q3:Take a snapshot of your test.support.random graph and draw a box around a section that shows it going above 0.90. Make sure this snapshot is sent to your email by using the @notification
## Answer:

Set Alert Monitor for test.support.random. It send a snapshot which is send to my email (sunhua_jp@hotmail.com) as below.

<img src="https://c1.staticflickr.com/5/4280/35484428906_ff4d4e6bfc.jpg" width="500" height="318" alt="LLLL">


# Level 3 - Alerting on your Data

Since you've already caught your test metric going above 0.90 once, you don't want to have to continually watch this dashboard to be alerted when it goes above 0.90 again. So let's make life easier by creating a monitor.

## L3-Q1:Set up a monitor on this metric that alerts you when it goes above 0.90 at least once during the last 5 minutes
## Answer:

Go to "New Monitor " and select "Metric" as type. Define the new Monitors and Set alert condition for test metric as below :

<img src="https://c1.staticflickr.com/5/4261/35515356155_8ca1f5a688_b.jpg" width="1024" height="544" alt="L3-Q1-S1">


## L3-Q2:Bonus points: Make it a multi-alert by host so that you won't have to recreate it if your infrastructure scales up.
## Answer:
Set up Multi-alert for all hosts in all locations as below:

<img src="https://c1.staticflickr.com/5/4281/35385184401_0e442302f8_b.jpg" width="1024" height="230" alt="L3-Q1-S2"></a>


## L3-Q3:Give it a descriptive monitor name and message (it might be worth it to include the link to your previously created dashboard in the message). Make sure that the monitor will notify you via email.
## Answer:

Name the monitor as test metric gose ablove 0.90. Insert the previousely created dashboard in the message.  


<img src="https://c1.staticflickr.com/5/4284/35477097096_5321758fa7_b.jpg" width="1024" height="443" alt="L3-Q1-S3"></a>

## L3-Q4:This monitor should alert you within 15 minutes. So when it does, take a screenshot of the email that it sends you.
## Answer:

<img src="https://c1.staticflickr.com/5/4215/34707141323_bb85694fc3_b.jpg" width="1024" height="764" alt="L3-Q1-S5">

## L3-Q5:Bonus: Since this monitor is going to alert pretty often, you don't want to be alerted when you are out of the office. Set up a scheduled downtime for this monitor that silences it from 7pm to 9am daily. Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.
## Answer:

Go to "Manage Downtime" and create a schedule as below.

<img src="https://c1.staticflickr.com/5/4258/34706930863_cfbeb7d082_b.jpg" width="912" height="1024" alt="L3-Q1-S4"></a>

The screenshot of notification email show as below:

<img src="https://c1.staticflickr.com/5/4230/35135335110_96caa4f6a9.jpg" width="500" height="294" alt="L3Q5">
