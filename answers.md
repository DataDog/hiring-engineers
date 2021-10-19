<h1>Datadog Hiring Exercise Answers ZC</h1>

<h3> Prerequisites - Setup the environment: </h3>
1. To set up the environment I chose to use a Ubuntu Server 21.04 running in VirtualBox 6.1. The links to download VirtualBox and the Ubuntu Server ISO are below.

[Ubuntu Download](https://ubuntu.com/download/server)

[VirtualBox Download](https://www.virtualbox.org/wiki/Downloads)

This [Youtube video](https://www.youtube.com/watch?v=-1ouhvjWV9s) provides a walk through on installing Ubuntu Server in VirtualBox.

2. Once the Ubuntu Server VM is up and running, I signed up for a trial at https://www.datadoghq.com/ and specifying "Datadog Recruiting Candidate" in the "Company" field of account information during sign up.

3. Once signed up, you will be asked to complete a few questions about your infrastructure and stack. As this is for a hiring exercise I just selected MySQL and moved on to setting up the agent.

4. To set up the agent I selected Ubuntu as my platform and used the one-step install below where the <ACCOUNT_API_KEY> is populated for your account in the Datadog console.
		DD_AGENT_MAJOR_VERSION=7 DD_API_KEY=<ACCOUNT_API_KEY> DD_SITE="datadoghq.com" bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_script.sh)"

[Basic Agent Usage for Ubuntu](https://docs.datadoghq.com/agent/basic_agent_usage/ubuntu/?tab=agentv6v7)

5. After the Datadog Agent is installed successfully you will be able to select Finish and move into the Datadog console.

<h3> Collecting Metrics: </h3>

1. To add tags to the server for future filtering we will need to modify the Agent config file and add the tags you would like. The tags will be created as a KEY:VALUE pair. For an introduction on tagging, review the doc below.

[Getting Started with Tags](https://docs.datadoghq.com/getting_started/tagging/)

2. We will be assigning tags manually in the configuration file of the Datadog Agent which uses a YAML configuration file. For Ubuntu the configuration YAML is located in:
		/etc/datadog-agent/datadog.yaml
To edit this YAML file I used VIM to add the following line for tags in the YAML configuration file noted above.
		tags: ["env:hiring_db","db_type:mysql"]
For users that may not be familiar with VIM commands to edit the YAML configuration file, please review the study guide by Daniel Miessler,
	[Learn VIM](https://danielmiessler.com/study/vim/).

3. Once you have completed adding the tags to the agent configuration file, restart the Datadog Agent with command below:
		$ sudo service datadog-agent restart

A screenshot of my host and it's tags is below.

<img src="/Datadog_Host_Map_tags.png">

4.  Next to install the MySQL database on your Ubuntu machine, run the following command:
		$ sudo apt install mysql-server
5. Now that MySQL is installed you will also want to run the DBMS's included security script. The script will take you through a series of prompts for security settings and options.  
		$ sudo mysql_secure_installation
6. Additional steps to configure the Datadog MySQL integration can be completed using the 'root' user for this lab's purposes. For additional information around creating a MySQL user that is not the 'root' user please review Step 3 of the linked guide: [How To Install MySQL on Ubuntu](https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-20-04)
7. Next log into MySQL using the following command:
		$ sudo mysql
8. You should now see something similar to the output below:
		Welcome to the MySQL monitor.  Commands end with ; or \g.
		Your MySQL connection id is 27
		Server version: 8.0.26-0ubuntu0.21.04.3 (Ubuntu)

		Copyright (c) 2000, 2021, Oracle and/or its affiliates.

		Oracle is a registered trademark of Oracle Corporation and/or its
		affiliates. Other names may be trademarks of their respective
		owners.

		Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

		mysql>

9. Next in the Datadog Console, select 'Integrations' in the left menu. Then in the search bar at the top, type in 'MySQL' and click on the 'MySQL Integration'. This will pop up information about this integration and how to configure it. Select 'Configure' to review the installation steps. The installation steps used for the MySQL database on my Ubuntu server and continued below.

10. Prepare your MySQL server for the Datadog Agent. The MySQL check in included in the Datadog Agent package. Note the different commands used for MySQL 8.0+ versions. To begin we will need to create a database user for the Datadog Agent:
		mysql> CREATE USER 'datadog'@'127.0.0.1' IDENTIFIED WITH mysql_native_password by '<UNIQUEPASSWORD>';
		Query OK, 0 rows affected (0.00 sec)
11. Verify the user was created successfully using the following two commands - replace <UNIQUEPASSWORD> with the password you created above:
		mysql -u datadog --password=<UNIQUEPASSWORD> -e "show status" | \
		grep Uptime && echo -e "\033[0;32mMySQL user - OK\033[0m" || \
		echo -e "\033[0;31mCannot connect to MySQL\033[0m"

		mysql -u datadog --password=<UNIQUEPASSWORD> -e "show slave status" && \
		echo -e "\033[0;32mMySQL grant - OK\033[0m" || \
		echo -e "\033[0;31mMissing REPLICATION CLIENT grant\033[0m"

	Your terminal will probably show a message stating 'Cannot connect to MySQL' and 'Missing REPLICATION CLIENT grant' similar to the ones below:

		mysql: [Warning] Using a password on the command line interface can be insecure.
		ERROR 1045 (28000): Access denied for user 'datadog'@'127.0.0.1' (using password: YES)
		Cannot connect to MySQL

		mysql: [Warning] Using a password on the command line interface can be insecure.
		ERROR 1045 (28000): Access denied for user 'datadog'@'127.0.0.1' (using password: YES)
		Missing REPLICATION CLIENT grant

12. The Agent needs a few privileges to collect metrics. Grant the user the following limited privileges ONLY:

		mysql> ALTER USER 'datadog'@'127.0.0.1' WITH MAX_USER_CONNECTIONS 5;
		Query OK, 0 rows affected (0.00 sec)

		mysql> GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'127.0.0.1';
		Query OK, 0 rows affected, 1 warning (0.00 sec)

		mysql> GRANT PROCESS ON *.* TO 'datadog'@'127.0.0.1';
		Query OK, 0 rows affected (0.00 sec)

13. If enabled, metrics can be collected from the performance_schema database by granting an additional privilege:
		mysql> show databases like 'performance_schema';
		+-------------------------------+
		| Database (performance_schema) |
		+-------------------------------+
		| performance_schema            |
		+-------------------------------+
		1 row in set (0.00 sec)

		mysql> GRANT SELECT ON performance_schema.* TO 'datadog'@'127.0.0.1';
		Query OK, 0 rows affected (0.00 sec)

14. Configure this check for the Agent running on the host. We will need to edit the mysql.d/conf.yaml file, in the /etc/datadog-agent/conf.d/mysql.d/ directory. On Agent intall there will only be a 'conf.yaml.example' file in that directory. We can change to that directory using the following command:
		$ cd /etc/datadog-agent/conf.d/mysql.d/
	Once in the appropriate directory, we can copy the existing 'conf.yaml.example' file and provide the name of the file we want to edit 'conf.yaml' using the command below
		$ sudo cp conf.yaml.example conf.yaml
	And edit the new file permissions for read, write and execute with the following command
		$ sudo chmod +rwx conf.yaml

15. Now that our 'conf.yaml' file has the appropriate permissions we will now use VIM (VIM guide previously linked in Step #2 above) to edit the file using the following command:
		$ vi conf.yaml
	Then add the following configuration block to the 'mysql.d./conf.yaml' file to collect MySQL metrics. Note: Wrap your password in single quotes in case a special character is present.
		init_config:

		instances:
		- server: 127.0.0.1
			user: datadog
			pass: "<YOUR_CHOSEN_PASSWORD>" # from the CREATE USER step earlier
			port: "<YOUR_MYSQL_PORT>" # e.g. 3306
			options:
				replication: false
				galera_cluster: true
				extra_status_metrics: true
				extra_innodb_metrics: true
				extra_performance_metrics: true
				schema_size_metrics: false
				disable_innodb_metrics: false

17. Restart the Datadog Agent to start sending MySQL metrics to Datadog using the following command:
		$ sudo service datadog-agent restart

The screenshot below shows the MySQL Integration Status showing the integration is working properly:
<img src="/Datadog MySQL Integration Status.png">

18. Next we will be creating a custom Agent check that will submit a metric named my_metric with a random value between 0 and 1000. The names of the configuration and check files must match. Our check will be called mymetric.py and the configuration file will be named mymetric.yaml

	- Use the following command to create the mymetric.py file in the appropriate directory
			$ sudo touch /etc/datadog-agent/checks.d/mymetric.py

	- Modify the file permissions to read, write, execute.
			$ sudo chmod +rwx /etc/datadog-agent/checks.d/mymetric.py

	- Follow the same two steps above to create the mymetric.yaml file in the /etc/datadog-agent/conf.d/ directory. Examples provided below.
			$ sudo touch /etc/datadog-agent/conf.d/mymetric.yaml

			$ sudo chmod +rwx /etc/datadog-agent/conf.d/mymetric.yaml

	- Use VIM to edit the mymetric.py file
			$ sudo vi /etc/datadog-agent/checks.d/mymetric.py

	- Add the following text to the mymetric.py script file:
			## This python script file is created to generate a metric named my_metric with a random value between 0 and 1000 for a custom Datadog Agent Check.

			import random
			from datadog_checks.base import AgentCheck

			class MetricCheck (AgentCheck):
				def check(self, instance):
					self.gauge('my_metric', random.randint(0, 1000))

	- Use VIM to edit the mymetric.yaml file
			$ sudo vi /etc/datadog-agent/conf.d/mymetric.yaml

	- Add the following text to your mymetric.yaml file:
			## Datadog Agent mymetric YAML File

			init_config:

			instances:
			[{}]

19. Verify your check is running using the following command:
		$ sudo -u dd-agent -- datadog-agent check mymetric

	- Your output should look something similar to below:
			=== Series ===
			{
			  "series": [
			    {
			      "metric": "my_metric",
			      "points": [
			        [
			          1633472795,
			          787
			        ]
			      ],
			      "tags": [],
			      "host": "zacserver",
			      "type": "gauge",
			      "interval": 0,
			      "source_type_name": "System"
			    }
			  ]
			}
			=========
			Collector
			=========

			  Running Checks
			  ==============

			    mymetric (unversioned)
			    ----------------------
			      Instance ID: mymetric:d884b5186b651429 [OK]
			      Configuration Source: file:/etc/datadog-agent/conf.d/mymetric.yaml
			      Total Runs: 1
			      Metric Samples: Last Run: 1, Total: 1
			      Events: Last Run: 0, Total: 0
			      Service Checks: Last Run: 0, Total: 0
			      Average Execution Time : 0s
			      Last Execution Date : 2021-10-05 22:26:35 UTC (1633472795000)
			  		Last Successful Execution Date : 2021-10-05 22:26:35 UTC (1633472795000)

			Check has run only once, if some metrics are missing you can try again with --check-rate to see any other metric if available.

20. Restart the Datadog Agent using the following command:
		$ sudo service datadog-agent restart

21. To change the check's collection interval so that it only submits the metric once every 45 seconds we will need to edit the mymetric.yaml file to include the following: 'min_collection_internal: 45' The mymetric.yaml should now look like below:
		## Datadog Agent mymetric YAML File

		init_config:
		min_collection_internal: 45
		instances:
		[{}]

	- We will need to start the agent again for the change to be updated.

Bonus Question: Can you change the collection interval without modifying the Python check file created? Yes, we have modified the collection interval using the YAML config file as noted above.

<h3> Visualizing Data: </h3>
I utilized the Datadog API to create a Timeboard (Dashboard) that contained the following queries: <br>
	- My custom metric scoped over my host. <br>
	- MySQL CPU Performance with the anomaly function applied <br>
	- My custom metric with the rollup function applied to sum up the last hour. <br>
	<br>


The python script I used to create the 'SE Hiring Exercise Dashbaord' is titled example.py and provided in this repository. A link to the Dashboard and a screenshot of the Dashboard are provided below.

[SE Hiring Exercise Dashboard Link](https://p.datadoghq.com/sb/5cf6b98a-200a-11ec-8a7b-da7ad0900002-f3bfaafcf748cb13ff9ea1ec21b3c0b5)

<img src="/SE Hiring Dashboard1.png">

<br>

<br>

The python script I used referenced the Datadog API docs pages linked below:<br>
[Datadog API Reference](https://docs.datadoghq.com/api/latest/)<br>
[Create a new Dashboard](https://docs.datadoghq.com/api/latest/dashboards/#create-a-new-dashboard)<br>
[Timeseries Widget](https://docs.datadoghq.com/dashboards/widgets/timeseries/)<br>
[API and Application Keys](https://docs.datadoghq.com/account_management/api-app-keys/)<br>

The Create a new Dashboard docs page contains the commands required to use the example.py script to create the dashboard and require an API Key and an App Key which can be found in the console using the API and Application Keys docs page.

		export DD_SITE="datadoghq.com" DD_API_KEY="<API-KEY>" DD_APP_KEY="<APP-KEY>"
		python3 "example.py"

Once I created the Dashboard I set the timeframe to the past 5 minutes and took a snapshot of the MySQL CPI Anomalies graph and used the @ notation to send it to myself. Screenshot below of the email notification.

<img src="/[Datadog] MySQL CPU Anomalies - datadogsehiring.zc@gmail.com - Gmail.png">

Bonus Question: What is the Anomaly graph displaying? The anomaly graph I created is displaying anomalies based on the MySQL CPU performance using the basic anomaly detection alogrithm with a bounds parameter of 2. Additional information around algorithms can be found in the linked docs pages below.

[Algorithms](https://docs.datadoghq.com/dashboards/functions/algorithms/)<br>
[Anomaly Monitor](https://docs.datadoghq.com/monitors/create/types/anomaly/)<br>

<h3> Monitoring Data: </h3>
To monitor the test metric I created, I then created a monitor to alert when the metric goes above 800. <br>
<br>
I used the docs page linked below to help create the monitor.

[Metric Monitor](https://docs.datadoghq.com/monitors/create/types/metric/)

The monitor I created reviewed the average of the custom metric (my_metric) and provided the following alerts based on thresholds: <br>
	- Warning at threshold 500<br>
	- Alerting at threshold 800 <br>
	- Notification for No Data for this query over the past 10 minutes. <br>

This monitor also sent me an email whenever it was triggered and provided different messages based on the type of alert. A screenshots of the monitor status message, and configuration is below.

<img src="/My Metric -Monitors _ Datadog.png">
<br>
<img src="/Monitor Status_ My Metric Monitor _ Datadog.png">
<br>
<br>

A screenshot of the email notification of the email alert generated for a warning is below.

<img src="/Warn_ My Metric Monitor on host_zacserver.png">

Bonus Question: I scheduled downtime to silence the monitor notifications from 7pm to 9pm daily on Monday to Friday and all day on Saturdays and Sundays. A screenshot of the scheduled downtimes email notifications are below.

<img src="/Scheduled downtime on My Metric Monitor started.png">

<h3> Collecting APM Data: </h3>
Using the Flask application provided in the hiring exercise I used the docs page linked below to instrument the Datadog APM solution.

[Tracing Python Applications](https://docs.datadoghq.com/tracing/setup_overview/setup/python/)

I used the following command to start ddtrace: <br>

	DD_LOGS_INJECTION=true ddtrace-run python3 flask_app.py


Bonus Question: What is the difference between a service and a resource? A service represents a job or query for data and can be grouped logically for scaling purposes. A resource is the specific action for a service.

Below is a screenshot and a link for the APM and Infra Metrics Dashboard:

<img src="APM and Infra Dashboard _ Datadog.png">

[APM and Infra Metrics Dashboard](https://p.datadoghq.com/sb/5cf6b98a-200a-11ec-8a7b-da7ad0900002-4a10ec21ad531fb2454807d79c1551a2)

The code for the Flask app I used is below:

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


<h3> Final Question: </h3>
I would use Datadog for Healthcare monitoring the availability of critical resources and ICU availability across multiple regions and hospital groups to identify any type of trends as flu season starts in conjunction with the existing COVID pandemic to assist state and regional healthcare decision makers to prioritize resources effectively.

