
# Collecting Metrics:

**Question: Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.**

**Answer:**

![alt text](https://github.com/grantker/hiring-engineers/blob/master/images/CollectingMetrics-1.png)
      

https://app.datadoghq.com/infrastructure/map?fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=availability-zone&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=true&palette=green_to_orange&paletteflip=false&node_type=host


**Question: Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.**

**Answer:**

![alt text](https://github.com/grantker/hiring-engineers/blob/master/images/CollectingMetrics-2.1.png)

![alt text](https://github.com/grantker/hiring-engineers/blob/master/images/CollectingMetrics-2.2.png)

https://app.datadoghq.com/account/settings#integrations/mongodb

https://app.datadoghq.com/screen/integration/13/mongodb---overview?page=0&is_auto=false&from_ts=1539676320000&to_ts=1539679920000&live=true



**Question: Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.**

**Answer:**

![alt text](https://github.com/grantker/hiring-engineers/blob/master/images/CollectingMetrics-3-4.png)

[Python check script - check_random.py](https://github.com/grantker/hiring-engineers/blob/master/DD-Scripts/check_random.py)


**Question: Change your check's collection interval so that it only submits the metric once every 45 seconds.**

**Answer:**

[Python check config - check_random.yaml](https://github.com/grantker/hiring-engineers/blob/master/DD-Scripts/check_random.yaml)


https://app.datadoghq.com/metric/explorer?live=true&page=0&is_auto=false&from_ts=1539676325551&to_ts=1539679925551&tile_size=m&exp_metric=my_metric&exp_scope=&exp_agg=avg&exp_row_type=metric


**Question:** Bonus Question Can you change the collection interval without modifying the Python check file you created?

**Answer:**

Yes ! By using min_collection_interval in the config yaml file .

![alt text](https://github.com/grantker/hiring-engineers/blob/master/images/CollectingMetricsBonus.png)

https://docs.datadoghq.com/developers/agent_checks/?tab=agentv6


# Visualizing Data:

**Question:** Utilize the Datadog API to create a Timeboard that contains:

Your custom metric scoped over your host.
Any metric from the Integration on your Database with the anomaly function applied.
Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.

![alt text](https://github.com/grantker/hiring-engineers/blob/master/images/VisualizingData-1.png)

Once this is created, access the Dashboard from your Dashboard List in the UI:

**Question: Set the Timeboard's timeframe to the past 5 minutes**

**Answer:**

![alt text](https://github.com/grantker/hiring-engineers/blob/master/images/VisualizingData-2.png)


https://app.datadoghq.com/dash/948267/visualizing-data-timeboard?live=false&page=0&is_auto=false&from_ts=1539666024608&to_ts=1539666324608&tile_size=m

**Question: Take a snapshot of this graph and use the @ notation to send it to yourself.**

**Answer:**

![alt text](https://github.com/grantker/hiring-engineers/blob/master/images/VisualizingData-3.png)

**Question: Bonus Question: What is the Anomaly graph displaying?**

**Answer:**

The Anomaly function is a statistical function used to determine if there are changes or outliers in seasonal behavior where a static threshold would not be suitable due to false positives .

In my example I am using a fairly stable Mongodb metric so you will not see anomalies however you can see the dynamic threshold as a grey band around the timeseries data 

# Monitoring Data:

**Question: Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.**

**Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:**

**Warning threshold of 500**
**Alerting threshold of 800**
**And also ensure that it will notify you if there is No Data for this query over the past 10m.**
**Please configure the monitor’s message so that it will:**

**Send you an email whenever the monitor triggers.**

**Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.**

**Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.**

**When this monitor sends you an email notification, take a screenshot of the email that it sends you.**

**Answer:**

![alt text](https://github.com/grantker/hiring-engineers/blob/master/images/MonitoringData-1.png)

https://app.datadoghq.com/monitors/6717201

**Question: Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:**

**One that silences it from 7pm to 9am daily on M-F,
And one that silences it all day on Sat-Sun.
Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.**

**Answer:**

![alt text](https://github.com/grantker/hiring-engineers/blob/master/images/MonitoringData-2.png)

# Collecting APM Data:

**Question: Bonus Question: What is the difference between a Service and a Resource?**

**A service is a set of application services i.e. Web Frontend , Database and middleware 
That ultimately work together to provide a service (Online banking)
A resource can be a URL or method in the service that helps facilitate this function .**


Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

**Answer:**

![alt text](https://github.com/grantker/hiring-engineers/blob/master/images/CollectingAPMData-1.png)

https://app.datadoghq.com/apm/traces?start=1539665960635&end=1539680360635&paused=false&env=production&traceID=10947544349931412619&spanID=17974173657378931260

# Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?

**Answer:**

Yes , in a simalar fashion to the above mentioned use cases ,
I think IOT monitoring in particular and renewable energy devices .
For example Solar panel power out-put , rain water collection , Heating and cooling efficency to build energy efficency profiles for buildings . I am especiallhy interested in this 
as I live in a country where we have issues around conservation of water and energy .

I believe these types of devices hooked up to sensors on raspbery PI or Arduino using DD to crunch the statistics could really be a game changer .


