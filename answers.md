

##Solutions Engineer Exercise

#Noah Kalkstein

##Prerequisites

I began setting up the environment by downloading and installing Vagrant after downloading it from their website (https://www.vagrantup.com/downloads.html). I began Vagrant with the command 'vagrant up.' I ssh'd into the machine with the command "vagrant ssh." I can also terminate the virtual machine with the command 'vagrant destroy.'

As suggested, I downloaded and installed Ubuntu/Xenial64 (version 16.04) via the command line (https://app.vagrantup.com/ubuntu/boxes/xenial64).  I found the Ubuntu/Xenial Vagrant Box in Hashicorp's Vagrant Cloud Box Catalog (https://app.vagrantup.com/boxes/search)

Once my Vagrant Ubuntu VM was up and running I visited Datadoghq.com and signed up for an account.  I installed the Agent on my machine with the single line install: 'DD_API_KEY="" bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"'


##Collecting Metrics:

#Step 1
With the Vagrant Ubuntu VM and the Datadog service started, I accessed the datadog.yaml configuration file at the following location: /etc/datadog-agent/datadog.yaml.  I used the command 'sudo vi datadog.yaml' and pressed 'i' (for insert) to edit the file and add tags:

<img src="https://github.com/nkalkstein/hiring-engineers/blob/master/Screen%20Shot%202018-11-26%20at%2010.33.17%20PM.png">

After restarting the Datadog service with the command 'sudo service datadog-agent restart,' the tags were visible in my hostmap on the Datadog website:

<img src="https://github.com/nkalkstein/hiring-engineers/blob/master/Screen%20Shot%202018-11-25%20at%2010.44.33%20PM.png">

#Step 2
I installed the MySQL database on my machine and then installed the related Datadog integration using the instructions on the Datadog site.

First I created a datadog user with replication rights in my MySQL server using the command:

 'sudo mysql -e "CREATE USER 'datadog'@'localhost' IDENTIFIED BY ''    
 ';"
 sudo mysql -e "GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'localhost' WITH MAX_USER_CONNECTIONS 5;"

Next, in order to get the full metrics catalog I granted privileges with the commands:


    sudo mysql -e "GRANT PROCESS ON *.* TO 'datadog'@'localhost';"
    sudo mysql -e "GRANT SELECT ON performance_schema.* TO 'datadog'@'localhost';"

  mysql -u datadog --password='

    ' -e "show status" | \
    grep Uptime && echo -e "\033[0;32mMySQL user - OK\033[0m" || \
    echo -e "\033[0;31mCannot connect to MySQL\033[0m"
    mysql -u datadog --password='

    ' -e "show slave status" && \
    echo -e "\033[0;32mMySQL grant - OK\033[0m" || \
    echo -e "\033[0;31mMissing REPLICATION CLIENT grant\033[0m"

Then I verified the additional priveleges I granted with the commands:

    mysql -u datadog --password='

    ' -e "SELECT * FROM performance_schema.threads" && \
    echo -e "\033[0;32mMySQL SELECT grant - OK\033[0m" || \
    echo -e "\033[0;31mMissing SELECT grant\033[0m"
    mysql -u datadog --password='

    ' -e "SELECT * FROM INFORMATION_SCHEMA.PROCESSLIST" && \
    echo -e "\033[0;32mMySQL PROCESS grant - OK\033[0m" || \
    echo -e "\033[0;31mMissing PROCESS grant\033[0m"

Next, in order to configure the Agent to connect to MySQL, I created and edited the file mysql.yaml using the command 'sudo vi mysql.yaml' and saved it in the '/etc/datadog-agent/conf.d' directory:

<img src="https://github.com/nkalkstein/hiring-engineers/blob/master/Screen%20Shot%202018-11-26%20at%2010.59.51%20PM.png">

#Step 3 and Step 4
Next I created a custom Agent check.  First I created a python file MyCheck.py with 'sudo vi MyCheck.py' and saved it in '/etc/datadog-agent/checks.d.' I edited the file in order to create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.:

<img src="https://github.com/nkalkstein/hiring-engineers/blob/master/Screen%20Shot%202018-11-26%20at%2011.06.32%20PM.png">

I also made a configuration file, MyCheck.yaml, and saved it in '/etc/datadog-agent/conf.d.' It is necessary for the python and Yaml files to have exactly the same name in order for the check to work. In order to change the check's collection interval so that it only submits the metric once every 45 seconds, I added the following code to MyCheck.yaml:

<img src="https://github.com/nkalkstein/hiring-engineers/blob/master/Screen%20Shot%202018-11-26%20at%2011.10.41%20PM.png">

I ran the following command to verify the check: 'sudo -u dd-agent -- datadog-agent check MyCheck.py' I got the following result:

<img src="https://github.com/nkalkstein/hiring-engineers/blob/master/Screen%20Shot%202018-11-20%20at%208.06.10%20PM.png">


#Bonus Question

It is possible to change the collection interval without modifying the python check file.  As described and shown in Step 3 above, you can edit the configuration file associated with your check by adding the code:

    init_config:
    instances:
       - min_collection_interval: 45



##Visualizing Data:

#Step 1
In order to visualize my data I generated API and App keys at 'Integrations tab -> APIs' on the Datadog site. I read the documentation section on creating a timeboard (https://docs.datadoghq.com/api/?lang=python#create-a-timeboard) in order to learn how to create a timeboard.  I utilized the Datadog API to create a Timeboard by creating and running the following python file:

<img src="https://github.com/nkalkstein/hiring-engineers/blob/master/Screen%20Shot%202018-11-27%20at%2012.25.06%20AM.png">

On the Dashboard UI, the timeboard looks like this:

<a <img src="https://github.com/nkalkstein/hiring-engineers/blob/master/Screen%20Shot%202018-11-27%20at%201.53.02%20AM.png"></a>

#Step 2
Using the "annotate" icon on the Timeboard graph, I set the Timeboard's timeframe to the past 5 minutes:

<img src="https://github.com/nkalkstein/hiring-engineers/blob/master/Screen%20Shot%202018-11-27%20at%201.59.38%20AM.png">

I took a snapshot of the graph and used the @ notation to send it to myself.

<img src="https://github.com/nkalkstein/hiring-engineers/blob/master/Screen%20Shot%202018-11-27%20at%202.13.49%20AM.png">


#Bonus Question

The Anomaly graph is displaying the number of MySQL connections. As soon as there are additional connections, the anomaly graph will show a red spike to represent the anomaly (connection).


## Monitoring Data

Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

Warning threshold of 500
Alerting threshold of 800
And also ensure that it will notify you if there is No Data for this query over the past 10m.
Please configure the monitor’s message so that it will:

Send you an email whenever the monitor triggers.

Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.

Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.

When this monitor sends you an email notification, take a screenshot of the email that it sends you.

Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

One that silences it from 7pm to 9am daily on M-F,
And one that silences it all day on Sat-Sun.
Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.


Collecting APM Data:
Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:

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

Bonus Question: What is the difference between a Service and a Resource?

Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

Please include your fully instrumented app in your submission, as well.

Final Question:
Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?

Instructions
If you have a question, create an issue in this repository.

To submit your answers:

Fork this repo.
Answer the questions in answers.md
Commit as much code as you need to support your answers.
Submit a pull request.
Don't forget to include links to your dashboard(s), even better links and screenshots. We recommend that you include your screenshots inline with your answers.
