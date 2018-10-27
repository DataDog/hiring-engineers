Prerequisites - Setup the environment
=====================================

<ol>
  <li>Environment used: Microsoft Windows 10 Surface Book
  <li>Hypervisor used: Virtual Box
  <li>Vagrant box used: Ubuntu 16.04
</ol>

The vagrant install
-------------------

<ol>
  <li>vagrant init ubuntu/xenial64
  <li>vagrant up
  <li>vagrant ssh
</ol>

<img src="http://www.thomatos.org/datadog/vagrant.png">

The agent installation
----------------------
Within the Ubuntu shell the command from the web page was provided as:

First 'curl' had to be installed using 
sudo apt-get install curl

DD_API_KEY=9fcece82deb81b6846ad9d9b85893fda bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"

The datadog-agent yaml file was updated and my tiny, infant, little dog started to bark.

<img src="http://www.thomatos.org/datadog/datadog-yaml.png">

Collecting Metrics
==================

Add tags
--------
Tags were added to the datadog.yaml file.

<img src="http://www.thomatos.org/datadog/tags-yaml.png">

Which resulted in the host map page showing my host with its tags.

<img src="http://www.thomatos.org/datadog/host-tags.png">

Install database
----------------
MySQL was installed from the integration page that involved first installing the MySQL service on the Ubuntu Shell:

sudo apt-get install mysql-server
sudo apt-get install mysql-client

The root user password was saved and next the datadog user had to be configured on the MySQL server which involved these steps:

1. Create a datadog user with replication rights in your MySQL server
sudo mysql -e "CREATE USER 'datadog'@'localhost' IDENTIFIED BY 'BG/ALNNK3KCWdbR1mkTSUMlP';"
sudo mysql -e "GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'localhost' WITH MAX_USER_CONNECTIONS 5;"
sudo mysql -e "GRANT PROCESS ON *.* TO 'datadog'@'localhost';"
sudo mysql -e "GRANT SELECT ON performance_schema.* TO 'datadog'@'localhost';"

2. SQL commands were run to prove the access and rights are working.

3. The Datadog agent had to be configured to connect to MySQL by editing mysql.yaml.

<img src="http://www.thomatos.org/datadog/mysql-yaml.png">

Custom Agent check with my_metric
---------------------------------
The Python script was added into the checks.d directory and used the random module.

<img src="http://www.thomatos.org/datadog/myagentcheck.png">

BONUS Custom interval
---------------------
The collection interval was changed to 45 seconds using the yaml file in conf.d for the agent as shown below as well as a screenshot of the my_metric custom metric from the agent.

<img src="http://www.thomatos.org/datadog/myagentcollectioninterval.png">

<img src="http://www.thomatos.org/datadog/myagentcollectiongraph.png">

Visualizing Data
================
A timeboard was created using the API. The embedded Python pip utility was used to install missing modules for the agent.
sudo /opt/datadog-agent/embedded/bin/pip install datadog

The relevant Python lines of code were acquired by creating a timeboard manually and reverse engineering the syntax to use in the Python code by looking at the JSON output.

The embedded Python pip utility was used to install missing modules for the check.
"q": "avg:my_metric{*}",
"q": "anomalies(avg:mysql.performance.cpu_time{*}, 'basic', 2)",
"q": "avg:my_metric{*}.rollup(sum, 3600)",

The anomanyl function setting:

<img src="http://www.thomatos.org/datadog/anomaly.png">

The email showing the 5 minute timeframe was sent using @et@thomatos.org

<img src="http://www.thomatos.org/datadog/email-anomaly.png">

A screenshot of the dashboard with my_metric, a MySQL metric and the 1 hour rollup shown here.

<img src="http://www.thomatos.org/datadog/timeboard-anomaly.png">

BONUS Anomaly
-------------
The anomaly function is used to highlight data points above or below a gray zone of normal behaviour showing any anomalies or deviations from a normal pattern.
