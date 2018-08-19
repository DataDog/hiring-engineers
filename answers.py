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
