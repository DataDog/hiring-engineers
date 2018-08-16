3. Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

    Class (my_metric)
        min_collection_interval: 0
        max_collection_interval: 100
        return


4. Change your check's collection interval so that it only submits the metric once every 45 seconds.

    Class (my_metric)
        min_collection_interval: 0
        max_collection_interval: 100
        self.timeout_event: 45
        return


