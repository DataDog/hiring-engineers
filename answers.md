> ### Level 1

> * Sign up for Datadog, get the agent reporting metrics from your local machine.

I signed up for the free 14-day trial and installed the agent (v5.5.2) on my Ubuntu (v14.04) ec2 instance (i-0f21a5cb). The native dashboard available from clicking the hostname link on the infrastructure page fleshed out in no time:
![My Agent](http://i.imgur.com/BTCVE56.png)

> * Bonus question: what is the agent?

The agent is open source software written in Python that collects performance metric and event data from the system it's installed on and aggregates the data to the Datadog service where it can be visualized and processed for alarming.

> * Submit an event via the API.

I used the available help documentation to create a Python script, send-event.py:
``` Python
ubuntu@ip-172-31-32-144:~$ cat send-event.py
from datadog import initialize, api

options = {
    'api_key':'************************************d23a',
    'app_key':'************************************a8e8'
}

initialize(**options)

title = "Something big happened!"
text = 'And let me tell you all about it here!'
tags = ['version:1', 'application:web']

api.Event.create(title=title, text=text, tags=tags)
```

> * Get an event to appear in your email inbox (the email address you signed up for the account with)

... and created a monitor that looks for the event created by the script by configuring the monitor trigger based on a match of keywords in the event text, "Something big happened":
![Event Definition](http://i.imgur.com/h3PvI7F.png)

This rendered the email notification shown below:
![Email Notification](http://i.imgur.com/50z2WCA.png)

> ### Level 2

> * Take a simple web app ([in any of our supported languages](http://docs.datadoghq.com/libraries/)) that you've already built and instrument your code with dogstatsd. This will create **metrics**.

I created a web.py app, installed the dogstatsd client package via pip and imported the module into my app:
``` Python
import web
import time
from datadog import initialize
from datadog import statsd

options = {
    'api_key':'************************************d23a',
    'app_key':'************************************a8e8'
}

initialize(**options)

urls = (
    '/', 'index'
)

class index:
    def GET(self):
        start = time.time()
        statsd.increment('web.get.count')
        duration = time.time() - start
        statsd.histogram('web.get.latency', duration)
        return "Index Page"

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()

```

> * While running a load test (see References) for a few minutes, visualize page views per second. Send us the link to this graph!

I wrote an ab (Apache Benchmark) wrapper in Python to execute load tests of a random number of requests (within a specified range):
``` Python
import random
import os
import sys

def main():
    test()

def test(page):
    hits=random.randint(100,1000)
    os.system("/usr/bin/ab -n %d -c 10 http://localhost:8080/" % (hits))

if __name__ == "__main__":
    main()
```

... and placed it in cron:

```
* * * * * /usr/bin/python /home/ubuntu/ab.py
```
For the per second resolution, I created a dashboard with a graph definition to capture a per second count:
![Graph Definition](http://i.imgur.com/8HaOsiL.png)

... selected a five minute period from the graph and switched to the full screen view:
![Graph View](http://i.imgur.com/mkAxwLo.png)

[Link to Page Views Graph](https://app.datadoghq.com/graph/embed?token=9b42954debd5ab07381794be3a44c12f8f83bd105c0265d0cd41818f85c046a7&height=400&width=800&legend=true" width="800" height="400" frameborder="0")

> * Create a histogram to see the latency; also give us the link to the graph

I created a simpler graph (no ask for per second on this one) that averages the latency measurments per host: 
![Latency Graph](http://i.imgur.com/qBL7wXF.png)
[Link to Latency Graph](https://app.datadoghq.com/graph/embed?token=f4381f2a0b27087f57f5085fe1b26da66ec305b1d95d3bd1704351c3efca4e82&height=400&width=800&legend=true" width="800" height="400" frameborder="0")

> * Bonus points for putting together more creative dashboards.

I updated this step with my final Web Stats dashboard which includes graphs that use the tagging implemented in later levels. Not too hard on the eyes if I do say so myself.
![Full Dashboard](http://i.imgur.com/qyY9TKN.png)
[Link to Full Dashboard](https://app.datadoghq.com/dash/79332/web-stats?live=true&page=0&is_auto=false&from_ts=1447108405491&to_ts=1447112005491&tile_size=m&fullscreen=false)

> ### Level 3

> Using the same web app from level 2:
> * tag your metrics with `support` (one tag for all metrics)
> * tag your metrics per page (e.g. metrics generated on `/` can be tagged with `page:home`, `/page1` with  `page:page1`)

In my web.py app, I created classes for two new pages (settings and messages) in addition to my original index page and updated the function calls to include the requisite tags (page:home, page:page1 and page:page2). I also added sleep calls with random lengths for more colorful latency numbers:
``` Python
class index:
    def GET(self):
        start = time.time()
        delay=random.uniform(0.01,0.1)
        sleep(delay)
        statsd.increment('web.get.count', tags = ["support","page:home"])
        duration = time.time() - start
        statsd.histogram('web.get.latency', duration, tags = ["support","page:home"])
        return "Index Page"

class settings:
    def GET(self):
        start = time.time()
        delay=random.uniform(0.2,0.6)
        sleep(delay)
        statsd.increment('web.get.count', tags = ["support","page:page1"])
        duration = time.time() - start
        statsd.histogram('web.get.latency', duration, tags = ["support","page:page1"])
        return "Settings Page"

class messages:
    def GET(self):
        start = time.time()
        delay=random.uniform(0.4,0.9)
        sleep(delay)
        statsd.increment('web.get.count', tags = ["support","page:page2"])
        duration = time.time() - start
        statsd.histogram('web.get.latency', duration, tags = ["support","page:page2"])
        return "Messages Page"

```

> * visualize the latency by page on a graph (using stacked areas, with one color per `page`)

I then created a new graph on my dashboard to include the stacked graphing of latency:
![Stacked Latency Graph](http://i.imgur.com/Z4Lj2EE.png)

> ### Level 4

> Same web app:
> * count the overall number of page views using dogstatsd counters.

I created a top list graph to take the sum of all page view metric values tagged with "support" and sorted by sum: 
![Overall Page Views Graph Definition](http://i.imgur.com/Qcku3V0.png)
![Overall Page Views Graph](http://i.imgur.com/Ht9vbMh.png)

> * count the number of page views, split by page (hint: use tags)

I repeated the above with a new graph and filtered on the page metric tag group instead of the support tag:
![Views per Page Graph Definition](http://i.imgur.com/WaGkApM.png)
![Views per Page Graph](http://i.imgur.com/OsNiS2h.png)

> * Bonus question: do you know why the graphs are very spiky?

There are a few factors at play that contribute to the spiky-ness of the data:
* Dogstatsd aggregates metric data to the agent's forwarder component on a 10s interval. This is referred to as a flush. Statsd doesn't timestamp the individual increments during the 10s flush period. Instead, the increments are tallied and pushed to the agent forwarder as an aggregate of the 10s period. So, if I send a metric that has incremented from a value of 0 by a value of 10 per second each second of the flush period, the result is a plot on the graph of 100 instead of 10 incremental plots of 10 each second. This makes for a steep incline.

* In addition, the increment metric resets to 0 when there are no new increments during the flush period. This creates a steep decline in the graph if that initial number of 100 drops back down to 0.

* Finally, the Apache Benchmark wrapper I created executes every minute at the top of the minute creating a significant gap between increments and contrasts the spikes that are graphed during the ab test cycles.

 
> ### Level 5

> Let's switch to the agent.

> * Write an agent check that samples a random value. Call this new metric: `test.support.random`

Simple enough, I created the two files needed to implement a custom check...

/etc/dd-agent/conf.d file:
```
$ cat pvfkb.yaml
init_config:

instances:
    [{}]
```

/etc/dd-agent/checks.d file:
```
$ cat pvfkb.py
from checks import AgentCheck
import random
class HelloCheck(AgentCheck):
    def check(self, instance):
        self.gauge('test.support.random', random.random())
```

> * Visualize this new metric on Datadog, send us the link.

... and created a new dashboard with a graph of the test.support.random metric.
![Custom Check, Random Metric Graph](http://i.imgur.com/TXJKwIE.png)
[Link to Custom Check, Random Metric Graph](https://app.datadoghq.com/graph/embed?token=9d058ae58e9ee005457f60bb015a2b00fa62d7df528c5c525966a5125964c250&height=400&width=800&legend=true" width="800" height="400" frameborder="0")
