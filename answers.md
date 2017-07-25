## Answers

### Level 0 (optional) - Setup an Ubuntu VM

* I launched a small instance on Google Cloud Platform using Google Compute Engine (GCE). Since I was using GCE, I was able to leverage the Google Compute Engine Integration. [Click here](https://p.datadoghq.com/sb/68e249c37-543864fd21) to view a read-only version of the GCE dashboard. Here is a screenshot of the dashboard:


### Level 1 - Collecting your Data

__In your own words, what is the Agent?__
* The Datadog Agent is a piece of platform-specific software that regularly collects metrics from its host, then sends it to Datadog where a user can monitor, visualize, and interact with the data. The Agent collects system data from its host machine, and can be configured to collect a wide variety of other metrics and event data from hosted processes and applications. Several Agents have been developed for many types of platforms including CentOS, Docker, Red Hat, and Amazon Linux.

*__What ACTUALLY is the Agent?__*
* The Agent is the link between Datadog and a host and its applications. Once configured (often with a single line of code), users can confidently rely on the Agent to consistently collect and consolidate key metrics vital to monitoring and maintaining their infrastructure and applications. Both simple and extremely extensible, the Agent does the heavy lifting of delivering host and application event data to your Datadog console.

__Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.__
* I added two custom tags to my DataDog Agent config file: 'env: learn' and 'owner: chris.' Here is a screenshot of the tags on the Host Map page:

__Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.__
* I installed a MySQL database on my instance, created a privileged service user for Datadog to collect database metrics, configured the mysql.yaml file, then installed the MySQL Datadog Integration. Here is a screenshot of the dashboard I created by installing and configuring the MySQL Integration:

__Write a custom Agent check that samples a random value. Call this new metric: `test.support.random`__
* I created a file called checkval.py in */etc/dd-agent/checks.d/*. The file contains the following snippet:

```python
import random
from checks import AgentCheck
class RandomCheck(AgentCheck):
  def check(self, instance):
    self.gauge('test.support.random', random.random())
```

The code successfully returns a random decimal value between 0 and 1. I created this initial timeseries chart to plot the random values returned over time:


### Level 2 - Visualizing your Data

__Since your database integration is reporting now, clone your database integration dashboard and add additional database metrics to it as well as your `test.support.random` metric from the custom Agent check.__
* I cloned the MySQL dashboard, added the `test.support.random` timeseries graph, and two additional widgets: 1) a query value that shows the number of MySQL queries per second, 2) a timeseries graph that shows the number of bytes received over time. Here is a screenshot of the dashboard:

__Bonus question: What is the difference between a timeboard and a screenboard?__
* With Datadog, you can create two types of dashboards; timeboards and screenboards, both of which enable you to create custom graphs, charts, and other widgets to help you better understand your data. The difference between these dashboards lies in their scope and their customizability:
  - __*TimeBoards*__ are dashboards where all graphs and charts are scoped to the same time range (i.e. the past hour, 12 hours, day, week, etc.). This simplifies the job of troubleshooting and correlating events across various system components; for example, on two separate graphs, users may align a drop in database writes to a spike in network traffic or system load, enabling root cause analysis. In order to simplify correlation of event data, all graphs are automatically organized in a grid pattern.
  - __*ScreenBoards*__ are dashboards that allow much more customization. Users can create custom widgets, graphs, and charts of any size or timeframe and organize them in a pattern of their choosing. This enables users to create a custom high-level view of systems.

__Take a snapshot of your `test.support.random` graph and draw a box around a section that shows it going above 0.90. Make sure this snapshot is sent to your email by using the @notification__
* Here is a screenshot of the snapshot I sent to myself:

* Here is a screenshot of the `test.support.random` graph with a red line at .90:

### Level 3 - Alerting on your Data

__Set up a monitor on this metric that alerts you when it goes above 0.90 at least once during the last 5 minutes__
* I created a monitor that will alert me if any host with the 'env:learn' tag has a `test.support.random` metric that goes above 0.9 at least once during the last 5 minutes. This alert is a Multi Alert which will send me a separate alert for every host that meets this condition. Also, since the 'env:learn' tag is specified, this monitor will automatically apply to additional instances I add to this environment. Here is a screenshot of the monitor config:

  
__Give it a descriptive monitor name and message. Make sure that the monitor will notify you via email. Take a screenshot of the email that it sends you.__
* I created a simple message that will notify me of a host that has a `test.support.random` metric that went above 0.9. The message provides simple dummy instructions and troubleshooting steps. The message references simple host tags like {{host.name}} and {{host.ip}}. Here is a screenshot of the email:


__Set up a scheduled downtime for this monitor that silences it from 7pm to 9am daily. Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.__
* I scheduled a couple monitor downtimes, one between 7pm and 9pm daily, and the other between 1:22am and 9:22am. Here are screenshots of the start and end of the scheduled downtime:
