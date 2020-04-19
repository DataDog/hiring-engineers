
Performance Monitoring: Collecting APM Data
===========================================

Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:

.. code-block::python
	from flask import Flask
	import logging
	import sys

	# Have flask use stdout as the logger
	main_logger = logging.getLogger()
	main_logger.setLevel(logging.DEBUG)
	c = logging.StreamHandler(sys.stdout)
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	c.setFormatter(formatter)
	main_logger.addHandler(c)

	app = Flask(__name__)

	@app.route('/')
	def api_entry():
		return 'Entrypoint to the Application'

	@app.route('/api/apm')
	def apm_endpoint():
		return 'Getting APM Started'

	@app.route('/api/trace')
	def trace_endpoint():
		return 'Posting Traces'

	if __name__ == '__main__':
		app.run(host='0.0.0.0', port='5050')


.. note:: Using both ``ddtrace-run`` and manually inserting the Middleware has been known to cause issues.

Bonus: Service vs Resource?
----------------------------

What is the difference between a Service and a Resource?

Dashboard: Unified APM and Metrics
===================================

Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

.. figure:: _images/bits.png
	:align: center
	:caption: APM and Infrastructure Metrics

.. pending

Please include your fully instrumented app in your submission, as well.


