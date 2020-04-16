Custom Agent Check
------------------

Here we create a custom Agent :term:`check <Check>` that submits a metric named my_metric with a random value between 0 and 1000.

.. note::warning This involves some manual deployment steps at the moment.

Since I'm deploying on a remote host, I commit my ``custom_hello`` files to git,
push the feature branch so that I can pull them onto the remote host.
The directory structure is important, so I find it expedient to symlink the files from my repo directory to the agent's ``conf.d`` and
``checks.d`` locations.

.. code-block::
	$ sudo -u dd-agent ln -sf zero2datadog/checks.d/custom_hello.py /etc/datadog-agent/checks.d/custom_hello.py
	$ sudo -u dd-agent ln -sf zero2datadog/conf.d/custom_hello.yaml /etc/datadog-agent/conf.d/custom_hello.yaml


.. image:: https://cl.ly/2c30093D1B1Y
	image courtesy of Brandon Roche https://www.reddit.com/r/datadog/comments/91hezx/custom_agent_check_help/

.. note:: This post clarifies the directory structure: https://www.reddit.com/r/datadog/comments/91hezx/custom_agent_check_help/

The ``custom_hello`` check
''''''''''''''''''''''''''

.. autoclass:: custom_hello
   :inherited-members:


