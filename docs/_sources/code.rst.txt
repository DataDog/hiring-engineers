Code for Exercises
===================

1. custom_my_metric_check.py

\

.. code-block::

    import random

    # try/expect block to make the custom check compatible with any version of the Agent

    try:
        #This will try to import the base class from new versions of the Agent
        from datadog_checks.base import AgentCheck
    except ImportError:
        #If the above fails this means the check is running in Agent version < 7
        from checks import AgentCheck

    __version__ = "1.0.0"

    class MyClass(AgentCheck):
        def check(self, instance):
            self.gauge('my_metric', random.randint(0,1000), tags=['env:dev','metric_submission_type:gauge','metric:my_metric'] + self.instance.get('tags', []))


\

2. custom_my_metric_check.yaml

\

.. code-block::

    init_config:

    instances:
        - min_collection_interval: 45

\

3. timeboard_data_exercise.py

\

.. code-block::

    from datadog import initialize, api

    options = {
        'api_key': 'YOUR_DD_API_KEY',
        'app_key': 'YOUR_DD_APP_KEY'
    }

    initialize(**options)

    title = 'Visualizing Data Exercise'
    widgets = [{
        'definition': {
            'type': 'timeseries',
            'requests': [
                 {'q': 'avg:my_metric{*}'}
             ],
            'title': 'Custom Metric Scoped Over Host'
        }},
        {
        'definition': {
            'type': 'timeseries',
            'requests': [
                {'q': 'anomalies(avg:mysql.performance.open_files{*}, "basic", 2)'}
            ],
            'title': 'MySql mysql.performance.open_files Anomaly Funtion'
            }},
        {
        'definition': {
            'type': 'timeseries',
            'requests': [
                {'q': 'sum:my_metric{*}.rollup(sum, 3600)'}
            ],
            'title': 'My_metric rolled up.'
        }
        }]
    layout_type = 'ordered'
    description = 'My_Metric Scoped Over Host.'
    is_read_only = True
    notify_list = ['bmello1487@gmail.com']
    template_variables = [{
        'name': 'host1',
        'prefix': 'host',
        'default': 'my-host'
    }]

    api.Dashboard.create(title=title,
                     widgets=widgets,
                     layout_type=layout_type,
                     description=description,
                     is_read_only=is_read_only,
                     notify_list=notify_list,
                     template_variables=template_variables)

\

4. flaskApp.py

\

.. code-block::

    from ddtrace import tracer
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


\




