# Solutions Engineer Hiring Exercise
### Troy Axthelm

## Environment
This environment is setup using Vagrant running debian/stretch 64. Ansible and the Datadog Ansible role have been used for instance configuration. Configuration files as they were produced by ansible can be found in the Ansible directory where you will also find manually generated files with additional comments for ease of use.

#### Note, this Ansible playbook is setup with the Datadog API key for my test account. If you wish to send metrics to a different datadog account, please change the API 

### Environment Setup:

1. clone or download this repo to the sytem you wish to run on
2. install vagrant https://www.vagrantup.com/docs/installation/
3. install ansible http://docs.ansible.com/ansible/latest/intro_installation.html
4. download the Datadog Ansible role `ansible-galaxy install Datadog.datadog`
5. from this directory, run the Vagrantfile to start your vm, `vagrant up` this may take some time initially as the debian stretch vagrant box will need to be downloaded
6. replace `<DD_API_KEY>` with your datadog api key in ./AnsibleFiles/demo-playbook.yml
7. from this directory, run the ansible playbook on your newly provisioned vm `ansible-playbook --private-key=.vagrant/machines/default/virtualbox/private_key --limit datadog-demo ./AnsibleFiles/demo-playbook.yml  -i ./AnsibleFiles/host`


## Collecting Metrics:

> Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

Tags were added as datadog_config varaiables in the ansible playbook.
 
```
vars:
    datadog_api_key: "<DD_API_KEY>" # replace with your datadog api key
    datadog_agent_version: "1:5.21.2-1" # for apt-based platforms, use a `5.12.3-1` format on yum-based platforms
    datadog_config:
      tags: "role:datadog-demo, department:soloutions-engineering"
      log_level: INFO
      apm_enabled: "true"
      log_enabled: true
```
Once the tags are added to the playbook, and applied with an Ansible run, the tags will be associated with the Datadog agent. Below is a Host view showing information about the host. Under the "Tags" section of the host description, you see the newly configured tags.

![hostmapview](./Screenshots/HostViewTags.png)

> Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

MySQL is installed and configured with the following tasks in the ansible playbook. We also include the mysql-python library which allows configuration of the database through ansible. We configure mysql with a mysql user "datadog". This user has REPLICATION CLIENT and PROCESS priviledges which is all the datadog mysql check will need.

```
  - name: Install mysql-server
    apt: name=mysql-server state=latest
  - name: Install mysql-python # allows us to use ansible mysql_db module
    apt: name=python-mysqldb state=latest
  - name: Create a new database with name 'datadogmysql'
    mysql_db:
      name: datadogmysql
      state: present
  - name: Create datadog mysql user with privledges
    mysql_user:
      name: datadog
      password: datadogdemo
      priv: '*.*:REPLICATION CLIENT/*.*:PROCESS'
      state: present
```

In the variables section of the playbook, a `datadog_checks` block is added. This is where you can add conifguration options for checks that will be created using the ansible datadog ansible role. In our case, the mysql check is added. This configuration file includes a single mysql instance running on localhost and will access the database as the datadog user we setup in the previous ansible run.

```   
   datadog_checks:
      mysql:
        init_config:
        instances:
          - server: localhost
            user: datadog
            pass: datadogdemo
            port: 3306
```

Once the playbook is run with the new configuration, MySQL metrics will be sent to datadog. Below is the default MySQL dashboard, you can see this in you dashboard list by installing the MySQL datadog integration.

![hostmapview](./Screenshots/MySQLDash.png)

> Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

This is a simple custom agent that will submit a guage metric with a random value between 0 and 1000.

```
from checks import AgentCheck
from random import randint

class RandomCheck(AgentCheck):
	def check(self, instance):
		# get a random number and send it as a guaged metric to datadog
		randnum=randint(0, 1000)
		self.gauge('agent.random.num', randnum)
```
It is also important to create a simple config file so the datadog agent knows to run this check.

```
init_config:
instances:
        [{}]
```

> Change your check's collection interval so that it only submits the metric once every 45 seconds.

By adding `min_collection_interval: 45` to the randomcheck config file, we can ensure that this check will only submit one metric within a 45 second interval. It is good to note that this sets a minimum interval and does not mean the check will run every 45 seconds.

> **Bonus Question** Can you change the collection interval without modifying the Python check file you created?
<TODO> explore other ways to modify the collection interval.

## Visualizing Data:

> Utilize the Datadog API to create a Timeboard that contains:

> * Your custom metric scoped over your host.
> * Any metric from the Integration on your Database with the anomaly function applied.
> * Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

> Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timemboard.

> Once this is created, access the Dashboard from your Dashboard List in the UI:

> * Set the Timeboard's timeframe to the past 5 minutes
> * Take a snapshot of this graph and use the @ notation to send it to yourself.
> * **Bonus Question**: What is the Anomaly graph displaying?

## Monitoring Data

Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

* Warning threshold of 500
* Alerting threshold of 800
* And also ensure that it will notify you if there is No Data for this query over the past 10m.

Please configure the monitor’s message so that it will:

* Send you an email whenever the monitor triggers.
* Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
* Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
* When this monitor sends you an email notification, take a screenshot of the email that it sends you.

* **Bonus Question**: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

    * One that silences it from 7pm to 9am daily on M-F,
    * And one that silences it all day on Sat-Sun.
    * Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.


## Collecting APM Data:

Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:

```
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
    app.run()
```    

* **Note**: Using both ddtrace-run and manually inserting the Middleware has been known to cause issues. Please only use one or the other.

* **Bonus Question**: What is the difference between a Service and a Resource?

Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

Please include your fully instrumented app in your submission, as well. 

## Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?
