Monitoring Data
Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.

TASK #11: 
Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:
•	Warning threshold of 500
•	Alerting threshold of 800
•	And also ensure that it will notify you if there is No Data for this query over the past 10m.

ANSWER #11:

To be on top of my problem, I need to be proactive. I might be able to spot any problem if I'm starring at the screen but that's making me unproductive. I just need to let Datadog to monitor everything for me and send me email whenever there are problems.
I would like to get notified when my metrics beyond threshold level, but I also dont want to be bother when they happen for a short period. just a burst.
When my metric is not showing up or get collected, I would like get notified as well because would normally mean something is down.

Steps:
- Go to New Monitor and Select Metric type
- Define the conditional metric and the matching hosts or tags
- Configure the Warning (Yellow) threshold as 500 and Alert (Red) threshold as 800.
- Alert condition is above or equal to
- During the last 5 minutes
- Configure if data missing for 10 minutes

Snapshot
- answer-task11-pic1.png

Reference:
https://docs.datadoghq.com/api/?lang=python#monitors
