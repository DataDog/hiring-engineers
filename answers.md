
## Prerequisites - Setup the Environment

### Environment
* OS: macOS Catalina 10.15.16
    * Vagrant 2.2.15
    * Ubuntu 18.04
    * MySQL DB 14.14

#### VM Setup

For the initial setup I followed the recommendations from the instructions of the technical exercise and spanned up fresh linux VM via Vagrant. 

First I downloaded [Vagrant](https://www.vagrantup.com/downloads)
After running the installation package I followed the steps of the vagrant installer: 
![vagrant install](img/vagrant.png)

After the successful vagrant installation in the terminal I ran command `vagrant init hashicorp/bionic64` - this creates a basic Ubuntu 64 bit box that should be sufficient for running the Datadog Agent and completing the technical exercise. 

Next I started the environment by running command `vagrant up` 

![vagrant init, vagrant up](img/vagrant-init.png)

### Agent Installation

Then it was time to install the Datadog Agent on my new environment. 

On the https://docs.datadoghq.com/agent/ page I selected the platform where I would run the Agent, in my case I chose Ubuntu.  There I found a link to installation instructions. 

By using an easy one-step install command I was able to successfully install the Agent. 


`DD_AGENT_MAJOR_VERSION=7 DD_API_KEY={DD_API_KEY} DD_SITE="datadoghq.com" bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_script.sh)"`

![Agent Installation](img/Agent-i.png)
![Agent Successfully Installed](img/agent-success.png)

To confirm that the Agent was installed and running I ran `sudo datadog-agent status`

![Agent Status](img/agent-status.png)

## Collecting Metrics 

### Adding tags
Here the first step is to add tags in the Agent config file. 
I started with reading about tags at https://docs.datadoghq.com/getting_started/tagging/. I learned that tagging is basically a method to observe aggregate data points and allows correlation and call to action between metrics, traces and logs by binding different data types. I also learned what tag keys are available. 
I navigated to `/etc/datadog-agent` and modified `datadog.yaml` file by adding the following:
 `hostname: vagrant`
```
tags:
    -environment: dev
    env: dev
```

As a result I was able to see the added tags on the Host Map page in DataDog. 
![Host map and tags](img/host-tags.png)

### Installing DataBase
I used MySQL database for the initial set up. 
To install the database I ran: 
` sudo apt install mysql-server ` - installs MySQL server
` sudo service mysql start ` - starts the server

After the installation was complete I confirmed that MySQL server is running by executing the `sudo systemctl status mysql.service` command

![MySQL](img/mysql.png)

##Integration MySQL with Datadog
The next step was to integrate the Agent with the database. 

From reading the Datadog documentation (https://docs.datadoghq.com/integrations/mysql/?tab=host#data-collected) I learned that on each MySQL server I needed to: 
* Create a database user for the Datadog Agent.
* Grant the user privileges. 

Create user with command `CREATE USER 'datadog'@'localhost' IDENTIFIED WITH mysql_native_password by 'datadog99';` where `datadog99` is a password

Grant privileges: 
 `GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'localhost' WITH MAX_USER_CONNECTIONS 5;`

`GRANT PROCESS ON *.* TO 'datadog'@'localhost';`

Enable metrics to be collected from the performance_schema database:
` show databases like 'performance_schema'; `
` GRANT SELECT ON performance_schema.* TO 'datadog'@'localhost'; `

### MySQL Metric Collection

The next step was to set up the config file for Metric Collection
In the directory `/etc/datadog-agent/conf.d/mysql.d` I edited the conf.yaml file to specify server, user, password and host: 
![MySQL metrics](img/mysql-config.png)

I restarted the Agent by running `sudo service datadog-agent restart`

### Create a Custom Agent check

For this task I followed the documentation on how to write the Custom Agent check (https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7)

From there I learned that the names of the configuration and check files must match, so I created a check file with the name `my_metric.py` in `/etc/datadog-agent/checks.d` directory and a configuration file `my_metric.yaml` in `/etc/datadog-agent/conf.d` directory. 

One of the requirements is to set check's collection interval so it only submits the metric once every 45 seconds. We can achieve that by adding `min_collection_interval` at an instance level

```
   init_config:

   instances:
   - min_collection_interval: 45
```

I learned that it does not mean that the metric is collected every 45 seconds, but rather that it could be collected as often as every 45 seconds.

I used the `hello.py` example from the documentation to write my own check file that satisfies the requirements of submitting a metric with a random value between 0 and 1000. 
In the check file I sent a metric `my_metric` on each call. I used the `randint` function to get a random value between 0 and 1000. The code of `my_metric.py` looks like this: 

![my_metric check file](img/my_metric.png)

After restarting the Agent by running `sudo service datadog-agent restart` I could see 
my changes on the `Metrics -> Explorer` page. In the Graph field I searched for `my_metric` and after selecting it from a dropdown I could see a diagram that shows a time when the call was submitted with the value from 0 to 1000. 

![Metrics Explorer page](img/Explorer.png)

Another way to make sure that my custom metric was being collected was by running the command `sudo -u dd-agent -- datadog-agent check my_metric`. From the output I could see that my Check was running and had all the configs that I set up.

![Status check](img/check-my_metric.png)

### Bonus Question
 Can you change the collection interval without modifying the Python check file you created?

I can change the collection interval by modifying the configuration `yaml` file and setting the `min_collection_interval` to desired interval: 

```
   init_config:

   instances:
   - min_collection_interval: 45
```


## Visualizing Data:

### Creating a Timeboard with Datadog API

The one difficalty I had was understanding the difference between timeboard vs dashboard. Once I understood that timeboard is a type of a dashboard I realised that I need to look into the documentaion for the creation of a new dashboard. [Docs API Dashboards](https://docs.datadoghq.com/api/latest/dashboards/)

I decided to use a Python script so I started with the installation of python 3 and pip on VM

I followed [these instructions](https://linuxize.com/post/how-to-install-python-3-7-on-ubuntu-18-04/) to install python 3 and [these instructions](https://linuxize.com/post/how-to-install-pip-on-ubuntu-18.04/) to install pip3. 

After that it was time to install the Datadog library that was going to be used in python script: 
`pip install datadog`

From [API documentation](https://docs.datadoghq.com/api/latest/?code-lang=python) I realised that in order to access the Datadog programmatic API I had to use Applicaton key and API key. 

I was able to access the API key by navigating to the `Integrations` page `API Keys' section. On the same `Integrations page` there is a section that refers to the `Teams page` for the creation of the application key. 

Once I had the keys I used the Python code example provided in [Dashboards documentation](https://docs.datadoghq.com/api/latest/dashboards/) to create my own script. 

`timeboard.py` file contains the following sections: 
 
 Options object contains API key and Application key. 

```
options = {
    'api_key': '<DATADOG_API_KEY>',
    'app_key': '<DATADOG_APPLICATION_KEY>'
}

`Options`are  passed to `initialize` function that was imported from `datadog` library
```
initialize(**options)
```  

Starting from line 10 I define properties of the Dashboard that is going to be created: 

`title = 'Data Visualization'` - name of the dashboard that is going to be created. That name is going to be used in datadog to find it on a dashboard list

Next we have a `widgets` array. It contains three widgets that were requested in the "Visualizing Data" part of the technichal exercise: 
 * Your custom metric scoped over your host.
 * Any metric from the Integration on your Database with the anomaly function applied.
 * Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
```
widgets = [{
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'my_metric{*} by {host}'}
        ],
        'title': 'My Custom Metric'
    }},
    {
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': "anomalies(avg:mysql.performance.cpu_time{host:vagrant}, 'agile', 2)"}
        ],
        'title': 'MySQLS Metric w/Anomaly'
    }},
    {
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': "my_metric{*}.rollup(sum, 3600)"}
        ],
        'title': 'All the Points for the Past Hour Summed Up With a Roll Up function'
    }}
]
```
Each widget consists of `definition` object. That object contains `type`, `requests`, `title` properties. 

`type` obvioulsy specifies type of the widget

`requests` specifies what kind of data is going to be displayed in the widget. For example for the task to visualize "any metric from the Integration on your Database with the anomaly function applied" I decided to select MySQL performace cpu time metric with `Agile` [anomaly detection algorithm](https://docs.datadoghq.com/monitors/monitor_types/anomaly/) and value of 2 bounds (standard deviations for the algorithm). 

For custom metric with the rollup function applied to sum up all the points for the past hour into one bucket I used instractions from [here](https://docs.datadoghq.com/dashboards/functions/rollup/) on how `rollup` function works and how to to use it in the request. I used rollup function with sum and 3600 arguments since I needed to sump all the points for the past hour or 3600 seconds. 

'title` sets the title of the widget. 

Line 37 through 44 is being used for setting additional properties of the dashboard. On line 47 an api call is being made and all above mentioned properties a passed). 

The `timeboard.py` file looks like this (it is also included in the repository): 
```
from datadog import initialize, api

options = {
    'api_key': '<DATADOG_API_KEY>',
    'app_key': '<DATADOG_APPLICATION_KEY>'
}

initialize(**options)

title = 'Data Visualization'
widgets = [{
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'my_metric{*} by {host}'}
        ],
        'title': 'My Custom Metric'
    }},
    {
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': "anomalies(avg:mysql.performance.cpu_time{host:vagrant}, 'agile', 2)"}
        ],
        'title': 'MySQLS Metric w/Anomaly'
    }},
    {
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': "my_metric{*}.rollup(sum, 3600)"}
        ],
        'title': 'All the Points for the Past Hour Summed Up With a Roll Up function'
    }}
]

layout_type = 'ordered'
description = 'A timeboard with memory info.'
is_read_only = True
notify_list = ['serge.pokrovskii@gmail.com']
template_variables = [{
    'name': 'host1',
    'prefix': 'host',
    'default': 'my-host'
}]

api.Dashboard.create(title=title,
                     widgets=widgets,
                     layout_type=layout_type,
                     description=description,
                     is_read_only=is_read_only,
                     notify_list=notify_list,
                     template_variables=template_variables)
```

After saving `timeboard.py` I ran `export DD_SITE="https://api.datadoghq.com/api/v1/dashboard" DD_API_KEY="<API-KEY>" DD_APP_KEY="<APP-KEY>"` and `python3 timeboard.py` to execute python file. 

After successfull execution I should be able to see `Data Visualization` dashboard name in the Dashboard list and access the Dashboard from `Dasboards` -> `Dasboard list` in the UI: 
![Dasboard list](img/dashboard.png)

![Timeboard](img/data-vis.png)

Timeboard can be accessed by following [this link](https://p.datadoghq.com/sb/r994pgswllop6yxx-aae689097938255beefc2e2edd446f2d)

### Set the Timeboard's timeframe and take a snapshot

UI allowed me to set the Timeboard's timeframe to the past 5 minutes and take a snapshot. 

![Snapshot](img/Snapshot.png)

I added `@` notation to find my name in the list to send it to myself. 
![notation](img/notation.png)

### What is the Anomaly graph displaying?

The graph is displaying a period of time when a metric is behaving differently than it has in the past, taking in accounts trends, seasonal day-of-week, and time-of-day patterns. In other words anomaly graph is displaying period of time when metric doesn't match the prediction. It is well-suited for metrics with strong trends and recurring patterns.

