# Solutions Engineer Answers
`Yoonhye Jung`
`Sydney`
`yoonhyej.jung@gmail.com`

## Questions

Please provide screenshots and code snippets for all steps.

## Prerequisites - Setup the environment

You can utilize any OS/host that you would like to complete this exercise. However, we recommend one of the following approaches:

* You can spin up a fresh linux VM via Vagrant or other tools so that you don’t run into any OS or dependency issues. [Here are instructions](https://github.com/DataDog/hiring-engineers/blob/solutions-engineer/README.md#vagrant) for setting up a Vagrant Ubuntu VM. We strongly recommend using minimum `v. 16.04` to avoid dependency issues.
* You can utilize a Containerized approach with Docker for Linux and our dockerized Datadog Agent image.

> Answer:   Set up `Vagrant Ubuntu 14.04 LTS` for this exercise.

Then, sign up for Datadog (use “Datadog Recruiting Candidate” in the “Company” field), get the Agent reporting metrics from your local machine.

> Answer:   Signed up and Installed "Datadog Agent v6" on Ubuntu
> 
><img src="https://github.com/Yoonhye/hiring-engineers/blob/Yoonhye_Solutions_Engineer/Screenshots_Yoonhye%20Jung_Solutions_Engineer/Setup_01_Agent%20installation.png" />

> 1. Click 'Intergrations-Agent' button on the top drop-down menu  
> 2. Find [Ubuntu](https://app.datadoghq.com/account/settings#agent/ubuntu) on the left-side menu
> 3. Follow the instruction for installing Datadog Agent v6 on Ubuntu
```
DD_API_KEY=5d35ac69e9371611b7100041d2959ee9 bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```
><img src="https://github.com/Yoonhye/hiring-engineers/blob/Yoonhye_Solutions_Engineer/Screenshots_Yoonhye%20Jung_Solutions_Engineer/Setup_02_Install%20agent%20on%20Ubuntu.png" />
> Apply 'easy one-step install' in Ubuntu terminal

><img src="https://github.com/Yoonhye/hiring-engineers/blob/Yoonhye_Solutions_Engineer/Screenshots_Yoonhye%20Jung_Solutions_Engineer/Setup_03_Start%20agent%20on%20Ubuntu.png" />
> Complete installation and start Datadog Agent
```
sudo start datadog-agent
```

## Collecting Metrics:

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
> Answer:   Edited "datadog.yaml" file to add tags `region:ap` `env:production` `role:database:mysql`
> 
> 1. Find "datadog.yaml" for Agent v6 configuration which is located in "/etc/datadog-agent/" for Linux(Ubuntu)
>>```
>>cd /etc/datadog-agent/
>>```

> 2. Use 'emacs' editor to add tags in "datadog.yaml" file
>>```
>>sudo emacs datadog.yaml
>>```
>See the form example for tagging in "datadog.yaml" file and add a line next to it

><img src="https://github.com/Yoonhye/hiring-engineers/blob/Yoonhye_Solutions_Engineer/Screenshots_Yoonhye%20Jung_Solutions_Engineer/Collecting%20Metrics_01_Tagging.png" />
>

> 3. Restart Datadog Agent for the applied changes
>>``` 
>>sudo service datadog-agent restart
>>```

> 4. See the updated tags on the Host Map page in Datadog
>
><img src="https://github.com/Yoonhye/hiring-engineers/blob/Yoonhye_Solutions_Engineer/Screenshots_Yoonhye%20Jung_Solutions_Engineer/Collecting%20Metrics_02_Tags%20on%20Hostmap%20page.png" />

> Link: [Host Map page](https://app.datadoghq.com/infrastructure/map?host=581392043&fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=availability-zone&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=true&palette=green_to_orange&paletteflip=false&node_type=host)

>>https://app.datadoghq.com/infrastructure/map?host=581392043&fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=availability-zone&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=true&palette=green_to_orange&paletteflip=false&node_type=host


* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

> Answer:   Installed MySQL on Ubuntu and Datadog intergration
> 
> 1. Install the MySQL server by using the Ubuntu package manager
>>```
>>sudo apt-get update
>>sudo apt-get install mysql-server
>>```
> 2. Go to ['Intergrations-Intergrations'](https://app.datadoghq.com/account/settings#integrations) menu and Find the MySQL API
> 
><img src="https://github.com/Yoonhye/hiring-engineers/blob/Yoonhye_Solutions_Engineer/Screenshots_Yoonhye%20Jung_Solutions_Engineer/Collecting%20Metrics_03_Database_Intergrations_MySQL.png" />

> 3. Follow the instruction to create a datadog user with a password
>>```
>>sudo mysql -e "CREATE USER 'datadog'@'localhost' IDENTIFIED BY 'tlvJHD8WLk3@yMS8PVECliiU';"
>>sudo mysql -e "GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'localhost' WITH MAX_USER_CONNECTIONS 5;"
>>```
>
> 4. Configure the Agent to connect to the MySQL  server 
> Edit "mysql.yaml" file located in `/etc/datadog-agent/conf.d`
>>``` 
>>sudo emacs mysql.yaml
>>```
><img src="https://github.com/Yoonhye/hiring-engineers/blob/Yoonhye_Solutions_Engineer/Screenshots_Yoonhye%20Jung_Solutions_Engineer/Collecting%20Metrics_04_Database_Intergrations_MySQL_yaml.png" />

> 5. Restart Datadog Agent for the applied changes
>>``` 
>>sudo service datadog-agent restart
>>```

> 6. Verify that the integration check has passed.
>>``` 
>>sudo datadog-agent status
>>```
><img src="https://github.com/Yoonhye/hiring-engineers/blob/Yoonhye_Solutions_Engineer/Screenshots_Yoonhye%20Jung_Solutions_Engineer/Collecting%20Metrics_05_Database_mysql_check_terminal.png" />
>

* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
> 
> Answer: Each check has a YAML configuration file and the check module with the same name as YAML file (e.g.: mycheck.py and mycheck.yaml)
> I created the two files in each folder as explained below.

> 1. Add a simple configuration file named "mycheck.yaml" in `/etc/datadog-agent/conf.d` folder
>>```
>>init_config:
>>
>>instances:
>>    [{}]
>>```

> 2. Add "mycheck.py" in `/etc/datadog-agent/checks.d` folder
> 
><img src="https://github.com/Yoonhye/hiring-engineers/blob/Yoonhye_Solutions_Engineer/Screenshots_Yoonhye%20Jung_Solutions_Engineer/Collecting%20Metrics_06_Custom%20Agent%20Check_py.png" />
>
> check the applied custom check in Datadog-agent status
>>```
>> sudo datadog-agent status
>>```
><img src="https://github.com/Yoonhye/hiring-engineers/blob/Yoonhye_Solutions_Engineer/Screenshots_Yoonhye%20Jung_Solutions_Engineer/Collecting%20Metrics_07_Custom%20Agent%20Check_mycheck.png" />
>

* Change your check's collection interval so that it only submits the metric once every 45 seconds.
> Answer:   Added a line `min_collection_interval: 45` at the instances level for Agent 6 in the YAML file
>
>>```
>>init_config:
>>
>>instances:
>>    - min_collection_interval: 45
>>```

* **Bonus Question** Can you change the collection interval without modifying the Python check file you created?
> Answer:   Change the collection interval on the Metrics page in Datadog
> 1. Click 'Metrics-Summary' button on the top drop-down menu  
> 2. Find 'my_metric' on the left-side menu and click
> 3. Click on the 'Metadata' Edit icon and insert interval value and save
>
><img src="https://github.com/Yoonhye/hiring-engineers/blob/Yoonhye_Solutions_Engineer/Screenshots_Yoonhye%20Jung_Solutions_Engineer/Collecting%20Metrics_08_Custom%20Agent%20Check_metadata.png" />


## Visualizing Data:

Utilize the Datadog API to create a Timeboard that contains:

* Your custom metric scoped over your host.
* Any metric from the Integration on your Database with the anomaly function applied.
* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
>
> Answer:  
> - Created a Timeboard by utilizing API 
> 1. Create `timeboard.py` file

>> create a graph for 'my_metric'
>><img src="https://github.com/Yoonhye/hiring-engineers/blob/Yoonhye_Solutions_Engineer/Screenshots_Yoonhye%20Jung_Solutions_Engineer/Visualizing%20Data_01_Timeboard%20script%201.png" />

>>  create a graph for 'my_metric' sum up for the past hour
>><img src="https://github.com/Yoonhye/hiring-engineers/blob/Yoonhye_Solutions_Engineer/Screenshots_Yoonhye%20Jung_Solutions_Engineer/Visualizing%20Data_01_Timeboard%20script%202.png" />

>>  create a graph for 'mysql' database with the anomaly function applied
><img src="https://github.com/Yoonhye/hiring-engineers/blob/Yoonhye_Solutions_Engineer/Screenshots_Yoonhye%20Jung_Solutions_Engineer/Visualizing%20Data_01_Timeboard%20script%203.png" />

> 2. Run `timeboard.py` file to utilize API 
>>```
>>sudo python timeboard.py
>>```

> 3. See a new dashboard added in Datadog
><img src="https://github.com/Yoonhye/hiring-engineers/blob/Yoonhye_Solutions_Engineer/Screenshots_Yoonhye%20Jung_Solutions_Engineer/Visualizing%20Data_01_Dashboard%20list.png" />

> - Created a Timeboard by using Datadog UI
><img src="https://github.com/Yoonhye/hiring-engineers/blob/Yoonhye_Solutions_Engineer/Screenshots_Yoonhye%20Jung_Solutions_Engineer/Visualizing%20Data_01_Timeboard.png" />
>

Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.

Once this is created, access the Dashboard from your Dashboard List in the UI:

* Set the Timeboard's timeframe to the past 5 minutes
> Answer:   Added a rollup function and set the timeframe of 5 minutes to the timeseries graph
> 1. Click pencil button to edit on the top-right corner of the timeboard  
> 2. Add a fuction by clicking + button and select rollup-avg
> 3. Set a timeframe in seconds in the period field. (5 mins = 300)
> 4. Click on Save 
><img src="https://github.com/Yoonhye/hiring-engineers/blob/Yoonhye_Solutions_Engineer/Screenshots_Yoonhye%20Jung_Solutions_Engineer/Visualizing%20Data_02_Timeframe_5mins.png" />

* Take a snapshot of this graph and use the @ notation to send it to yourself.
> Answer:   
> 1. click a graph’s snapshot icon.
><img src="https://github.com/Yoonhye/hiring-engineers/blob/Yoonhye_Solutions_Engineer/Screenshots_Yoonhye%20Jung_Solutions_Engineer/Visualizing%20Data_03_notation.png" />
>
> 2. Mark the interesting region, and tell everyone what’s happening.
><img src="https://github.com/Yoonhye/hiring-engineers/blob/Yoonhye_Solutions_Engineer/Screenshots_Yoonhye%20Jung_Solutions_Engineer/Visualizing%20Data_04_notation%20updated.png" />
>
> 3. Receive an email with real-time annotations.
><img src="https://github.com/Yoonhye/hiring-engineers/blob/Yoonhye_Solutions_Engineer/Screenshots_Yoonhye%20Jung_Solutions_Engineer/Visualizing%20Data_05_notation%20email.png" />

* **Bonus Question**: What is the Anomaly graph displaying?
> Answer:   Anomaly graph shows normal trends as well as abnormal metric trends with different color when a metric is behaving differently than it has in the past. It provides deeper context for dynamic metrics by analyzing a metric’s historical behavior.



## Monitoring Data

Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:
> Answer:   Created a new monitor in the selected timeframe against a given threshold through 'Threshold alert' method.
> 1. Click setting button on the top-right corner of the timeboard  
> 2. Select 'Create Monitor' in drop-down and click
><img src="https://github.com/Yoonhye/hiring-engineers/blob/Yoonhye_Solutions_Engineer/Screenshots_Yoonhye%20Jung_Solutions_Engineer/Monitoring%20Data_01_Create%20Monitor.png" />
> 3. Choose 'Threshold alert' method 
><img src="https://github.com/Yoonhye/hiring-engineers/blob/Yoonhye_Solutions_Engineer/Screenshots_Yoonhye%20Jung_Solutions_Engineer/Monitoring%20Data_02_Set%20Alert.png" />

* Warning threshold of 500
* Alerting threshold of 800
> 4. Set alert conditons 
* And also ensure that it will notify you if there is No Data for this query over the past 10m.
> 5. Select 'Notify'for No Data condition field
><img src="https://github.com/Yoonhye/hiring-engineers/blob/Yoonhye_Solutions_Engineer/Screenshots_Yoonhye%20Jung_Solutions_Engineer/Monitoring%20Data_03_Set%20Alert.png" />

Please configure the monitor’s message so that it will:

* Send you an email whenever the monitor triggers.
* Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
* Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
* When this monitor sends you an email notification, take a screenshot of the email that it sends you.

> Answer:   Set email Notification by using message template variables for a multi-alert in the Edit field
> 
><img src="https://github.com/Yoonhye/hiring-engineers/blob/Yoonhye_Solutions_Engineer/Screenshots_Yoonhye%20Jung_Solutions_Engineer/Monitoring%20Data_04_Create%20Message.png" />
>
><img src="https://github.com/Yoonhye/hiring-engineers/blob/Yoonhye_Solutions_Engineer/Screenshots_Yoonhye%20Jung_Solutions_Engineer/Monitoring%20Data_05_Email%20Alert.png" />
>


* **Bonus Question**: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

  * One that silences it from 7pm to 9am daily on M-F,
  * And one that silences it all day on Sat-Sun.
  * Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification. 
> Answer:  Go to ['Manage Downtime'](https://app.datadog.com/monitors#/downtime) page 
> 1. Click 'Manage Downtime' button in the 'Monitor' top drop-down menu  
><img src="https://github.com/Yoonhye/hiring-engineers/blob/Yoonhye_Solutions_Engineer/Screenshots_Yoonhye%20Jung_Solutions_Engineer/Monitoring%20Data_06_Downtime%20menu.png" />
>
> 2. Select'my_metric' on the monitor menu in the first step 'Choose what to slience'
> 3. Set Schedule for a specific times by selecting 'Recurring' tab for this excercise 
> 4. Set Repeat Every: 1 'weeks' in the second field
>
><img src="https://github.com/Yoonhye/hiring-engineers/blob/Yoonhye_Solutions_Engineer/Screenshots_Yoonhye%20Jung_Solutions_Engineer/Monitoring%20Data_07_Manage%20Downtime.png" />
>
><img src="https://github.com/Yoonhye/hiring-engineers/blob/Yoonhye_Solutions_Engineer/Screenshots_Yoonhye%20Jung_Solutions_Engineer/Monitoring%20Data_08_Set%20Downtime%20schedule.png" />
>
><img src="https://github.com/Yoonhye/hiring-engineers/blob/Yoonhye_Solutions_Engineer/Screenshots_Yoonhye%20Jung_Solutions_Engineer/Monitoring%20Data_09_Downtime%20email.png" />

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

* **Note**: Using both ddtrace-run and manually inserting the Middleware has been known to cause issues. Please only use one or the other. 

> Answer:   I used the given Flask app for collecting APM data 
>           (I upgraded to Ubuntu 16.04 for this excercise as I faced errors in Ubuntu 14.04)
> 
>  Link: [APM Monitor for my flask app] https://app.datadoghq.com/apm/service/flask/flask.request?start=1536713774564&end=1536717374564&env=production&paused=false(https://app.datadoghq.com/apm/service/flask/flask.request?start=1536713774564&end=1536717374564&env=production&paused=false)
>
>
> 1. Set up Flask in Ubuntu
>> Install `python-virtualenv ` to create virtual environment for Python projects
>>>```
>>>cd ~
>>>sudo apt-get install python-virtualenv 
>>>sudo apt-get install python-pip
>>>```
> >Create `flask-application` folder for the Flask app 
>>>```
>>>mkdir flask-application
>>>cd flask-application
>>>```
>
>> Create a virtual environment for flask `flask-env`and activate it
>>>```
>>>mkdir flask-application
>>>cd flask-application
>>>source flask-env/bin/activate
>>>```
>
>>> Install Flask in the flask-env
>>>```
>>>(flask-env) vagrant@ubuntu-xenial:~/flask-application$ pip install Flask
>>>```
>
> 2. Add `flaskapp.py` in the flask-env
> 
>>```
>>(flask-env) vagrant@ubuntu-xenial:~/flask-application$ emacs flaskapp.py
>>```
><img src="https://github.com/Yoonhye/hiring-engineers/blob/Yoonhye_Solutions_Engineer/Screenshots_Yoonhye%20Jung_Solutions_Engineer/Collecting%20APM%20Data_03_app.png" />

> 3. Install the Datadog Tracing library `ddtrace` using pip
>>```
>>sudo pip install ddtrace
>>```
>
> 4. Enable APM trace colletion in `datadog.yaml`
><img src="https://github.com/Yoonhye/hiring-engineers/blob/Yoonhye_Solutions_Engineer/Screenshots_Yoonhye%20Jung_Solutions_Engineer/Collecting%20APM%20Data_01_Config.png" />
>

> 5. Instrument the Flask application by using `ddtrace-run`
>>``` 
>>(flask-env) vagrant@ubuntu-xenial:~/flask-application$ ddtrace-run python flaskapp.py
>>```
><img src="https://github.com/Yoonhye/hiring-engineers/blob/Yoonhye_Solutions_Engineer/Screenshots_Yoonhye%20Jung_Solutions_Engineer/Collecting%20APM%20Data_02_run.png" />

> 6. Open another terminal window in Ubuntu and send a HTTP request using cURL
>>``` 
>>$ curl 'http://127.0.0.1'
>>```

> 7. Traces are available to see on [APM](https://app.datadoghq.com/apm/) page in Datadog

><img src="https://github.com/Yoonhye/hiring-engineers/blob/Yoonhye_Solutions_Engineer/Screenshots_Yoonhye%20Jung_Solutions_Engineer/Collecting%20APM%20Data_04_APM%20page.png" />
>

* **Bonus Question**: What is the difference between a Service and a Resource?
> Answer:   A "Service" is the name of a set of processes that work together to provide a feature set, while a "Resource" is a particular query to a service. For instance, a simple web application may consist of two services: a single webapp service and a single database service. For a SQL database service, a resource would be the SQL of the query itself like `select * from users where id = ?`

Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.
Please include your fully instrumented app in your submission, as well.

## Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?

> Answer:   House electricity monitoring system which can monitor electricity consumption by device, time and space. Intergrated devices, such as electricity Usage Monitor, power meter and smart plug can be used for this monitoring system.

## References

### How to get started with Datadog

* [Datadog overview](https://docs.datadoghq.com/)
* [Guide to graphing in Datadog](https://docs.datadoghq.com/graphing/)
* [Guide to monitoring in Datadog](https://docs.datadoghq.com/monitors/)

### The Datadog Agent and Metrics

* [Guide to the Agent](https://docs.datadoghq.com/agent/)
* [Datadog Docker-image repo](https://hub.docker.com/r/datadog/docker-dd-agent/)
* [Writing an Agent check](https://docs.datadoghq.com/developers/agent_checks/)
* [Datadog API](https://docs.datadoghq.com/api/)

### APM

* [Datadog Tracing Docs](https://docs.datadoghq.com/tracing)
* [Flask Introduction](http://flask.pocoo.org/docs/0.12/quickstart/)

### Vagrant

* [Setting Up Vagrant](https://www.vagrantup.com/intro/getting-started/)

### Other questions:

* [Datadog Help Center](https://help.datadoghq.com/hc/en-us)
