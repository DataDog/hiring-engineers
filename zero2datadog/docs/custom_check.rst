Custom Agent Check
------------------

Here we create a custom Agent :term:`check <Check>` that submits a metric named my_metric with a random value between 0 and 1000.

Since I'm deploying on a remote host, I commit my ``custom_hello`` files to git,
push the feature branch so that I can pull them onto the remote host.
The agent looks for files in ``/etc/datadog-agent/checks.d/`` so I find it expedient to symlink the files from my repo :wdirectory
as the ``dd-agent``.

.. code-block::
	$ sudo -u dd-agent ln -sf custom_hello.py /etc/datadog-agent/checks.d/custom_hello.py
	$ sudo -u dd-agent ln -sf custom_hello.yaml /etc/datadog-agent/checks.d/custom_hello.yaml


.. autoclass:: custom_hello
   :inherited-members:

