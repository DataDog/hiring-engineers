Q: Can you change the collection interval without modifying the Python check file you created?


A: Yes, the yaml file that is related to the check can control the collection interval using the option "min_collection_interval".  It's context is slightly different depending on the version of the check

Q: What is the Anomaly graph displaying?


A: The Anomaly graph displays a metric that is behaving differently from the 'standard' value is it's had in the past.  This means the metric is averaged over a user defined period of time (for example, one week).  Then if the metric is different (by a user defined threshold) from that established threshold, it will be visually identified on the metrics graph (i.e. on a line graph the line will turn red is the anomaly is detected.  This process can also be used to send alerts to the team.

