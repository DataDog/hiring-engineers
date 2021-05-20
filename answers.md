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

In order to create the dashboard using the api, I first researched Datadog's [dashboard api documentation](https://docs.datadoghq.com/api/latest/dashboards/#create-a-new-dashboard). I found example python code which I copied and replaced the configurations to fit the task requirements. Find the exact python script used in the `/scripts` folder.

I noticed the rollup function did not display information after creating the dashboard. I decided to add another 60s rollup dashboard to verify a successful rollup function.
![Verified dashboard](/images/verify_dashboard.png "Post dashboard verification")

According to the [anomaly documentation](https://docs.datadoghq.com/monitors/monitor_types/anomaly/), this timeseries graph attempts to predict the future based on previous data. It will then tell you when the data points are outside the bounds of those predictions.

## Monitoring Data

I created a monitor that with warnings on the random data that my_metric was transmitting. I set the alarm threshold for 800 and warning for 500. The alarm was taking too long to trigger so I reduced to one minute. After successfully triggering I increase it to 10 minutes.

![Verified monitor](/images/verify_monitor.png "Post monitor verification")





## Collecting APM Data:

I noticed that the versions were all different so I updated everything and specified python3:
```
sudo -H pip3 install --upgrade pip
pip install ddtrace
ddtrace-run python3 app.py
```



## Final Question: