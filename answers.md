
Answers to Solutions engineer exercise

I used a spare Ubuntu 16.04 server i had in my office for this exercise.

Tools and learning resources I used to complete the exercise:
Datadogs website and online documentation
Youtube videos, mostly datadog but a few other providers as well
Some GitHub repos with sample code and the datadog opensource code as well as forums such as stackoverflow (but I did not find a lot there)
And lets not forget good old fashioned trial and error with the tooling.
I also used the chat feature on datadogs website.
I tried to find any additional resources through online learning tools such as Udemy, but there was nothing there.

I found the documention to be OK but lacking in detail that I would have prefered. Several sections are inconsistant with regards to version 5 vs version 6 of the agent. Small differences but to someone new to the product they lead to confusion when trying to self educate. Additional examples would have been welcomed as well, and also tools that I call "jump starters".  Simple exercises that provide a working base that can then be deconstructed and expanded to augment self learning. There were some instances in the documentation that were close but more would have been nice. I did read on public forums for Datadog analysis that ramp up can be a little challenging because of the small amount of learning resources, but once learned it becomes more intuitive. 


Collecting Metrics:

See the following screenshot for the added tags:

See following screenshot for added MySQL integration:

See code and agent confirmation the "my_metric" functions properly.

See log detail and screenshot to confirm interval has been switched to 45 seconds.

Collecting Metrics Bonus Question:
I do not beleive so, not without changing the globaly defined interval set within the agent itself. But I am not sure about this.
  
  
  

Visualizing Data:

See snapshot for custom metric scoped over my host:

See Snapshot for MySQL metric with th anomaly function applied:

See snapshot for custom metric with the rollup function applied for one hour buckets:

See snapshot for 5 minute time window

See snapshot for the email I had sent to myself with the @notation

Visualize Data Bonus Question:
The Anomaly function returns the usual results along with an "expected normal" range by using past data. They provide a "historical context" so you can see how the metric behaved in the past as well as a seperate "evaluation window" that is longer than the alerting window to provide some immediate context.


Monitoring Data:

See screen shot of email alert sent to my email. I tried using the {{host.name}} variable from the documentaion but it did not resolve into an IP or Hostname. Is this a problem in my definition or just a documentation issue. Repeated searches on Datadog site and broad internet searches turned up no additional hints.

See screenshot of my alert definition and subsequent email notification:

Collecting APM Data:

See my flask_app code with the middleware inserted

Difference betwen a service and a resource:

A service is a set of processes that do the same job. For instance, a simple web application may consist of two services: A single webapp service and a single database service. Whereas a Resource is a particular action for a service.  For a web application: some examples might be a canonical URL, such as /user/home or a handler function like web.user.home (often referred to as “routes” in MVC frameworks).  For a SQL database: a resource is the query itself, such as SELECT * FROM users WHERE id = ?.


Final Question:
I imagine there is little limit to the monitoring of data that DataDog can provide. My thoughts immediately went to a DOD project I read about a few years back with Homeland Security. The goal was to install micro sensors all over the streets and rooftops of buildings in a city, making a massive network of real time air quality data (or possbily radiation detectors or known chemical agents.. etc). The sensors give data constantly with changes in weather and chemical densities. With a tool such as datadog you could  instrutment metrics, alerts and monitors to warn qagainst something as simple as poor air quality in a region to detecting the build up of radiation and idenitfy a possible dirty bomb. With triangualtion of the data you could even make accurate esitmates of where the pollutant is coming from, its estimated growth and path across the city, etc... In a world of IOT and BigData, DataDogs uses will only continue to grow.





