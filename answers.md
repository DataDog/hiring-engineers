Your answers to the questions go here.

Datadog is the essential monitoring platform for cloud applications. We bring together data from servers, containers, databases, and third-party services to make your stack entirely observable. These capabilities help DevOps teams avoid downtime, resolve performance issues, and ensure customers are getting the best user experience. [Datadog](https://www.datadoghq.com/about/press/)

With DevOps CI/CD culture, Datadog provides you with the ability to monitor and maintain your Infrastructe as it grows with statefull or stateless servers and serverless applications. As Infrastructure as a code and containerization grows more prominent, companies will need an all in one monitoring tool to provide you detailed insight into your entire environment.

It provides robust reporting of your cloud applications with a basic datadog agent installation. CPU, Load, Memory, Network and disk monitoring for your cloud or on premis servers and applications. Datadog comes with over 250 integrations that allow you to monitor all of your systems, apps, and services.These integrations are easy to setup and generate statistics immediately. Datadog provides an easy to use UI that allows you to see and monitor your Infrastructure and your entire application stack. The UI provides you easy to use Event Stream, Dashboards, Host maps, Monitors and metrics to see your server and application in full detail.

In the below exercise I will demonstrate the ease of installation and configuration of servers, datadog agents, Intergrations, Metrics, Dashboards and finally an APM(Application Performance Monitoring) of a Flask app that monitors http traffic.

I created multiple environments, virtual and physical, on premis and in the cloud. 3 Ubuntu servers(1 vagrant/virtualbox on premis Mac Pro, 2 AWS Ubuntu EC2 AMI), 1 standalone on premis RHEL server and one Amazon Linux AMI in AWS.

Each server recieved an Agent. One servers agent is a docker container.

# 1. Setting up the Enviornment
Screen Prints and configuration of Vagrant/Virtual Box Environment:

First download [Vagrant](https://www.vagrantup.com/intro/getting-started/).

<img src="https://github.com/kchitwood/hiring-engineers/blob/kchitwood-patch-1/vagrant%20download%202.png"></a>

Once Downloaded, just double click the file and the installation wizard will appear.

<img src="https://github.com/kchitwood/hiring-engineers/blob/kchitwood-patch-1/vagrant%20install%201.png" width="500" height="332" alt="_DSC4652"></a>

Choose the directory for the installation of the product

<img src="https://github.com/kchitwood/hiring-engineers/blob/kchitwood-patch-1/vagrant%20install%203.png" width="500" height="332" alt="_DSC4652"></a>

Once completed you should see a successful installation screen.

<img src="https://github.com/kchitwood/hiring-engineers/blob/kchitwood-patch-1/vagrant%20install%20successful.png" width="500" height="332" alt="_DSC4652"></a>

Download [Virtual Box](https://download.virtualbox.org/virtualbox/6.0.4/VirtualBox-6.0.4-128413-OSX.dmg)

After Download is completed, double click for virtual box installation wizard to appear.

<img src="https://github.com/kchitwood/hiring-engineers/blob/kchitwood-patch-1/virtual%20box%20install%202.png"></a>

Selcect Defaults, and installation should complete successfully.

<img src="https://github.com/kchitwood/hiring-engineers/blob/kchitwood-patch-1/virtual%20box%20install%20completed.png" width="500" height="332" alt="_DSC4652"></a>

Once Virtual box has completed, run this command from the command line as root to create your vagrantfile.
vagrant init hashicorp/precise64

<img src="https://github.com/kchitwood/hiring-engineers/blob/kchitwood-patch-1/vagrantfile%20creation.png"></a>

Run vagrant up command from the command line, this will build your box.

<img src="https://github.com/kchitwood/hiring-engineers/blob/kchitwood-patch-1/vagrant%20up.png"></a>

Screen Prints for AWS:

<img src="https://github.com/kchitwood/hiring-engineers/blob/kchitwood-patch-1/Launch%20Ec2%20Ubuntu%20AMI.png" width="500" height="332" alt="_DSC4652"></a>

<img src="https://github.com/kchitwood/hiring-engineers/blob/kchitwood-patch-1/Final%20Review%20EC2%20Launch.png" width="500" height="332" alt="_DSC4652"></a>

<img src="https://github.com/kchitwood/hiring-engineers/blob/kchitwood-patch-1/Ec2%20Instance%20Launch.png" width="500" height="332" alt="_DSC4652"></a>

<img src="https://github.com/kchitwood/hiring-engineers/blob/kchitwood-patch-1/EC2%20Image%20running.png" width="500" height="332" alt="_DSC4652"></a>

Screen Prints for Agent installs:

Docker Install-

<img src="https://github.com/kchitwood/hiring-engineers/blob/kchitwood-patch-1/Command%20line%20docker%20install.png" width="500" height="332" alt="_DSC4652"></a>

<img src="https://github.com/kchitwood/hiring-engineers/blob/kchitwood-patch-1/Command%20line%20install%20docker.png" alt="_DSC4652"></a>

<img src="https://github.com/kchitwood/hiring-engineers/blob/kchitwood-patch-1/Docker%20Info.png"></a>

Docker Datadog-agent

<img src="https://github.com/kchitwood/hiring-engineers/blob/kchitwood-patch-1/dd%20inst%20v%20Dock.png" width="500" height="332" alt="_DSC4652"></a>

<img src="https://github.com/kchitwood/hiring-engineers/blob/kchitwood-patch-1/Datadog%20Docker%20container%20running.png"></a>

<img src="https://github.com/kchitwood/hiring-engineers/blob/kchitwood-patch-1/dd-agent%20docker%20dd%20Infra.png"></a>


Ubuntu Curl Download and install-

<img src="https://github.com/kchitwood/hiring-engineers/blob/kchitwood-patch-1/ub%20API%20Key.png"></a>

<img src="https://github.com/kchitwood/hiring-engineers/blob/kchitwood-patch-1/ubuntu%20without%20docker.png"></a>

Ubuntu Vagrant datadog-agent install-

<img src="https://github.com/kchitwood/hiring-engineers/blob/kchitwood-patch-1/dd%20inst%20vbox%20ub.png"></a>

2. Collecting Metrics
  
  2.A Adding Tags: By editing the datadog.yaml, you can create custom tags.

<img src="https://github.com/kchitwood/hiring-engineers/blob/kchitwood-patch-1/creating%20tags%20in%20datadog%20yaml%20.png" width="500" height="332" alt="_DSC4652"></a>

<img src="https://github.com/kchitwood/hiring-engineers/blob/kchitwood-patch-1/Event%20logs%20showing%20tags.png" width="500" height="332" alt="_DSC4652"></a>

<img src="https://github.com/kchitwood/hiring-engineers/blob/kchitwood-patch-1/Infrastructure%20Host%20map.png" width="500" height="332" alt="_DSC4652"></a>

<img src="https://github.com/kchitwood/hiring-engineers/blob/kchitwood-patch-1/Infrastructure%20list%20showing%20tags.png" width="500" height="332" alt="_DSC4652"></a>

  2.B Install MySQL Database: 
  
  You can install mysql from Ubuntu using apt install mysql-server, go to integration page in Datadog UI,
  select MySQL and you will be provided instructions on how to configure your mysql.yaml, add the user and grant permisions for datadog.   
  Once the datadog user is added and permisions granted, it provides some test SQL to insure it is correct.
  
<img src="https://github.com/kchitwood/hiring-engineers/blob/kchitwood-patch-1/Installing%20Mysql%20Ubuntu%20command%20line.png" width="500" height="332" alt="_DSC4652"></a>
 
<img src="https://github.com/kchitwood/hiring-engineers/blob/kchitwood-patch-1/mysql%20command%20line.png" width="500" height="332" alt="_DSC4652"></a>
 
<img src="https://github.com/kchitwood/hiring-engineers/blob/kchitwood-patch-1/Datadog%20mysql%20integration%20page.png" width="500" height="332" alt="_DSC4652"></a>
 
<img src="https://github.com/kchitwood/hiring-engineers/blob/kchitwood-patch-1/mysql%20datadog%20grant.png" width="500" height="332" alt="_DSC4652"></a> 
 
<img src="https://github.com/kchitwood/hiring-engineers/blob/kchitwood-patch-1/Testing%20mysql%20datadog%20user.png" width="500" height="332" alt="_DSC4652"></a>
  
  This mysql.yaml would be used for a standard agent or a Docker agent container install.
  
 <img src="https://github.com/kchitwood/hiring-engineers/blob/kchitwood-patch-1/mysql%20yaml%20config%20file%20for%20docker%20dd-agent.png" width="500" height="332" alt="_DSC4652"></a>
  
  If you use the Docker container for Datadog-agent(dd-agent), you will need to start the Docker container to point to a different mount
  so you can include the custom yaml files.

<img src="https://github.com/kchitwood/hiring-engineers/blob/kchitwood-patch-1/dock%20dd%20yaml%20file.png"></a>


  2.C Create custom Agent Check: 
  You can create custom checks using python code. You will need to create a my_metric.yaml file in the 
  /etc/datadog-agent/conf.d filesystem. This will provide the interval for collection and other custom configurations. Second, you 
  will need to place your python code in a .py file in the /etc/datadog-agent/checks.d filesystem and then restart your agent.
  
<img src="https://github.com/kchitwood/hiring-engineers/blob/kchitwood-patch-1/my_metric.yaml.png" alt="_DSC4652"></a>
 
<img src="https://github.com/kchitwood/hiring-engineers/blob/kchitwood-patch-1/my%20metric%20code.png" width="500" height="332" alt="_DSC4652"></a>
 
Bonus=No, I could not find anything documented that you could change the interval other than the .yaml config file.

3. Visulizing Data
  
  3.A Utilize the Datadog API to create a timeboard that Contains: Use Datadog UI, navigate to the dashboards and select New Dashboard.
  Two options will come up(New Timeboard,New Screenboard). Select the Timeboard option. Start adding graphs to your board as stated below.
  
<img src="https://github.com/kchitwood/hiring-engineers/blob/kchitwood-patch-1/timeboard%20with%203%20metrics%20.png" width="500" height="332" alt="_DSC4652"></a>
  
  3.B Go to Metrics Explorer page in Datadog UI, Select the metric you want to graph, my_metric, and graph over host.
  
<img src="https://github.com/kchitwood/hiring-engineers/blob/kchitwood-patch-1/my_metric%20graph%20over%20host.png" width="500" height="332" alt="_DSC4652"></a>
  
  3.C Go to Monitors section in Datadog UI. Create new monitor and select anomoly type. You can select the metric and the alert.
  
  3.D Create a rollup function applied to sum up all the points for the past hour into one bucket.Go to Managed Monitors in the Datadog
  UI. Edit your the my_metric monitor and create alert conditions to trigger when metric is above and avg over 5mins.
  
<img src="https://github.com/kchitwood/hiring-engineers/blob/kchitwood-patch-1/My_metric%20alert.png" width="500" height="332" alt="_DSC4652"></a>
  
  3.E Snapshot and email of Graph.
  
<img src="https://github.com/kchitwood/hiring-engineers/blob/kchitwood-patch-1/Email%20snapshot%20of%20graph%205m.png" width="500" height="332" alt="_DSC4652"></a>
  
Bonus - When brought to 5min, the anomaly graph sometimes displays not enough data.
  
4. Monitoring Data
  
  4.A,B,C Create New Monitor with thresholds and alerts. In Datadog UI, navigate to monitor. Create new. select metric. 
  Select the metric to monitor, choose from or exclude if needed. Use Avg by for this exercise. Set Alert Conditions to above, on average, 5min. Set alert to 800, set warning at 500. Select notify if data is missing. In Say whats happening section,  you can use variables to define message and the value of the alerts. You can also specifiy who to notify.
   
<img src="https://github.com/kchitwood/hiring-engineers/blob/kchitwood-patch-1/Metric%20Threshold%20800%20500.png" alt="_DSC4652"></a> 
 
<img src="https://github.com/kchitwood/hiring-engineers/blob/kchitwood-patch-1/Metric%20Threshold%20800%20500%20pg2.png" width="500" height="332" alt="_DSC4652"></a>
 
<img src="https://github.com/kchitwood/hiring-engineers/blob/kchitwood-patch-1/Metric%20Threshold%20800%20500%20pg3.png" width="500" height="332" alt="_DSC4652"></a>
 
<img src="https://github.com/kchitwood/hiring-engineers/blob/kchitwood-patch-1/Metric%20Threshold%20800%20500%20pg4.png" alt="_DSC4652"></a>
   
   4.D Screenshot of alert emails:
   
<img src="https://github.com/kchitwood/hiring-engineers/blob/kchitwood-patch-1/alert%20Email.png" width="500" height="332" alt="_DSC4652"></a>
 
<img src="https://github.com/kchitwood/hiring-engineers/blob/kchitwood-patch-1/Email%20test%20warning%20threshold.png" width="500" height="332" alt="_DSC4652"></a>
 
<img src="https://github.com/kchitwood/hiring-engineers/blob/kchitwood-patch-1/Email%20test%20no-data%20threshold.png" width="500" height="332" alt="_DSC4652"></a>
   
  Bonus  In the Datadog UI, go to the Monitors, Manage Downtime, Set schedule for muting alerts.
   
<img src="https://github.com/kchitwood/hiring-engineers/blob/kchitwood-patch-1/Schedule%20weekday%20downtime.png" width="500" height="332" alt="_DSC4652"></a>
 
<img src="https://github.com/kchitwood/hiring-engineers/blob/kchitwood-patch-1/Scheduled%20downtime%20show%20muted%20.png" width="500" height="332" alt="_DSC4652"></a>
 
<img src="https://github.com/kchitwood/hiring-engineers/blob/kchitwood-patch-1/Email%20schedule%20daily%20nightime%20.png" width="500" height="332" alt="_DSC4652"></a>
 
<img src="https://github.com/kchitwood/hiring-engineers/blob/kchitwood-patch-1/Email%20scheduled%20downtime%20started%20weekend.png" width="500" height="332" alt="_DSC4652"></a>
 
<img src="https://github.com/kchitwood/hiring-engineers/blob/kchitwood-patch-1/Email%20scheduled%20downtime%20weekend.png" width="500" height="332" alt="_DSC4652"></a>
   
   5. Collecting APM Data
  
   5.A Create an Flask App and instrument this using Datadogs APM solution:
    First, install python-pip, Flask and ddtrace. Create python script, my_app.py, copied the flask code provided.
   
<img src="https://github.com/kchitwood/hiring-engineers/blob/kchitwood-patch-1/installing%20flask.png" width="500" height="332" alt="_DSC4652"></a>
 
<img src="https://github.com/kchitwood/hiring-engineers/blob/kchitwood-patch-1/installing%20ddtrace.png" width="500" height="332" alt="_DSC4652"></a>
 
<img src="https://github.com/kchitwood/hiring-engineers/blob/kchitwood-patch-1/installing%20python-pip.png" width="500" height="332" alt="_DSC4652"></a> 
   
  Edit the datadog.yaml to configure APM in the agent.
   
<img src="https://github.com/kchitwood/hiring-engineers/blob/kchitwood-patch-1/APM%20config%20in%20datadog%20yaml.png" width="500" height="332" alt="_DSC4652"></a>
   
  Restart the datadog-agent. 
  Execute the scritp using ddtrace-run python my_app.py 
   
<img src="https://github.com/kchitwood/hiring-engineers/blob/kchitwood-patch-1/Running%20my%20APM%20my_app.py.png" width="500" height="332" alt="_DSC4652"></a>
 
<img src="https://github.com/kchitwood/hiring-engineers/blob/kchitwood-patch-1/Flask%20service%20trace%20graphs.png" width="500" height="332" alt="_DSC4652"></a>
 
<img src="https://github.com/kchitwood/hiring-engineers/blob/kchitwood-patch-1/Flask%20service%20map.png" width="500" height="332" alt="_DSC4652"></a>
 
<img src="https://github.com/kchitwood/hiring-engineers/blob/kchitwood-patch-1/Flask%20service%20map%20with%20hover.png" width="500" height="332" alt="_DSC4652"></a>
   
   Bonus: A Service is a set of processes that do the same job. A Resource is an action for a service, such as a select query.
  This is the final Time board with all the metrics and graphs included in the exercise.
   
<img src="https://github.com/kchitwood/hiring-engineers/blob/kchitwood-patch-1/Finished%20Time%20Board.png" width="500" height="332" alt="_DSC4652"></a>
   
   6. Final Question
   
   What is a creative way Datadog should monitor? 
   
  Collect and monitor data for any type of major event, example Super Bowl, that could collect media information, such as streaming, 
  twitter ,facebook and other social media along with tv, cable, satilite services to provide Geospatial type information as how each
  georaphic location is reacting or utilizing such events.
  
  
   
