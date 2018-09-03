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

My custom Agent check that submits a metric named my_metric with a random value between 0 and 1000, in checks.d/hello.py:

```
import random
from checks import AgentCheck
class HelloCheck(AgentCheck):
    def check(self, instance):
        self.gauge('hello.world', 1)
        self.gauge('my_metric', random.randint(0,1001))
```

Here's where I adjusted the interval, in conf.d/hello.yaml:

```
init_config:

instances:
   - min_collection_interval: 45
```

After changing my check's collection interval to submit the metric once every 45 seconds, the data points occur less frequently on the graph as expected:

<img src="https://github.com/512ddhelg/hiring-engineers/blob/solutions-engineer/images/1-my_metric-interval-increased.png">

**Bonus Question** Can you change the collection interval without modifying the Python check file you created?

* My Custom check inherits from Agent check. Rather than modifying the interval in my file, I could edit the process interval in Datadog.yaml.

## Section 2: Visualizing Data

The script that I've used to create my Timeboard is <a href="https://github.com/512ddhelg/hiring-engineers/blob/solutions-engineer/scripts/create-timeboard.py">here</a>.

Here's the link to that dashboard created via API (by executing <a href="https://github.com/512ddhelg/hiring-engineers/blob/solutions-engineer/scripts/create-timeboard.py">create-timeboard.py</a>):
https://app.datadoghq.com/dash/905077

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

**Bonus Question** Setup two Downtimes.

The first Downtime silences the monitor from 7pm to 9am daily on M-F. Here's the email notification that I received:

<img src="https://github.com/512ddhelg/hiring-engineers/blob/solutions-engineer/images/3-downtime-notification.png">


The second Downtime silences the monitor all day on Sat-Sun, and I set it to begin next weekend. Here's the email notification that I received:

<img src="https://github.com/512ddhelg/hiring-engineers/blob/solutions-engineer/images/3-downtime-notification-weekend.png">


## Section 4: Collecting APM Data

First, I enabled networking in my Vagrantfile by exposing the VM's port 5050 on the host port 8081:

<img src="https://github.com/512ddhelg/hiring-engineers/blob/solutions-engineer/images/4-enabling-networking.png">

I used ddtrace-run instead of manually instrumenting the Python Flask app. The How-To for manual instrumentation can be found in the docs <a href="https://docs.datadoghq.com/tracing/advanced_usage/?tab=python#manual-instrumentation">here</a>.

I used the Flask app that was provided in the instructions, and I included it <a href="https://github.com/512ddhelg/hiring-engineers/blob/solutions-engineer/scripts/flask-app.py">here</a>.


Then I opened up my browser and hit the various endpoints (resources) to generate some results. Consequently my Flask service appeared in Datadog APM:

<img src="https://github.com/512ddhelg/hiring-engineers/blob/solutions-engineer/images/4-apm-service-flask.png">

Drilling down into the service, I can scroll down and see how many requests have occurred on the various Resources:

<img src="https://github.com/512ddhelg/hiring-engineers/blob/solutions-engineer/images/4-apm-service-flask-details.png">

**Bonus Question** What is the difference between a Service and a Resource?

A Service is a higher-level entity that can be traced, such as a web resource or a database. A Service may have several Resources. For example, a web application is a Service, and the various http endpoints that it supports are among its Resources. I deployed the given Flask app, which is a Service. Each HTTP route that it defines is a Resource.

For the official definitions of Service and Resource, see the documentation here: https://docs.datadoghq.com/tracing/visualization/

Screenshot of dashboard showing both APM and Infra metrics:

<img src="https://github.com/512ddhelg/hiring-engineers/blob/solutions-engineer/images/4-dashboard-both-apm-and-infra.png">

Link to dashboard showing both APM and Infra metrics:
https://app.datadoghq.com/dash/904267



## Final Question

Is there anything creative you would use Datadog for?

I visit the Adirondacks every Summer, which has hiking trails that are heavily used. There is limited parking near the trailheads and on the sides of the road. I could imagine IoT devices (with Datadog agent installed) deployed to these areas that report on the occupancy of parking spots. This data could be analyzed by the State to better understand the demand on their parks and trails. They could deploy more personnel to locations under peak conditions, or develop better plans to maintain the trail at the appropriate frequency, or develop a more informed strategy for parking concerns. The State could build an app that allows consumers to see parking availability in real-time, and allow them to identify trails or parks that are hidden gems not overrun by visitors.

Separately, cable companies or power companies could use devices with Datadog agent to proactively identify outages and respond to them without having to rely on individuals reporting outages. Notifications would be used to let consumers know when an outage has occurred and when it has been restored.

## Links to dashboards

My dashboard created via API (by executing <a href="https://github.com/512ddhelg/hiring-engineers/blob/solutions-engineer/scripts/create-timeboard.py">create-timeboard.py</a>):
https://app.datadoghq.com/dash/905077

Link to dashboard showing both APM and Infra metrics:
https://app.datadoghq.com/dash/904267
