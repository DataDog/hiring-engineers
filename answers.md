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
![level1-event-API.png](/level1-event-API.png)

### Event API with email
```ruby
require 'rubygems'
require 'dogapi'
api_key='...'
dog = Dogapi::Client.new(api_key)
dog.emit_event(Dogapi::Event.new('What if @guillaume.deberdt@hec.edu ?', :msg_title => 'Mailing with mention'))
```
![level1-event-API-email.png](/level1-event-API-email.png)

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
![level2-page_views_per_sec.png](/level2-page_views_per_sec.png)
![level2-latency.png](/level2-latency.png)

I'm quite surprise by the result of the page views per second. There is none sometimes whereas there are some page views.
![level2-page_views.png](/level2-page_views.png).

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

![level3-latency_per_tag.png](/level3-latency_per_tag.png)
![level3-latency_per_tag-settings.png](/level3-latency_per_tag-settings.png)

# Level 4

### Overall number of page views and by page

![level4-page_views_overall.png](/level4-page_views_overall.png)
![level4-page_views_per_page.png](/level4-page_views_per_page.png)
![level4-page_views_per_page-graph.png](/level4-page_views_per_page-graph.png)

# Level 5

### Agent check that samples a random values

First we need to create a ***random_check.yaml*** in ***/etc/dd-agent/conf.d/***

```yaml
init_config:

instances:
  [{}]
```
Then ***random_check.py*** in ***/etc/dd-agent/checks.d/***

```python
from checks import AgentCheck
import random

class random_check(AgentCheck):
  def check(self,instance):
    self.gauge('test.support.random' , random.random())
```
And we restrat with ***sudo /etc/init.d/datadog-agent restart***

### Visualize it

![level5-test.support.random.png](/level5-test.support.random.png)