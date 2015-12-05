<h1>DataDog Support Engineer Challenge</p>
<p>By Chris Slaight</p>

<h2>Level 1</h2>

<p>To answer the question regarding the Agent, this is essentially the component of the software that resides within whatever host you're monitoring with Datadog. Its essential purpose is to collect metrics and events and then send them into the Datadog cloud, where you can truly make something of the data.
<br><br>
After installing the Agent on my local MacBook and grabbing an API key, I was able to successfully create a small Ruby app to send an Event back to Datadog, which also forwarded to my email inbox by the use of tagging myself.
</p>
```ruby
require 'rubygems'
require 'dogapi'
#Define api_key from Datadog
api_key = "6dbff62a24a033178e720f2907618ec6"
#Create dog object
dog = Dogapi::Client.new(api_key)
#Call emit_event to send a new event back to Datadog, tagging my username to generate an email
dog.emit_event(Dogapi::Event.new('Send me an email @chrisjslaight@gmail.com '))
```

<h2>Level 2</h2>

<p>For this level, I've chosen to implement Dogstatsd on my Cloud9 IDE Ubuntu development server for a holiday shopping list Rails app I've been working on. The below method was placed in the main application_controller.rb file to be accessible by all controllers:</p>
```ruby
def render_page
	#This is to be called for any generic web page load
	statsd = Statsd.new
	statsd.increment('web.page_views')
	return 'Page viewed.'
end
```
<p>For the actual implementation, I added a before_action for all page navigation controller actions for my primary controller, people_controller.rb:</p>
```ruby
before_action :render_page, only: [:index,:export,:new,:edit,:show]
```
<h2>Level 3</h2>

<p>Answer goes here</p>

<h2>Level 4</h2>

<p>Answer goes here</p>

<h2>Level 5</h2>

<p>Answer goes here</p>