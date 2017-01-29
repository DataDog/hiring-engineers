# Answers to Datadog's support hiring challenge.
by Brian Deutsch.

## Level 1

* A screenshot of Datadog's agent installed and collecting system metrics, within minutes of installation:

![alt text](http://i.imgur.com/mMt5Rm3.png "Agent Installed")

* Datadog's agent is the software that runs on your hosts.  It is responsible for collecting events and metrics from both your local machine, and external applications (the latter using it's statsD server).  The agent then forwards this information to Datadog so the user can visualize and monitor their performance data.

* I was able to submit an event via the API using a cURL request:

![alt text](http://i.imgur.com/TBYEzM6.png "API post event using cURL")

* I also submitted an event programmatically using Dogapi.  I tagged myself in an event comment, triggering a notification.

![alt text](http://i.imgur.com/ouNJ9gC.png "Event displayed with notifcation tag")

## Level 2

* A screenshot of dogstatsD being added to my Sinatra application:

![alt text](http://i.imgur.com/tw3jk4M.png "dogstatsD instrumentation")

* I ran a load test using AB to send 300 requests to my application.  I've included a screen shot of the resulting page views graph below, in addition to a graph on my page views dashboard displaying average views per second.

* [Link to page views dashboard](https://app.datadoghq.com/dash/108420/page-views?live=false&page=0&is_auto=false&from_ts=1458583415000&to_ts=1458583821000&tile_size=m&fullscreen=false "Link to page views dashboard")

![alt text](http://i.imgur.com/w1QAxNN.png "Page views after load test")

* Utilizing the histogram method produced more page view statistics to analyze, such as median, 95th percentile, average, count, and max.  Below is a screenshot from one of the graphs I produced comparing this data:

![alt text](http://i.imgur.com/puAwnzK.png "Comparing page view data")

## Level 3

* I added a global tag of support to all metrics: `statsd = Statsd.new('localhost', 8125, :tags => ['support:true'])`

* The application I tested utilized two routes, '/' and '/about'.  I passed these tags of 'page:home' and 'page:about' respectively, so that I could visualize page views for each separately.

* [Click to view on dashboard](https://app.datadoghq.com/dash/109856/level-4-overall-page-views?live=false&page=0&is_auto=false&from_ts=1458660342898&to_ts=1458661316898&tile_size=m)

![alt text](http://i.imgur.com/6lge8iz.png "Views by page with stacked areas")

## Level 4

* I counted 3,133 total page views using dogstatsd counters.

* Since adding tags per page, I had 301 total views for the '/about' route, and 203 views for the '/' route (this does not include views that occurred prior to using tags per page).

* Here is a snapshot of a resulting graph, including both overall page views and results per page:

![alt text](http://i.imgur.com/D0BrkPZ.png "Overall views, and views per page")

* The graphs I produced did not seem too spiky; though I assume an application with more consistent traffic over time may result in graphs with far more outliers than mine.

## Level 5

* Finally, I wrote an agent check that samples a random value, called test.support.random.  Doing so required me to create two new files, one in YAML and another in python.  It was a good experience to briefly look into python, which is new to me.  Below I have included code snippets, a screen shot, and dashboard link.


```python
from checks import AgentCheck
import random
class RandomCheck(AgentCheck):
    def check(self, instance):
        random_value = random.random()
        self.gauge('test.support.random', random_value)
```



![alt text](http://i.imgur.com/VKbrJjt.png "Testing a random sample - agent check")

* [Link to custom agent on a dashboard](https://app.datadoghq.com/dash/110108/random-value?live=true&page=0&is_auto=false&from_ts=1458673289243&to_ts=1458676889243&tile_size=m&fullscreen=false)
