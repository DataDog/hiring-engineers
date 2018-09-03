Submitted by: David Oslander

## Section 1: Collecting Metrics

Screenshot of my host and its tags on the Host Map page in Datadog:

<img src="https://github.com/512ddhelg/hiring-engineers/blob/solutions-engineer/images/1-host-tags.png">

I installed a Postgres database and started it:

```
sudo service postgresql start
```

I installed the Postgres integration in Datadog:

<img src="https://github.com/512ddhelg/hiring-engineers/blob/solutions-engineer/images/1-postgresql-installed.png">

My custom Agent check that submits a metric named my_metric with a random value between 0 and 1000:
<img src="https://github.com/512ddhelg/hiring-engineers/blob/solutions-engineer/images/1-my_metric-py.png">

After changing my check's collection interval to submit the metric once every 45 seconds, the data points occur less frequently on the graph as expected:
<img src="https://github.com/512ddhelg/hiring-engineers/blob/solutions-engineer/images/1-my_metric-interval-increased.png">

**Bonus Question** Can you change the collection interval without modifying the Python check file you created?

* My Custom check inherits from Agent check. Rather than modifying the interval in my file, I could edit the process interval in Datadog.yaml.

## Section 2: Visualizing Data

The script that I've used to create my Timeboard is <a href="https://github.com/512ddhelg/hiring-engineers/blob/solutions-engineer/scripts/create-timeboard.py">here</a>.

Here's a screenshot of the Timeboard that I created via API:
<img src="https://github.com/512ddhelg/hiring-engineers/blob/solutions-engineer/images/2-timeboard-created-via-api.png">

Here's the snapshot of a graph on the Timeboard (scoped to last 5 minutes) that I sent to myself:
<img src="https://github.com/512ddhelg/hiring-engineers/blob/solutions-engineer/images/2-snapshot-sent-to-self.png">

**Bonus Question** What is the Anomaly graph displaying?

* For my Postgres integration, I initially chose the metric named postgresql.max_connections. Since I did nothing more than start one database and leave it alone, the Anomaly graph doesn't yield any useful insights. That's because the value of my metric is 100 at all times. If the value had fluctuated over time, I would have seen a gray band around the usual results, indicating an expected "normal" range. Since the metric postgresql.max_connections wasn't useful, I scrolled through the remaining metrics for postgres but I couldn't find a metric that showed the gray band in a satisfying way. I suppose I could take some actions on the Postgres environment that would result in a more satisying graph, but I don't think that's the point of this exercise. The point is to be able to correctly interpret the graphs.

Just for fun, changing the metric on my Anomaly graph to "my_metric", results in a graph that shows the gray band, and the expected normal range close to 500. The most narrow part of the band corresponds to the time window when the values were on average closest to 500:

<img src="https://github.com/512ddhelg/hiring-engineers/blob/solutions-engineer/images/2-bonus-my_metric.png">


## Section 3: Monitoring Data

Screenshot of the email sent to me by my monitor:
<img src="https://github.com/512ddhelg/hiring-engineers/blob/solutions-engineer/images/3-email-notification.png">

**Bonus Question** Two downtimes.

First one silences the monitor from 7pm to 9am daily on M-F. Email notification received:
<img src="https://github.com/512ddhelg/hiring-engineers/blob/solutions-engineer/images/3-downtime-notification.png">


Second one silences the monitor all day on Sat-Sun: Email notification received:
<img src="https://github.com/512ddhelg/hiring-engineers/blob/solutions-engineer/images/3-downtime-notification-weekend.png">


## Section 4: Collecting APM Data

## Final Question
