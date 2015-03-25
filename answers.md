### Level 1

* Sign up for Datadog, get the agent reporting metrics from your local machine.

Install went smoothly.

![Datadog agent install] (http://scottenriquez.com/datadog/datadog-install.png)

* Bonus question: what is the agent?

The Datadog Agent runs on a host to collect metrics and events. This information is sent to Datadog where you can use the information in a number of ways. There are three components to the Agent - the collector, Dogstatsd, and forwarder. The collector runs with the installed integrations and captures system metrics. Dogstatsd is a statsd daemon used for sending metrics from an application. The forwarder queues and sends data from the collector and Dogstatsd to Datadog.

* Submit an event via the API.

Event sent from API

```ruby
require 'rubygems'
require 'dogapi'

dog = Dogapi::Client.new(api_key)

dog.emit_event(Dogapi::Event.new("Here's my first Datadog event, bark bark", :msg_title => 'Bark'))
```

![Event submitted via API] (http://scottenriquez.com/datadog/first-event.png)

* Get an event to appear in your email inbox (the email address you signed up for the account with)

Event emailed

```ruby
require 'rubygems'
require 'dogapi'

dog = Dogapi::Client.new(api_key)

dog.emit_event(Dogapi::Event.new("Here's my second Datadog event, bark bark @sjenriquez@gmail.com", :msg_title => 'Bark', :priority => 'high', :alert_type=> 'success'))
```

![Event emailed] (http://scottenriquez.com/datadog/email.png)


### Level 2

* Take a simple web app ([in any of our supported languages](http://docs.datadoghq.com/libraries/)) that you've already built and instrument your code with dogstatsd. This will create **metrics**.

I used a motorcycle social web app I built in Sinatra where users upload motorcycle photos and upvote/downvote their favorites.

I created a helper module that is called when the main photos page is requested.

```ruby
module Datadog

	STATSD = Statsd.new

	def self.render_page
		STATSD.increment('web.page_views')
	end

end
```

```ruby
get '/photos' do            # Display all photos from all users
  @photos = Photo.all
  Datadog.render_page
  erb :'photos/index'
end
```

* While running a load test (see References) for a few minutes, visualize page views per second. Send us the link to this graph!

![Page views] (http://scottenriquez.com/datadog/page-views.png)

[Link to graph](https://app.datadoghq.com/dash/integration/custom%3Aweb?from_ts=1427240500666&to_ts=1427242634000&tile_size=m&tpl_var_scope=*)

* Create a histogram to see the latency; also give us the link to the graph

I defined a db_latency method in the Datadog module to measure database query latency.

```ruby
def self.db_latency
	start_time = Time.now
	photos = Photo.all
	duration = Time.now - start_time
	STATSD.histogram('database.query.time', duration)
	photos
end
```

This method is called inside the photos controller.
```ruby
get '/photos' do            # Display all photos from all users
  Datadog.render_page
  @photos = Datadog.db_latency
  erb :'photos/index'
end
```

* Bonus points for putting together more creative dashboards.

I combined a few metrics from all the ones available so far. This overlays Page Views, DB latency, and System CPU usage.

![Bonus graph] (http://scottenriquez.com/datadog/db-query-page-view-cpu.png)

[Link to graph](https://app.datadoghq.com/dash/44175/custom-metrics---database-cloned?from_ts=1427240838571&to_ts=1427242705238&tile_size=m&fullscreen=57437774)

### Level 3

Using the same web app from level 2:
* tag your metrics with `support` (one tag for all metrics)
* tag your metrics per page (e.g. metrics generated on `/` can be tagged with `page:home`, `/page1` with  `page:page1`)
* visualize the latency by page on a graph (using stacked areas, with one color per `page`)

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