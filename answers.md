Your answers to the questions go here.

I installed the agent on a Windows Server 2016 box. 

I used the Nuget Datadog.Trace package to send traces to datadaog, and the service application I wrote  
uses the ServiceStack .NET framework. You can see it hosted here;

http://datadog.rift.ie/metadata

It's a very basic app, just returning the stirngs as outlined in the Flask app. 

rift.ie is a url I use for personal projects and playing with different frameworks. 

I added screenshots which cover the tasks.

My ApiKey is 0abc30d0ee629946d0716b1f448b0a1a
And App Key is 9df11451b5e157dff64b13f79374e8cfc9f47b1d

_Can you change the collection interval without modifying the Python check file you created?_

There's a 'my_metric.yaml' file which goes into the C:\ProgramData\Datadog\conf.d folder with the same name as
your python script. You can set the `- min_collection_interval` value there.

If you check the agent logs you'll see output with your set interval

2019-04-04 21:26:27 CEST | INFO | (pkg/collector/scheduler.go:63 in Schedule) | Scheduling check custom_metric
2019-04-04 21:26:27 CEST | INFO | (pkg/collector/scheduler/scheduler.go:76 in Enter) | Scheduling check custom_metric with an interval of 45s


_What is the Anomoly graph testing?_

The anomaly algo lets you set a threshold value, if your metric deviates over or above this predicted range, it will
come up in the graph, it is also possible to set alerts to fire if the threshold is met. 

_Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:_

Screenshot added. 

_What is the difference between a Service and a Resource?_

A service is a set of resources that do the same job.  A web application may include the app itself
and a database application. 

It is a term for the seperate applications running within a single application to fulfill the applications purpose. 

A resourse is a particular action for a service. For a web app it might be an endpoint, for a database it might be a query.
Resources are grouped together under canonical names. 

_Is there anything creative you would use Datadog for?_

I like the idea of using Datadog to quantify demand by using logs and tracing on a large distributed system.
This could be applied to the housing market, flights, loans. Any indistry where the traffic itself is marketabe data,
so the logs and analytic data doesn't only become an insight into a system of applications, but 
gives real insight into a market or industry.  

I'm sure there are large companies using Datadog for this very purpose. I think it could be a way of marketing Datadog to 
industries outside tech, or even targeting people in a company outside technical roles. For instance, by using pattern matching
on requests you could instantly tell a large online retailer which product lines are the most popular, that kind of idea. 

Just from learning the small parts of it I did completing this task, I think the scope of the system is massive. 



 