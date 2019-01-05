# Questions

Hi there, my name is Sara Burke. I'm applying for a Solutions Engineer position at DataDog's SF office. Below you'll find my coding challenge answers in roughly the same order as the questions presented in the README file.

## Prerequisites - Setup the environment

I chose to keep the VM simple and follow recommendations to make an Ubuntu VM using Vagrant. I haven't had many opportunities to work with Docker, so I'll try to isolate the learning part of this process to DataDog products.

* Initially, I tried (and failed) to install the DataDog Agent using provisioning within the Vagrantfile and a shell script. My knowledge of setting up Vagrant from scratch with provisions is spotty, particularly in working with keys.

![DataDog failed to install using script.](imgs/01-Screen-Shot-datadog-failed-to-install.png)

* So instead I'll admit defeat and successfully run the Agent's "easy one-step install" in the shell. I am going to spend more time in the future learning about Vagrantfiles and detailed provisioning/shell scripts.

![DataDog succeeded in installation.](imgs/02-Screen-Shot-successful-datadog-install.png)

* Great! It's working. Let's move on.

![confirmation that DataDog is receiving data from one host.](imgs/03-Screen-Shot-hosts-show-1.png)

## Collecting Metrics

* I decided to spin up a couple of additional Vagrant instances of Ubuntu (total of one Trusty64, two Xenial64s). This time I successfully used Vagrant's provisioning to install the DataDog Agent on first "Vagrant up". Previously, I must have accidentally included a newline when adding the one-liner-install into the the provisioning file. I have included these [Vagrant related files in the docs folder.](docs/vagrant/)

* I added tags and changed hostnames on the Agent config files across the three VMs and restarted the Agent. Then I discovered that I should have prepended the one-liner-intalls in the provisioning files with "DD_INSTALL_ONLY=true". Since changes can take up to 30 minutes to take full effect, DataDog was recognizing the new hostnames as separate machines. Temporarily, five hosts were displayed instead of three.

* A snippet of some changes that I made to the datadog.yaml are displayed below.

```yaml
# Force the hostname to whatever you want. (default: auto-detected)
hostname: Primary.machine

# ...

# Set the host's tags (optional)
tags:
  - importance:high
  - env:prod
  - role:database
```

* Tag functionality displayed across three VMs on the Host Map.

![screenshot of host map with tags selected.](imgs/04-Screen-Shot-host-map-tags.png)

* I installed MySQL using an [installation shell file](docs/vagrant/install.sh) linked to my [Vagrantfile](docs/vagrant/install.sh) provisions with the script snippet below.

```bash
# MySQL ========================
    # Set MySQL Password
    debconf-set-selections <<< "mysql-server mysql-server/root_password password $DBPASSWD"
    debconf-set-selections <<< "mysql-server mysql-server/root_password_again password $DBPASSWD"

    # Install MySQL
    apt-get -y install mysql-server

    # Create a new database
    mysql -uroot -p$DBPASSWD -e "CREATE DATABASE $DBNAME"
```

* I installed the DataDog integration for MySQL via shell and then performed the checks shown below.

![shell My SQL integration confirmation](imgs/05-Screen-Shot-MySQL-confirm.png)

* I also ran datadog-agent status checks for MySQL integration, and confirmed the integration via web GUI.

![DataDog status checks](imgs/06-Screen-Shot-mySQL-check-success.png)

* I created a custom Agent check named my_metric that generated a random int between 0 and 1000 in Python. Displayed below are the code snippets, with comments trimmed, to make this check function properly.

[my_metric python file:](docs/datadog/my_metric.py)
```python
import random

for jj in range(1):
    my_metric = random.randint(0, 1001)

try:
    from checks import AgentCheck
except ImportError:
    from datadog_checks.checks import AgentCheck

__version__ = "1.0.0"

class my_metric_check(AgentCheck):
    def check(self, instance):
            self.gauge('my_metric', random.randint(0, 1001))

```

[my_metric yaml file:](docs/datadog/my_metric.yaml)
```yaml
instances: [{}]
```

* Here is a screen shot of a successful Agent check on my_metric.

![custom metric checked](imgs/07-Screen-Shot-my_metric-agent-check-success.png)

* I changed my_metric's collection interval to once every 45 seconds by changing the [my_metric.yaml](docs/datadog/my_metric.yaml) file to contain the following code snippet.

```yaml
# instances: [{}]

init_config:

instances:
  - min_collection_interval: 45
```

* **Bonus Question** Can you change the collection interval without modifying the Python check file you created?
  * Yes, interval collection can be changed within the metric's yaml file as shown in the last step.

## Visualizing Data

* The timeboard below was created with this [API-timeboard.py](docs/datadog/API-timeboard.py) script I created. Completing this task took longer than I expected in looking through the API docs. So, I used the GUI for creating graphs to generate JSON so I could better understand the structure of the requests, which helped give me additional perspective.

![Timeboard created via DataDog API](imgs/08-Screen-Shot-API-timeboard-view.png)

* In this screen shot, I've shortened the Timeboard's timeframe to the last 5 minutes, taken a snapshot, and used the @ notation to send it to myself.

![snapshot](imgs/09-Screen-Shot-snapshot-5min-timeframe.png)

* **Bonus Question**: What is the Anomaly graph displaying?
  * My Anomaly graph is showing the MySQL kernel_time which displays the percentage of CPU time spent in kernel space by MySQL. The anomaly part of this graph shows grey shading over the visualization showing the expected behavior based on previous data.

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

## Collecting APM Data

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

* **Bonus Question**: What is the difference between a Service and a Resource?

Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

Please include your fully instrumented app in your submission, as well.

## Final Question

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?

## Instructions

If you have a question, create an issue in this repository.

To submit your answers:

* Fork this repo.
* Answer the questions in answers.md
* Commit as much code as you need to support your answers.
* Submit a pull request.
* Don't forget to include links to your dashboard(s), even better links and screenshots. We recommend that you include your screenshots inline with your answers.
