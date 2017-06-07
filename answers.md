# Level 1

### The Agent

* The Agent is a piece of software that the user installs onto a host that transmits system metrics and application data to Datadog. The Agent is made up of the collector, which collects system metrics; dogstatsd, which allows the user to send custom application data; and the forwarder, which sends all of the data to Datadog over HTTPS.

### Host Map With Tags
![](./screenshots/hostmap_with_tags.png)

* I added a few example tags to my host, Kims-Macbook-Pro.local, in the Agent config file and viewed them on the Host Map.

### test.support.random Agent Check
    from checks import AgentCheck
    import random
    class RandomCheck(AgentCheck):
        def check(self, instance):
        self.gauge('test.support.random', random.random())
 
 * After installing the Datadog integration for PostgreSQL, I wrote the test.support.random Agent check. Here is the code from my random.py file in checks.d. 

# Level 2

### Cloned Postgres Dashboard w/ Additional Metrics
![](./screenshots/cloned_dashboard.png)

* I cloned my Postgres timeboard and added some additional metrics, including a count of databases and a graph of my test.support.random metric. 

### Dashboard Types
* Timeboards: all graphs are scoped to the same time, appear in a grid, and graphs can be shared individually
* Screenboards: more customizable layout, widgets can have different time frames, can be shared as an entire read-only entity

### test.support.random Graph Snapshot
![](./screenshots/snapshot.png)

* I took a snapshot of the test.support.random graph going above 0.9 and sent myself a notification. I liked the easy-to-use interface for pinpointing a specific segment of a graph and notifying a teammate about it.

# Level 3

### test.support.random Multi-Alert Monitor
![](./screenshots/multialert.png)

* I set up a multi-alert monitor on the test.support.random metric so that I would be notified if it went above 0.9 on any host within the past 5 minutes.

### Monitor Notification
![](./screenshots/monitor_notification.png)

* Next, I set up a notification message that would tell me which host the issue occurred on, send me a link to the relevant dashboard in the message body, and send an additional notification when the random value returned to "safe" levels.

### Monitor Email Received
![](./screenshots/monitor_email.png)

* I successfully received an email notification from the monitor.

### Downtime Scheduled
![](./screenshots/downtime.png)

* I scheduled downtime on the test.support.random monitor from 7pm-9am PST and my "teammate" received an email notification.

# Final Thoughts

Overall, I found that the provided documentation was extremely clear and helpful in detailing the product's available features and explaining how to utilize the Agent and the Datadog web app. Although I just scratched the surface of integrations and Agent checks in this exercise, I can tell that they're powerful tools and would be interested in delving deeper into their applications. As for the web app, I found the provided functionalities user-friendly and enjoyed exploring the different features. Although I was just looking at a small sample size of data from my own local machine, I can imagine how useful these tools would be when applied to the large-scale systems of a major organization.

After taking some time to explore the product, I think that working at Datadog would be an engaging challenge and a great way to continue my growth and development as an engineer.
