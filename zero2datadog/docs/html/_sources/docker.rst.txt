Docker containers
=================


Dockerhub has images of production and experimental releases of the agent. I run the image from the shell using:

.. code-block::bash
	DOCKER_CONTENT_TRUST=1 \
	docker run -d --name=dd_docker \
		-v /var/run/docker.sock:/var/run/docker.sock:ro \
		-v /proc/:/host/proc/:ro \
		-v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro \
		-e DD_API_KEY=$DD_API_KEY \
		datadog/agent:7  # The road to hell is paved with the 'latest' tag.

I use ``docker-compose`` to combine the agent with Mariadb and also to isolate this experiment from the rest of my local machine.

.. include:: ../docker/docker-compose.yaml
