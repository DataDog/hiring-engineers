Your answers to the questions go here.

# **Prerequisites - Setting up the environment:**
Create a virtual box using Vagrant. Defalt vagrant setup uses "hashicorp/precise64" which is a standard Ubuntu 12.04. However, the latest MongoDb community ediition requires a higher version of Ubuntu so I used an "ubuntu/trusty64" box instead.  I kept the example of port forwarding. This is my Vagrantfile:

    # All Vagrant configuration is done below. The "2" in Vagrant.configure
    # configures the configuration version (we support older styles for
    # backwards compatibility). Please don't change it unless you know what
    # you're doing.
    Vagrant.configure("2") do |config|
       config.vm.box = "ubuntu/trusty64"
       config.vm.provision "shell", path: "bootstrap.sh"
       config.vm.network :forwarded_port, guest: 80, host: 4567
       config.vm.network "public_network"
    end

I wanted to ensure that the Apache, the Datadog Agent and mongo were installed on the box so I added both to my startup bootstrap script. The install required apt-transport-https o I added that as well. Here is my bootstrap script:


    echo "provision"
    apt-get update
    apt-get install -y apache2
    if ! [ -L /var/www ]; then
      rm -rf /var/www
      ln -fs /vagrant /var/www
    fi
    apt-get install python-pip
    apt-get install apt-transport-https
    DD_API_KEY=b2a09e1d3eebae34b2fa02e37ee824e8 bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
    apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4
    echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/4.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.0.list
    apt-get update
    sudo apt-get install -y mongodb-org

# Collecting Metrics:
## Adding Tags - Virtual
First I had to change the permisisons of the datadog.yaml file so that I could add the tags
  sudo chmod a+rw datadog.yaml
