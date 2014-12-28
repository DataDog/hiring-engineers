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

### Level 4

Same web app:
* count the overall number of page views using dogstatsd counters.
* count the number of page views, split by page (hint: use tags)
* visualize the results on a graph
* Bonus question: do you know why the graphs are very spiky?

### Level 5

Let's switch to the agent.

* Write an agent check that samples a random value. Call this new metric: `test.support.random`
* Visualize this new metric on Datadog, send us the link.

Here is a snippet that prints a random value in python:

```python
import random
print(random.random())
```