# Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

    Class (my_metric)
        min_collection_interval: 0
        max_collection_interval: 100
        return


# Change your check's collection interval so that it only submits the metric once every 45 seconds.

    Class (my_metric)
        min_collection_interval: 0
        max_collection_interval: 100
        self.timeout_event: 45
        return

 # Any metric from the Integration on your Database with the anomaly function applied.

    Class (my_metric)
        min_collection_interval: 0
        max_collection_interval: 100
        self.timeout_event: 45
        avg(last_1h):anomalies(avg:system.cpu.system{name:Jason}, 'basic', 3, direction='above', alert_window='last_5m', interval=20, count_default_zero='true') >= 1
        return

# Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
    Class (my_metric)
        min_collection_interval: 0
        max_collection_interval: 100
        self.timeout_event: 45
        "q": "avg:system.disk.free{*}.rollup(avg, 60)"
        return

# Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:
    from flask import Flask
    import logging
    import sys


    main_logger = logging.getLogger()
    main_logger.setLevel(logging.DEBUG)
    c = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    c.setFormatter(formatter)
    main_logger.addHandler(c)

    app = Flask(my_metric)

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

