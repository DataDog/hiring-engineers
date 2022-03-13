# DataDog Tech Assessment Sales Engineer
Andrew Hartzell

## Set up the Environment

Already have a version of Ubuntu installed on VirtualBox - will use that for this test.

**Install the DD agent**

<img src="/screenshots/dd_agent_install.png" alt="Ubuntu up and running" style="height: 125px; width:300px;"/>

**Appears in dashboard**

<img src="/screenshots/dd_dash.png" alt="Agent in Dash" style="height: 125px; width:300px;"/>

## Collecting Metrics


**Add tags in config file - host + tags on host map page in DD**
<br><img src="/screenshots/tagsyaml.png" alt="Add tags to yaml file" style="height: 125px; width:300px;"/>


**Restart Agent so updated tags will appear in host map**
```  
sudo systemctl restart datadog-agent.service
```
<img src="/screenshots/hostmaptags.png" alt="Tags appear in hostmap" style="height: 125px; width:500px;"/>  

**Install Database**
>Opted to use MySQL database for this part of the exercise.  Per the DD MySQL docs the MySQL check is included in the DD Agent and no additional install is needed on your SQL server.

Next steps in the SQL integration detail preparing your server by adding a datadog user and password.

<img src="/screenshots/dd_sql_user.png" alt="Create DD SQL user" style="height: 55px; width:691px;"/>  

I attempted to run the commands in the MySQL docs for verifying user creation and received syntax errors.  After spending a lot of time looking for answers I was still unable to figure out what the issue was and decided to move on to the next action item.

<img src="/screenshots/sql_users.png" alt="Show all SQL users" style="height: 200px; width:250px;"/><br> 


**Update User Privleges**

Agent privileges updated to collect metrics

<img src="/screenshots/update_user.png" alt="Update DD privleges" style="height: 54px; width:691px;"/> 

Grant access to performance_schema

<img src="/screenshots/perf_schema.png" alt="Give DD access to performance schema" style="height: 54px; width:691px;"/> 

Add configuration to collect SQL metrics

<img src="/screenshots/conf_yaml.png" alt="Add SQL metrics config" style="height: 200px; width:250px;"/> 

Restart the user agent to sending SQL metrics back DD.  Write some data to the SQL database so metrics populate.

<img src="/screenshots/mysql_metrics.png" alt="SQL appear in metrics" style="height: 100px; width:250px;"/> 


## Create Custom Agent Check
>Create a custom Agent check that submits a metric name my_metric with a random value between 0 and 1000.

Create the config file ```my_metric.yaml``` (needs to match the name of my_metric.py).

Navigate to ```/checks.d``` and create the python script.  Import the random module, use the snippet provided in the guide to import AgentCheck module.
Final step is create my_metric with random number between 1-1000.

<img src="/screenshots/my_metric.png" alt="my_metric.py script" style="height: 100px; width:250px;"/> 

Verify the check is running with: 
```
sudo -u dd-agent -- datadog-agent check my_metric
```

<img src="/screenshots/check_ok.png" alt="Check my_metric" style="height: 100px; width:225px;"/> 

My_metric appears in Metrics Dashboard:

<img src="/screenshots/metrics_dash.png" alt="Check my_metric in DD metrics dashboard" style="height: 100px; width:225px;"/> 

**Bonus Question**
> _Can you change the the collection interval without updating the python check file created?_
>>Yes! You can update the collection interval in the my_check.yaml file you created:

<img src="/screenshots/collection_interval.png" alt="Update collection interval in config file" style="height: 100px; width:225px;"/>


## Visualzing Data
> _Utlilize the Data Dog API to create a Timeboard that contains:_
> - Your custom metric scoped over your host.
> - Any metric from the integration on your database with the anomaly function applied.
> - Your custom metric with the rollup funciton applied to sum up all the points for the past hour into one bucket.
>

Quite a few pieces to navigate/work through here.  I initially started by looking at the API reference docs.  You can view the full script <a href="/python_code/dashboard.py">here</a>.

1. Install datadog-api-client. Then execute the script provided via the <a href="https://github.com/DataDog/datadog-api-client-python">python-github docs</a>.
2. Then I used the code provided in the <a href="https://docs.datadoghq.com/api/latest/dashboards/#create-a-new-dashboard">dashboard docs</a> to create a new dashboard to confirm I could get everything working, even if the data wasn't what we were looking for yet.
3. Through quite a bit of trial and error, and looking over the <a href="https://docs.datadoghq.com/dashboards/widgets/timeseries/">Timeseries widget</a> reference and JSON examples I was able to complete the custom metric part of the assignment.
4. Once I understood the structure/syntax I referenced the <a href="https://docs.datadoghq.com/dashboards/functions/algorithms/#anomalies">Algorithms</a> page to use the anamoly function for part 2.
5. Some more required reading was needed on the <a href="https://docs.datadoghq.com/dashboards/functions/rollup/">Rollup function</a> in order to complete step 3.

