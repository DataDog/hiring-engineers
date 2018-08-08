
Answers to Solutions engineer exercise

I used a spare Ubuntu 16.04 server i had in my office for this exercise.




Collecting Metrics:

See the following screenshot for the added tags:

See following screenshot for added MySQL integration:

See code and agent confirmation the "my_metric" functions properly.

See log detail and screenshot to confirm interval has been switched to 45 seconds.

Collecting Metrics Bonus Question:
I do not beleive so, not without changing the globaly defined interval set within the agent itself. But I am not sure about this.
  
  
  

Visualizing Data:

See snapshot for custom metric scoped over my host:

See Snapshot for MySQL metric with th anomaly functino applied:

See snapshot for custom metric with the rollup functino applied for one hour buckets:

See snapshot for 5 minute time window

See snapshot for the email I had sent to myself with the @notation

Visualise Data Bonus Question:
The Anomaly function returns the usual results along with an "expected normal" range by using past data. They provide a "historical context" so you can see how the metric behaved in the past as well as a seperate "evaluation window" that is longer than the alerting window to provide some immediate context.




Monitoring Data:

