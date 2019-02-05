Your answers to the questions go here.


## Questions

Please provide screenshots and code snippets for all steps.

## Prerequisites - Setup the environment

*Clone the repo to the desktop, check out the correct branch and setup the vagrant host.*
```bash
git clone https://github.com/daclutter/hiring-engineers.git
cd hiring-engineers
git checkout solutions-engineer
vagrant init hasicorp/precise64
vagrant up
```

You can utilize any OS/host that you would like to complete this exercise. However, we recommend one of the following approaches:

* You can spin up a fresh linux VM via Vagrant or other tools so that you don’t run into any OS or dependency issues. [Here are instructions](https://github.com/DataDog/hiring-engineers/blob/solutions-engineer/README.md#vagrant) for setting up a Vagrant Ubuntu VM. We strongly recommend using minimum `v. 16.04` to avoid dependency issues.
* You can utilize a Containerized approach with Docker for Linux and our dockerized Datadog Agent image.

Then, sign up for Datadog (use “Datadog Recruiting Candidate” in the “Company” field), get the Agent reporting metrics from your local machine.



*Install the Agent on the host - the install command, including the API KEY is desplayed on the Datadog getting started page.*
```bash
sudo apt-get install -y curl
DD_API_KEY=<API_KEY> bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```

## Collecting Metrics:

*Default vagrant install is missing vim, install it.*
```bash
sudo apt-get install -y vim
```
* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

*Add the following lines into the config file*
```bash
sudo vim /etc/datadog-agent/datadog.yaml
```
```yaml
# Set the host's tags (optional)
tags:
   - interview
   - home:desktop
   - role:testing
```

*Restart the datadog-agent*
```bash
sudo service datadog-agent restart
```

*Look at the [host map](https://app.datadoghq.com/infrastructure/map?host=817478908&fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=availability-zone&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=true&palette=green_to_orange&paletteflip=false&node_type=host)*

![Hostmap](/images/01-hostmap_tags.png)

* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

*Install MySQL, setting the MySQL root password in the install process (You will be prompted)*
```bash
sudo apt-get install -y mysql-server 
```

*Follow the [MySQL integration instructions](https://app.datadoghq.com/account/settings#integrations/mysql), [alternative instructions](https://docs.datadoghq.com/integrations/mysql/)*

*Create a user for the datadog agent to use with replications rights:*
```bash
sudo mysql -e "CREATE USER 'datadog'@'localhost' IDENTIFIED BY '<PASSWORD>';"
sudo mysql -e "GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'localhost' WITH MAX_USER_CONNECTIONS 5;"
```
*If you created a password for the root user you will need to use the below commands and enter the password at the prompt:*
```bash
sudo mysql -e "CREATE USER 'datadog'@'localhost' IDENTIFIED BY '<PASSWORD>';" -p 
sudo mysql -e "GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'localhost' WITH MAX_USER_CONNECTIONS 5;" -p
```

*Grant additional privileges to get full metrics access*
```bash
sudo mysql -e "GRANT PROCESS ON *.* TO 'datadog'@'localhost';" -p
sudo mysql -e "GRANT SELECT ON performance_schema.* TO 'datadog'@'localhost';" -p
```

*Use the following commands to verify the above*
```bash
vagrant@precise64:/etc/datadog-agent$ mysql -u datadog --password='<PASSWORD>' -e "show status" | \
> grep Uptime && echo -e "\033[0;32mMySQL user - OK\033[0m" || \
> echo -e "\033[0;31mCannot connect to MySQL\033[0m"
Uptime  1191
Uptime_since_flush_status       1191
MySQL user - OK
vagrant@precise64:/etc/datadog-agent$ mysql -u datadog --password='<PASSWORD>' -e "show slave status" && \
> echo -e "\033[0;32mMySQL grant - OK\033[0m" || \
> echo -e "\033[0;31mMissing REPLICATION CLIENT grant\033[0m"
MySQL grant - OK
```

*Use the following commands to verify the additional privileges*
```bash
vagrant@precise64:/etc/datadog-agent$ mysql -u datadog --password='<PASSWORD>' -e "SELECT * FROM performance_schema.threads" && \
> echo -e "\033[0;32mMySQL SELECT grant - OK\033[0m" || \
> echo -e "\033[0;31mMissing SELECT grant\033[0m"
MySQL SELECT grant - OK
vagrant@precise64:/etc/datadog-agent$ mysql -u datadog --password='<PASSWORD>' -e "SELECT * FROM INFORMATION_SCHEMA.PROCESSLIST" && \
> echo -e "\033[0;32mMySQL PROCESS grant - OK\033[0m" || \
> echo -e "\033[0;31mMissing PROCESS grant\033[0m"
+----+---------+-----------+------+---------+------+-----------+----------------------------------------------+
| ID | USER    | HOST      | DB   | COMMAND | TIME | STATE     | INFO                                         |
+----+---------+-----------+------+---------+------+-----------+----------------------------------------------+
| 50 | datadog | localhost | NULL | Query   |    0 | executing | SELECT * FROM INFORMATION_SCHEMA.PROCESSLIST |
+----+---------+-----------+------+---------+------+-----------+----------------------------------------------+
MySQL PROCESS grant - OK

```

*Edit and setup the `/etc/datadog-agent/conf.d/mysql.d/conf.yaml` configuration file with the below configuration*
```bash
sudo vim /etc/datadog-agent/conf.d/mysql.d/conf.yaml
```
```yaml
init_config:

instances:
  - server: 127.0.0.1
    user: datadog
    pass: <PASSWORD>
    tags:
        - interview_db
    options:
      replication: 0
      galera_cluster: 1
```

*Restart the agent for the configuration changes to take effect*
```bash
sudo service datadog-agent restart
```

*Verify the changes using the status command*
```bash
vagrant@precise64:/etc/datadog-agent/conf.d/mysql.d$ sudo datadog-agent status | grep -A 5 mysql
    mysql (1.5.0)
    -------------
      Instance ID: mysql:59e1aacfe586f820 [OK]
      Total Runs: 5
      Metric Samples: Last Run: 64, Total: 319
      Events: Last Run: 0, Total: 0
      Service Checks: Last Run: 1, Total: 5
      Average Execution Time : 76ms
```

*Install the integration on the Datadog Web Interface*

* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
* Change your check's collection interval so that it only submits the metric once every 45 seconds.
* **Bonus Question** Can you change the collection interval without modifying the Python check file you created?

## Visualizing Data:

Utilize the Datadog API to create a Timeboard that contains:

* Your custom metric scoped over your host.
* Any metric from the Integration on your Database with the anomaly function applied.
* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.

Once this is created, access the Dashboard from your Dashboard List in the UI:

* Set the Timeboard's timeframe to the past 5 minutes
* Take a snapshot of this graph and use the @ notation to send it to yourself.
* **Bonus Question**: What is the Anomaly graph displaying?

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

## Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?