<a href=https://p.datadoghq.com/sb/2c4e08fe-9f4b-11ec-8590-da7ad0900002-47d32d434b9f94eb95e12c99588bfec3>Public Dashboard Link</a>

<img src="/screenshots/data_viz_dash.png" alt="Dashboard Visualization via API" style="height: 300px; width:600px;"/><br>

**Timeboard timeframe set to last 5 minutes**<br>

Using the GUI I updated the timeframe from 1 hour to 5 minutes, took a snapshot of ```my_metric``` graph and sent a message to myself.

<br><img src="/screenshots/5min_timeboard.png" alt="Timeboard 5 Min Timeframe" style="height: 330px; width:660px;"/>

**Snapshot sent to myself**

<img src="/screenshots/snapshot_timeboard.png" alt="Timeboard 5 Min Timeframe" style="height: 250px; width:330px;"/>

**Bonus Question**
>_What is the anomaly graph displaying?_
>>The anamoly algorithim is used to display the expcted behavior of a metric based on historical data.  The bounds param sets the width of the band and can be thought of as standard deviations.  Any data point falling out side of the gray band would be an anamoly.

## Monitoring Data
>_Create a metric monitor that watches the average of your custom metric and will alert if above the following values over the past 5 minutes:_
> - Warning threshold of 500
> - Alerting threshold of 800
> - Notify you if there is No Data for this query over the past 10m.

Creating monitors using the GUI - scheduled them as requested/described + added the notification email.  Since my host would not actually exceed the metrics on it's own I used the test notification option that pops up prior to saving your monitor, which appeared in my email immediately.

<br><img src="/screenshots/metric_monitor.png" alt="Metric Monitor" style="height: 200px; width: 400px;" />

<img src="/screenshots/notification.png" alt="Notification" style="height: 200px; width: 600px;" />

<img src="/screenshots/email_notification.png" alt="Email Notification" style="height: 300px; width: 300px;" />

**Bonus Question**
> _Set up two scheduled downtimes for this monitor:_
> - One that silences it from 7pm to 9am daily on M-F,
> - One that silences it all day on Sat-Sun.
> - Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

Scheduling downtime for the monitor was fairly intuitive.  I set up two - one for the weekdays, one for the weekend.  

<br><img src="/screenshots/weekday_downtime.png" alt="Weekday Downtime" style="height: 300px; width: 400px;" />
<img src="/screenshots/email_downtime.png" alt="Metric Monitor" style="height: 150px; width: 350px;" />
<img src="/screenshots/weekend_downtime.png" alt="Weekend Downtime" style="height: 200px; width: 400px;" />


## Collecting APM Data
> _Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution_

I installed Flask and DD Trace using the documenation I found <a href="https://docs.datadoghq.com/tracing/setup_overview/setup/python/?tab=containers">here</a> and <a href="https://app.datadoghq.com/apm/docs?architecture=host-based&language=python">here</a>.  I set up the configuration snippet to instrument the application that was provided as part of the exercise.

<img src="/screenshots/apm_config.png" alt="APM Config" style="height: 200px; width: 400px;" />

You can see an overview of APM services under the APM tab and get an overview of Requests, Errors, Latency etc.  I exported all of these modules to the cloned Infrastructure dashboard (renamed Infrastructure and APM Dash).  View <a href="https://p.datadoghq.com/sb/2c4e08fe-9f4b-11ec-8590-da7ad0900002-982f7c84669f87c67fe4a1f941e44978">the dashboard.</a>  View <a href="/python_code/app.py">the app.</a>


<img src="/screenshots/infra_apm_dash.png" alt="APM Config" style="height: 200px; width: 400px;" />

**Bonus Question**
> _What is the difference between a Service and a Resource?_
>> Per the APM Glossary page - a **Service** is a building block in microservice architecture.  As a broad definition, services group together endpoints, queries, or jobs for the purposes of building an application. For example, a group of URL endpoints may be grouped together under an API service. A **Resource** is a domain of an application.  RTesources are usually an instrumented endpoint, db query, or background job.  For example an ecommerce site may have web endpoints that handle things like checkouts, cart updates, purchases, etc.  The endpoints themselves are examples of resources.

## Final Question
> _Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!_
>
>_Is there anything creative you would use Datadog for?_
>>I love the outdoors and I especially like fishing in Massachusetts lakes.  Massachusetts has struggled with the health of its watersheds in the past, but recent conservation efforts coupled with modern technology have reatly improved watershed health in the last decade or so.  Each year Massachusetts sees an incredible number of migratory fish move from the sea into local freshwater lakes, and counting/monitoring the size of these migrations is used to understand the health of the ecosystem.  Many of the highest volume locations have installed "fish cams" that use image recognition applications to count the overall size of the migration.  Using DD to track and monitor performance of the devices and apps will ensure that local scientists can accurately monitor the migration and make informed decisions regarding the health of Massachusetts watersheds and the ecosystem.
