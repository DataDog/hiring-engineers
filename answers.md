## Answers to [Questions](README.md)

### Level 0 (optional) - Setup an Ubuntu VM

Installed a fresh Rasbian image (debian flavor) on a SD card for a Raspberry PI 3 to kick the tires with Datadog
`curl -L -O https://downloads.raspberrypi.org/raspbian_latest`


### Level 1 - Collecting your Data

Signed up [Datadog](http://www.datadoghq.com) with my email: phriscage@gmail.com and ran through the Datadog agent install from [source](http://docs.datadoghq.com/guides/basic_agent_usage/source/) since I am running ARM linux (armv71)

* Install package dependencies:

	```
	sudo apt-get install sysstat -y
	```

* Install the Datadog agent:

	```
	DD_API_KEY=******************************** sh -c "$(curl -L https://raw.githubusercontent.com/DataDog/dd-agent/master/packaging/datadog-agent/source/setup_agent.sh)"
	```

* Nohup since there isn't system init scripts for Rasbian:

	```
	nohup /home/pi/.datadog-agent/bin/agent &
	```

* Tail the logs to see what's going on:

	```
	tail -f /home/pi/.datadog-agent/logs/*.log
	```

* What is an agent?

	An agent is an executable that runs on a client system that performs tasks and functions to collect data and metrics about the client before sending the data to a destination server. The Datadog agent aggregates data about the client’s system and application performance data based off user-defined configuration parameters.

* Add custom host tags to the master *datadog.conf* configuration:

	```
	...
	# Set the host's tags (optional)
	# tags: mytag, env:prod, role:database
	tags: phriscage, env:development, role:iot_node
	...
	```

* Verify the agent is reporting the data and host tags in the Host Map Dashboard

https://app.datadoghq.com/dash/integration/custom%3Atest?live=true&tpl_var_scope=host%3Athing1.fios-router.home&page=0&is_auto=false&from_ts=1494175120839&to_ts=1494178720839&tile_size=m

![Host Map page](images/host_map_page.png)

* Install MongoDB:

	```
	sudo apt-get install mongodb-server -y
	sudo systemctl enable mongodb
	```

* Configure Datadog agent for MongoDB integration:

	```
	mongo admin --eval 'db.addUser("datadog", "topsecret", true)'
	```

	```
	$ mongo admin --eval 'db.addUser("datadog", "topsecret", true)'
	MongoDB shell version: 2.4.10
	connecting to: admin
	{
		"user" : "datadog",
		"readOnly" : true,
		"pwd" : "25cec8dabe1e57938cd54715e308851d",
		"_id" : ObjectId("590e16df46a184e51fe94645")
	}
	```

* Verify the username exists and credentials work:

	```
	$ echo "db.auth('datadog', 'ntrQqBX2R0blu3OdlBPsNs5Q')" | mongo admin | grep -E "(Authentication failed)|(auth fails)" &&
	> echo -e "\033[0;31mdatadog user - Missing\033[0m" || echo -e "\033[0;32mdatadog user - OK\033[0m"
	datadog user - OK
	$
	```

* Copy the mongo.yaml.example configuration to mongo.yaml in the *agent/conf.d* directory and modify the server and tag with the new configuration

	```
	init_config:

	instances:
	  # Specify the MongoDB URI, with database to use for reporting (defaults to "admin")
	  # E.g. mongodb://datadog:LnCbkX4uhpuLHSUrcayEoAZA@localhost:27016/my-db
	  #- server: mongodb://user:pass@host:port/db-name
	  - server: mongodb://datadog:ntrQqBX2R0blu3OdlBPsNs5Q@localhost:27017
		tags:
		   - "env:development"
		   - "role:iot_node"
	...
	```

* Check your mongo configuration file is formatted correctly:

	```
	sh /home/pi/.datadog-agent/bin/agent configcheck
	```

	```
	mongo.yaml is valid
	All yaml files passed. You can now run the Datadog agent.
	```

* Verify the agent check is working:

	```
	sh /home/pi/.datadog-agent/bin/agent check mongo
	```

	```
	…
	Service Checks:
	[{'check': 'mongodb.can_connect',
	  'host_name': 'thing1.fios-router.home',
	  'id': 1,
	  'message': None,
	  'status': 0,
	  'tags': ['db:admin',
			   'env:development',
			   'role:iot_node',
			   'host:localhost',
			   'port:27017'],
	  'timestamp': 1494177462.202923}]
	Service Metadata:
	[{}]
		mongo (5.13.1)
		--------------
		  - instance #0 [OK]
		  - Collected 59 metrics, 0 events & 1 service check
	```

* SIGHUP the process to reload:

	```
	kill -HUP `pgrep supervisord`
	```

* Verify the new metrics are reporting in the Datadog dashboard:

https://app.datadoghq.com/screen/integration/mongodb

![MongoDB Dashboard](images/mongodb_dashboard.png)


* Create a new python script custom.py in the ‘agent/checks.d’ directory.
Create a custom class that inherits from ‘AgentCheck’ class and send a random value for ‘test.support.random’

	```
	""" Custom AgentCheck """
	from checks import AgentCheck
	from random import random


	class CustomCheck(AgentCheck):
		""" Simple check for sending a random value """

		def check(self, instance):
			value = random()
			self.log.info("Generated random value: '%s'" % value)
			self.gauge('test.support.random', value)
	```

* Create a custom custom.yaml configuration file. Place in the ‘agent/conf.d’ directory:

	```
	init_config:

	instances:
		[{}]
	```

* Run the agent to verify the custom check is working

	```
	sh /home/pi/.datadog-agent/bin/agent check custom
	```

	```
	…

	2017-05-07 17:16:22,005 | INFO | dd.collector | checks.custom(custom.py:11) | Generated random value: '0.58668851607'
	Metrics:
	[('test.support.random',
	  1494177382,
	  0.5866885160699251,
	  {'hostname': 'thing1.fios-router.home', 'type': 'gauge'})]
	Events:
	[]
	Service Checks:
	[]
	Service Metadata:
	[{}]
		custom (5.13.1)
		---------------
		  - instance #0 [OK]
		  - Collected 1 metric, 0 events & 0 service checks
	```

* SIGHUP the process to reload:

	```
	kill -HUP `pgrep supervisord`
	```

* Verify the new metrics are reporting in the Datadog dashboard:

https://app.datadoghq.com/infrastructure/map?fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=none&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=false&palette=green_to_orange&paletteflip=false&host=293133905&app=test

![Host Map Custom](images/host_map_custom_page.png)


### Level 2 - Visualizing your Data

* Clone the MongoDB dashboard and add the test.support.custom metric.

https://app.datadoghq.com/screen/181511/mongodb--custom-metric

![MongoDB Custom Metric](images/mongodb_custom_metric_dashboard.png)


* Bonus question: What is the difference between a timeboard and a screenboard?

A timeboard is a type of Datadog dashboard with all graphs scoped to the same time period. The graphs are displayed in a grid-like fashion to assist in troubleshooting and correlation of events. This enables users to adjust the time period for the timeboard and all the graphs time frames shift in union.

A screenboard is a type of Datadog dashboard that provides more flexibility than a timeboard. The components of a screenboard are created with drag-and-drop widgets that can have customized time periods for each widget.

* Take a snapshot of your `test.support.random` graph and draw a box around a section that shows it going above 0.90. Make sure this snapshot is sent to your email by using the @notification
I created a screenshot and tagged with @notification, but never received any notification emails

![Custom Metric Notification](images/custom_metric_notification.png)
![Event Notifications Dashboard](images/event_notification_dashboard.png)


### Level 3 - Alerting on your Data

* Set up a monitor on this metric that alerts you when it goes above 0.90 at least once during the last 5 minutes
* Bonus points:  Make it a multi-alert by host so that you won't have to recreate it if your infrastructure scales up.

![Custom Metric Alert](images/custom_metric_alert.png)

* Give it a descriptive monitor name and message (it might be worth it to include the link to your previously created dashboard in the message).  Make sure that the monitor will notify you via email.

![Custom Metric Monitor](images/custom_metric_monitor.png)

* This monitor should alert you within 15 minutes. So when it does, take a screenshot of the email that it sends you.

![Custom Metric Monitor Email](images/custom_metric_monitor_email.png)

* Bonus: Since this monitor is going to alert pretty often, you don't want to be alerted when you are out of the office. Set up a scheduled downtime for this monitor that silences it from 7pm to 9am daily. Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

![Custom Metric Monitor Downtime](images/custom_metric_monitor_downtime.png)
![Custom Metric Monitor Downtime Email](images/custom_metric_monitor_downtime_email.png)

