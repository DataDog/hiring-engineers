
Answers to Solutions engineer exercise

I used a spare Ubuntu 16.04 server I had in my office for this exercise.

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
<img src="https://farm2.staticflickr.com/1774/44035401161_511f662ab7_o_d.png">

See following screenshot for added MySQL integration:
<img src="https://farm2.staticflickr.com/1831/43129368465_dc8be776fc_o_d.png">

Please see code for  the "my_metric" in repo.

See log detail and screenshot to confirm interval has been switched to 45 seconds.
<img src="https://farm2.staticflickr.com/1780/44035378421_e149da6191_o_d.png">

Collecting Metrics Bonus Question:
I do not beleive so, not without changing the globaly defined interval set within the agent itself. But I am not sure about this.
  
  
  

Visualizing Data:

See snapshot for custom metric scoped over my host, for MySQL metric with the anomaly function applied and or custom metric with the rollup function applied for one hour buckets::
<img src="https://farm2.staticflickr.com/1796/44035378851_e9e305f6eb_o_d.png">

See snapshot for the email I had sent to myself with the @notation
<img src="https://farm2.staticflickr.com/1817/29145566007_f28b4e4f2a_o_d.png">

Visualize Data Bonus Question:
The Anomaly function returns the usual results along with an "expected normal" range by using past data. They provide a "historical context" so you can see how the metric behaved in the past as well as a seperate "evaluation window" that is longer than the alerting window to provide some immediate context.


Monitoring Data:

See screen shot of email alert sent to my email. I tried using the {{host.name}} variable from the documentaion but it did not resolve into an IP or Hostname. Is this a problem in my definition or just a documentation issue? Repeated searches on Datadog site and broad internet searches turned up no additional hints.
<img src="https://farm2.staticflickr.com/1812/30166920618_7f0243571f_o_d.png">

See screenshot of my alert definition and subsequent email notification:
<img src="https://farm2.staticflickr.com/1811/44035377911_c0543c7f7c_o_d.png">

<img src="https://farm2.staticflickr.com/1792/44035378501_6571698302_o_d.png">

Collecting APM Data:
This task caused me the most trouble but it was of my own making. In the initial exercise I created a few tags, one of which was and env tag (env:yamltest). Little did I know that this would cause me issues down the line when trying to view my traces. I initially used the ddtrace-run command as guided by the datadog interface tooling. Everything seemed fine yet i couldnt see any trace data. I chatted brielfy with support and Brendan, both confirmed that my trace seemed to be set up correctly yet I still could see not data. I was advised to instead put the middleware code in the app and try again. I did, and got the same result. It wasn't until later when experimenting anyway I could that I realized that my env was defaulted to env:none ( as I later read in the documentation as well) and simply had to select my env:yamltest from the little dropdown box at the top of the traces screen, and poof there was all my data. A small but troubling mistake on my part.
<img src="https://farm2.staticflickr.com/1794/29097988477_f2203abbc9_o_d.png">

See my code "flask_app" in the repo.

Difference betwen a service and a resource:

A service is a set of processes that do the same job. For instance, a simple web application may consist of two services: A single webapp service and a single database service. Whereas a Resource is a particular action for a service.  For a web application: some examples might be a canonical URL, such as /user/home or a handler function like web.user.home (often referred to as “routes” in MVC frameworks).  For a SQL database: a resource is the query itself, such as SELECT * FROM users WHERE id = ?.


Final Question:
I imagine there is little limit to the monitoring of data that DataDog can provide. My thoughts immediately went to a DOD project I read about a few years back with Homeland Security. The goal was to install micro sensors all over the streets and rooftops of buildings in a city, making a massive network of real time air quality data (or possbily radiation detectors or known chemical agents.. etc). The sensors give data constantly with changes in weather and chemical densities. With a tool such as datadog you could  instrutment metrics, alerts and monitors to warn qagainst something as simple as poor air quality in a region to detecting the build up of radiation and idenitfy a possible dirty bomb. With triangualtion of the data you could even make accurate esitmates of where the pollutant is coming from, its estimated growth and path across the city, etc... In a world of IOT and BigData, DataDogs uses will only continue to grow.





