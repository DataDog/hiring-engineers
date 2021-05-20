## Collecting Metrics:
The tags were added by updating the tags attribute in the yaml file located at `/etc/datadog-agent/datadog.yaml`:
![Updated tags](/images/update_tags.png "Update tags image")

Verified that the tags were changed on the application:
![Verified tags](/images/verify_tags.png "Post tag verification")

Installed  MongoDB and the datadog integration for MongoDB is already installed into the agent as noted [here](https://docs.datadoghq.com/integrations/mongo/?tab=standalone). I was able to verify that the integration worked by running a check:
![Verified mongo](/images/verify_mongo.png "Post mongo verification")

Created a custom agent check named my_metric that submitted a random value between 0 and 1000 and changed the collection interval to 45 seconds by updating the `/etc/datadog-agent/config.d/my_metric.yaml` file to add the time interval attribute:
![Verified custom agent](/images/verify_custom_agent.png "Post mongo verification")




## Visualizing Data:
Utilize the Datadog API to create a Timeboard that contains:
* Your custom metric scoped over your host.
* Any metric from the Integration on your Database with the anomaly function applied.
* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.
Once this is created, access the Dashboard from your Dashboard List in the UI:
* Set the Timeboard's timeframe to the past 5 minutes
* Take a snapshot of this graph and use the @ notation to send it to yourself.
* **Bonus Question**: What is the Anomaly graph displaying?

In order to create the dashboard using the api, I first researched Datadog's [dashboard api documentation](https://docs.datadoghq.com/api/latest/dashboards/#create-a-new-dashboard). I found example python code which I copied and replaced the configurations to fit the task requirements. Find the exact python script used in the `/scripts` folder.

The 
##
![Verified custom agent](/images/verify_custom_agent.png "Post mongo verification")

According to the [anomaly documentation](https://docs.datadoghq.com/monitors/monitor_types/anomaly/), this timeseries graph attempts to predict the future based on previous data. It will then tell you when the data points are outside the bounds of those predictions.




## Monitoring Data

Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.
Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:
* Warning threshold of 500
* Alerting threshold of 800
* And also ensure that it will notify you if there is No Data for this query over the past 10m.
Please configure the monitor’s message so that it will:
* Send you an email whenever the monitor triggers.
* Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
* Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
* When this monitor sends you an email notification, take a screenshot of the email that it sends you.

## Collecting APM Data:


## Final Question: