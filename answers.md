
Answers to Solutions engineer exercise

I used a spare Ubuntu 16.04 server i had in my office for this exercise.

Tools and learning resources I used to complete the exercise:
Datadogs website and online documentation
Youtube videos, mostly datadog but a few other providers as well
Some GitHub repos with sample code and the datadog opensource code as well as forums such as stackoverflow (but I did not find a lot there)
And lets not forget good old fashioned trial and error with the tooling.
I tried to find any additional resources through online learning tools suchs as Udemy, but there was nothing there.

I found the documention to be OK but lacking in detail that I would have prefered. Several sections are inconsistant with regards to version 5 vs version 6 of the agent. Small differences but to someone new to the product they lead to confusion when tryingt o self educate. Additional examples would have been welcomed as well, and also tools that I call "jump starters".  Simple exercises that provide a working base that can then be deconstructed and expanded to augment self learning. There were some instances in the documentation that were close but more would have been nice. I did reaed in the public Datadog analysis that ramp up can be a little challanging because of the small amount ot learning resources, but once learned it is a more intuitive tool. 




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

See screenshot of my alert definition:



