# Gmail Account Login:
datadogtrial4@gmail.com/9UWHVt3Tt9F3rHM
 
# DataDog Account Login:
datadogtrial4@gmail.com/7gnTm39MeGF7Pak
 
api key id: 99b545d0-b46a-47ed-bcda-6596c34c11e8
api key: dd875915a89fed833c075fd810dd9322

app key id: f91f6486-f393-4cd1-b616-4ee25e1e4bf6
app key: e674a94dcc1882b58a6391c4ed12f59dd4ac60b8

# Root Login into MySQL:
root/password

# DataDog Login into MySQL:
datadog/datadog

# Sample database in MySQL:
DS2

# Logging into MySQL:
mysql -u root -p
Or use MySQL Workbench

# Starting and stopping MySQL:
sudo service mysql stop
sudo service mysql start
sudo service mysql status

# Starting and stopping DataDog Agent:
sudo service datadog-agent start
sudo service datadog-agent stop
sudo service datadog-agent status

# Location of MySQL Server configuration file:
/etc/mysql/mysql.conf.d/mysqld.cnf
  # To edit this file:
  # 1) sudo service mysql stop
  # 2) sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
  # 3) sudo service mysql start
 
# Location of DataDog yaml file:
/etc/datadog-agent/datadog.yaml
  # To edit this file:
  # 1) sudo service datadog-agent stop
  # 2) sudo nano /etc/datadog-agent/datadog.yaml
  # 3) sudo service datadog-agent start

# Location of DataDog MySQL yaml file:
/etc/datadog-agent/conf.d/mysql.d/conf.yaml
  # To edit this file:
  # 1) sudo service datadog-agent stop
  # 2) sudo nano /etc/datadog-agent/conf.d/mysql.d/conf.yaml
  # 3) sudo service datadog-agent start

# The instructions in https://github.com/DataDog/hiring-engineers/tree/solutions-engineer:
SECTION 1 ("1 DD Tags" folder in Firefox Bookmarks Toolbar)
Collecting Metrics:

    Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
    	See https://docs.datadoghq.com/getting_started/tagging/assigning_tags/?tab=noncontainerizedenvironments
    	1) sudo service datadog-agent stop
    	2) sudo nano /etc/datadog-agent/datadog.yaml
    	3) remove the "#" in front of "tags:"
    	4) on the next line, add "- doohickey:doodad"
    	5) in the dashboard, on the left, select Infrastructure -> Host Map
    	6) you will see one hexagon for "DataDog-VirtualBox" (that's the virtual machine I created)
    	7) click that hexagon
    	8) a window will appear below the hexagon
    	9) on the right side of that window, you will see "Tags", and below that, "doohickey:doodad"
    Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
    	1) followed the instructions in https://docs.datadoghq.com/database_monitoring/setup_mysql/selfhosted/?tab=mysql57
    Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
        To read about metrics, go to https://docs.datadoghq.com/metrics.
    	1) go to https://docs.datadoghq.com
    	2) in the search box, search for "custom Agent check"
    	3) click the title of the first hit to go to https://docs.datadoghq.com/metrics/agent_metrics_submission/?tab=count
    	4) scroll down that page until you get to the Tutorial section, and follow the instructions there:
    		a) go to /etc/datadog-agent/conf.d
    		b) sudo mkdir metrics_example.d
    		c) sudo chown dd-agent metrics_example.d
    		d) sudo chgrp dd-agent metrics_example.d
    		e) cd metrics_example.d
    		f) sudo touch metrics_example.yaml
    		g) sudo chown dd-agent metrics_example.yaml
    		h) sudo chgrp dd-agent metrics_example.yaml
    		i) sudo nano metrics_example.yaml
    		j) insert one line "instances: [{}]"
    		k) cd /etc/datadog-agent/checks.d
    		l) sudo touch metrics_example.py
    		m) sudo chown dd-agent metrics_example.py
    		n) sudo chgrp dd-agent metrics_example.py
    		o) sudo nano metrics_example.py
    		p) insert the text from the web page above, but substituting "my_metric" in place of "example_metric", and "1000" in place of "10"
    		q) sudo service datadog-agent restart
    	5) to "Validate your custom check is running correctly with the Agent’s status subcommand":
    		a) run "sudo datadog-agent status"
    		b) run "sudo -u dd-agent -- datadog-agent check metrics_example"
    Change your check's collection interval so that it only submits the metric once every 45 seconds.
    	1) go to https://docs.datadoghq.com
    	2) in the search box, search for "check collection interval"
    	3) click the title of the first hit to go to https://docs.datadoghq.com/developers/custom_checks/write_agent_check
    	4) follow the instructions there:
    		a) cd /etc/datadog-agent/conf.d
    		b) sudo touch checkvalue.yaml
    		c) sudo chown dd-agent checkvalue.yaml
    		d) sudo chgrp dd-agent checkvalue.yaml
    		e) sudo nano checkvalue.yaml
    		f) insert into checkvalue.yaml the yaml text from https://docs.datadoghq.com/developers/custom_checks/write_agent_check
    		g) cd /etc/datadog-agent/checks.d
    		h) sudo touch checkvalue.py
    		i) sudo chown dd-agent checkvalue.py
    		j) sudo chgrp dd-agent checkvalue.py
    		k) sudo nano checkvalue.py
    		l) insert into checkvalue.py the python text from https://docs.datadoghq.com/developers/custom_checks/write_agent_check
    		m) sudo service datadog-agent restart    	
    Bonus Question Can you change the collection interval without modifying the Python check file you created?

SECTION 2 ("2 DD Timeboards" folder in Firefox Bookmarks Toolbar)
Visualizing Data:

    Utilize the Datadog API to create a Timeboard that contains:

    Your custom metric scoped over your host.
    Any metric from the Integration on your Database with the anomaly function applied.
    Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
    1) A Timeboard is a type of Dashboard.  Instructions for creating one are at https://docs.datadoghq.com/dashboards/timeboards.
    2) To go to the created timeboard, go to the list of Dashboards at https://app.datadoghq.com/dashboard/lists, and select "DataDog Timeboard".
    3) A new timeboard is empty except for the "Add widgets" widget.
    	a) I chose timeseries for all widgets.
    	b) After selecting timeseries, you get a screen where you can select a particular Metric to graph and the metric name and type.
    	c) You can click on the field where the metric goes, and a small window pops up, with the link "Edit in Metrics Summary" at the bottom.
    	d) Click that link.  You will get a list of all the available metrics.
    	e) Going back to the screen where you select a particular metric, just below the metric select is the button "Add Formula".
    	f) Click that to bring up a list of all formulas.  Two of them are "rollup" where you can select a time period, and "anomalies".

    Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.
    pip3 install datadog-api-client

    Once this is created, access the Dashboard from your Dashboard List in the UI:

    Set the Timeboard's timeframe to the past 5 minutes
    Take a snapshot of this graph and use the @ notation to send it to yourself.
    
    Bonus Question: What is the Anomaly graph displaying?

SECTION 3 ("3 DD Metric Monitor" folder in Firefox Bookmarks Toolbar)
Monitoring Data

    Since you’ve already caught your test metric going above 800 once,
    you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again.
    So let’s make life easier by creating a monitor.

    Create a new Metric Monitor that watches the average of your custom metric (my_metric)
    and will alert if it’s above the following values over the past 5 minutes:
        Warning threshold of 500
        Alerting threshold of 800
        And also ensure that it will notify you if there is No Data for this query over the past 10m.
        1) An overview of Metric Monitors is located at https://docs.datadoghq.com/monitors/create/types/metric/?tab=threshold.
        2) More about Metric Monitors, including how to test them, is located at https://docs.datadoghq.com/monitors/notify.
        3) To create a monitor, go to https://app.datadoghq.com/monitors/create/metric.  Also go to this webpage to see how a monitor is created.
        4) Variables involved in monitoring are found at https://docs.datadoghq.com/monitors/notify/variables/?tab=is_alert.
        5) To see all monitors, go to https://docs.datadoghq.com/monitors/manage.  The one I created for this exercise is named "There was an incident."
            a) To see the definition of that monitor, go to https://app.datadoghq.com/monitors/62490297.
            b) To edit that monitor, hover your mouse above that monitor.  A set of icons will appear on the right, including a pencil icon to edit it.

    Please configure the monitor’s message so that it will:
        Send you an email whenever the monitor triggers.
        Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
        Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
        When this monitor sends you an email notification, take a screenshot of the email that it sends you.
        
    Bonus Question: Since this monitor is going to alert pretty often,
    you don’t want to be alerted when you are out of the office.
    Set up two scheduled downtimes for this monitor:
        One that silences it from 7pm to 9am daily on M-F,
        And one that silences it all day on Sat-Sun.
        Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

SECTION 4 ("4 DD APM" folder in Firefox Bookmarks Toolbar)
Collecting APM Data:

    Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:
    1) The overview of DataDog APM is located at https://docs.datadoghq.com/tracing
    2) The first place to go for setup is https://docs.datadoghq.com/tracing/setup_overview.
    3) The instructions for DataDog APM in Python is located at:
    	a) https://docs.datadoghq.com/tracing/setup_overview/setup/python/?tab=otherenvironments
    	b) https://docs.datadoghq.com/tracing/runtime_metrics/python
    4) What we did was:
    	a) Created a directory for this exercise: /home/ernie/Desktop/APM.
    	b) Ran "sudo pip install ddtrace", as directed to do in https://docs.datadoghq.com/tracing/setup_overview/setup/python/?tab=otherenvironments.
    	c) Created a Python file in this directory named "stuff.py".
    	d) Put into stuff.py these 2 lines, as directed to do in https://docs.datadoghq.com/tracing/runtime_metrics/python.
    	   from ddtrace.runtime import RuntimeMetrics
	   RuntimeMetrics.enable()
	e) At the command line, execute "python3 stuff.py" to generate data for DataDog.
	f) Went to the list of DataDog Dashboards at https://app.datadoghq.com/dashboard/lists, and noticed a new dashboard: "Python Runtime Metrics".
	g) Clicked on "Python Runtime Metrics" to see this new dashboard.
	h) Or go to https://app.datadoghq.com/dash/integration/30267/python-runtime-metrics.

    Note: Using both ddtrace-run and manually inserting the Middleware has been known to cause issues. Please only use one or the other.

    Bonus Question: What is the difference between a Service and a Resource?

