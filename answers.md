**Collecting Metrics**

> Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

![dd_hostmap](https://user-images.githubusercontent.com/7505624/149841596-0256e6cf-7e5b-4611-a698-5b777e5185ef.png)

> Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

I installed a PostgreSQL database.

![dd_psql](https://user-images.githubusercontent.com/7505624/149823610-b0c8bf30-04b3-4c0c-ae51-914f5380ef3e.png)

After that I installed the Datadog integration for PostgreSQL.

![dd_psql_integration](https://user-images.githubusercontent.com/7505624/149823667-87499972-8112-4af8-9c16-b3ee1c5fc43a.png)

> Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

![dd_custom_my_metric_py](https://user-images.githubusercontent.com/7505624/149760908-99fd8369-40e4-4e6c-b418-419da0d45ac1.png)

> Change your check's collection interval so that it only submits the metric once every 45 seconds.
![dd_custom_my_metric_yaml](https://user-images.githubusercontent.com/7505624/149761004-c166b0d3-9115-4b5c-984c-2d3386dee4b9.png)


> **Bonus Question:** Can you change the collection interval without modifying the Python check file you created?

Based on the documentation here: https://docs.datadoghq.com/metrics/summary/#metrics-metadata, I was expecting that the collection interval for a metric can be overwritten in the Metrics Summary, metric metadata configuration, but when trying that, the min_collection_interval as defined in custom_my_metric.yaml was still applied. After removing the min_collection_interval from custom_my_metric.yaml, the default interval of 15 seconds was used. 

**Visualizing Data**

> Utilize the Datadog API to create a Timeboard that contains:
> - Your custom metric scoped over your host.
> - Any metric from the Integration on your Database with the anomaly function applied.
> - Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
> Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.

I wrote this script to create the Timeboard: 
```
#!/usr/bin/env python3

import requests

def create_dashboard(api_key, application_key):
    headers = {"Content-Type": "application/json","DD-API-KEY": api_key, "DD-APPLICATION-KEY": application_key}
    post_data = {
    "layout_type": "ordered",
    "title": "Visualizing Data",
    "widgets": [
        {
            "definition": {
                "requests": [
                    {
                        "q": "my_metric{host:vagrant}"
                    }
                ],
                "title": "Custom Metric",
                "type": "timeseries"
            }
        },
        {
            "definition": {
                "requests": [
                    {
                        "q": "anomalies(postgresql.rows_returned{host:vagrant}, 'basic', 2)"
                    }
                ],
                "title": "PostgreSQL rows returned + anomaly function",
                "type": "timeseries"
            }
        },
        {
            "definition": {
                "requests": [
                    {
                        "q": "my_metric{host:vagrant}.rollup(sum,3600)"
                    }
                ],
                "title": "Custom Metric Sum Last Hour",
                "type": "timeseries"
            }
        }
    ]
}
    response = requests.post("https://api.datadoghq.eu/api/v1/dashboard",headers=headers, json=post_data)
    print(response.json())

if __name__ == "__main__":
    application_key = "REMOVED"
    api_key = "REMOVED"
    create_dashboard(api_key, application_key)
```
> Once this is created, access the Dashboard from your Dashboard List in the UI:

![dd_dashboard](https://user-images.githubusercontent.com/7505624/149829529-73ccb7de-5046-47a8-8007-1e9df510bc43.png)

Link to the dashboard: https://app.datadoghq.eu/dashboard/jt9-7a4-h5n/visualizing-data

> Set the Timeboard's timeframe to the past 5 minutes
> Take a snapshot of this graph and use the @ notation to send it to yourself.

![dd_snapshot](https://user-images.githubusercontent.com/7505624/149829715-6e457def-ef69-48ae-affe-1b4ff6ead036.png)

> **Bonus Question:** What is the Anomaly graph displaying?


**Monitoring Data**

> Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:
> - Warning threshold of 500
> - Alerting threshold of 800
> - And also ensure that it will notify you if there is No Data for this query over the past 10m.

Link to the monitor: https://app.datadoghq.eu/monitors/4026348

Configuration of the thresholds. 

![dd_monitor1](https://user-images.githubusercontent.com/7505624/149833528-78421c97-a01c-4814-b34a-8c65931ba0ba.png)

> Please configure the monitor’s message so that it will:
> - Send you an email whenever the monitor triggers.
> - Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
> - Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.

Configuration of the messages.

![dd_monitor2](https://user-images.githubusercontent.com/7505624/149833565-ff1ebedd-1192-4bef-a332-ff671366e512.png)

> When this monitor sends you an email notification, take a screenshot of the email that it sends you.

Alert email sent to me by the monitor.

![dd_alert](https://user-images.githubusercontent.com/7505624/149833144-dfc61e2f-cf6c-42d1-87cf-2a1410402673.png)

> Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:
> - One that silences it from 7pm to 9am daily on M-F,
> - And one that silences it all day on Sat-Sun.
> - Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

I was able to schedule downtimes via Monitors > Manage Downtimes.

This is the downtime configuration that silences the monitor 7PM to 9AM Monday to Friday.

![dd_downtime_mo_fr](https://user-images.githubusercontent.com/7505624/149833665-ef631fd7-f3b9-4398-b449-0da4056c3f84.png)

This is the email confirmation that I received for the scheduled downtime.

![dd_downtime_mo_fr_email](https://user-images.githubusercontent.com/7505624/149833740-044d289e-072b-4f30-a876-935badd72265.png)

This is the downtime configuration that silences the monitor all day on Saturday and Sunday.

![dd_downtime_sat_sun](https://user-images.githubusercontent.com/7505624/149833780-037516ed-7676-4cde-bd78-cd3b9c07d100.png)

And this is the email confirmation I received.

![dd_downtime_sat_sun_email](https://user-images.githubusercontent.com/7505624/149833837-9c7e4e7c-d1c9-4fa1-88ca-768f84cab288.png)


**Collecting APM Data**

> Bonus Question: What is the difference between a Service and a Resource?

> Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

> Please include your fully instrumented app in your submission, as well.

