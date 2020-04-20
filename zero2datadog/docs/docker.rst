.. _docker_agent:

`datadog-agent` Docker container
--------------------------------

Dockerhub has images of production and experimental releases of the agent. I run the image from the shell using:

.. code-block::bash
	DOCKER_CONTENT_TRUST=1 \
	docker run -d --name=dd_docker \
		-v /var/run/docker.sock:/var/run/docker.sock:ro \
		-v /proc/:/host/proc/:ro \
		-v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro \
		-e DD_API_KEY=$DD_API_KEY \
		datadog/agent:7  # I pin the image version because the road to hell is paved with the 'latest' tag.


Orchestrating multiple Containers
----------------------------------


I use ``docker-compose`` to combine the agent with Mariadb and also to isolate this experiment from the rest of my local machine.

.. literalinclude:: ../docker/docker-compose.yaml


For more complex arrangements of containers, such as testing the :term:APM features, the compose file can be much longer.

.. literalinclude:: ../docker/ddtrace-compose.yaml


Configure Auto-discovery for Docker containers
'''''''''''''''''''''''''''''''''''''''''''''''

https://docs.datadoghq.com/agent/docker/integrations/?tab=docker describes how to prepare the agent for discovering processes
running inside containers.
In this exercise, I use the auto-discovery template to pass credentials as environment variables and avoid including them in the file.
This reduces the risk of leaks when the files get checked into version control.
The stanza for Mariadb in my docker-compose.yaml looks like this:

.. code-block:: yaml

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

