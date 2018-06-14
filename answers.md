### Setting Up the environment:
We used vagrant along with virtual box for this task. For the guest machine we choose Ubuntu 16.04
### Collecting Metrics: 
#### 1. Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog 
For this task, we added the tags in the config file on the host, under /etc/datadogagent/datadog.yaml:

![screenshot](/images/img1.png)

Making this modification wasn’t particularly complicated, we had to wait a while before we can see the modification in HostMap.

![screenshot](/images/img2.png)

#### 2. Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database. 
We choose to installe MySQL on the host, and its associated Datadog integration.
The integration process was very clear and easy to follow, except the config file path 
that was not correct: conf.d/mysql.yaml when it is conf.d/mysql.d/conf.yaml

![screenshot](/images/img3.png)

Once we made the configuration, we run the check to see if everything is ok:

![screenshot](/images/img4.png)

#### 3. Create a custom Agent check that submits a metric named my metric with a random value between 0 and 1000. 
After reading the documentation of how to create a custom agent check, we created a custom agent check that creates a random value between 0 & 1000 named "my metric".

![screenshot](/images/img5.png)

Check that the metric is running correctly:

![screenshot](/images/img6.png)

Once this is done, we visualize the my metric metric through the WEB UI.

![screenshot](/images/img7.png)

#### 4. Change your check's collection interval so that it only submits the metric once every 45 seconds. 
We thought about adding a wait timer in the python code, this will stop the code 45s every time before submitting the metric.

![screenshot](/images/img8.png)

#### 5. Bonus Question Can you change the collection interval without modifying the Python check file you created? 
It is mentioned in the documentation that the collection interval can be configured int the YAML files using min collection interval.
datadog-agent/conf.d/my metric.d/my metric.yaml

![screenshot](/images/img9.png)

### Visualizing Data: 
#### 1. Utilize the Datadog API to create a Timeboard that contains:
 - Your custom metric scoped over your host.
 - Any metric from the Integration on your Database with the anomaly function applied.
 - Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket 

It took me a while to read and understand how the Datadog API works, to make the query I sometimes use the graphic UI to understand the syntax.

This is the timeboard code along with anomaly detection:

![screenshot](/images/img10.png)

#### 2. Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard. 
Done
#### 3. Once this is created, access the Dashboard from your Dashboard List in the UI:

- Set the Timeboard's timeframe to the past 5 minutes 

![screenshot](/images/img11.png)

We access the newly created Dashboard, and adjust the Tiemframe to the past 5 minutes.
#### 4. Take a snapshot of this graph and use the @ notation to send it to yourself. 
All we had to do is to simply choose the camera icon, add your name to the ‘@’ notation to send it to your account.

![screenshot](/images/img12.png)
![screenshot](/images/img13.png)

#### 5. Bonus Question: What is the Anomaly graph displaying? 
Anomaly graph is used to determine when a metric is behaving abnormally, the abnormal behavior is determined based on the past metric values. It will display the anomaly of the metric behavior.

### Monitoring Data: 
#### 1. Create a new Metric Monitor that watches the average of your custom metric (my metric) and
will alert if it’s above the following values over the past 5 minutes:
- Warning threshold of 500
- Alerting threshold of 800
- And also ensure that it will notify you if there is No Data for this query over the past 10m.

![screenshot](/images/img14.png)

Please configure the monitor’s message so that it will:

- Send you an email whenever the monitor triggers.
- Create different messages based on whether the monitor is in an Alert, Warning, or No Data
state.
- Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.

![screenshot](/images/img15.png)

When this monitor sends you an email notification, take a screenshot of the email that it sends
you. 

#### 2. Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted
when you are out of the office. Set up two scheduled downtimes for this monitor:
- One that silences it from 7pm to 9am daily on M-F,
- And one that silences it all day on Sat-Sun.

![screenshot](/images/img16.png)
![screenshot](/images/img17.png)

Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

![screenshot](/images/img18.png)
![screenshot](/images/img19.png)

When the downtime starts: 

![screenshot](/images/img20.png)

### Collecting APM Data: 
#### 1. Bonus Question: What is the difference between a Service and a Resource? 
A service is a set of processes that do the same job, for example database services or webapp services. While a resource is a particular action for a service.
#### 2. Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics. 
For this APM configuration, we started by installing dd-trace, blinker and flask for pyton using pip and then setting up the APM configuration in datadog.yaml (enable APM and set env to prod) :

![screenshot](/images/img21.png)

Then we run the flask app using dd-trace :

![screenshot](/images/img22.png)

However, in our datadog UI we were unable to see the APM metrics, even though we can see the trace agent services receiving bytes:

![screenshot](/images/img23.png)

We tried several configurations (in datadog.yaml and the app code), but we couldn't get the APM to start.

![screenshot](/images/img25.png)

[Dasboard URL](https://app.datadoghq.com/dash/826035/hadhemis-timeboard-2-jun-2018-1944?live=true&page=0&isauto=false&fromts=1528491582880&tots=1528664382880&tilesize=m) 

![screenshot](/images/img24.png)

### Final Question:

#### Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!Is there anything creative you would use Datadog for?

One of the ways to use Datadog would be to monitor how much time people spend on social media and games on their smartphones, 
it can be set to trigger alerts when the time spent is above a certain limit. 
It can also be used to monitor medical devices (heart device, glucose device,...) in hospitals or at home, 
to notify their relatives if anything is wrong or if there is any abnormal activity.
