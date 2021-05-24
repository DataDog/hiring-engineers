## Collecting Metrics:
The tags were added by updating the tags attribute in the yaml file located at `/etc/datadog-agent/datadog.yaml`:
<br />
<img src="/images/update_tags.png" width="500">

Verified that the tags were changed on the application:
<br />
<img src="/images/verify_tags.png" width="500">

Installed  MongoDB and the datadog integration for MongoDB is already installed into the agent as noted [here](https://docs.datadoghq.com/integrations/mongo/?tab=standalone). I was able to verify that the integration worked by running a check:
<br />
<img src="/images/verify_mongo.png" width="500">

Created a custom agent check named my_metric that submitted a random value between 0 and 1000 and changed the collection interval to 45 seconds by updating the `/etc/datadog-agent/config.d/my_metric.yaml` file to add the time interval attribute:
<br />
<img src="/images/verify_custom_agent.png" width="500">

## Visualizing Data:

In order to create the dashboard using the api, I first researched Datadog's [dashboard api documentation](https://docs.datadoghq.com/api/latest/dashboards/#create-a-new-dashboard). I found example python code which I copied and replaced the configurations to fit the task requirements. Find the exact python script used in the `/scripts` folder.

I noticed the rollup function did not display information after creating the dashboard. I decided to add another 60s rollup dashboard to verify a successful rollup function.
<br />
<img src="/images/verify_dashboard.png" width="500">

According to the [anomaly documentation](https://docs.datadoghq.com/monitors/monitor_types/anomaly/), this timeseries graph attempts to predict the future based on previous data. It will then tell you when the data points are outside the bounds of those predictions.

## Monitoring Data

I created a monitor that with warnings on the random data that my_metric was transmitting. I set the alarm threshold for 800 and warning for 500. The alarm was taking too long to trigger so I reduced to one minute. After successfully triggering I increase it to 10 minutes.
<br />
<img src="/images/verify_monitor.png " width="500">


## Collecting APM Data:

I noticed that the versions were all different so I updated everything and specified python3:
```
sudo -H pip3 install --upgrade pip
pip install ddtrace
ddtrace-run python3 app.py
```
 
 I was still receiving this error:
 ![Error apm data](/images/error_flask.png "Error apm data)

 Ultimately, I decided that the issue was with the VM and the way it was loading in the python modules. It was taking too long to troubleshoot so I decided to use my native MacOS for this portion. I installed the agent on my machine and setup the apm via the steps [here](https://docs.datadoghq.com/tracing/setup_overview/setup/python/?tab=containers)

I enable the apm configuration in the `/opt/datadog-agent/etc/datadog.yaml` configuration file to enable the settings as stated in the documentation. The APM service took a long time to start appearing in my console but the data did show up eventually.
<br />
<img src="/images/verify_flask_running.png" width="500">

And the traces in the flask application:
<br />
<img src="/images/verify_apm.png" width="500">

## Final Question:
If I had datadog available I would use it to learn and monitor plant growth. One of my hobbies is to grow plants but unfortunately I learned early on that I did not have a green thumb. I have bought some auto-planters that could do a lot of the work for me but found that it was too expensive. I have even built one myself using an Arduino. I would use Datadog to monitor many metrics that are directly related with plant growth. The anomoly detection feature would be great to find any datapoints that may be killing plants.