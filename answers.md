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

<img src="https://p.datadoghq.com/snapshot/view/dd-snapshots-prod/org_12653/2014-08-04/a985ead1a255024be129c605789535f357d6d082.png" width="500" height="332">

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

[Link to my dashboard] (https://app.datadoghq.com/dash/dash/25921?from_ts=1407099646194&to_ts=1407107663248&tile_size=m)
See graph before last and last graphs for the two next questions.

####Count overall number of page views using counters
Using the cumsum function starting 5p.m. : 1.97K views
<img src=https://p.datadoghq.com/snapshot/view/dd-snapshots-prod/org_12653/2014-08-04/0271ccd67821ff13325760c19c3d23922d71614c.png width="500" height="332">

####Count number of page views split by page
I introduced the tag *page* later on. Using the cumsum function starting 11 p.m., the purple line (*page*=**two**) reaches 0.97K views at the end, the pink line (*page*=**two**) reaches 0.51K views.
<img src=https://p.datadoghq.com/snapshot/view/dd-snapshots-prod/org_12653/2014-08-05/e8cf7c40bdf54dbff3f5e237bcfb2ca76d99c2e4.png width="500" height="332"> 

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
