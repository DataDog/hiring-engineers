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

I have experience with creating monitors in Zabbix so this part was pretty straight forward and easier for me than I expected. Since it was all gui work here are all the screencaps. 
![MetricMonitor](https://github.com/jmeagheriv/hiring-engineers/blob/master/Monitor.jpg)
![MetricMonitor2](https://github.com/jmeagheriv/hiring-engineers/blob/master/Monitor2.JPG)
![monitor triggered email](https://github.com/jmeagheriv/hiring-engineers/blob/master/MonitorEmail.JPG)

### Monitoring Data bonus: Downtime scheduled

![M-F](https://github.com/jmeagheriv/hiring-engineers/blob/master/M-F%20Downtime.JPG)
![Weekends](https://github.com/jmeagheriv/hiring-engineers/blob/master/Sat-Sun%20Downtime.JPG)

### Collecting APM Data

I installed the ddtrace and flask using pip. `pip install ddtrace` and `pip install flask` respectively. Using the `ddtrace-run python flask_app.py` command on the provided file I had the flask app running with datadog tracing the app. I opened a second window and made the api calls as well as few that I knew would fail. I updated the metric dashboard from the visualizing data section. The APM_int screen cap was taken the next day from the others so the data doesn't match up. While researching the bonus question I found this [link](https://help.datadoghq.com/hc/en-us/articles/115000702546-What-is-the-Difference-Between-Type-Service-Resource-and-Name-) that specifically answers the question. A service is set of processes that make a feature and resource is a single query to a  service
![apm1](https://github.com/jmeagheriv/hiring-engineers/blob/master/APM.JPG)
![apm2](https://github.com/jmeagheriv/hiring-engineers/blob/master/APM_Trace_PostingTraces.JPG)
![apm3](https://github.com/jmeagheriv/hiring-engineers/blob/master/APM_Dashboard_update.JPG)
![apm4](https://github.com/jmeagheriv/hiring-engineers/blob/master/APM_int.JPG) 

### Final Question

I work on cloud infrastructure for a telecommunications company. One of the interesting things with telecommunication applications is that there is a global standard for mobile systems. This standard makes the inputs and outputs of the radio functions the same across countries and companies. Each function has set inputs and outputs that are the same across all networks. Which is nice for cross compatibility. However when it comes to monitoring these systems, the differences in the applications become very clear. Every application has its own unique infrastructure, hosted on different hardwares, using different processes, different databases but ultimately giving the same outputs. Integrating in datadog would be very helpful to untangle this sort of mess. 




