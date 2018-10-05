# Visualizing Data

Create a timeboard that displays the metrics collected.

### Custom metric scoped on host:vagrant

1. Navigate the Datadog interface: Dashboards > New Dashboard

2. Specify Dashboard name and choose **New Timeboard**.

3. Create a new graph by dragging the timeseries icon to the Timeboard.

4. Click on the JSON editor and copy-paste the configuration:

    ```
    {
      "viz": "timeseries",
      "status": "done",
      "requests": [
        {
          "q": "avg:my_check{host:vagrant}",
          "type": "line",
          "style": {
            "palette": "dog_classic",
            "type": "solid",
            "width": "normal"
          },
          "conditional_formats": [],
          "aggregator": "avg"
        }
      ],
      "autoscale": true
    }
    ```
    JSON config [here](../scripts/average_check.json).

    Output:
    
    ![Alt text](../images/2_metric_avg.png?raw=true "Custom metric scoped on host:vagrant")

### Anomaly detection on postgresql.percent_usage_connections

1. Create another timeseries graph copy-paste the following configuration on the JSON editor:

    ```
    {
      "viz": "timeseries",
      "requests": [
        {
          "q": "anomalies(avg:postgresql.percent_usage_connections{host:vagrant}, 'basic', 2)",
          "type": "line",
          "style": {
            "palette": "dog_classic",
            "type": "solid",
            "width": "normal"
          },
          "conditional_formats": [],
          "aggregator": "avg"
        }
      ],
      "autoscale": true,
      "status": "done"
    }
    ```
    JSON config [here](../scripts/anomaly_db.json).

    Output:
    
    ![Alt text](../images/2_anomaly.png?raw=true "Anomaly detection on postgresql.percent_usage_connections")

### Using Rollup function on the custom metric

Sums up all the points for the past hour into one bucket.

1. Create another timeseries graph copy-paste the following configuration on the JSON editor:

    ```
    {
      "viz": "timeseries",
      "status": "done",
      "requests": [
        {
          "q": "avg:my_check{host:vagrant}.rollup(sum, 60)",
          "type": "line",
          "style": {
            "palette": "dog_classic",
            "type": "solid",
            "width": "normal"
          },
          "conditional_formats": [],
          "aggregator": "avg"
        }
      ],
      "autoscale": true
    }
    ```
    JSON config [here](../scripts/rolledup_check.json).

    Output:
    
    ![Alt text](../images/2_rolledup.png?raw=true "Using Rollup function on the custom metric")

### Setting the Timeboard's timeframe to the past 5 minutes
To set the timeframe to the last 5 minutes, drag on the map directly and select the last 5 minutes.

Output:

![Alt text](../images/2_five_minutes.png?raw=true "Set the Timeboard's timeframe to the past 5 minutes")

### Taking a snapshot of a graph and using the @ notation to notify someone
To send a snapshot, click on the camera button on top of the graph. Use the @ notation to indicate the recipient of the notification.

Interface:

![Alt text](../images/2_at_notation.png?raw=true "Taking a snapshot of a graph and using the @ notation to notify someone")

Sample Notification:

![Alt text](../images/2_sample_email.png?raw=true "Sample Notification")

### What is the Anomaly graph displaying?

The Anomaly graph displays the results of Datadog's Anomaly detection feature.

Anomaly detection is an algorithmic feature that allows you to identify when a metric is behaving differently than it has in the past, taking into account trends, seasonal day-of-week and time-of-day patterns. It is well-suited for metrics with strong trends and recurring patterns that are hard or impossible to monitor with threshold-based alerting.

For more information, read about Anomaly detection [here](https://docs.datadoghq.com/monitors/monitor_types/anomaly/).
