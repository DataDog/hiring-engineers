Setup the DataDog project
==========================


Then, sign up for Datadog (use “Datadog Recruiting Candidate” in the “Company” field),
get the Agent reporting metrics from your local machine.
The rest of the exercises will work best on a Linux host
either via Vagrant/Virtualbox or a bare metal VM, but not Docker Desktop.


Configure the DataDog agent
---------------------------

Provide the agent with the details it needs to receive data from MariaDB. Edit the ``~/.datadog-agent/etc/conf.d/mysql.d/conf.yaml``.
In my case, it looks like this:

.. code-block::yaml

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
		  galera_cluster: false
		  extra_status_metrics: true
		  extra_innodb_metrics: true
		  extra_performance_metrics: true
		  schema_size_metrics: false
		  disable_innodb_metrics: false



Using Docker containers
-----------------------------

.. include:: docker.rst


