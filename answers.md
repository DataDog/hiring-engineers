

# Solutions Engineer Exercise

## Noah Kalkstein

# Prerequisites

I began setting up the environment by downloading and installing Vagrant after downloading it from their website (https://www.vagrantup.com/downloads.html). I began Vagrant with the command 'vagrant up.' I ssh'd into the machine with the command "vagrant ssh." I can also terminate the virtual machine with the command 'vagrant destroy.'

As suggested, I downloaded and installed Ubuntu/Xenial64 (version 16.04) via the command line (https://app.vagrantup.com/ubuntu/boxes/xenial64).  I found the Ubuntu/Xenial Vagrant Box in Hashicorp's Vagrant Cloud Box Catalog (https://app.vagrantup.com/boxes/search)

Once my Vagrant Ubuntu VM was up and running I visited Datadoghq.com and signed up for an account.  I installed the Agent on my machine with the single line install: 'DD_API_KEY="" bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"'


# Collecting Metrics:

## Step 1
With the Vagrant Ubuntu VM and the Datadog service started, I accessed the datadog.yaml configuration file at the following location: /etc/datadog-agent/datadog.yaml.  I used the command 'sudo vi datadog.yaml' and pressed 'i' (for insert) to edit the file and add tags:

<img src="https://github.com/nkalkstein/hiring-engineers/blob/master/Screen%20Shot%202018-11-26%20at%2010.33.17%20PM.png">

After restarting the Datadog service with the command 'sudo service datadog-agent restart,' the tags were visible in my hostmap on the Datadog website:

<img src="https://github.com/nkalkstein/hiring-engineers/blob/master/Screen%20Shot%202018-11-25%20at%2010.44.33%20PM.png">

## Step 2
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

## Step 3 and Step 4
Next I created a custom Agent check.  First I created a python file MyCheck.py with 'sudo vi MyCheck.py' and saved it in '/etc/datadog-agent/checks.d.' I edited the file in order to create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.:

<img src="https://github.com/nkalkstein/hiring-engineers/blob/master/Screen%20Shot%202018-11-26%20at%2011.06.32%20PM.png">

I also made a configuration file, MyCheck.yaml, and saved it in '/etc/datadog-agent/conf.d.' It is necessary for the python and Yaml files to have exactly the same name in order for the check to work. In order to change the check's collection interval so that it only submits the metric once every 45 seconds, I added the following code to MyCheck.yaml:

<img src="https://github.com/nkalkstein/hiring-engineers/blob/master/Screen%20Shot%202018-11-26%20at%2011.10.41%20PM.png">

I ran the following command to verify the check: 'sudo -u dd-agent -- datadog-agent check MyCheck.py' I got the following result:

<img src="https://github.com/nkalkstein/hiring-engineers/blob/master/Screen%20Shot%202018-11-20%20at%208.06.10%20PM.png">


## Bonus Question

It is possible to change the collection interval without modifying the python check file.  As described and shown in Step 3 above, you can edit the configuration file associated with your check by adding the code:

    init_config:
    instances:
       - min_collection_interval: 45



# Visualizing Data:

## Step 1
In order to visualize my data I generated API and App keys at 'Integrations tab -> APIs' on the Datadog site. I read the documentation section on creating a timeboard (https://docs.datadoghq.com/api/?lang=python#create-a-timeboard) in order to learn how to create a timeboard.  I utilized the Datadog API to create a Timeboard by creating and running the following python file:

<img src="https://github.com/nkalkstein/hiring-engineers/blob/master/Screen%20Shot%202018-11-27%20at%2012.25.06%20AM.png">

On the Dashboard UI, the timeboard looks like this:

<img src="https://github.com/nkalkstein/hiring-engineers/blob/master/Screen%20Shot%202018-11-27%20at%201.53.02%20AM.png">

## Step 2
Using the "annotate" icon on the Timeboard graph, I set the Timeboard's timeframe to the past 5 minutes:

<img src="https://github.com/nkalkstein/hiring-engineers/blob/master/Screen%20Shot%202018-11-27%20at%201.59.38%20AM.png">

I took a snapshot of the graph and used the @ notation to send it to myself.

<img src="https://github.com/nkalkstein/hiring-engineers/blob/master/Screen%20Shot%202018-11-27%20at%202.13.49%20AM.png">


## Bonus Question

The Anomaly graph is displaying the number of MySQL connections. As soon as there are additional connections, the anomaly graph will show a red spike to represent the anomaly (connection).


# Monitoring Data

## Step 1

Using the UI on the Datadog site I am able to create a monitor by clicking on 'Monitors -> New Monitor':

<img src="https://github.com/nkalkstein/hiring-engineers/blob/master/Screen%20Shot%202018-11-27%20at%2011.44.01%20AM.png">

I created a new monitor that has a warning threshold of 500, an alerting threshold of 800, and a notification if there is no data over the past 10 minutes, simply by completing the form.  I also configured the monitor to send me an email whenever it is triggered, with different messages based on whether the monitor is an Alert, a Warning or No Data State.

<img src="https://github.com/nkalkstein/hiring-engineers/blob/master/Screen%20Shot%202018-11-27%20at%2011.49.53%20AM.png">

<img
src="https://github.com/nkalkstein/hiring-engineers/blob/master/Screen%20Shot%202018-11-27%20at%2011.51.03%20AM.png">

I can also view the triggered monitor by clicking on 'Triggered Monitor' in the Dashboard dropdown menu:

<img src="https://github.com/nkalkstein/hiring-engineers/blob/master/Screen%20Shot%202018-11-27%20at%2011.52.35%20AM.png">

## Bonus Question

In order to be able to schedule downtimes for my monitor, I use the 'Manage Downtime' dropdown menu.   I configured the monitor to be silenced from 7pm to 9am M-F and all day on Sat-Sun:

<img src="https://github.com/nkalkstein/hiring-engineers/blob/master/Screen%20Shot%202018-11-27%20at%2012.11.05%20PM.png">

<img src="https://github.com/nkalkstein/hiring-engineers/blob/master/Screen%20Shot%202018-11-27%20at%2012.11.15%20PM.png">

I also made sure that a notification email is sent out when I schedule downtime:

<img src="https://github.com/nkalkstein/hiring-engineers/blob/master/Screen%20Shot%202018-11-27%20at%2012.20.36%20PM.png">


# Collecting APM Data:

## Step 1
Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:


Using the provided Flask app, I am able to to collect APM data.  After installing flask with 'pip install flask' I am able to import the flask app.  Next I need to install dd-trace with the command 'pip install ddtrace' in order to trace the application we installed. After installing dd-trace we can instrument the application using the command 'ddtrace-run python flask_app.py'.  With the application running in one terminal we are able to make api calls in another terminal:  


<img src="https://github.com/nkalkstein/hiring-engineers/blob/master/Screen%20Shot%202018-11-27%20at%201.09.40%20PM.png">

After we've begun collecting traces we can see them in the dashboard from the APM dropdown menu in the trace list:

<img
src="https://github.com/nkalkstein/hiring-engineers/blob/master/Screen%20Shot%202018-11-27%20at%201.12.35%20PM.png">


## Bonus Question

A "Service" refers to a process or processes that generate different aspects of a feature.  An application may have only a couple services or many services, depending on the complexity of the application.

A "Resource" refers to a query to a service, as described above.  For instance, the actual code of a query to a database would be a resource, whereas the query system itself would be the service.


# Final Question:

There are truly unlimited possibilities for the implementation of Datadog. One in particular that I think would be interesting is to use Datadog to monitor all of metrics assocationed with the various agencies of New York City Government. With such a wide range of missions and systems to accomplish their goals, the number of different technologies at use is tremendous. Therefore it is often difficult to compare or create associations between metrics from different agencies using different systems, databases, infrastructure, etc.  An application like Datadog would be necessary to accomplish such a complex task.
