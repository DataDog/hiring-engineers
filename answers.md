## LEVEL 1
Note: All instructions are given for a Linux machine

### Get agent reporting from local machine
You should be able to see something like this on your dashboard:
![Local metrics] (http://i296.photobucket.com/albums/mm184/leungz/1metrics_from_local_machine_zps48c1ca8a.png)

Use this command to install the agent on Debian:
```
DD_API_KEY=YOURKEY bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/dd-agent/master/packaging/datadog-agent/source/install_agent.sh)"
```

##### Your Datadog API Key
YOURKEY = your API Key given to you by Datadog, which can be found under the Integrations tab. Click on API and you will see API Keys. Use that Key.

After installation, you should see something like this:
![install_agent] (http://i296.photobucket.com/albums/mm184/leungz/agentinstall_zps075fed60.png)


### What is the agent? 
The agent is software that run on your hosts that collects events and metrics and sends it to Datadog. It consists of the collector (runs checks on current machine, capture metrics like memory etc.), dogstatsd (statsd backend server where metrics from an application can be sent to), and the forwarder (data that is pushed from dogstatsd and the collector and sent to Datadog).


###### Troubleshoot:
- 'INFO exited: dogstatsd (exit status 1; not expected)' and 'INFO gave up: collector entered FATAL state, too many start retries too quickly' errors: It may be a problem of the agent not being fully installed. Try installing again.

### Submit an event via the API: 
Open a new ruby file
```ruby
require 'rubygems'
require 'dogapi'
api_key = "YOURKEY"
dog =  Dogapi::Client.new(api_key)
dog.emit_event(Dogapi::Event.new('Event submitted via API', :msg_title => 'Event Submitted'))
```
Run it and you should see this in your Events stream.
![event_api](http://i296.photobucket.com/albums/mm184/leungz/eventapi_zpscd77e31f.png)

###### Troubleshoot:
- dogapi load error: Try installing dogapi (gem install dogapi) 
- gem command not found error : Make sure you have installed rubygems (sudo apt-get install rubygems)


### Get an event to appear in your email inbox: 
In this line, add your email.
```ruby
dog.emit_event(Dogapi::Event.new('Event submitted via API @youremail@youremailprovider.com', :msg_title => 'Event Submitted'))
```
Run it and you should see this in your inbox:
![Email API] (http://i296.photobucket.com/albums/mm184/leungz/eventapi2_zpsd623cc3e.png)

###### Tips:
To check if the agent is running: 
```sudo /etc/init.d/datadog-agent status ```
To start the agent:
```sudo /etc/init.d/datadog-agent start ```
To stop the agent:
```sudo /etc/init.d/datadog-agent stop```
To restart the agent
```sudo /etc/init.d/datadog-agent restart ```

## LEVEL 2


### Take a simple web app that you've already built and instrument your code with dogstatsd
I used a ruby on rails app that allows users to manage a list of their bookmarks. 

![bookmark home](http://i296.photobucket.com/albums/mm184/leungz/bookmarks_zps8e10f8a6.png)

Create a module
```ruby
#PageView.rb

 def page_view_count
  $statsd.increment('my_page_views')
  return
 end
```
Create an instance, call 
```ruby
#bookmarks_controller.rb

require 'statsd'
$statsd = Statsd.new 'localhost', 8125

...
#call page_view_count in your method
...
```

### While running a load test (see References) for a few minutes, visualize page views per second. Send us the link to this graph!

Some code for the load test
```ruby
#loadtest.rb
exec 'ab -c 110 -n 130 PutYourAddressHere'
exec 'ab -c 3 -n 234 PutYourAddressHere'
...
```

[Visualization](https://app.datadoghq.com/graph/embed?token=cf4a6cd673d3b73b37c3869355a47ba66f1b371293bca720a2ab6f78f15ac5d7&height=300&width=600&legend=true" frameborder="0" height="300" width="600")

![Page View Graph] (http://i296.photobucket.com/albums/mm184/leungz/pageviewpersec_zps23bef1a0.png)

###### Troubleshooting - my own experience:
Problem: So... my metric was created but would not increment. 
Solution: After I checked everything else, I realized it was because I signed up for my account more than 2 weeks ago and the free trial had expired before I started on the challenge. On the free trial you only get to store data for one day. You might be thinking, well that should still have worked - except that I was using a vm that had a wrong date and time (date was 1.5 days late, no idea why I missed out on setting it, but it's a VM I don't use a lot). On the plus side somehow I read a lot about graphite while trying to figure it out. 


### Create a histogram to see the latency
```ruby
#PageView.rb

...
 def latency
    start_time = Time.now
    page_view_count
    duration = Time.now - start_time
    $statsd.histogram('page_view_latency', duration)
  end
...
```
```ruby
#bookmarks_controller.rb

require 'statsd'
$statsd = Statsd.new 'localhost', 8125

...
#call latency in your method
...
```
[Visualization](https://app.datadoghq.com/graph/embed?token=10e40f59b8db84ae1eaf2b29a84d6cb195f3df04d58c684795aad2088cf73375&height=300&width=600&legend=true" frameborder="0" height="300" width="600")

![Latency View Graph] (http://i296.photobucket.com/albums/mm184/leungz/latency_zpsc2083964.png)

### Bonus

Gauge of Gigabytes used by local machine. Could be run as a daemon.

![Gigs used Graph] (http://i296.photobucket.com/albums/mm184/leungz/gigsused_zpsb78bcd2c.png)

## Level 3
Using the same web app from Level 2

### Tag your metrics with support (one tag for all metrics)

Added tags like ```$statsd.increment('my_page_views', :tags => ['support']) ```

### Tag your metrics per page (e.g. metrics generated on / can be tagged with page:home, /page1 with page:page1)

I tagged my metrics for comparing page views per bookmark. I changed the method to accept an argument ```page_view_count(params[:id])``` . I made it optional in case I wanted to count the homepage which does not have an id. I used string interpolation ```bookmark:#{myargument}``` to get the different params in my bookmark tag so I know which page called this method.

Bonus graph: page views rate/sec 

![Pv graph] (http://i296.photobucket.com/albums/mm184/leungz/pvmetrics_zps6659c5f8.png)


### Visualize the latency by page on a graph (using stacked ares, with one color per page)

![Latency per page graph](http://i296.photobucket.com/albums/mm184/leungz/latencybypage_zpsf72371d1.png)


## Level 4

### Count the overall number of page views using dogstatsd counters.

Added a tag for overall count.
```$statsd.increment('my_page_views', :tags => ['support', 'bookmark:total']) ```

### Count the number of page views, split by page (hint: use tags)

```$statsd.increment('my_page_views', :tags => ['support', 'bookmark:total', "bookmark:#{myvariable}"]) ```

### Visualize the results on a graph.
![Total page count] (http://i296.photobucket.com/albums/mm184/leungz/totalpagecount_zps16627b5a.png)

### Bonus question: do you know why the graphs are so spiky?

My best guess is ...

##### Summary: 
Aggregation levels imposed by datadog agent causes these spikes.

##### Detailed Explanation: 
- These are not raw points. Even if your page is hit every 0.001 seconds in a constant manner, because of the aggregation it will not be as smooth as plotting the raw points.
- Metrics aggregation level is at 30 seconds. (In ```agent_metrics.py``` the constant ```MAX_COLLECTION_TIME = 30```). This is divided over the aggregation period that Datadog's query engine thinks makes sense. 
- For example, in one my graphs, between 18:44:30 and 18:45:00, the site was hit 775 times (seen under count). When viewed at rate/sec, it was divided into 3 periods, at 18:44:30, 18:44:40 and 18:44:50 at 265, 248 and 262 hits respectively. These add up to 775. The 30 second period before this had a total count of 816, and the 30 second period after this had a total count of 823. Datadog code probably does a weighted division when dividing the total count by three, depending on what came before and after. 

##### Things that could possibly make it extra spiky
- Dogstatsd flush interval is set at default 10 seconds. (In ```dogstatsd.py```, ```DOGSTATSD_FLUSH_INTERVAL = 10```) but if for some reason you flush less often than the metrics aggregation time, that could affect it.
- You don't send all your metric points over UDP to the StatsD server, instead you are using a sample rate such as ```:sample_rate => 0.5``` that only sends half the time. 



## Level 5

Let's switch to the agent

### Write an agent check that samples a random value. Call this metric: test.support.random

In /etc/dd-agent/conf.d/ is my ```ranvalcheck.yaml```
```yaml
init_config:

instances:
    [{}]
```

In /etc/dd-agent/checks.d is my ```ranvalcheck.py```
```ruby
import random
from checks import AgentCheck

class Ranvalcheck(AgentCheck):
    def check(self, instance):
        self.gauge('test.support.random', val)
```
I ran ```PYTHONPATH=. python checks.d/ranvalcheck.py``` in the root directory.

### Visualize this new metric on Datadog, send us the [link] (https://app.datadoghq.com/graph/embed?token=e76f121eb8c5c0607a20053985f06ba88ef58f8d7d7f375520c489c1605e5cb5&height=300&width=600&legend=true" frameborder="0" height="300" width="600).

![test support graph] (http://i296.photobucket.com/albums/mm184/leungz/testsupport_zps42108b71.png)


###### Troubleshooting tips

I had an error where I ran the PYPTHONPATH=. ... with no errors, but no metric showed up. If this happens to you, try re-installing your python dependencies like this ```pip install -r requirements.txt```





