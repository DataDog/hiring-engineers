.. _docker_agent:

`datadog-agent` Docker container
--------------------------------

It's possible to do this exercise using just a single agent running on the host, however I like using different combinations of packages,
and I can more easily keep a portable collection of files. To keep my local config outside of source
control, I set up a local config directory:

.. literalinclude:: local_tree.txt


 and insert it using an environment variable ``DD_CONFIG_HOME``:

.. literalinclude:: ../docker/datadog/Dockerfile



Orchestrating multiple containers
----------------------------------


I use ``docker-compose`` to combine the agent with Mariadb and also to isolate this experiment from the rest of my local machine.

.. literalinclude:: ../docker/docker-compose.yaml


For more complex arrangements of containers, such as testing the :term:APM features, the compose file can be much longer.

.. literalinclude:: ../docker/ddtrace-compose.yaml


Configure Auto-discovery for Docker containers
'''''''''''''''''''''''''''''''''''''''''''''''

In this exercise, I use the auto-discovery template to pass credentials as environment variables and avoid including them in the file.
This reduces the risk of leaks when the files get checked into version control.
https://docs.datadoghq.com/agent/docker/integrations/?tab=docker describes how to prepare the agent for discovering processes
running inside containers.

