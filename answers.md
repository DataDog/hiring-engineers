# Support Engineer Challenge
***
## Level 1

* **Sign up for Datadog, get the agent reporting metrics from your local machine.**
![Marks Mac Book Pro Metrics](http://markewaldron.com/img/MarksMacBookProMetrics.png)
* **Bonus question: What is the agent?**
    * The agent is a piece of software that runs as a background process on the user's machine. It collects information about the host, as well as events and metrics from applications using DataDogs statsd. This information is then reported back to the DataDog servers so the user can monitor their systems.


* **Submit an event via the API.**
![API Event](http://www.markewaldron.com/img/API_Event.png)

``` ruby

require 'rubygems'
require 'dogapi'

api_key='API Key for Account'

dog = Dogapi::Client.new(api_key)

dog.emit_event(Dogapi::Event.new('This is an event from EventTest on Marks MacBook Pro', :msg_title => 'EventTest'))

```

* **Get an event to appear in your email inbox (the email address you signed up for the account with)**
![Say My Name](http://www.markewaldron.com/img/BB_SayMyName.gif)
![Email - API Event](http://www.markewaldron.com/img/API_Event_Email.png)

``` Ruby
require 'rubygems'
require 'dogapi'

api_key='API Key for Account'

dog = Dogapi::Client.new(api_key)

dog.emit_event(Dogapi::Event.new(' @markewaldron@gmail.com This is an event from EventTest on Marks MacBook Pro', :msg_title => 'Email - EventTest'))
```

***
## Level 2
* **Take a simple web app that you've already built and instrument your code with dogstatsd. This will create metrics**
    * I integrated dogstatsd with a Pinterest clone I wrote in Ruby on Rails. In order to do this, I added the `dogstatsd-ruby` gem to my `Gemfile` and then made the necessary changes to my `pins_controller.rb` file.
``` Ruby
require 'statsd'
STATSD = Statsd.new

class PinsController < ApplicationController
  before_action :find_pin, only: [:show, :edit, :update, :destroy, :upvote]
  before_action :authenticate_user!, except: [:index, :show]

  def index
    @pins = Pin.all.order("created_at DESC")
    STATSD.increment('PostIt.page.views')
  end
...
```
In the `STATSD.increment` call, I specify `PostIt.page.views` in order to separate it from other page views I may implement in the future.

* **While running a load test (see References) for a few minutes, visualize page views per second. Send us the link to this graph!**
    * Using Apache Benchmark, I ran `ab -n 5000 -c 100 http://localhost:3000/`. The test took 994 seconds to run on my 2011 MacBook Pro, with a mean 5.03 requests per second. The above load test yielded this graph:
![PostIt Page Views](http://www.markewaldron.com/img/PostIt_Page_Views_Per_Second.png)
[PostIt Page Views Per Second](https://app.datadoghq.com/dash/61095/postit?live=false&page=0&is_auto=false&from_ts=1438275770000&to_ts=1438276505641&tile_size=s&fullscreen=61369166)

* **Create a histogram to see the latency; also give us the link to the graph**
    * Using `pin_controller.rb` from above, I added a `start` variable to store the initial time, and a `latency` variable after the `@pins = Pin.all.order("created_at DESC")` call to store the amount of time the request took. After the changes, the `pin_controller.rb` file looks like this:
``` Ruby
  def index
    start = Time.now
    @pins = Pin.all.order("created_at DESC")
    latency = Time.now - start
    STATSD.histogram('PostIt.latency', latency)
    STATSD.increment('PostIt.page.views')
  end
```
The above code yielded this histogram:
![PostIt_Latency](http://www.markewaldron.com/img/PostIt_Latency.png)
[PostIt Latency](https://app.datadoghq.com/dash/61095/postit?live=false&page=0&is_auto=false&from_ts=1438275644727&to_ts=1438276735636&tile_size=s&fullscreen=61326699)

* **Bonus points for putting together more creative dashboards.**
![PostIt Dashboard](http://markewaldron.com/img/PostIt_Dash.png)

***
## Level 3
* **Tag your metrics with support (one tag for all metrics)**
    * Using the same `pin_controller.rb` as above, I added a `support` tag to `STATSD.histogram` and `STATSD.increment`.
``` Ruby
  def index
    start = Time.now
    @pins = Pin.all.order("created_at DESC")
    latency = Time.now - start
    STATSD.histogram('PostIt.latency', latency, :tags => ['support'])
    STATSD.increment('PostIt.page.views', :tags => ['support'])
  end

  def show
    start = Time.now
    STATSD.increment('PostIt.page.views', :tags => ['support'])
    latency = Time.now - start
    STATSD.histogram('PostIt.latency', latency, :tags => ['support'])
  end
```
* **Tag your metrics per page (e.g. metrics generated on / can be tagged with page:home, /page1 with page:page1)**
    * Building upon the code posted above, I added a `page:home` tag to my Index, and a `page:show'#{@pin.title}'` tag to my Show page. I used interpolation in order to differentiate between the various Show pages.

``` Ruby
  def index
    start = Time.now
    @pins = Pin.all.order("created_at DESC")
    latency = Time.now - start
    STATSD.histogram('PostIt.latency', latency, :tags => ['support', 'page:home'])
    STATSD.increment('PostIt.page.views', :tags => ['support', 'page:home'])
  end

  def show
    start = Time.now
    STATSD.increment('PostIt.page.views', :tags => ['support', "page:show'#{@pin.title}'"])
    latency = Time.now - start
    STATSD.histogram('PostIt.latency', latency, :tags => ['support', "page:show'#{@pin.title}'"])
  end
```
* **Visualize the latency by page on a graph (using stacked areas, with one color per page)**
    * I staggered the start of each test by about 2 seconds. The result was this histogram:
![PostIt Tagged Latency](http://www.markewaldron.com/img/PostIt_Tagged_Latency.png)
[PostIt Tagged Latency](https://app.datadoghq.com/dash/61095/postit?live=false&page=0&is_auto=false&from_ts=1438288255204&to_ts=1438288555204&tile_size=s&fullscreen=61357585)

***
##Level 4

* **Count the overall number of page views using dogstatsd counters.**
![PostIt Page View Total](http://www.markewaldron.com/img/PostIt_Page_Views_Total.png) [PostIt Page View Total](https://app.datadoghq.com/dash/61095/postit?live=false&page=0&is_auto=false&from_ts=1438297718056&to_ts=1438298123000&tile_size=s&fullscreen=61363028)
* **Count the number of page views, split by page (hint: use tags)**
![PostIt Page Views by Tag](http://www.markewaldron.com/img/PostIt_Page_Views_Split.png) [PostIt Page Views by Tag](https://app.datadoghq.com/dash/61095/postit?live=false&page=0&is_auto=false&from_ts=1438297718056&to_ts=1438298123000&tile_size=s&fullscreen=61363028)
* **Bonus question: Do you know why the graphs are very spiky?**
    * The graph is spikey due to the way the data is aggregated. The Apache Bench test is sending x page views per second, and then the DataDog agent is relaying the information every 10 seconds. If I was sending exactly 10 requests every 10 seconds, the graph would be much smoother.

***
## Level 5
######Almost done, now let's switch to the agent.
![Jake Arms](http://www.markewaldron.com/img/AdventureTime_Jake_Arms.gif)
* **Write an agent check that samples a random value. Call this new metric: `test.support.random`**
    * Following the instructions on the [Datadog Docs](http://docs.datadoghq.com/guides/agent_checks/) page, I created a `testrandom.yaml` file in the `conf.d` folder with the code:
``` yaml
init_config:

instances:
  [{}]
```

Then I created a `testrandom.py` file in the `checks.d` folder with the code:
``` python
from checks import AgentCheck
import random

class RandomCheck(AgentCheck):
  def check(self, instance):
    self.gauge('test.support.random', random.random())
```

* **Visualize this new metric on Datadog, send us the link.**
![Test Support Random](http://www.markewaldron.com/img/Test_Support_Random.png)
[Test.Support.Random](https://app.datadoghq.com/dash/61385/random?live=false&page=0&is_auto=false&from_ts=1438461876000&to_ts=1438465498829&tile_size=m&fullscreen=61463943)
