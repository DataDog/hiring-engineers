Setup the DataDog project
==========================


Then, sign up for Datadog (use “Datadog Recruiting Candidate” in the “Company” field),
get the Agent reporting metrics from your local machine.
The rest of the exercises will work best on a Linux host
either via Vagrant/Virtualbox or a bare metal VM, but not Docker Desktop for Mac.


Configure the DataDog agent
---------------------------

The agent will read configuration info from two sources:

	* The ``datadog.yaml`` file for general agent-specific details. It looks like

.. code-block::

	hostname: gearbox09.dev.controlplane.info
	tags:
	  - environment: dev
	  - admin_email: jitkelme@gmail.com
	  - os: ubuntu-bionic
	  - host: gearbox09
	env: dev
	log_level: 'info'

and then it will scan the contents of the ``conf.d`` folder, looking for ``conf.yaml`` files. For example, this is a
config file for MySQL:

.. code-block::

	init_config:

	instances:
	- server: 127.0.0.1
	user: datadog
	pass: <redacted>
	port: "3306"
	options:
	replication: false
	galera_cluster: true
	extra_status_metrics: true
	extra_innodb_metrics: true
	extra_performance_metrics: true
	schema_size_metrics: false
	disable_innodb_metrics: false


There are examples for most integrations in the ``~/.datadog-agent/etc/conf.d/`` directory.




