Collecting Metrics
==================



Create a custom Agent check
---------------------------

First, create a custom agent :term:check using the Web UI.
Next, configure the check to submit a metric named ``my_metric`` with a random value between 0 and 1000.

.. code-block::python
	class MyClass(AgentCheck):
		   self.monotonic_count(
				"my_metric",
				random.randint(0, 1000),
				tags=["env:dev", "metric_submission_type:monotonic_count", "admin_email:jikelme@gmail.com],
			)
Custom Agent Check
------------------

Here we create a custom Agent :term:`check <Check>` that submits a metric named my_metric with a random value between 0 and 1000.

.. note:: This involves some manual deployment steps at the moment.

Since I'm deploying on a remote host, I commit my ``custom_hello`` files to git,
push the feature branch so that I can pull them onto the remote host.
The directory structure is important, so I copy the files from my repo directory to the agent's ``conf.d`` and
``checks.d`` locations.

.. code-block::
	$ sudo -u dd-agent cp zero2datadog/checks.d/custom_hello.py /etc/datadog-agent/checks.d/custom_hello.py
	$ sudo -u dd-agent cp zero2datadog/conf.d/custom_hello.yaml /etc/datadog-agent/conf.d/custom_hello.yaml

If you have an IDE like PyCharm or VS Code, you can synchronize the file transfer.

.. figure:: ./_images/02_agent_paths.png
	:align: center
	:caption: Image courtesy of Brandon Roche https://www.reddit.com/r/datadog/comments/91hezx/custom_agent_check_help/

.. note:: This post clarifies the directory structure: https://www.reddit.com/r/datadog/comments/91hezx/custom_agent_check_help/

The ``custom_hello`` check
''''''''''''''''''''''''''

.. autoclass:: custom_hello
   :inherited-members:

Change the check's collection interval
----------------------------------------

Change your check's collection interval so that it only submits the metric once every 45 seconds.

Bonus: Can you change the collection interval without modifying the Python check file you created?
--------------------------------------------------------------------------------------------------

Can you change the collection interval without modifying the Python check file you created?
