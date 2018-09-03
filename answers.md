PS: Please enlarge the whole webpage to check the screenshots.😉

# Prerequisites - Setup the environment

Answers : I use Vagrant and VirtualBox to setup the test environment. Since I am working on a windows PC, I choose cmder as the console emulator for Shell.

**Step 1.**

Download Vagrant (Windows 64 bit) from [here](https://releases.hashicorp.com/vagrant/2.1.4/vagrant_2.1.4_x86_64.msi).👈
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/1.png" width="750px" />
</div>

Download VirtualBox from [here](https://download.virtualbox.org/virtualbox/5.2.18/VirtualBox-5.2.18-124319-Win.exe).👈
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/10.png" width="750px" />
</div>

Download cmder from [here](https://github.com/cmderdev/cmder/releases/download/v1.3.6/cmder.zip).👈
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/30.png" width="750px" />
</div>

**Step 2.**

Install the above tools and locate the ubuntu image (16.04) from [here](https://app.vagrantup.com/boxes/search?utf8=%E2%9C%93&sort=downloads&provider=&q=ubuntu).👈
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/40.png" width="750px" />
</div>

**Step 3.**

Create a new folder name as ubuntu under c:\, run cmder.exe and run cmd "vagrant box add ubuntu/xenial64" to copy the Ubuntu image to the local host. Once Vagrant finish copying the image, run "cd c:\ubuntu" and "vagrant init ubuntu/xenial64" to generate the config files in c:\ubuntu. Then run "vagrant up" to spin up the test environment.
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/50.PNG" width="750px" />
</div>

<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/60.PNG" width="750px" />
</div>

**Step 4.**

After cmd "vagrant up" is completed, a virtual machine will be generated in Virtualbox, once that has been confirmed, run cmd "vagrant ssh-config" through cmder to get the ssh login info and run the cmd "ssh vagrant@127.0.0.1 -p *port number* -i *location of the private key*" to login to the VM. (The third step only happens on the first login)
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/80.PNG" width="750px" />
</div>

**Step 5.**

Signup a free datadog trail account from [here](https://www.datadoghq.com/#) 👈and use “Datadog Recruiting Candidate” in the “Company” field and login after creating the account.
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/90.png" width="750px" />
</div>

# Collecting Metrics

**Step 1.**

Install the datadog agent: When login for the first time, datadog will ask to setup the agent, choose "Ubuntu" to get the install cmd as _DD_API_KEY=b233617fcf6a0f29a9715078391b4716 bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"_. In the meantime, bottom is displayed as "Waiting for agent to report".
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/92.png" width="750px" />
</div>

Login to Shell through cmder as step 4 in the previous section and run the datadog install cmd. ("sudo su" is for switching to root account)
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/110.PNG" width="750px" />
</div>

Once you see the below screenshot, that means the agent has been installed successfully. Also, the agent status will change to as in the screenshot below.
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/120.PNG" width="750px" />
</div>
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/93.png" width="750px" />
</div>

Move to the /etc/datadog-agent directory and edit datadog.yaml, update it as below.
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/130.PNG" width="750px" />
</div>
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/140.PNG" width="750px" />
</div>

Run cmd "apt-get update" when you login as root and then run "reboot" to restart the VM. Then the tags are updated as in the screenshot.
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/81.PNG" width="750px" />
</div>
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/160.png" width="750px" />
</div>

**Step 2.**

Install mysql on ubuntu by running cmd "apt-get install mysql-server", during the installation, mysql will ask for root password, input the password and hit ok. Once it finishs installing, run cmd "systemctl status mysql.service" to check the status, when you see the screenshot below, that means mysql has been installed successfully.
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/170.PNG" width="750px" />
</div>
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/180.PNG" width="750px" />
</div>

Follow the latest mysql integration doc from [here](https://docs.datadoghq.com/integrations/mysql/).👈
Login to mysql and Create the datadog user and give access:
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/190.PNG" width="750px" />
</div>

Run the check cmds.
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/200.PNG" width="750px" />
</div>

Give access to performance_schema.
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/210.PNG" width="750px" />
</div>

Create the conf.yaml in mysql.d directory and edit it as described in the doc.
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/220.PNG" width="750px" />
</div>
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/230.PNG" width="750px" />
</div>

Install the mysql integration from datadog website.
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/240.PNG" width="750px" />
</div>
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/250.png" width="750px" />
</div>

I got 3 warning messages on mysql section when I run the "datadog-agent status" cmd😨, screenshot as below, and the fix as well😊
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/251.PNG" width="750px" />
</div>
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/252.PNG" width="750px" />
</div>
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/253.PNG" width="750px" />
</div>

Return to datadog website and check the host, all mysql integration has been successfully installed. 
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/260.png" width="750px" />
</div>

**Step 3.**

Reference doc is [here](https://docs.datadoghq.com/developers/agent_checks/).👈
Browse into /etc/datadog-agent/conf.d and create my_metric.yaml and edit as in the screenshot.
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/280.PNG" width="750px" />
</div>

Browse into /etc/datadog-agent/checks.d and create my_metric.py as below.
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/290.PNG" width="750px" />
</div>

Check my_metric by running cmd "datadog-agent check my_metric" and get the screenshot below.
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/300.PNG" width="750px" />
</div>

**Step 4.**

Set min_collection_interval: 45, code is included in the previous screenshots. And metric will be shown on the datadog website as below.
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/310.png" width="750px" />
</div>

**Bonus Question**

Set min_collection_interval: 45, code is included in the previous screenshots.

# Visualizing Data

**Step 1.**

Reference doc can be found in [here](https://docs.datadoghq.com/api/?lang=python#timeboards).👈

Locate the api key and the app key from Integration -- APIs, need to generate the application key for the first time.
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/320.PNG" width="750px" />
</div>

Create a timeboard.py file under /etc/datadog-agent and attach the code as below.
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/370.PNG" width="750px" />
</div>

Before running the cmd "python timeboard.py" in Shell, first run "apt install python-minimal", "apt install python-pip" and "pip install datadog"
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/331.PNG" width="750px" />
</div>
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/340.PNG" width="750px" />
</div>
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/350.PNG" width="750px" />
</div>

Then run the "python timeboard.py" cmd and check the "Dashboards" -- "Dashboards List", two graphs are created. The First graph contains the same metric in different format as displayed in the screenshot at the bottom, pink is the one with the rollup (1 hour) function and the blue one is the normal my_metric. 
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/380.png" width="750px" />
</div>

**Step 2.**

On the "My Timeboard" webpage, hang ove the mouse to the current time on the graph, click and hold the mouse to drag it to the time point on the graph 5 mins ago. Scrrenshot as below.
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/390.png" width="750px" />
</div>

Snapshot the graph as below and confirm the email as below
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/400.PNG" width="750px" />
</div>
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/410.PNG" width="750px" />
</div>
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/420.PNG" width="750px" />
</div>

**Bonus Question**

Grey area on the graph is what datadog consider as the normal range and the red section indicates not normal usage.

# Monitoring Data

**Step 1.**

Choose "Monitors" -- "New Monitor", then choose "Metric", on the setup page, update the arguments as requested.
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/430.PNG" width="750px" />
</div>
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/440.png" width="750px" />
</div>
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/450.png" width="750px" />
</div>

**Step 2.**

Input the code showed below into "Say what's happening" section. (Since it's taking too long to get an alert on a 5 mins base, so I change to 1 min just to get the alert email).
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/461.png" width="750px" />
</div>

Screenshots of different messages depends on different status.
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/470.png" width="750px" />
</div>
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/473.png" width="750px" />
</div>

**Bonus Question**

This can setup through "Monitors" -- "Manage Downtime"
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/500.PNG" width="750px" />
</div>

Alert will be muted from 7 PM until 9 AM the next day from Mon to Fri every week.
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/510.png" width="750px" />
</div>

Alert will be muted during Sat and Sun.
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/520.png" width="750px" />
</div>

Notification screenshots as below. (Time in the email is UTC)
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/490.png" width="750px" />
</div>
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/480.png" width="750px" />
</div>

I change the downtime setting just to get the notification email as below.
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/491.png" width="750px" />
</div>
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/492.png" width="750px" />
</div>

# Collecting APM Data

Reference can be found from [here](https://docs.datadoghq.com/tracing/setup/python/).👈

Install Datadog Tracing library by running cmd "pip install ddtrace"
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/600.PNG" width="750px" />
</div>

Create a test.py under /etc/datadog-agent and attach the code as below.
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/630.PNG" width="750px" />
</div>

Run "ddtrace-run python test.py" cmd and then browse to datadog website, "APM" -- "Services".
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/640.PNG" width="750px" />
</div>
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/650.PNG" width="750px" />
</div>
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/651.png" width="750px" />
</div>

The link to the dashboard with both APM and Infrastructure Metrics is [here](https://app.datadoghq.com/dash/904405/allens-timeboard-2-sep-2018-2136?live=true&page=0&is_auto=false&from_ts=1535885101126&to_ts=1535888701126&tile_size=m).👈 Screenshot as below.
<div align="center">
<img src="https://github.com/allenz16/hiring-engineers/blob/solutions-engineer/screenshots/660.png" width="750px" />
</div>

**Bonus Question**

A Resource is a particular action for the service. For example, a database is a service, a query is a resource.

# Final Question

Hmmm😑, can't really say this is creative, but monitor IoT sounds cool, you can remotely check like what's happening at your home and prepare what needs to be done in advance. 😁
