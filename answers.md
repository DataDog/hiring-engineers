# MARTIN FEJOZ's Answers to the challenge

###Level 1

####Bonus question: What is the agent?
The agent is a software that runs on machines, in order to collect events and metrics and send them to Datadog for monitoring. The agent is open-source.
The agent contains three parts: 
- the collectors that automatically collects data (thanks to integrations)
- a back-end server called dogstats designed to receive custom metrics and events from applications
- a forwarder that transmits data to Datadog

####Submit an event via the API
The following code created an event: 

```

from statsd import statsd

statsd.event("Exercise event", "First event posted through the API")
```

####Get an event to appear in your email inbox
Insertion of `@martin.fejoz@gmail.com` in a comment.

###Level 2

####Instrument your web app to get **metrics**
I built a few php pages hosted on a local server (on my machine).
I set two metrics: page views (named *web.page.views*) and form submission (*math.operation*).

####Vizualize page views per second in a graph during a load test
I used Apache Bench sending 10000 requests, 30 at one time.

<img src="https://www.dropbox.com/s/6732wj8lt6e9q9p/Level2%20-%20Test%20load.JPG" width="500" height="332" alt="Page view graph 1"></a>
[Datadog link to the graph] (https://p.datadoghq.com/snapshot/view/dd-snapshots-prod/org_12653/2014-08-04/a985ead1a255024be129c605789535f357d6d082.png)

####Create a histogram to see the latency
Not done. I haven't found a way to turn the load test in a latency metrics.

###Level 3

####Tag your metrics with `support`
As all my metrics are provided by the same host, I used the tag `support` on my machine in *Datadog>Infrastructure* section.

####Tag your metrics per page
I used the following code on every page :

```
<?php DataDogStatsD::increment('website.page.view', 1, array('page' => 'PAGE NAME HERE'));?>
```

#### Latency
Same as in Level 2. Not done.

###Level 4

####Count overall number of page views using counters
<img src="https://www.dropbox.com/s/c4w3c99zwnii3lo/Level4%20-%20overall%20page%20view.JPG" width="500" height="332" alt="Overall page views"></a>
[Link to the graph on Datadog] (https://app.datadoghq.com/dash/dash/25921?from_ts=1407077654701&to_ts=1407108317388&tile_size=m)
1.97 K page views at 01:00:00 (using ab load test tool).

####Count number of page views split by page
<img src="https://www.dropbox.com/s/w1zfoiptka2sc65/Level4%20-%20page%20view%20by%20page%20tag.JPG" width="500" height="332" alt="Overall page views split by page"></a>
[Link to the graph on Datadog] (https://app.datadoghq.com/dash/dash/25921?from_ts=1407099956865&to_ts=1407106992835&tile_size=m)

###Level 5

####Write an agent check that samples a random value
**RandomTestCheck.yaml**
```
init_config:

instances:

```
**RandomTestCheck.py**
```
import random

from checks import AgentCheck

class RandomTestCheck(AgentCheck):
	def check(self, instance):
		self.gauge('test.support.random', random.random())
```