Next I added the tags to the file:
  ![VM-tag](https://github.com/sddangelo/hiring-engineers/blob/solutions-engineer/CollectingMetrics-AddTagsToVMHostConfigFile.png)
  ![VM-host](https://github.com/sddangelo/hiring-engineers/blob/solutions-engineer/CollectingMetrics-AddTagsToHostUI-virtual.png)
https://app.datadoghq.com/infrastructure/map?host=714118764&fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=availability-zone&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=true&palette=green_to_orange&paletteflip=false&node_type=host&app=(no-namespace)  
  
## Adding Tags - Local (Windows)
I also added a tag to the datadog.yaml file on my pc.
  ![Local-tag](https://github.com/sddangelo/hiring-engineers/blob/solutions-engineer/CollectingMetrics-AddTagsToLocalHostConfigFile.png)
  ![Local-host](https://github.com/sddangelo/hiring-engineers/blob/solutions-engineer/CollectingMetrics-AddTagsToHostUI-Local.png)
https://app.datadoghq.com/infrastructure/map?host=713823022&fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=availability-zone&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=true&palette=green_to_orange&paletteflip=false&node_type=host&app=(no-namespace)

## Install a Database (virtual)
Mongo was intalled in the bootstrap so just need to add an admin user and make config changes. 
First add the admin user. 
Start the admin shell: mongo. 
Use the admin database: use admin.
Add the admin user with the correct priviledges:

               db.createUser({
                   "user":"datadog",
                    "pwd": "datadog",
                    "roles" : [
                         {role: 'userAdminAnyDatabase', db: 'admin' },
                         {role: 'clusterMonitor', db: 'admin'},
                         {role: 'read', db: 'local' },
                            "readWriteAnyDatabase"]
                 })

Now we need to configure the mongo database to turn security authorization to enabled and to change the bindIP so that the connections will work. First we need to change the permissions on the mongod.conf file so that we can edit. 
Then we change the following lines:

      Add: 
        security:
          authorization:enabled
      Change:
        bindIP=0.0.0.0
Next we need to configure datadog to recognize Mongo. First we need to change the permissions on the conf.d/mongo.d directory so that we can copy the example conf.yaml.example file to conf.yaml. Then we edit the connection string to connect to admin with the admin user. 

        mongodb://datadog:datadog@vagrant-ubuntu-trusty-64:27017/admin

Next we restart the mongod service (sudo service mongod restart) to pick up the mongo changes.

Then we restart the datadog agent (sudo serivce datadog-agent restart) to pick up the agent changes.

Run a check to ensure that everything is working as expected and that datadog recognizes mongo by running: (sudo datadog-agent status). We should see mongo under the Collector section without any errors. Made the same corresponding changes to the Windows configuration after intall. Also used insertMany to insert documens into data into the database for each host.

## Create a custom agent
Two files must be created for a custom agent: mycheck.py which is the actual custom check and mycheck.yaml which is the config file for that check. I installed the check in both windows (base datadog directory- \ProgramData\Datadog\) and my virtual box (base datadog directory - /etc/datadog-agent). 

This is mycheck.py. It goes in checks.d directory under the datadog files.

      import random
      # the following try/except block will make the custom check compatible with any Agent version
      try:
           # first, try to import the base class from old versions of the Agent...
         from checks import AgentCheck
      except ImportError:
           # ...if the above failed, the check is running in Agent version 6 or later
         from datadog_checks.checks import AgentCheck
      # content of the special variable __version__ will be shown in the Agent status page
      __version__ = "1.0.0"

      class MyMetricCheck(AgentCheck):
      def check(self, instance):
        self.gauge('my_metric', random.randint(500,1000))

Test the custom check by running: sudo datadog-agent check mycheck / C:\Program Files\Datadog\Datadog Agent\embedded\agent.exe check mycheck. Should see that it shows under Running Checks without any error. If no errors, then restart the agent so that the new check can be picked up by the agent. 


This is mycheck.yaml. It goes in conf.d directory under the datadog files.

      init_config:
        -min_collection_interval: 45
  
      instances: [{}] 


BONUS QUESTION: The collection interverval is changed in the config file of the custom agent (mycheck.yaml)


# Visualizing Data:

## Create a Timeboard using the API
To build the timeboard, I first created dashboard graphs for each of the three difference scenarios to build out what I thought it shoudl look like. Then I switched to the JSON tab to get the actual query that I could use for the API call. I then used the sample code from the API documentation as a starting point and filled everything in. This is the python file to build the api: CreateTimeboard.py

    import sys, json, base64, requests, urllib,time

    from datadog import initialize, api

    uri_base = 'https://api.datadoghq.com/api/'

    options = {'api_key': 'b2a09e1d3eebae34b2fa02e37ee824e8',
              'app_key': 'b5df64de9f718407e456520074814c859c61404b'}

    initialize(**options)

   
    title = "My Timeboard"
    description = "An informative timeboard."
    graphs = [{
        "definition": {
            "events": [],
            "requests": [
                {"q": "avg:system.mem.free{*}"}
            ],
            "viz": "timeseries"},
        "title": "Average Memory Free"},
         {"definition": {
            "events": [],
            "requests": [
                {"q": "avg:my_metric{host:vagrant-ubuntu-trusty-64}"}],
            "viz": "timeseries"},
         "title": "mymetric"},
         {"definition": {
            "events": [],
            "requests": [
                {"q": "avg:my_metric{host:vagrant-ubuntu-trusty-64}.rollup(sum, 3600)"}],
            "viz": "query_value"},
         "title": "Rollup of mymetric - last hour"},
         {"definition": {
            "events": [],
            "requests": [
                {"q": "anomalies(avg:mongodb.metrics.document.insertedps{host:DESKTOP-ID5D6FG}, 'basic', 3)"}],
            "viz": "timeseries"},
         "title": "Anomolies of Documents inserted per second"}]

    template_variables = [{
        "name": "host1",
        "prefix": "host",
        "default": "host:my-host"
    }]

    read_only = True

    try:
      msg = api.Timeboard.create(title=title,
                         description=description,
                         graphs=graphs,
                         template_variables=template_variables,
                         read_only=read_only)
      print(msg)
  
    except Exception as e:
       print(e)

This is the dashboard:
![timeboard](https://github.com/sddangelo/hiring-engineers/blob/solutions-engineer/Visualizing%20Data%20-%20The%20Timeboard.png)

This is the dashboard link:
https://app.datadoghq.com/dash/1010026/my-timeboard?tile_size=m&page=0&is_auto=false&from_ts=1544077800000&to_ts=1544164200000&live=true

## This is the snapshot of the 5 minute timeframe. 
To get below 1hour you must click and drag on a graph for a 5 minute time period. To get the snapshot and send it, click on the camera of the graph and in the comment section use the @mention functionality to select the person to send it to.
![5Min](https://github.com/sddangelo/hiring-engineers/blob/solutions-engineer/Visualizing%20Data%20-%20snapshot.png)

## Bonus Question
Anomoly graph is displaying the standard deviation from the norm for documents inserted per second. 
The bounds for the deviation is set to 2 and the type is basic. 
The Basic type uses simple lagging rolling quantile computation to determine the range of expected values, b
The bounds of 2 will flag anything that is 2 times or more the normal deviation. 

# Monitoring Data:
## Ceate a new Metric Montior
This is the setup for the new monitor:
![monitor](https://github.com/sddangelo/hiring-engineers/blob/solutions-engineer/MonitoringData-NewMonitorSetup.png)

This is the screen shot of the alert:
![Alert](https://github.com/sddangelo/hiring-engineers/blob/solutions-engineer/Visualizing%20Data%20-%20Alert.png)

This is the link to the Monitor:
https://app.datadoghq.com/monitors#7429019/edit

## Schedule Downtime 
Because the work week and weekend downtimes are different, we need to have two different downtimes scheduled. Each gets their own messages. 

### This is for the weekend downtime:
https://app.datadoghq.com/monitors#downtime?id=430788410
![monitor](https://github.com/sddangelo/hiring-engineers/blob/solutions-engineer/MonitoringData-DownTimeWeekendSetup.png)
![mailweekend](https://github.com/sddangelo/hiring-engineers/blob/solutions-engineer/Visualizing%20Data%20-%20Weekends%20Downtime%20Notification.png)

### This is for the workweek downtime:
https://app.datadoghq.com/monitors#downtime?id=431699277
![monitor](https://github.com/sddangelo/hiring-engineers/blob/solutions-engineer/MonitoringData-DownTimeWorkWeekSetup.png)
![mailworkweek](https://github.com/sddangelo/hiring-engineers/blob/solutions-engineer/Visualizing%20Data%20-%20WorkDays%20Downtime%20Notification.png)



# Collection APM Data:
## Instrument an application
I did not use ddtrace-run as I wanted to manually configure the traces via the wrap method. At first, I could see that traces were being created but I was not seeing them in the agent. After turning on debug, I was able to determine that my traces were being "dropped" with this error:
      2018-12-06 20:27:13 ERROR (api.go:249) - dropping trace reason: invalid span (SpanID:8565060984642929983): span.normalize: durations need to be strictly positive (debug for more info), [servi...  

After researching, I figured out that some of the other flask calls as part of the scan did not take any time (0 duration). To fix this issue, I added some slight "sleep" time to the calls and this fixed the issue.

My instrumented app: flaskapp.py
    import time # Need this for sleep statements.
    import logging
    import json_log_formatter
    import sys

    from flask import Flask
    from ddtrace import tracer
    from ddtrace import config
    config.flask['distributed_tracing_enabled']=False
    config.flask['trace_signals']=False
    config.flask['service_name']='flask'
    from ddtrace.contrib.flask import TraceMiddleware

    # Configuring Datadog tracer
    app = Flask(__name__)
    traced_app = TraceMiddleware(app, tracer, service="flask", distributed_tracing=False)

    # Have flask use stdout as the logger
    main_logger = logging.getLogger()
    main_logger.setLevel(logging.DEBUG)
    c = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    c.setFormatter(formatter)
    main_logger.addHandler(c)

    @tracer.wrap(name='api_entry', service='flask')    
    def log_api_entry():
        time.sleep(0.01)
        return 'Entrypoint to the Application'

    @tracer.wrap(name='apm_endpoint', service='flask')    
    def log_apm_endpoint():
        time.sleep(0.01)
        return 'Getting APM Started'
    
    @tracer.wrap(name='apm_endpoint', service='flask')    
    def log_trace_endpoint():
        time.sleep(0.01)
        return 'Posting Traces'

    @app.route('/')
    def api_entry():
        time.sleep(0.02);
        msg = log_api_entry()
        return msg

    @app.route('/api/apm')
    def apm_endpoint():
        time.sleep(0.02);
        msg = log_apm_endpoint()
        return msg

    @app.route('/api/trace')
    def trace_endpoint():
        time.sleep(0.02);
        msg = log_trace_endpoint()
        return msg

## Dashboard of APM Trace
To create a graph with the APM data, I first created a timeseries graph. I seleced APM Events and then linked on the link to go to Trace Serach & Analytics. Next I cllcked on my serivce (flask) and the APM graphs appear. I selected the Export to Timeboard link for "Total Request" and it created an APM graph for me. I added a hostmap graph as well based on the Datadog.Trace_Agent.Trace_Writer over hosts metric. This is my dashboard:
![apmdb](https://github.com/sddangelo/hiring-engineers/blob/solutions-engineer/Collecting%20APM%20Data.png)
https://app.datadoghq.com/dash/1013141/apm-dashboard?tile_size=m&page=0&is_auto=false&from_ts=1544162460000&to_ts=1544166060000&live=true


## Bonus Question
A "Service" is the name of a set of processes that work together to provide a feature set. 
These services are defined by the user when instrumenting their application with Datadog. 

A "Resource" is a particular query to a service. For a web application, some examples might be a canonical URL like /user/home or a handler function like web.user.home (often referred to as "routes" in MVC frameworks). For a SQL database, a resource would be the SQL of the query itself like select * from users where id = ? The Tracing backend can track thousands (not millions or billions) of unique resources per service, so resources should be grouped together under a canonical name, like /user/home rather than have /user/home?id=100 and /user/home?id=200 as separate resources.
These resources can be found after clicking on a particular service. 

# Bonus Questions:
I would use Datadog to monitor the locations of people who view a particular instagram page so that we can tell which pages pull the most internation views.

