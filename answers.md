## Environment Set Up
To avoid OS or dependency issues, utilize [Vagrant](https://www.vagrantup.com/intro/getting-started/) to spin up a Ubuntu VM. Make sure to use minimum `v. 16.04`. 

1. [Download](https://www.vagrantup.com/downloads) the proper package for your platform and [Install](https://www.vagrantup.com/docs/installation) Vagrant.

2. Download the appropriate package for [VirtualBox](https://www.virtualbox.org/wiki/Downloads) to use as a hypervisor.

3. Navigate to your command prompt and enter the following command to initialize Vagrant:
```
vagrant init hashicorp/bionic64
```

4. Start your VM and SSH into it with:
```
vagrant up
vagrant ssh
```
![image](https://user-images.githubusercontent.com/80560551/111412584-e54bcb00-8699-11eb-80bf-255154f4e018.png)

5. Sign up for a Datadog trial at https://www.datadoghq.com/ . After creating a Datadog account, follow [get started with the Datadog agent](https://docs.datadoghq.com/getting_started/agent/) documentation. Select Ubuntu to see installation instructions for your VM and run the one-step install.

Then, get the Agent reporting metrics from your local machine and move on to the next section.

Here's a summary of my Agent's reporting metrics:
![image](https://user-images.githubusercontent.com/80560551/112403345-75f25e80-8ccb-11eb-9d6f-4bab5da88b25.png)


## Collecting Metrics

1. To [add tags](https://docs.datadoghq.com/getting_started/tagging/assigning_tags/?tab=noncontainerizedenvironments#configuration-file) to your host via the agent config file, locate the datadog.yaml file (/etc/datadog-agent/datadog.yaml). I uncommented the tag section and added environment, role and region keys with their values and saved the file with the changes.
![image](https://user-images.githubusercontent.com/80560551/111956489-123c1b80-8aa8-11eb-901d-33b5dae6005b.png)
To view the tags on the [Host Map](https://docs.datadoghq.com/infrastructure/hostmap/#overview) page (found under the Infrastructure tab) in Datadog, restart the Agent running as a service with `sudo service datadog-agent restart` command ([found here](https://docs.datadoghq.com/agent/basic_agent_usage/ubuntu/?tab=agentv6v7)). The Tags section in the following screenshot gets populated with the keys and values defined in the agent config file:
![image](https://user-images.githubusercontent.com/80560551/111961101-d4da8c80-8aad-11eb-9e09-0f516ce64dcf.png)

2. [Install MongoDB on Ubuntu](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/#install-mongodb-community-edition). I followed this documentation to install MongoDB Community Edition using the apt package manager. These are the commands I used for Ubuntu 18.04 version:
```
wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -

echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list

sudo apt-get update
sudo apt-get install -y mongodb-org
```
I used the following command to determine the init system my platform uses: `ps --no-headers -o comm 1` which resulted in systemd and used the appropriate commands to start MongoDB and check its status:
```
sudo systemctl start mongod
sudo systemctl status mongod
```
(This was resulting in an error which I fixed by changing the permission settings on /var/lib/mongodb and /tmp/mongodb-27017.sock to set the owner to mongodb user using the following commands and then started MongoDB up again.)
```
sudo chown -R mongodb:mongodb /var/lib/mongodb
sudo chown mongodb:mongodb /tmp/mongodb-27017.sock
```
Start a mongo shell on the same host machine as the mongod. The following runs on your localhost with default port 27017:
```
mongo
```


Install the respective Datadog [integration](https://docs.datadoghq.com/integrations/).
Following the steps listed in [MongoDB](https://docs.datadoghq.com/integrations/mongo/?tab=standalone), I created a read-only user for the Datadog Agent in the admin database:
```
use admin
db.createUser({
  "user": "datadog",
  "pwd": "<UNIQUEPASSWORD>",
  "roles": [
    { role: "read", db: "admin" },
    { role: "clusterMonitor", db: "admin" },
    { role: "read", db: "local" }
  ]
})
```
![image](https://user-images.githubusercontent.com/80560551/111971303-6e5b6b80-8ab9-11eb-8ef3-6d1382f26b9f.png)

To configure a single agent running on the same node to collect all available mongo metrics, edit mongo.d/conf.yaml file located in (/etc/datadog-agent/conf.d/) of your Agent's configuration directory with the following:
```
init_config:
    service: "mongod.service"
instances:
  - hosts:
      - "127.0.0.1"
    username: datadog
    password: <UNIQUEPASSWORD>
    database: admin
```
Refer to sample mongo.d/conf.yaml.example for all configuration options.

Restart the Agent `sudo service datadog-agent restart`.

Infrastructure List allows us to see the mongodb connections have been configured:
![image](https://user-images.githubusercontent.com/80560551/112413244-1ac96780-8cdd-11eb-8983-c07e1882b924.png)

3. Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

Refer to [Writing a Custom Agent Check](https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7) documentation.

Create a python check file in /etc/datadog-agent/checks.d directory. I created custom_my_metric.py:
![image](https://user-images.githubusercontent.com/80560551/112420847-2a4fad00-8ceb-11eb-9de1-1b7fc946df38.png)

Create a config file with the same name as the check file and place in /etc/datadog-agent/conf.d
I created custom_my_metric.yaml:
![image](https://user-images.githubusercontent.com/80560551/112420948-5c610f00-8ceb-11eb-8d95-1f7e8e6b8c32.png)

Here's my_metric in the Metric Explorer:
![image](https://user-images.githubusercontent.com/80560551/112421381-253f2d80-8cec-11eb-9eb9-91344edb4d16.png)

4. Change your check's collection interval so that it only submits the metric once every 45 seconds.

The default collection interval is 15. I edited my metric config file to change the collection interval of my check:
![image](https://user-images.githubusercontent.com/80560551/112422112-992e0580-8ced-11eb-9aa7-f9a721ea37d9.png)

Bonus Question: Can you change the collection interval without modifying the Python check file you created?

Yes, by editing the config file as seen in the screenshot above. Also, it can be changed via the Metrics Explorer on the UI as seen below:
![image](https://user-images.githubusercontent.com/80560551/112422883-d5ae3100-8cee-11eb-8dcb-1030e0feb4e7.png)

## Visualizing Data

Refer to the [API](https://docs.datadoghq.com/api/) documentation.

Before creating a Timeboard, install [python 3](https://phoenixnap.com/kb/how-to-install-python-3-ubuntu) and [pip](https://linuxize.com/post/how-to-install-pip-on-ubuntu-18.04/) on your VM (links are for Ubuntu 18.04 platform).
Verify installations with `python3 --version` and `pip3 --version`

Next, execute the following command:
```
pip3 install datadog
```
Now we can move on to creating an [Application key](https://docs.datadoghq.com/account_management/api-app-keys/#application-keys) which will be used with an [API key](https://docs.datadoghq.com/account_management/api-app-keys/#api-keys)-- together they provide users access to Datadog’s programmatic API. The linked documentation specifies how to create the keys in the UI. 

Once you have the keys, use the Python code example provided in this [dashboards](https://docs.datadoghq.com/api/latest/dashboards/) documentation to create your python script for your timeboard. Make sure to replace the api_key and app_key values. 

Utilize the Datadog API to create a Timeboard that contains:
1. Your custom metric scoped over your host.

[Request JSON Schema](https://docs.datadoghq.com/dashboards/graphing_json/request_json/) and
[Scope](https://docs.datadoghq.com/dashboards/graphing_json/request_json/#scope) documentation demonstrate how to format the requests value. 

Here's my script that displays a widget with my_metric (custom metric we created earlier) scoped over host: 

```
from datadog import initialize, api

options = {
    'api_key': '<DATADOG_API_KEY>',
    'app_key': '<DATADOG_APPLICATION_KEY>'
}

initialize(**options)

title = 'Data Visualization Timeboard'
widgets = [{
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'my_metric{*} by {host}'}
        ],
        'title': 'My Custom Metric'
    }
}]
layout_type = 'ordered'
description = 'A timeboard with metric info.'
is_read_only = True
notify_list = ['aasthag06@gmail.com']
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
 In the widgets array, edit the requests value array to display whichever metric you wish to see on your Dashboard.
 
2. Any metric from the Integration on your Database with the anomaly function applied.

Refer to the [Anomaly function](https://docs.datadoghq.com/dashboards/functions/algorithms/#anomalies) documentation

Expand the mytimeboard python script to include another widget.
Here, I use the mongodb.uptime metric, basic algorithm and value of 2 bounds (standard deviations for the algorithm).
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
            {'q': "anomalies(avg:mongodb.uptime{*}, 'basic', 2)"}
        ],
        'title': 'MongoDB Metric w/Anomaly'
    }}
]
```
3. Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

Refer to the [Rollup function](https://docs.datadoghq.com/dashboards/functions/rollup) documentation

Add another widget to the python script:
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
            {'q': "anomalies(avg:mongodb.uptime{*}, 'basic', 2)"}
        ],
        'title': 'MongoDB Metric w/Anomaly'
    }},
    {
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': "my_metric{*}.rollup(sum,3600)"}
        ],
        'title': 'Custom Metric w/Rollup Sum for Past Hr'
    }}
]
```
Here, I supplied the rollup function with sum and 3600 arguments since we want to sum up all the points for the past hour (3600 seconds).
Run the python script via `python3 mytimeboard.py`

Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.
Timeboard script - [mytimeboard.py](https://github.com/guptaa1/hiring-engineers/blob/solutions-engineer/mytimeboard.py)

Once this is created, access the Dashboard from your Dashboard List in the UI:
![image](https://user-images.githubusercontent.com/80560551/112702260-1d989980-8e50-11eb-9b49-85f15b0d5d1e.png)

Timeboard link: https://p.datadoghq.com/sb/7v4fbr3s27ph9g51-d0362a45bf21a0ce7a9068962657e50f

4. Set the Timeboard's timeframe to the past 5 minutes
The highlighted arrow allows the user to change the time settings on the dashboard:
![image](https://user-images.githubusercontent.com/80560551/112702294-36a14a80-8e50-11eb-869a-f1bff4b9baa6.png)

6. Take a snapshot of this graph and use the @ notation to send it to yourself.
![image](https://user-images.githubusercontent.com/80560551/112702723-c398d380-8e51-11eb-9bc6-c4bc86c4f5d5.png)
![image](https://user-images.githubusercontent.com/80560551/112702818-fb078000-8e51-11eb-91f0-ead58913b424.png)

Bonus Question: What is the Anomaly graph displaying?
The grey bands show what is expected based on past trends. When the time doesn't match the prediction, you see an anomaly.
In the following anomaly graph for the past day, an anomaly is seen in red:
![image](https://user-images.githubusercontent.com/80560551/112702925-5f2a4400-8e52-11eb-88d5-93b7f51ce6d9.png)

## Monitoring Data
Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:
* Warning threshold of 500
* Alerting threshold of 800
* And also ensure that it will notify you if there is No Data for this query over the past 10m.

Follow along to [create a monitor in Datadog](https://docs.datadoghq.com/monitors/monitor_types/#create)

Under the Monitors tab, select New Monitor and then select Metric for the monitor type. See the image below for monitor configuration details that accounts for the 3 bullets listed above:
![image](https://user-images.githubusercontent.com/80560551/112704541-41f87400-8e58-11eb-8356-684874a2b97c.png)

Please configure the monitor’s message so that it will:

* Send you an email whenever the monitor triggers.
* Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
* Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.

The following image shows the monitor's message configurations to account for the above 3 bullets:
![image](https://user-images.githubusercontent.com/80560551/112705685-25126f80-8e5d-11eb-9a29-0558e8343f0c.png)

* When this monitor sends you an email notification, take a screenshot of the email that it sends you.
![image](https://user-images.githubusercontent.com/80560551/112706184-c1d60c80-8e5f-11eb-9e11-4c0cd4965795.png)

* **Bonus Question**: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

  * One that silences it from 7pm to 9am daily on M-F,
  * ![image](https://user-images.githubusercontent.com/80560551/112706599-90127500-8e62-11eb-9927-4e65d3d5f804.png)
  * And one that silences it all day on Sat-Sun.
  * ![image](https://user-images.githubusercontent.com/80560551/112706747-98b77b00-8e63-11eb-92b1-2bea115b4843.png)
  * Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.
![image](https://user-images.githubusercontent.com/80560551/112706694-2c3c7c00-8e63-11eb-8206-956ebfb9ad05.png)
![image](https://user-images.githubusercontent.com/80560551/112706771-b84ea380-8e63-11eb-8ec4-c63476e12565.png)

## Collecting APM Data:

Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:

```python
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
```

Create a python file in your VM that contains the above flask code. I call mine flaskapp.py:
![image](https://user-images.githubusercontent.com/80560551/112708147-90643d80-8e6d-11eb-801d-50729a4f08b1.png)

Install flask on your VM:
```
pip3 install flask
```

Refer [APM Intro](https://app.datadoghq.com/apm/intro) to get started. Select Host-Based environment to set up the trace collection. Since we have already installed a Datadog Agent on our VM, we can skip step 1 and select python for step 2. Execute the following command to install ddtrace, Datadog's tracing library for Python. It is used to trace requests as they flow across web servers, databases and microservices so that developers have great visiblity into bottlenecks and troublesome requests.

```
sudo -H python3 -m pip install ddtrace
```

With the prereqs out of the way, we can begin to instrument our flask application.
Instrumentation describes how an application sends traces to APM.

Edit your datadog.yaml file (found in the directory /etc/datadog-agent) to enable the apm agent as seen in this image:
![image](https://user-images.githubusercontent.com/80560551/112709536-b55dae00-8e77-11eb-85c2-b14f30eb932d.png)

After saving the changes to your datadog.yaml, restart your agent:
```
sudo service datadog-agent restart
```

To instrument the application, execute the following command after editing it with your service name (the name your service will show within the Datadog UI), environment name, and your python application file name.
```
DD_SERVICE="<SERVICE>" DD_ENV="<ENV>" DD_LOGS_INJECTION=true ddtrace-run python3 <MY-APP>.py
```
I utilize the following for my flaskapp:
```
DD_SERVICE="flaskapp" DD_ENV="dev" DD_LOGS_INJECTION=true DD_TRACE_ENABLED=true ddtrace-run python3 flaskapp.py
```
Learn more about ddtrace-run environment variables [here](https://docs.datadoghq.com/tracing/setup_overview/setup/python/?tab=containers#configuration)

The flask application is running on http://0.0.0.0:5050/
![image](https://user-images.githubusercontent.com/80560551/112710056-86493b80-8e7b-11eb-87d9-b6ab92221f9c.png)

To [test your application](https://docs.datadoghq.com/getting_started/tracing/#test), send your traces to Datadog using curl. Your application should be running (as shown above). In a separate command prompt run:
```
vagrant ssh
curl http://0.0.0.0:5050/
```
![image](https://user-images.githubusercontent.com/80560551/112710261-f1dfd880-8e7c-11eb-821a-295043fefb2b.png)

This correctly outputs: "Entrypoint to the Application" as defined in our flask application when "/" endpoint is hit. 
Let's test the other two endpoints as well:
![image](https://user-images.githubusercontent.com/80560551/112710319-60249b00-8e7d-11eb-9f2f-0280e89b6b74.png)

Upon hitting an endpoint, a GET flask request is generated in the terminal where you ran the ddtrace-run command from: 
![image](https://user-images.githubusercontent.com/80560551/112710501-f5745f00-8e7e-11eb-9181-ed8cef0f06a8.png)
200 HTTP status code means the request was successful

In the UI, APM > Services also reflects the flaskservice we just stood up:
![image](https://user-images.githubusercontent.com/80560551/112710804-09b95b80-8e81-11eb-95cf-c89a3b438b7a.png)

Clicking upon it takes us to this view:
![image](https://user-images.githubusercontent.com/80560551/112710825-22297600-8e81-11eb-92f1-dd58f1b4f1b2.png)

![image](https://user-images.githubusercontent.com/80560551/112710830-2ce40b00-8e81-11eb-80b4-320fe3fcd790.png)

* **Note**: Using both ddtrace-run and manually inserting the Middleware has been known to cause issues. Please only use one or the other.

* **Bonus Question**: What is the difference between a Service and a Resource?

A Service groups together endpoints, queries, or jobs for the purposes of building your application.
Resources represent a particular domain of a customer application - they are typically an instrumented web endpoint, database query, or background job.
A Service is essentially a group of Resources. 

[APM Glossary](https://docs.datadoghq.com/tracing/visualization/) provides a breakdown of APM concepts.

Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.
APM and Infrastructure Metricks Dashboard Link: https://p.datadoghq.com/sb/7v4fbr3s27ph9g51-a0170d013410b6e5b7d506ea1c4c8aa2
![image](https://user-images.githubusercontent.com/80560551/112711601-e4c7e700-8e86-11eb-9b81-0d9c1eeae4a8.png)

Please include your fully instrumented app in your submission, as well.
See [flaskapp.py](https://github.com/guptaa1/hiring-engineers/blob/solutions-engineer/flaskapp.py)

## Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?

Restaurants can benefit from the Datadog monitoring system. The system can take into account past orders to identify and predict the most common food items and the times/days during the week in which they're in demand so the restaurants can plan accordingly to prevent food wastage. In addition, Datadog can serve as a restaurant inventory management system and assist with menu engineering. This data driven approach will create a more efficient system, saving time and money while increasing the profit margin overall. The system can also analyze heavy customer traffic patterns of the day and using that data to schedule staff shifts to properly accommodate customers during peak hours while minimizing staff shifts during the slow hours. 
