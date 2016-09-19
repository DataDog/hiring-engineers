# DataDog Support Engineer Assignment

#### By Shaun Carland

## Table of Contents
1. Level 1 
	a. What is an Agent?
		
		i.Collector
		
		ii. DogStatsD
		
		iii. Forwarder
		
		iv. SupervisorD
		
	b. Setting Up DataDog on my Machine
	c. Setting Up MySQL DataDog Integration
	d. Creating a Custom Agent
	
2. Level 2
	a. My Dashboard
	b. ScreenBoards vs TimeBoards
3. Level 3
	a. Setting up a Monitor  

##Level 1 

### What is an agent?

An agent is a tool that can be installed on a host.  The agent sends information to DataDog to collect information, reports, and events from a platform.  From DataDog, the user can set up metrics to measure a variable on their system (for example, CPU Usage, I/O wait, Network Traffic, ect).  

The architecture of agent is composed of four components: the Collector, DogStatsD, the Forwarder, and the SupervisorD.  Each component of the architecture runs on its own process and is written in Python.    

##### Collector
The collector (agent.py) performs two operations.  Firstly, the collector gathers system metrics such as memory and CPU usage.  Secondly, the collector executes checks on the machine.  The collector also runs checks on the host’s integrations (such as MySQL, Chef, or Amazon Web Services).   

##### DogStatsD

DogStatsD (dogstatsd.py) is a StatsD backend that takes the aggregation several data points into a single custom metric over a preset period of time.  For example, if a user wanted to count page views on their website, they could insert a command to increment a metric every time the page is rendered.  Each time the command to increment the metric is called, a UDP packet is created.  DogStatsD collects these metric increments over a defined period of time (10 seconds by default) and sends the aggregated metric count to DataDog using an HTTPs connection.  The user can then go on DataDog to visualize the aggregated metric data.  

##### Forwarder

The data from the collector and DogStatsD does not go directly to DataDog.  Instead, the data is sent to and queued in  the third component of the agent architecture; the forwarder.    The forwarder then buffers and communicates this data to DataDog via HTTPS.

##### SuperVisorD

The fourth and final component of the Agent architecture is SuperVisorD.  The purpose of SuperVisorD  is to ensure all of the processes described above are running smoothly and correctly.  It accomplishes this by running a master process as the root user, and forks all of the other subprocesses as the dd-agent user.  

A diagram explaining the architecture is depcited in agent_diagram.png 

### Setting Up DataDog On My Machine

To set up DataDog on my machine, I first created an Ubuntu Virtual Machine using Vagrant.  This was to ensure a consistent development environment and to eliminate issues regarding dependencies or machine’s operating system (OSX Yosemite).  My virtual machine’s metrics are displayed through DataDog in system_metrics.png.  As shown, I added several tags to my host.  I decided to specifically tag my host with the region of the world it is in (New England).  This would be useful if, as a user, I wanted to detect specific metrics from my hosts in one part of the country.  

### Setting Up MySQL DataDog Integration

I chose to use a MySQL DataDog integration because out of the databases listed in the assignment, MySQL is the database I have most experience with.  Since I was using Vagrant to run a Virtual Machine, I had to first install MySQL, then create a DataDog user on my MySQL server, and update the mysql.yaml file in my conf.d directory.  I found using the info command (sudo /etc/init.d/datadog-agent info) very helpful in troubleshooting issues during this process.  

Now that I know how to integrate DataDog with MySQL, I look forward to using it to visualize the performances of MySQL databases used in my various projects and in any projects I work on in the future!

### Creating a Custom Agent
The first step in creating an agent was to create a new Agent Check to sample a random number between 0 and 1.  This agent check was written in the file (/etc/dd-agent/checks.d/random.py) using Python.  My custom created check inherits from the AgentCheck module and sends a gauge of a randomly sampled number between zero and one each time it is called to the test.support.random metric.   The second step was to create a configuration file (/etc/dd-agent/conf.d/random.yaml) using YAML.  Both the agent check and configuration files are located in this pull request.

I found using the following command very helpful in troubleshooting the process of setting up an agent: 

sudo -u dd-agent dd-agent check my_check


## Level 2 

###My Dashboard

A copy of the MySQL database with additional metrics (test.support.random and the number of tables in the database) is displayed in database_integration_dashboard.png.  The dashboard can also be found at https://app.datadoghq.com/dash/185089/mysql---overview-cloned?live=true&page=0&is_auto=true&from_ts=1474285180288&to_ts=1474288780288&tile_size=xs.  

###ScreenBoards Vs TimeBoards

DataDog has the ability to create two different types of dashboards; ScreenBoards and TimeBoards.  Both allow the user to visualize data collected from their system.  However, there are some key differences between these two dashboards.  TimeBoards scope all of the data within a specific time interval.  As shown in database_integration_dashboard.png, the time interval selected is “The Past Hour”.  This means the data in the graphs is scoped to data points within the last hour.  Individual graphs on a TimeBoard can be shared between collaborators.

A ScreenBoard provides a heads-up display into a user’s system, allowing the user to determine their system’s current status or performance.   Widgets on a screenboard are not bound by the same time frame.  A ScreenBoard can be shared as a whole unit, while a TimeBoard can only share its individual graphs.

Looking at random_over_9.png, the graph indicates where the value is above 0.9 in the grey box.  A snapshot of the graph going over 0.9 sent to my e-mail is shown in random_over_9_email.png.  

##Level 3

### Setting up a Monitor


I created a monitor to send me an e-mail whenever the random value went over 0.9.  I made the alert a multi alert by host.  I wrote a message with a link to my dashboard.  The alert message that I received is displayed in email_alert.png.  I also set up scheduled downtime between 7pm and 9am daily.  I included a screenshot of this alert under the file scheduled_downtime_email.png.

## Closing Remarks

I enjoyed doing this exercise a lot! It was extremely rewarding to solve each problem and learn such a complex, interesting system.  It challenged me in a different technical manner that I was not used to; figuring out how a system works and troubleshooting it, rather than just sitting down and writing code.  I hope I have the opportunity to continue solving problems like the ones in this exercise with DataDog!

 
