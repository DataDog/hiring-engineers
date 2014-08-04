Level 1
What is the agent?
The agent is a software that runs on machines, in order to collect events and metrics and send them to Datadog for monitoring. The agent is open-source.
The agent contains three parts: 
- the collectors that automatically collects data (thanks to integrations)
- a back-end server called dogstats designed to receive custom metrics and events from applications
- a forwarder that transmits data to Datadog

Le fichier "1-Post event.py" contenant le code suivant a créé un événement : 
---- CODE BEGINS HERE
# Import the module.
from statsd import statsd

# Post a simple message
statsd.event("Exercise event", "First event posted through the API")
---- CODE ENDS HERE

Level 2
- Load test: page views per second
https://p.datadoghq.com/snapshot/view/dd-snapshots-prod/org_12653/2014-08-04/a985ead1a255024be129c605789535f357d6d082.png
https://www.dropbox.com/s/6732wj8lt6e9q9p/Level2%20-%20Test%20load.JPG
- Latency: not done.

Level 3
- I tagged my host with the tag 'support'. And I tagged all my metrics with 'support' e.g.
---PHP CODE
<?php DataDogStatsD::increment('website.page.view', 1, array('support', 'page' => 'home'));?>
---PHP CODE
- Latency: not done.

Level 4
- Overall Number of page views
https://app.datadoghq.com/dash/dash/25921?from_ts=1407077654701&to_ts=1407108317388&tile_size=m
https://www.dropbox.com/s/c4w3c99zwnii3lo/Level4%20-%20overall%20page%20view.JPG

- Number of page views, split by page
https://app.datadoghq.com/dash/dash/25921?from_ts=1407099956865&to_ts=1407106992835&tile_size=m
https://www.dropbox.com/s/w1zfoiptka2sc65/Level4%20-%20page%20view%20by%20page%20tag.JPG

Level 5
---RandomTestCheck.yaml
init_config:

instances:
    [{}]
---RandomTestCheck.py
import random

from checks import AgentCheck

class RandomTestCheck(AgentCheck):
	def check(self, instance):
		self.gauge('test.support.random', random.random())