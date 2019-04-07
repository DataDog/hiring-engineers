Your answers to the questions go here.

I installed the agent on a Windows Server 2016 box. 

I used the Nuget Datadog.Trace package to send traces to datadaog, and the service application I wrote  
uses the ServiceStack .NET framework. You can see it hosted here;

http://datadog.rift.ie/metadata

It's a very basic app, just returning the strings as outlined in the Flask app. 

rift.ie is a url I use for personal projects and playing with different frameworks. 

I added screenshots which cover the tasks.

My ApiKey is 0abc30d0ee629946d0716b1f448b0a1a  
And App Key is 9df11451b5e157dff64b13f79374e8cfc9f47b1d

_**Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.**_

![Host map screenshot with tags](https://github.com/DataDog/hiring-engineers/blob/c8b76cffd3ab13e3885752e26bdbef09580aaea5/screenshots/host_map.png?raw=true)

_**Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.**_

![Installed Postgres Database Image](https://github.com/DataDog/hiring-engineers/blob/c8b76cffd3ab13e3885752e26bdbef09580aaea5/screenshots/postgres_check_running.png?raw=true)

_**Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.**_

![my_metric UI screenshot](https://github.com/DanielFitzgerald/hiring-engineers/blob/daniel-fitzgerald-solutions-engineer-test/screenshots/my_metric_dashboard.png?raw=true)

_**Can you change the collection interval without modifying the Python check file you created?**_

There's a 'my_metric.yaml' file which goes into the C:\ProgramData\Datadog\conf.d folder with the same name as
your python script. You can set the `- min_collection_interval` value there.

If you check the agent logs you'll see output with your set interval

2019-04-04 21:26:27 CEST | INFO | (pkg/collector/scheduler.go:63 in Schedule) | Scheduling check custom_metric\
2019-04-04 21:26:27 CEST | INFO | (pkg/collector/scheduler/scheduler.go:76 in Enter) | Scheduling check custom_metric with an interval of 45s

_**Utilize the Datadog API to create a Timeboard that contains...:**_

https://app.datadoghq.com/dashboard/ni3-m43-8rt/timeboard-dan?tile_size=m&page=0&is_auto=false&from_ts=1554664080000&to_ts=1554667680000&live=true

![timeboard screenshot](https://github.com/DanielFitzgerald/hiring-engineers/blob/daniel-fitzgerald-solutions-engineer-test/screenshots/time_board_request.png?raw=true)

My Metric and Host\
https://app.datadoghq.com/dashboard/w2p-k8w-dnc/timeboard?from_ts=1554666315000&is_auto=false&live=true&page=0&tile_size=xl&to_ts=1554667215000

Postgres Connections and Anomaly\
https://app.datadoghq.com/dashboard/7v3-zsc-isd/database-connection-metric-with-anomoly?tile_size=m&page=0&is_auto=false&from_ts=1554663660000&to_ts=1554667260000&live=true

my_metric Rollup\
https://app.datadoghq.com/dashboard/mr6-t5z-udd/custom-metric-rollup?tile_size=m&page=0&is_auto=false&from_ts=1554663720000&to_ts=1554667320000&live=true

_**What is the Anomoly graph testing?**_

The anomaly algo lets you set a threshold value, if your metric deviates over or above this predicted range, it will
come up in the graph, it is also possible to set alerts to fire if the threshold is met. 

https://app.datadoghq.com/dashboard/7v3-zsc-isd/database-connection-metric-with-anomoly?tile_size=m&page=0&is_auto=false&from_ts=1554662400000&to_ts=1554666000000&live=true

_**Monitoring Data**_

_**Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:**_

Monitor
https://app.datadoghq.com/monitors/9385657\
Nightly
https://app.datadoghq.com/monitors#downtime?id=500514459\
Weekend
https://app.datadoghq.com/monitors#downtime?id=499122232

![alert screenshot](https://github.com/DanielFitzgerald/hiring-engineers/blob/daniel-fitzgerald-solutions-engineer-test/screenshots/metric_text_conditions.png?raw=true)

![alert email screenshot](https://github.com/DanielFitzgerald/hiring-engineers/blob/daniel-fitzgerald-solutions-engineer-test/screenshots/monitor_alert_email.png?raw=true)

_**Collecting APM Data:**_

You can hit these URLs to create the traces;
http://datadog.rift.ie/api/trace?format=json\
http://datadog.rift.ie/api/apm?format=json\
http://datadog.rift.ie/entry?format=json

Code\
https://github.com/DanielFitzgerald/hiring-engineers/blob/daniel-fitzgerald-solutions-engineer-test/src/DataDog.TechnicalTest/DataDog.TechnicalTest.ServiceInterface/MyServices.cs

Trace List\
https://app.datadoghq.com/apm/traces?start=1554664663893&end=1554668263893&paused=false&env=dev%3Adub

_**What is the difference between a Service and a Resource?**_

A service is a set of resources that do the same job.  A web application may include the app itself
and a database application. 

It is a term for the seperate applications running within a single application to fulfill the applications purpose. 

A resource is a particular action for a service. For a web app it might be an endpoint, for a database it might be a query.
Resources are grouped together under canonical names. 

_**Is there anything creative you would use Datadog for?**_

I like the idea of using Datadog to quantify demand by using logs and tracing on a large distributed system.
This could be applied to the housing market, flights, loans. Any indistry where the traffic itself is marketabe data,
so the logs and analytic data doesn't only become an insight into a system of applications, but 
gives real insight into a market or industry.  

I'm sure there are large companies using Datadog for this very purpose. I think it could be a way of marketing Datadog to 
industries outside tech, or even targeting people in a company outside technical roles. For instance, by using pattern matching
on requests you could instantly tell a large online retailer which product lines are the most popular, that kind of idea. 

Just from learning the small parts of it I did completing this task, I think the scope of the system is massive. 



 