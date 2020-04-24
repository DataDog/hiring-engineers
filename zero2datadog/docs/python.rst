
Extend the Agent's Python environment
'''''''''''''''''''''''''''''''''''''

The Agent includes a complete Python environment, which you can extend with ``pip install ...``.
This is what that looks like using a Linux host:

.. code-block:: bash
	$ sudo -Hu dd-agent /opt/datadog-agent/embedded/bin/pip install -U pyyaml
