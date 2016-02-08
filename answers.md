# Level 1

### Regristration
Adress used : guillaume.deberdt@hec.edu

### What is the agent ?
The agent is a software that watch for metrics on your machine and send it to datadog.

### Event API
```ruby
require 'rubygems'
require 'dogapi'
api_key='...'
dog = Dogapi::Client.new(api_key)
dog.emit_event(Dogapi::Event.new('Hello dog !', :msg_title => 'Hello'))
```

### Event API with email
```ruby
require 'rubygems'
require 'dogapi'
api_key='...'
dog = Dogapi::Client.new(api_key)
dog.emit_event(Dogapi::Event.new('What if @guillaume.deberdt@hec.edu ?', :msg_title => 'Mailing with mention'))
```

# Level 2

For this par I took a local web app in Ruby on Rails with 4 public pages
* demoreel (root)
* production
* resume
* contact

I used the level2-tsung.xml file for load test

### Page views count & latency
I've added some code in my static_pages_controller.rb

```ruby
class StaticPagesController < ApplicationController
  require 'statsd'
  layout false

  def contact
    start = Time.now
    s = Statsd.new
    s.increment('web.page_views')
    render 'contact'
    lag = Time.now - start
    s.histogram('latency', lag)
  end

# [...]
# Similar for demoreel, production and resume function

end
```
Results in level2-page_views_per_sec.png and level2-latency.png

I'm quite surprise by the result of the page views per second. There is none sometimes whereas there are some page views (level2-page_views.png).

# Level 3

### Tagging metrics

To tag metrics all metrics I've introduced a variable in my controller 
```ruby
common_tags = ["support"]
```

Then in each function I've introduced the specific tag
```ruby
  def contact
    start = Time.now
    s = Statsd.new
    tags = Array.new(common_tags).push("page:contact")
    s.increment('web.page_views', :tags => tags)
    render 'contact'
    lag = Time.now - start
    s.histogram('latency', lag, :tags => tags)
  end
```