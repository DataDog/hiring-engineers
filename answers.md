### Level 1

* Sign up for Datadog, get the agent reporting metrics from your local machine.

I had a few minutes of trouble after installing the agent - it was installed but not reporting metrics. I was able to uninstall and reinstall it to fix the issue.

![Installed](http://i.imgur.com/0abvaKJ.png "Agent installed")

* Bonus question: what is the agent?

The Datadog agent collects events, metrics, and data from your hosts to make it easy to track, visualize, and monitor your data in a centralized place. There are three main parts to the agent. First, the collector gathers system info, like memory and CPU, on the machine on which the agent is installed. Next, the Dogstatsd is a statsd backend server to which you can send custom metrics from your app. Finally, the forwarder grabs data from both dogstatsd and the collector and queues it to be sent to Datadog.

* Submit an event via the API.

In hello_dog.rb:

```
require 'rubygems'
require 'dogapi'

api_key = "redacted"

dog = Dogapi::Client.new(api_key)

dog.emit_event(Dogapi::Event.new('You have successfully submitted an event via API! @sfdrago@gmail.com', :msg_title => 'API Event'))
```

Run `ruby hello_dog.rb` in terminal

![Event](http://i.imgur.com/KmZtIuC.png "Event via Api")

* Get an event to appear in your email inbox (the email address you signed up for the account with)

![Email](http://i.imgur.com/PC7zQN6.png "Email Mention")

### Level 2

* Take a simple web app ([in any of our supported languages](http://docs.datadoghq.com/libraries/)) that you've already built and instrument your code with dogstatsd. This will create **metrics**.

I am using a simple Stack Overflow clone built on Rails. I added a Ruby statsd client to the Application Controller to instrument the code and track metrics.

```ruby
#in application_controller.rb
require 'statsd'
$statsd = Statsd.new

def render_page
  $statsd.increment('web.page_views')
end
```


* While running a load test (see References) for a few minutes, visualize page views per second. Send us the link to this graph!

In the controller action that renders the homepage, I call the render_page method to increment the page view counter.

I used Apache Benchmarking to simulate page views. I ran two load tests:

![Page Views](http://i.imgur.com/PmVsuIH.png "Page Views")

[Page Views](https://app.datadoghq.com/graph/embed?token=c4ff73b1732f108f10212baa55aba5a60af5dfd78025683f83c2be8bd18bc004&height=300&width=600&legend=false)

* Create a histogram to see the latency; also give us the link to the graph

I added a method to the application controller to track homepage latency:

```ruby
#in application_controller.rb
def latency
  start_time = Time.now
  render_page
  duration = Time.now - start_time
  $statsd.histogram('homepage.latency', duration)
end
```

I then ran another load test to simulate more page views.

![Latency Histogram](http://i.imgur.com/WyqXYUi.png "Average Latency Histogram")

[Average latency histogram](https://app.datadoghq.com/graph/embed?token=e7bd4bab9741998196e3be359557a4d0a314c1b33a19fb90339abfc151edf1b3&height=300&width=600&legend=false)

* Bonus points for putting together more creative dashboards.

### Level 3

Using the same web app from level 2:
* tag your metrics with `support` (one tag for all metrics)

To tag metrics within an app, I can add the tag to the options included in the argument, like so:

`$statsd.increment('web.page_views', :tags => ['support'])`

* tag your metrics per page (e.g. metrics generated on `/` can be tagged with `page:home`, `/page1` with  `page:page1`)

Tagged using string interpolation in ruby: `page = "question:#{@question.id}"`

* visualize the latency by page on a graph (using stacked areas, with one color per `page`)

![Latency by page](http://i.imgur.com/Tt9wDzq.png "Average latency by page")
[Latency by page](https://app.datadoghq.com/graph/embed?token=e7eae13f035e6dc52cdfc9d662edb8f54e623dd5fd5e64b698f0fcdb7cd3eaf0&height=300&width=600&legend=true)

### Level 4

Same web app:
* count the overall number of page views using dogstatsd counters.

To count page views, I used the .increment method: `$statsd.increment('web.page_views', :tags => ['support', page])`

* count the number of page views, split by page (hint: use tags)

Using the above code, I passed "page" as an argument to the method that calls the .increment method. This allows me to vary which page is being tracked based on which controller method it is called from.

* visualize the results on a graph

![Page Views By Page](http://i.imgur.com/ZDR5fdQ.png "Page views by page")

[Page views by page](https://app.datadoghq.com/graph/embed?token=a79451323814f3c9a39f4cea352f2b68af95c809174c543827aff9e825922105&height=300&width=600&legend=true)

* Bonus question: do you know why the graphs are very spiky?

I would guess it is because of the way the data is graphed - we are graphing page views over time, but a page view is registered as an instantaneous event. I am thinking that at the time interval dictated by the code that graphs the metrics, the value is recorded and graphed. Since it happens every x seconds, the graph is spiky, rather than a smoother curve.

### Level 5

Let's switch to the agent.

* Write an agent check that samples a random value. Call this new metric: `test.support.random`
First, I created a config file called randval.yaml in the agent/conf.d directory that includes the following:

```
init_config:

instances:
    [{}]
```

Next, I created a file called randval.py in agent/checks.d that includes the following:

```
import random

from checks import AgentCheck

class RandomCheck(AgentCheck):
  def check(self, instance):
    rand_val = random.random()
    self.gauge('test.support.random', rand_val)
```
* Visualize this new metric on Datadog, send us the link.

Next I ran PYTHONPATH=. python checks.d/test.py from the agent root directory. This should have resulted in the new test.support.random metric appearing on Datadog - unfortunately, I think there is something wrong in my Python version installation that is causing this not to happen. I'm not getting feedback as to any failure and after running the agent info command, it doesn't appear that the custom agent check is recognized by the system.

