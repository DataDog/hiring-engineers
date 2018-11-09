Your answers to the questions go here.
# Solution Engineer Answers
# by John Meagher

### Prerequisites - Setup the environment

  To begin this project I installed vagrant on PC. Using the windows 64 bit installer from the vagrant [downloads page](https://www.vagrantup.com/downloads.html). I used the default options for the installation. Once installed you can use vagrant commands in the command line. You can add prebuilt vagrant machines to your system by using the `vagrant box add <url>` command. The specific box that I used was "https://cloud-images.ubuntu.com/xenial/current/xenial-server-cloudimg-amd64-vagrant.box" which I found on vagrantbox.es. It is a ubuntu 16.04 linux box. Once the box is added to your system you can bring it online by using the `vagrant up` command. After about a minute or so your vm will be online at which point you you can access it using `vagrant ssh <vm name>`. I kept my VM named default in vagrant. This following screenshot shows my setup coming online.
![vagrant](https://github.com/jmeagheriv/hiring-engineers/blob/master/vagrant.JPG)



### Collecting Metrics
  I went to the datadoghq.com website and signed up for my own account following the instruction prompts. On the first login I followed the getting started instructions to install the agent. It is very easy to get the agent started as there is a one step install command for ubuntu. This screenshot shows the final output of the agent installation finishing up and begin reporting.

![agent](https://github.com/jmeagheriv/hiring-engineers/blob/master/agent%20installed.JPG)

  Once I ran the command on my vm, metrics started reporting to the dashboard. The default metrics report on datadog itself as well as system outputs such as cpu.idle time, ntp offset, and system disk used. The agent configuration file is the /etc/datadog-agent/datadog.yaml. Here you can set special configuration for your agent and add things like host tags to identify this specific agent.

![agenttags](https://github.com/jmeagheriv/hiring-engineers/blob/master/datadogtags.JPG)

  After changing this file the agent needs to be restarted with `systemctl restart datadog-agent`. Once it's restarted you can see the tags appear in your dashboard. Here are my tags showing in the dashboard.

![tagged host](https://github.com/jmeagheriv/hiring-engineers/blob/master/HostTagged.JPG)

  The next step is to install the database. I went with mongodb community edition, the instrutions are [here](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/). Once the install from `apt-get` command finished, mongodb was started with this `sudo service mongod start` command. To integrate mongodb with datadog you need to run go to the configuration section of the mongodb integration. This section adds a datadog user to mongodb, and configures the mongodb server in the conf.d/mongo.d/conf.yaml file. You can check the status of integrations on your system using the `datadog-agent checkconfig` command. My output for this command is [here](https://github.com/jmeagheriv/hiring-engineers/blob/master/checkconfig.txt).

![ddusermongo](https://github.com/jmeagheriv/hiring-engineers/blob/master/MongoDB_DDuser%20setup.JPG?raw=true)

  To create a custom agent check there are two parts. The first part is a yaml file which needs to be located in the /etc/datadog-agent/conf.d to standardize this all of the other agent checks are located inside of their own subdirectories but datadog-agent is able to read any yaml file as long as it is within the conf.d directory. I created a checkvalue.d subdirectory for my [checkvalue.yaml](https://github.com/jmeagheriv/hiring-engineers/blob/master/checkvalue.yaml) file. The second portion of the custom agent check is the actual script the agent will run to perform the check. This file must be located in /etc/datadog-agent/checks.d, that is where my [checkvalues.py](https://github.com/jmeagheriv/hiring-engineers/blob/master/checkvalues.py) file is located. This file will by default be run by the agent every 15s and report the result to datadog. There are two methods to change this 15s value. You can change the script or the yaml file. In the script you can include a line that waits for before submitting the metric or you can change the yaml file to contain a min_collection_interval which is what I went with. 

### Visualizing Data
  There are two ways to create timeboards. For this challenge I am using the API, for which documentation can be found [here](https://docs.datadoghq.com/api/?lang=python#overview). The specific section of the documentation that I used to create my timeboard.py file is the "Graph Snapshot" section. I was a bit confused that first time I read it as I thought that it wouldn't be a timeboard but would rather take a single snapshot of a graph. My [timeboard.py](https://github.com/jmeagheriv/hiring-engineers/blob/master/timeboard.py) file creates 3 graphs. First of which displays my_metric scoped. The second is the concurrent users of mongodb with an anomaly function applied. The third graph is a rollup function of my_metric over an hour. Here is the timeboard that is created when the timeboard.py script is run on my vm. 
![metric](https://github.com/jmeagheriv/hiring-engineers/blob/master/Rollup.JPG)
In order to change the timeframe for the timeboard you can select a value from the dropdown menu. However the shortest timeframe is 1 hour. In order to display short time frames you can click and drag on the graph itself and it will change the timeframe for all graphs on the timeboard. When you select a shorter time frame you are able to send a snapshot of it via email notification by tagging a person in the comment section.
![metric_email](https://github.com/jmeagheriv/John_Meagher_Solution_Engineer/blob/master/MetricEmail.JPG)
![metric5m](https://github.com/jmeagheriv/hiring-engineers/blob/master/5m%20interval.JPG)
  In this picture, the timeframe is only 5 minutes. The 5 minute interval selected doesnt encapsulate the rollup function value. The way this rollup function is configured, once per hour it will display the sum of my_metric over the course of that hour. If timeframe doesn't contain the moment the value is added up it won't show on the graph. The second graph also doesn't seem very interesting despite having the anomaly function applied. The graph will show if there are an unusual amount of connections. If I were to create a bunch of mongodb sessions concurrently and end them abruptly, the anomaly graph will color in that spike red. If I left those sessions running for a long time eventually the graph will normalize that number of connections and it will no longer be red. It uses the history of the metric to predict the future values. If the value is outside of the expected range it will color it red on the graph. The first graph to me is actually the least interesting since it is a simple time series graph so it will graph the values of the metric without doing anything special. 

### Monitoring Data

  To create the monitor I felt it was best to use the dashboard. Under the Monitors drop down I selected 'New Monitor' with monitor type "Metric".
![dropdownMonitor](https://github.com/jmeagheriv/John_Meagher_Solution_Engineer/blob/master/Monitor%20Dropdown.JPG)
  This brings up the actual creation of the monitor. You can selection a detection method, define the metric, set the alert condtions, put in some information as to what this monitor does, and notify team members when the monitor is triggered. The next screenshot shows the monitor I have configured for my metric. It will trigger if my_metric is over 500 or there is no data from my_metric and it will alert for values over 800. ![MetricMonitor](https://github.com/jmeagheriv/hiring-engineers/blob/master/Monitor.jpg)
  In the 4th section I have set up the messages sent for the monitor. This section uses markdown so I able to put in conditions. The conditions will change the message the monitor displays depending on its status. I have also set up the monitor to notify me when it gets triggered. You can also check on triggered monitors from the dashboard in the "Triggered Monitors" dropdown.
![monitor triggered email](https://github.com/jmeagheriv/hiring-engineers/blob/master/MonitorEmail.JPG)
![MetricMonitor2](https://github.com/jmeagheriv/hiring-engineers/blob/master/Monitor2.JPG)
  Some monitors might only be significant during certain time periods so you are able to schedule downtime in the "Manage Downtime" dropdown section. I have set up downtime so my monitor will only trigger during business hours. The downtime starts each weekday at 7pm until 9am the next day. I have also configured the monitor to be off on weekends. When downtime is scheduled you can include a notification for team members. The following screenshots show the different downtimes I have created as well as the email notification that can be configured.
![M-F](https://github.com/jmeagheriv/hiring-engineers/blob/master/M-F%20Downtime.JPG)
![Weekends](https://github.com/jmeagheriv/hiring-engineers/blob/master/Sat-Sun%20Downtime.JPG)
![downtime](https://github.com/jmeagheriv/John_Meagher_Solution_Engineer/blob/master/DowntimeEmail.JPG)
  

### Collecting APM Data
  In order to actually collect APM data, we first need an application. The example application is flask. In order for the application in the example to work I needed to first install flask. I was able to do so using pip, specifically `pip install flask`. This will allow for the flask_app.py in the example to import flask. With an application installed we also need to trace it. Datadog uses a seperate utility for APM data. In order to get this functionality we need to install dd-trace. Fortunately it is also installed with pip so `pip install dd-trace`. Once dd-trace is installed we can instrument the application. This can be done by running the application through dd-trace using `dd-trace-run python flask_app.py`. This will run the application in one window. In order to pick up traces we need to make api calls in another window. The following screenshot shows the instrumented app and the second window with api calls to this application.
![apm4](https://github.com/jmeagheriv/hiring-engineers/blob/master/APM_int.JPG) 

  Once we have collected some traces we can see them in the dashboard. The traces can be seen on the APM dropdown in the trace list. Here are my collected traces in the dashboard.
 ![apm1](https://github.com/jmeagheriv/hiring-engineers/blob/master/APM.JPG)
  On the traces list you will come across services and resources. The line between them can be blurry. This is because a resouce is a query to service. A service is a set of processes that make up a feature. More information on this tab and the other information on it can be found [here](https://help.datadoghq.com/hc/en-us/articles/115000702546-What-is-the-Difference-Between-Type-Service-Resource-and-Name-). Now that we have APM data in the traces tab we can display traces on the timeboard that we created earlier. To do this you can navigate to the timeboard in the "Dashboard List" and select the "add a graph" box. Choose your trace in the metric box and the type of graph that you want. I went with a time series of trace.flask.request.hits. See that graph in the below screencap
 ![apm3](https://github.com/jmeagheriv/hiring-engineers/blob/master/APM_Dashboard_update.JPG)
 

### Final Question

I work on cloud infrastructure for a telecommunications company. One of the interesting things with telecommunication applications is that there is a global standard for mobile systems. This standard makes the inputs and outputs of the radio functions the same across countries and companies. Each function has set inputs and outputs that are the same across all networks. Which is nice for cross compatibility. However when it comes to monitoring these systems, the differences in the applications become very clear. Every application has its own unique infrastructure, hosted on different hardwares, using different processes, different databases but ultimately giving the same outputs. Integrating in datadog would be very helpful to untangle this sort of mess. 




