# Datadog Enterprise Sales Engineer Assignment - Los Angeles

# Setup the Environment

You can utilize any OS/host that you would like to complete this exercise. However, we recommend one of the following approaches:
You can spin up a fresh linux VM via Vagrant or other tools so that you don’t run into any OS or dependency issues. Here are instructions for setting up a Vagrant Ubuntu VM. We strongly recommend using minimum v. 16.04 to avoid dependency issues. You can utilize a Containerized approach with Docker for Linux and our dockerized Datadog Agent image. Then, sign up for Datadog (use “Datadog Recruiting Candidate” in the “Company” field), get the Agent reporting metrics from your local machine.

I downloaded Vagrant 2.2.10 for Mac OSX 64-bit [here.](https://www.vagrantup.com/downloads) I've never used Vagrant so I followed [this](https://learn.hashicorp.com/tutorials/vagrant/getting-started-index?in=vagrant/getting-started) quickstart guide to get up and running. When I'm doing work on a VM, it's always important for me to have backups enabled so I can do a point in time restore if I need to. It's a little different with Vagrant, since you're working locally. I came across exactly what I needed with ```vagrant snapshot``` and everything about saving and restoring snapshots can be found [here.](https://www.vagrantup.com/docs/cli/snapshot)

It's recommended to use Ubuntu 16.04 and the Vagrant box for that is [xenial64.](https://app.vagrantup.com/ubuntu/boxes/xenial64)
To get my new image running I simply needed to run the following commands

    vagrant init ubuntu/xenial64
    vagrant up

Once I had my VM environment setup correctly, I created my Datadog trial (with “Datadog Recruiting Candidate” in the “Company” field)and installed the agent with the documentation provided [here.](https://app.datadoghq.com/signup/agent#ubuntu) All I needed to do was run this command 

     DD_AGENT_MAJOR_VERSION=7 DD_API_KEY=Your API key goes here DD_SITE="datadoghq.com" bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_script.sh)" 
and I was all setup and ready to go. I verified installation with the following command

    $ datadog-agent version
    Agent 7.22.1 - Commit: 6f0f0d5 - Serialization version: v4.40.0 - Go version: go1.13.11



# Collecting Metrics

Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
The documentation I followed for this section can be found [here.](https://docs.datadoghq.com/getting_started/tagging/)
I navigated to ```/etc/datadog-agent/datadog.yaml``` and navigated to @param tags and added the following:
```

#tags:
# -environment:dev
# -project:solutionsengineerassignment

```
I restarted Agent running as a service ```sudo service datadog-agent restart``` For agent usage specific to Ubuntu, I followed the documentation [here.](https://docs.datadoghq.com/agent/basic_agent_usage/ubuntu/?tab=agentv6v7) [This](https://www.datadoghq.com/blog/tagging-best-practices/) blog post is really helpful to understand best practices for tagging your infrastructure and applications. 

 ![Tags](https://github.com/jasondunlap/hiring-engineers/blob/master/DD_tags.png) 

   
Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
I chose to install MySQL database with the following steps
```
$ sudo apt-get update
$ sudo apt-get install mysql-server
$ mysql_secure_installation

```
[This](https://www.datadoghq.com/blog/monitoring-mysql-performance-metrics/) blog post is really helpful to determine which MySQL metrics that you should be monitoring to ensure optimal database performance. 
I followed [these](https://docs.datadoghq.com/integrations/mysql/?tab=host) steps in MySQL so that the Datadog agent can start collecting metrics. 
```

mysql> CREATE USER 'datadog'@'localhost' IDENTIFIED BY 'JasonPW';

mysql -u datadog --password=JASONPW -e "show status" | \
grep Uptime && echo -e "\033[0;32mMySQL user - OK\033[0m" || \
echo -e "\033[0;31mCannot connect to MySQL\033[0m"
# The Agent needs a few privileges to collect metrics. Grant the user the following limited privileges ONLY:
mysql> GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'localhost' WITH MAX_USER_CONNECTIONS 5;
Query OK, 0 rows affected, 1 warning (0.00 sec)

mysql> GRANT PROCESS ON *.* TO 'datadog'@'localhost';
Query OK, 0 rows affected (0.00 sec)

```
After that I updated the configuration file located at ```/etc/datadog-agent/conf.d/mysql.d/conf.yaml```



    init_config:
     
    instances:
    - host: localhost
     user: datadog
     pass: "JasonPW" # replace and update with your password
     port:  3306
     options:
     replication: false
     galera_cluster: true
     extra_status_metrics: true
     extra_innodb_metrics: true
     extra_performance_metrics: true
     schema_size_metrics: false
     disable_innodb_metrics: false

You need to restart the agent ```sudo service datadog-agent restart``` and you can go to Metrics Explorer to view MySQL

![MySQL](https://github.com/jasondunlap/hiring-engineers/blob/master/mysql.png)
![Metrics Explorer](https://github.com/jasondunlap/hiring-engineers/blob/master/metricsexplorer_mysql.png)


Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000. Change your check's collection interval so that it only submits the metric once every 45 seconds.

I went to ```/etc/datadod-agent/checks.d/``` and create the file ```my_metric.py``` which you can see below. 



    #!/usr/bin/python
     
    import random
     
    from datadog_checks.base import AgentCheck
     
    __version__ = '1.0.0'
     
     
    class My_Metric(AgentCheck):
     
    def check(self, instance):
       self.gauge('my_metric', random.randrange(0, 1000),
        tags = ['TAG_KEY:TAG_VALUE'])



**Please Note** It's important to note the specific locations of these two files. It's also important that both the names of the configuration and check files are matching. The YAML file below is located at ```/etc/datadog/conf.d/my_metric.yaml``` 

```

init_config:

instances:
  - min_collection_interval: 45

```

I found this [tutorial](https://docs.datadoghq.com/developers/metrics/agent_metrics_submission/?tab=count) and this [one.](https://datadoghq.dev/summit-training-session/handson/customagentcheck/)
[Writing a Custom Agent Check](https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7) has everything you need to help with the python script. 

Finally, to double check everything is working ok, run ```sudo -u dd-agent -- datadog-agent check my_metric```



    Running Checks
    ==============
     
    my_metric (1.0.0)
    -----------------
      Instance ID: my_metric:5ba864f3937b5bad [OK]
      Configuration Source: file:/etc/datadog-agent/conf.d/my_metric.yaml
      Total Runs: 1
      Metric Samples: Last Run: 1, Total: 1
      Events: Last Run: 0, Total: 0
      Service Checks: Last Run: 0, Total: 0
      Average Execution Time : 0s
      Last Execution Date : 2020-09-30 23:51:30.000000 UTC
      Last Successful Execution Date : 2020-09-30 23:51:30.000000 UTC


   You can go to Metrics > Explore in the Datadog Dashboard and see it works

![My_Metric](https://github.com/jasondunlap/hiring-engineers/blob/master/my_metric.png)

Bonus Question Can you change the collection interval without modifying the Python check file you created?
You can change the following parameter ```min_collection_interval``` to whatever value you want on the ```my_metric.yaml``` You wouldn't need to change anything in the Python script. 

# Visualizing Data
Utilize the Datadog API to create a Timeboard that contains:
Your custom metric scoped over your host.
Any metric from the Integration on your Database with the anomaly function applied.
I found MySQL integrations in Python [here.](https://github.com/DataDog/integrations-core/blob/master/mysql/datadog_checks/mysql/mysql.py) [This](https://www.datadoghq.com/blog/monitoring-mysql-performance-metrics/) blog post was very helpful as well. 
Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard. 

Prior to running the Python script, it's necessary to complete a few steps to setup your environment on your Vagrant box. The first thing that I need to is install [pip.](https://pip.pypa.io/en/stable/) pip is the Python package installer which allows people to install verious different packages from the [python package index.](https://pypi.org) Once pip is installed, we will use it to install the Datadog Python Library.
1. ```apt-get update```
2. ```curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"```
3. ```python3 get-pip.py```
4. Verify pip is installed correctly ```pip --version``` ```pip 20.2.3 from /home/vagrant/.local/lib/python3.5/site-packages/pip (python 3.5)```
5. ```pip install datadog```

Once all the steps above are completed, you execute the Python script ```python3 datadogdashboard.py```



    from datadog import initialize, api
     
    options = {
    'api_key': 'API Key Hidden',
    'app_key': 'App Key Hidden'
    }
    initialize(**options)
     
    title= "Visualizing Data"
    widgets= [
    {
    "definition":{
    "type":"timeseries",
    "requests": [
    {
      
      "q":"avg:my_metric{*}"
       }
      ],
      "title":"my_metric_average"
     }
       },
    {
        "definition":{
        "type":"timeseries",
        "requests":[
            {
       
      
                "q":"anomalies(avg:mysql.performance.cpu_time{*},'basic',2)"
            }
        ],
        "title":"anomolies cpu function"
       }
    },
     {
        "definition":{
        "type":"timeseries",
        "requests":[
            {
       
                "q":"avg:my_metric{*}.rollup(sum,3600)"
            }
        ],
        "title":"my_metric rollup"
    }
     }
    ]
     
    layout_type = 'ordered'
    description = 'the dashboard exercise'
    is_read_only = True
    notify_list = ['dunlap.jason@gmail.com']
     
     
    api.Dashboard.create(title=title,
                     widgets=widgets,
                     layout_type=layout_type,
                     description=description,
                     is_read_only=is_read_only,
                     notify_list=notify_list)


The code example for the Python script is located [here](https://docs.datadoghq.com/api/v1/dashboards/)

I created my Application and API keys from the Datadog dashboard, Under Integrations > [API's.](https://app.datadoghq.com/account/settings#api) **Please note** Be careful not to accidentally commit your API keys or any other credentials to Github. 

Once this is created, access the Dashboard from your Dashboard List in the UI:

![Dashboard List](https://github.com/jasondunlap/hiring-engineers/blob/master/data.png)

Set the Timeboard's timeframe to the past 5 minutes
Take a snapshot of this graph and use the @ notation to send it to yourself.
![?](https://github.com/jasondunlap/hiring-engineers/blob/master/anomolies_email.png)
Bonus Question: What is the Anomaly graph displaying?
The anamoly graph is displays changes in value from previous patterns. You can see those changes in red. 

# Monitoring Data
Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

Warning threshold of 500
Alerting threshold of 800
![800500](https://github.com/jasondunlap/hiring-engineers/blob/master/800_500.png)
And also ensure that it will notify you if there is No Data for this query over the past 10m.
Please configure the monitor’s message so that it will:

Send you an email whenever the monitor triggers.
Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.

![MySQL](https://github.com/jasondunlap/hiring-engineers/blob/master/warn.png)
![800](https://github.com/jasondunlap/hiring-engineers/blob/master/800.png)
![No Data](https://github.com/jasondunlap/hiring-engineers/blob/master/nodata.png)


Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

One that silences it from 7pm to 9am daily on M-F,
And one that silences it all day on Sat-Sun.
![downtime1](https://github.com/jasondunlap/hiring-engineers/blob/master/downtime1.png)
![downtime2](https://github.com/jasondunlap/hiring-engineers/blob/master/downtime2.png)
![downtime3](https://github.com/jasondunlap/hiring-engineers/blob/master/downtime3.png)
![weekend1](https://github.com/jasondunlap/hiring-engineers/blob/master/weekenddowntime1.png)
![weekend2](https://github.com/jasondunlap/hiring-engineers/blob/master/weekenddowntime2.png)
![weekend3](https://github.com/jasondunlap/hiring-engineers/blob/master/weekenddowntime3.png)
Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.
![weekend](https://github.com/jasondunlap/hiring-engineers/blob/master/weekenddowntime4.png)
![weekend](https://github.com/jasondunlap/hiring-engineers/blob/master/downtime4.png)

# Collecting APM Data

If you're new to Application Performance Monitoring, I would highly recommend going [here](https://docs.datadoghq.com/tracing/visualization/) to familiarize yourself with APM terminology. Also, it's important to go [here](https://app.datadoghq.com/apm/intro) for the Datadog APM introduction. There is an introduction to APM video along with all of the documentation necessary to complete this section. 

Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:
Getting [started](https://app.datadoghq.com/apm/docs?architecture=host-based) only takes five minutes and your configuration snippet is created dynamically on the page. 

Let's first download```pip install ddtrace``` and ```pip install flask```on our Vagrant host.

The following commmand starts the application

     sudo  DD_SERVICE="test" DD_ENV="dev" DD_LOGS_INJECTION=true DD_PROFILING_ENABLED=true ddtrace-run python3 flaskapp.py 
 
  This shows the app is running

    vagrant@ubuntu-xenial:/etc/datadog-agent/checks.d$ ddtrace-run python3 flaskapp.py 
    * Serving Flask app "flaskapp" (lazy loading)
    * Environment: production
    WARNING: This is a development server. Do not use it in a production deployment.
    Use a production WSGI server instead.
    * Debug mode: off
    INFO:werkzeug: * Running on http://0.0.0.0:5050/ (Press CTRL+C to quit)
    2020-10-04 22:40:24,506 - werkzeug - INFO -  * Running on http://0.0.0.0:5050/ (Press CTRL+C to quit) 

  Here is the file

    from flask import Flask
    import logging
    import sys
     
    # Have flask use stdout as the logger
    main_logger = logging.getLogger()
    main_logger.setLevel(logging.DEBUG)
    c = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    c.setFormatter(formatter)
    main_logger.addHandler(c)
     
    app = Flask(__name__)
     
    @app.route('/')
    def api_entry():
    return 'Entrypoint to the Application'
     
    @app.route('/api/apm')
    def apm_endpoint():
    return 'Getting APM Started'
     
    @app.route('/api/trace')
    def trace_endpoint():
    return 'Posting Traces'
     
    if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5050')   

Note: Using both ddtrace-run and manually inserting the Middleware has been known to cause issues. Please only use one or the other.
I used ddtrace and the documentation I followed for tracing python applications is [here.](https://docs.datadoghq.com/tracing/setup/python/) If you're looking for more advanced usage of ddtrace, please look at this [link.](https://ddtrace.readthedocs.io/en/stable/advanced_usage.html#ddtracerun)

One last thing I needed to do is send some traffic to the various endpoints such as ```/api/apm``` and ```api/trace``` We know our application is running at ```http://0.0.0.0:5050/``` so we can 

      curl http://0.0.0.0:5050/
      curl http://0.0.0.0:5050/api/apm
      curl http://0.0.0.0:5050/api/trace

You can see the requests in real time from your terminal window
     

     2020-10-07 22:38:44,875 - ddtrace.tracer - DEBUG - 
      name flask.request
        id 666318657609852178
    trace_id 1098856669353764473
    parent_id None
    service flaskapm-app
    resource GET /
      type web
     start 1602110324.873107
       end 1602110324.875369
    duration 0.002262s
     error 0
      tags 
           env:dev
           flask.endpoint:api_entry
           flask.url_rule:/
           flask.version:1.1.2
           http.method:GET
           http.status_code:200
           http.url:http://0.0.0.0:5050/
           runtime-id:d10bd7f1adbe4bc895c5f33e94c7be23
           version:1.1

Bonus Question: What is the difference between a Service and a Resource?
Service is a collection of resources such as DB queries and a resource is part of a service such as an endpoint.

Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.
[link to dashboard.](https://p.datadoghq.com/sb/x6w2dmyiho29dvdu-0aed1950a4bf74c63ee271b2e42474a7
)
![app_infra](https://github.com/jasondunlap/hiring-engineers/blob/master/apm_infra.png)
![infra](https://github.com/jasondunlap/hiring-engineers/blob/master/apm_services.png)
![trace](https://github.com/jasondunlap/hiring-engineers/blob/master/apm_trace.png)
![profile](https://github.com/jasondunlap/hiring-engineers/blob/master/apm_profiles.png)
![analytics](https://github.com/jasondunlap/hiring-engineers/blob/master/appanalytics.png)
![cpu](https://github.com/jasondunlap/hiring-engineers/blob/master/infras.png)
Please include your fully instrumented app in your submission, as well.

# Final Question
Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?

Personally, I would like to build a plant monitoring application on my Rasberry PI. It would be cool to monitor the app using Datadog. I would like to see Datadog used for Covid-19 contact tracing apps too. I would also like to see more cloud partnerships like the recently announced one with Azure :)




