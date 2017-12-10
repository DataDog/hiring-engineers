<h1>Table of Content</h1>

1. Installing DataDog Agent
1. Create Tags on Agent
1. Configuring Database
1. Creating Custom Metric
1. Create Timeboard with Datadog API
  
 <h2>1. Installing Datadog Agent</h2>
  
Begin by signing up the Datadog website and filling out all required credentials and information.
![screenshot](https://raw.githubusercontent.com/FantasyStarr/hiring-engineers/debdbde804f263ec43926b810dc206986dd7639d/Screenshot%20from%202017-12-05%2021-19-32.png)
   
Reach this screen by clicking the link below.
![screenshot](https://raw.githubusercontent.com/FantasyStarr/hiring-engineers/master/Screenshot%20from%202017-12-05%2021-22-40.png)
 <br>https://app.datadoghq.com/signup/agent
  
Depending on the Operarting system you are using, click on the operating system on the left bar and click on it. In this case since we are using Ubuntu, click on Ubuntu.
  
Press CTRL + ALT + T to pull up the terminal. Copy the key and paste it into the terminal and press enter.
![screenshot](https://raw.githubusercontent.com/FantasyStarr/hiring-engineers/master/Screenshot%20from%202017-12-05%2021-30-01.png)

The installation should be successful if you see the screen below.

![screenshot](https://raw.githubusercontent.com/FantasyStarr/hiring-engineers/master/Screenshot%20from%202017-12-05%2022-20-42.png)

<h2>2. Create Tags on Agent</h2>
To show that your machine is currently being monitored, it has to tagged to be shown on the Host Map. 

In your command prompt with in `vagrant ssh`

Type in `sudoedit /etc/dd-agent/datadog.conf`

Press `CRTL + V` until you see the line below.

#tags: country:au, state:nsw, role:database

Remove the "#" and add the tag of your choice, in my case it looks like above.

![screenshot](https://raw.githubusercontent.com/FantasyStarr/hiring-engineers/master/sudoeditagent.PNG)

Press CTRL + X , Press Y then Enter to save the changes.
 
[Go to your Host Map by clicking here](https://app.datadoghq.com/infrastructure/map)

<h2>3. Configuring Database</h2>

Install my SQL with the commands below

`sudo apt-get update`<br>
`sudo apt-get install mysql-server`<br>
`/usr/bin/mysql_secure_installation`<br>

Access MySQL by using `/usr/bin/mysql -u root -p`

Following the configuration steps in the link below. This will be for MYSQL integation.

https://app.datadoghq.com/account/settings#integrations/mysql 

This didn't work for me, so I followed the steps in the knowledge base.

https://docs.datadoghq.com/integrations/mysql/

![screenshot](https://raw.githubusercontent.com/FantasyStarr/hiring-engineers/master/mysqlsuccess.PNG)
![screenshot](https://raw.githubusercontent.com/FantasyStarr/hiring-engineers/master/mysqlverification.PNG)

<h2>4. Creating Custom Metric</h2>
 
 The basic creation of a random number generator being returned as a metric on Datadog dashboard is made by following this link
 
 https://docs.datadoghq.com/guides/agent_checks/
 
Create two files using the commands below<br>

`sudo touch /etc/dd-agent/conf.d/my_metric.yaml`<br>
`sudo touch /etc/dd-agent/checks.d/my_metric.py`

Edit the my_metric.py with the code below
```python
import random
from checks import AgentCheck

class randomCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', random.randint(0,1000))
```
Edit the configuration my_metric.yaml file with the code below
```yaml
init_config:
 min_collection_interval: 45
instances:
    [{}]
```

Reset the agent and view the custom metric in your host map or the metric summary page
![screenshot](https://raw.githubusercontent.com/FantasyStarr/hiring-engineers/master/customMetric.PNG)
![screenshot](https://raw.githubusercontent.com/FantasyStarr/hiring-engineers/master/customMetricCollect.PNG)

<h2>5. Create Timeboard with Datadog API</h2>


https://docs.datadoghq.com/api/#timeboards Used as an reference to create a basic timeboard and editted 

Used https://docs.datadoghq.com/guides/anomalies/ to run anomalies function

Following the reference in the link below will make a timeboard with our custom metric, any MySQL Metric with the anomaly function, and a sum of of custom metrics within the last hour.

Ran into a problem with Python, but updating it fixed the issue. I've received SNIMissingWarning & InsecurePlatformWarning while running the script, but it appeared to have not affected the overall script as the dashboard was generated.

The script below was ran using the `python ./[filename]` command

```python
from datadog import initialize, api

options = {
    'api_key': '[api]',
    'app_key': '[app]'
}

initialize(**options)

title = "Custom Metric and MYSQL"
description = "An informative timeboard."
graphs = [
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{*} by {precise64}"}
	
        ],
    "viz": "timeseries"
    },
    "title": "My Custom Metric for Host"
},
{
    "definition": {
        "events": [],
        "requests": [
	    {"q": "anomalies(avg:mysql.performance.cpu_time{*}, 'basic', 2)"}
        ],
    "viz": "timeseries"
    },
    "title": "MySQL CPU Perfomance with Anomaly Detection"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "my_metric{*} by {precise64}.rollup(sum, 3600)"}
        ],
    "viz": "timeseries"
    },
    "title": "Sum of Custom Metric within past hour"
}
]


template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:my-host"
}]

read_only = False

api.Timeboard.create(title=title, description=description, graphs=graphs, template_variables=template_variables, read_only=read_only)

```

If this script ran correctly, it should look something like the image below [or click here](https://app.datadoghq.com/dash/417964/custom-metric-and-mysql?live=true&page=0&is_auto=false&from_ts=1512863051946&to_ts=1512866651946&tile_size=m&tpl_var_host1=*)

![screenshot](https://raw.githubusercontent.com/FantasyStarr/hiring-engineers/master/customTimeboard.PNG)

Using the UI in the Timeframe, we're going to set the timeline to 5 minutes and add notation on the graph.

Notation can be added by holding shift and clicking on a point of the graph.

![screenboard](https://raw.githubusercontent.com/FantasyStarr/hiring-engineers/master/notation.PNG)


