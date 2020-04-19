

Collecting Metrics:
====================


Add tags in the agent config file
----------------------------------

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

On OS X the config file for the :term:datadog-agent<Agent> is at ``~/.datadog-agent/datadog.yaml``
For now, the contents of the file can be limited to:

.. code-block::yaml
	api_key: <REDACTED>
	hostname: Trials-MacBook-Pro.local
	hostname_fqdn: true
	tags:
	  - environment:dev
	  - host:macbook
	  - admin_email:jitkelme@gmail.com
	  - expires:20200630
	env: dev

Restart the agent after updating this file and you will begin to see data in your Host Map:

.. |host_map_tags| image:: path/filename.png
  :width: 400
  :alt: Web UI Host Map with agent-provided tags.


Add an integration for MySQL
-----------------------------

* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

Use the instructions at the Documentation site (https://docs.datadoghq.com/integrations/mysql/) because they are closer
to what you will find on your desktop machine.

Using the Containerized approach is likely to be smoother if you are using OS X and have installed  ``mariadb`` via Homebrew.
Check the status of your setup using ``brew info mariadb`` and pay close attention the Caveats section of the response.

.. code-block::
	mariadb: stable 10.4.11 (bottled)
	Drop-in replacement for MySQL
	https://mariadb.org/
	Conflicts with:
	  mariadb-connector-c (because both install plugins)
	  mysql (because mariadb, mysql, and percona install the same binaries)
	  mytop (because both install `mytop` binaries)
	  percona-server (because mariadb, mysql, and percona install the same binaries)
	/usr/local/Cellar/mariadb/10.4.11 (742 files, 167.8MB) *
	  Poured from bottle on 2020-01-31 at 21:50:48
	From: https://github.com/Homebrew/homebrew-core/blob/master/Formula/mariadb.rb
	==> Dependencies
	Build: cmake ✔, pkg-config ✔
	Required: groonga ✔, openssl@1.1 ✔
	==> Caveats
	A "/etc/my.cnf" from another install may interfere with a Homebrew-built
	server starting up correctly.

	MySQL is configured to only allow connections from localhost by default

	To have launchd start mariadb now and restart at login:
	  brew services start mariadb
	Or, if you don't want/need a background service you can just run:
	  mysql.server start
	==> Analytics
	install: 10,322 (30 days), 36,656 (90 days), 171,886 (365 days)
	install-on-request: 10,175 (30 days), 35,985 (90 days), 167,487 (365 days)
	build-error: 0 (30 days)

Installing the database into a container is going to be less disruptive to your environment.
To prepare MySQL to communicate with the DataDog agent, open the mysql client with ``mysql -u root`` (or your local equivalent), and run these commands
to create the datadog user and grant access to the database.

.. code-block::
	CREATE USER 'datadog'@'localhost' IDENTIFIED BY '<redacted>';
	GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'localhost' WITH MAX_USER_CONNECTIONS 5;
	GRANT PROCESS ON *.* TO 'datadog'@'localhost';
	GRANT SELECT ON performance_schema.* TO 'datadog'@'localhost';


Exit the mysql client and use the following commands to verify the user and the access grant.

.. code-block::bash
	mysql -u datadog --password= '<redacted>' -e "show status" | \
	grep Uptime && echo -e "\033[0;32mMySQL user - OK\033[0m" || \
	MySQL user - OK

	mysql -u datadog --password='<redacted>' -e "show slave status" && \
	echo -e "\033[0;32mMySQL grant - OK\033[0m" || \
	echo -e "\033[0;31mMissing REPLICATION CLIENT grant\033[0m"
	MySQL grant - OK

Configure the DataDog agent
---------------------------

Provide the agent with the details it needs to receive data from MariaDB. Edit the ``~/.datadog-agent/etc/conf.d/mysql.d/conf.yaml``.
In my case, it looks like this:

.. code-block::
init_config:
instances:
  - server: 127.0.0.1
    user: datadog
    pass: <READACTED>
    tags:
      - environment:dev
      - admin_email:jitkelme@gmail.com
      - expires:20200630
    options:
      replication: false
      galera_cluster: true
      extra_status_metrics: true
      extra_innodb_metrics: true
      extra_performance_metrics: true
      schema_size_metrics: false
      disable_innodb_metrics: false

Configure Auto-discovery for containers - Docker
''''''''''''''''''''''''''''''''''''''''''''''''

https://docs.datadoghq.com/agent/docker/integrations/?tab=docker describes how to prepare the agent for discovering processes
running inside containers.
In this exercise, I use the auto-discovery template to pass credentials as environment variables and avoid including them in the file.
This reduces the risk of leaks when the files get checked into version control.
The stanza for Mariadb in my docker-compose.yaml looks like this:

.. code-block::
  mariadb10:
    image: mariadb:10
    ports:
     - "3310:3306/tcp"
    environment:
      - MYSQL_ROOT_PASSWORD="${MYSQL_ROOT_PASSWORD}"
      - MYSQL_USER="${MYSQL_USER}"
      - MYSQL_PASSWORD="${MYSQL_PASSWORD}"
      - MYSQL_DATABASE=my_db
    labels:
      com.datadoghq.ad.check_names: '[mysql]'
      com.datadoghq.ad.init_configs: ''
      com.datadoghq.ad.instances: '{"server": "%%host%%", "user": "datadog","pass": "%%env_$MYSQL_PASSWORD%%"}'

Extend the Agent's Python environment
'''''''''''''''''''''''''''''''''''''

.. code-block::
	$ sudo -Hu dd-agent /opt/datadog-agent/embedded/bin/pip install -U httpx fastapi


Create a custom Agent check
---------------------------

First, create a custom agent :term:check using the Web UI.
Next, configure the check to submit a metric named ``my_metric`` with a random value between 0 and 1000.

Change the check's collection interval
----------------------------------------

Change your check's collection interval so that it only submits the metric once every 45 seconds.

Bonus: Can you change the collection interval without modifying the Python check file you created?
--------------------------------------------------------------------------------------------------

Can you change the collection interval without modifying the Python check file you created?

Visualizing Data using the Python API
=====================================

Utilize the Datadog API to create a :term:Timeboard
---------------------------------------------------

* Your custom metric scoped over your host.

* Any metric from the Integration on your Database with the anomaly function applied.

* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket


Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.

Visualizing Data using the Web UI
=================================

Once this is created, access the Dashboard from your Dashboard List in the UI:

* Set the Timeboard's timeframe to the past 5 minutes
* Take a snapshot of this graph and use the ``@`` notation to send it to yourself.

Bonus: What is the Anomaly graph displaying?
---------------------------------------------



Monitoring Data
================

Constraining Alerts
--------------------

Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

* Warning threshold of 500
* Alerting threshold of 800
* And also ensure that it will notify you if there is No Data for this query over the past 10m.

Configuring Notifications
-------------------------

Please configure the monitor’s message so that it will:

* Send you an email whenever the monitor triggers.
* Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
* Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
* When this monitor sends you an email notification, take a screenshot of the email that it sends you.

Bonus: Scheduling maintenance windows
----------------------------------------------

Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

  * One that silences it from 7pm to 9am daily on M-F,
  * And one that silences it all day on Sat-Sun.
  * Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

Performance Monitoring: Collecting APM Data
===========================================

Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:

.. code::python
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


.. note:: Using both ``ddtrace-run`` and manually inserting the Middleware has been known to cause issues.

Bonus: Service vs Resource?
----------------------------

What is the difference between a Service and a Resource?

Dashboard: Unified APM and Metrics
===================================

Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

Please include your fully instrumented app in your submission, as well.

Final Question:
================


Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?


How to prepare your answers
===========================

If you have a question, create an issue in this repository.

To submit your answers:

Fork this repo.

.. Answer the questions in answers.md

.. Commit as much code as you need to support your answers.

.. Submit a pull request.

.. Don't forget to include links to your dashboard(s), even better links and screenshots

Troubleshooting Tips
=====================


Sending a flare
----------------

.. code-block::bash
	datadog-agent flare
	Please enter your email:
	jitkelme@gmail.com
	Asking the agent to build the flare archive.
	/var/folders/kk/r7wkm6_10nd6hr90cvq2dclw0000gp/T/datadog-agent-2020-04-12-14-58-12.zip is going to be uploaded to Datadog
	Are you sure you want to upload a flare? [y/N]
	y
	Your logs were successfully uploaded. For future reference, your internal case id is 330337


Useful Resources
=================

Pycharm remote interpreter
''''''''''''''''''''''''''

Configure Pycharm to run the code using the Datgod embedded python. Make your user id a member of the ``dd-agent`` group: ``$ sudo usermod -a -G dd-agent bpabon``
see https://www.jetbrains.com/help/pycharm/create-ssh-configurations.html?keymap=secondary_macos&section=macOS

Running multiple MySQL on Mac OS X
https://stackoverflow.com/questions/51189634/installing-mariadb-with-mysql-on-mac

MariaDB docker hub
https://hub.docker.com/_/mariadb

Using Containerized Environments:
https://docs.datadoghq.com/agent/faq/template_variables/



References
==========

Don’t forget to read the [References](https://github.com/DataDog/hiring-engineers/blob/solutions-engineer/README.md#references)

How to get started with Datadog
-------------------------------

* [Datadog Help Center](https://help.datadoghq.com/hc/en-us)
* [Datadog overview](https://docs.datadoghq.com/)
* [Guide to graphing in Datadog](https://docs.datadoghq.com/graphing/)
* [Guide to monitoring in Datadog](https://docs.datadoghq.com/monitors/)

The Datadog Agent and Metrics
------------------------------

* [Guide to the Agent](https://docs.datadoghq.com/agent/)
* [Datadog Docker-image repo](https://hub.docker.com/r/datadog/docker-dd-agent/)
* [Writing an Agent check](https://docs.datadoghq.com/developers/write_agent_check/)
* [Datadog API](https://docs.datadoghq.com/api/)

APM
------

* [Datadog Tracing Docs](https://docs.datadoghq.com/tracing)
* [Flask Introduction](http://flask.pocoo.org/docs/0.12/quickstart/)




.. Internal meta data below....

.. |host_map_tags| replace:: Web UI Host Map
