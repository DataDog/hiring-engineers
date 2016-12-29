# Challenge : Hiring Support Engineer

# Level 1

## Sign up for Datadog, get the agent reporting metrics.


I had already subscribed to Datadog a few months ago to monitor the blog I was building. I changed the name of the Company to *"Datadog Recruiting Candidate"* for the Challenge.

I had installed the agent on my EC2 server hosting my Blog. The host is based on Ubuntu.

I used the *easy one-step install* instruction to be found in the ***Integrations>Agent*** tab on Datadog personal account. 
System-related metrics are available on the ***Metrics>Explorer*** tab. 
I chose to represent three main metrics:
+ the available disk space on the host (or system.disk.in.use )
+ the CPU usage ( or system.cpu.user)
+ the average available memory percentage over the past 5 minutes.

These three metrics will enable me to help me monitor my web app and make sure I constantly have enough memory, disk space available and responsive CPU.

Here are the representations of these three metrics : 
![Initial metrics](/images-challenge/Blog-initial-metrics.png)


The complete Blog Dashboard can also be found [here](https://p.datadoghq.com/sb/15d4408a4-8201f2536e)



## Bonus question: what is the agent?

The agent is a piece of software embedded on the host to be monitored. It is composed of three main parts:

- ***The Collectors*** will collect the metrics related to the host system such as CPU or memory, and will check those related to the supported integrations.
- ***DogstatsD*** will collect metrics that the user settles according to their needs. Metrics are collected from an app. This is available in several languages to best adapt the clients’ needs in terms of applications / services to monitor.
- ***The Forwarder*** collects data from the collector and the dogstatsd , puts them on a queue then send them do Datadog for analysis and visualization capabilities.


## Submit an event via the API.

In order to do that, I first created an API key on the personal-account Datadog *Integration>API* tab, to enable the transactions to be authenticated. I then created the Python script as follows :


```python
# Configuration of the module with the authentication required to communicate with the API
from datadog import initialize

# The API key is generated through the Integration>API part of the Datadog Website
options = { 
    'api_key':'personal_api-key'
    }

initialize(**options)

# Use Datadog REST API client
from datadog import api

title = "Something happened"
text = "This is a test creating an event through the datadog API"
tags = ['API-test']

# Create the event thanks to the elements that we have defined above
api.Event.create(title=title, text=text, tags=tags)
```

![Event](/images-challenge/event.png) 


## Get an event to appear in your email inbox (the email address you signed up for the account with)

In order to get an event to appear in my mailbox, I created an alert thanks to the Datadog's *Monitor>New_Monitor>Event* section. 
I configured the Alert to send me a notification when at least 3 Events containing the text “Something” occurred over the past 4 Hours 

![Alert-creation](/images-challenge/Alert-creation.png) 


After launching 4 times the Event via the API, I logically received the following email : 
![Email-2](/images-challenge/mail-alert.png) 
![Email-3](/images-challenge/mail-content.png) 

I settled my alert to be triggered when 3 events happened in a timeslot of 4 hours. Therefore I received an email of recovery 4 hours after the initial alert, informing me that the alert was recovered. 

# Level 2 


## Take a simple web app (in any of our supported languages) that you've already built and instrument your code with dogstatsd. This will create metrics.

I chose to achieve this question on my Ruby on Rails based [blog](http://blog.ofievet.net/).
The code can be found [here](https://github.com/oceanef/Blog).

+ So I had to ***first integrate the dogstatsd-ruby gem.***

I added the gem to the Gemfile to do so, then ran the command bundle install to update the installations:

```python
#Monitor with Datadog
gem 'dogstatsd-ruby', '~> 1.6'
```
Then I needed to enable the application to send metrics through the Statsd client, from anywhere in the app. 
I did that by updating my blog app on my test environment located in a Vagrant virtual machine. That enabled me to test any changes I was applying to my web app : 

+ Update the ***config>application.rb*** file 

We configure the whole application to access ‘statsd’ when needed and create the global value $statsd referring to the creation of an instance of statsd server :

```ruby
require File.expand_path('../boot', __FILE__)

require 'rails/all'

#Enable the statsd server to aggregate the data from the appplication
require 'statsd'
$statsd = Statsd.new('localhost', 8125)
```

+ Create dedicated metrics for my app 

I began by monitoring the pages views and the posts views. I updated the posts-controller.rb file:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;* Counting the number of views of the Index/Home page :

```ruby
def index
		@posts = Post.all.order('created_at DESC')
# Everytime a user sees the home page containing the post index, 
#statsd will increment the count and send it to Datadog
		tags = "page:index"
		$statsd.increment('blog.page.views', :tags => [tags])
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;* Counting the number of views of the posts, tagging the posts as per their titles : 

```ruby
def show
		@post = Post.find(params[:id])
		tags = "page:#{@post.title}"
		$statsd.increment('blog.page.views', :tags => [tags])
	end
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;* Counting the number of failures of post creations and updates, creating one metric with two tags : 

New Metric: blog.failed.post

***Tag1 : post:creation***

```ruby
def create
		@post = Post.new(post_params)
		if @post.save
			redirect_to @post
		else 
			render 'new'
	#Every-time someone fails to create a new post, statsd increments the count and sends it to Datadog
	#Here the metrics refers to a post creation failure, tag refers to the initial creation of a post
			tags = "post:creation"
			$statsd.increment('blog.failed.post', :tags => [tags])
		end
end
```

***Tag2 : post:update***

```ruby
def update
		@post =  Post.find(params[:id])

		if @post.update(params[:post].permit(:title, :body, :image))
			redirect_to @post
		else
			render 'edit'
	#Every-time someone fails to create a new post, statsd increments the count and sends it to Datadog
	#Here the metrics refers to a post creation failure, tags refers to the update of a post
			tags = "post:update"
			$statsd.increment('blog.failed.post', :tags => [tags])
		end
	end
```

After a few tests viewing posts a purposely failing post creations and updates, here are the data visualized on the Datadog platform : 


![statsd-test-metrics-vagrant](/images-challenge/statsd-test-metrics-vagrant.png) 


## While running a load test for a few minutes, visualize page views per second. Send us the link to this graph!
## Create a histogram to see the latency; also give us the link to the graph


I ran the load test on my EC2 blog-server after updating my production environment with Datadog monitoring: 

+ I first did a ***ab load test*** on 500 queries, but the result was not that demonstrating as shown in below :

![blog-initial-load-test](/images-challenge/initial-load-test.png) 


+ I decided to really stress the system through ***a 500,000 request load test*** and decided to show several metrics as shown below

![blog-real-load-test](/images-challenge/real-loadtest.png) 


The full public Blog Dashboard is also available [here](https://p.datadoghq.com/sb/15d4408a4-8201f2536e) 

The timeboard blog Dashboard is available can also be accessed on [my Datadog personal account](https://app.datadoghq.com/dash/92559/blog---challenge-support-engineer?live=true&page=0&is_auto=false&from_ts=1453091885894&to_ts=1453264685894&tile_size=m)
*See what happened on January 18th, between 9h30 pm and 10:30pm, EST*  

In order to get the latency of the pages, I added a custom metrics using the Statsd client as follows : 

```ruby
def index
	#Start the count before the action of rendering the index page
		start_time = Time.now
		@posts = Post.all.order('created_at DESC')
	#After the action, calculate the timeslot with the duration variable
		duration = Time.now - start_time
		tags = "page:index"
	#Add the histogram of the new metrics 'blob.latency'. We keep the same tag to well identify the page view
		$statsd.histogram('blog.latency', duration, :tags => [tags, 'support'])
		$statsd.increment('blog.page.views', :tags => [tags, 'support'])
	end
```
A detailed description of the concerned pages is present in Level 3


We can see several interesting elements here: 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;* The CPU was loaded up to 80%, as if there were a limit in its usage 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;* The latency is very limited : this should come from the fact that the web server, web app and database are hosted on the same physical server

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;* We notice that the maximum of Apache requests per second is twice as low as the MySQL. The max requests per second amount is at 200 for Apache, and 400 for MySQL

# Level 3 

## Tag your metrics with support (one tag for all metrics)

I update the metrics from level 2 with the tag "support"

```ruby
def index
		@posts = Post.all.order('created_at DESC')
# Everytime a user sees the home page containing the post index, 
#statsd will increment the count and send it to Datadog
		tags = "page:index"
		$statsd.increment('blog.page.views', :tags => [tags, 'support'])
```

```ruby
def show
		@post = Post.find(params[:id])
		tags = "page:#{@post.title}"
		$statsd.increment('blog.page.views', :tags => [tags, 'support'])
	end
```

```ruby
def create
		@post = Post.new(post_params)
		if @post.save
			redirect_to @post
		else 
			render 'new'
	#Every-time someone fails to create a new post, statsd increments the count and sends it to Datadog
	#Here the metrics refers to a post creation failure, tag refers to the initial creation of a post
			tags = "post:creation"
			$statsd.increment('blog.failed.post', :tags => [tags, 'support'])
		end
end
```

```ruby
def update
		@post =  Post.find(params[:id])

		if @post.update(params[:post].permit(:title, :body, :image))
			redirect_to @post
		else
			render 'edit'
	#Every-time someone fails to create a new post, statsd increments the count and sends it to Datadog
	#Here the metrics refers to a post creation failure, tags refers to the update of a post
			tags = "post:update"
			$statsd.increment('blog.failed.post', :tags => [tags, 'support'])
		end
	end
```

Here are the graphs I get on the Datadog interface : 

![support-tag](/images-challenge/support-tag.png) 

This is coherent with the fact that I first queried normal page views that purposely failed post creations and updates 


## Tag your metrics per page (e.g. metrics generated on / can be tagged with page:home, /page1 with page:page1)

*See Level 2 for the beginning*

I have started with tagging my index, posts and the failure notification. Let’s do that for the rest of the web app. 

Remain the following pages : 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;* Sign up and Log in

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;* New post page ( dedicated to the admin, that is me )

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;* As the comments for the posts are directly written below the post, this refers to the same page view

***Sign up and log-in pages*** counts using dogstatsd. These pages are linked to the devise gem.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;* Sign-up : We can update the code on the ***views>devise>registration>new.html.erb*** section of the app 

```erb
<%= render "devise/shared/links" %>

  <% tags = "page:sign_up" %>
  <% $statsd.increment('blog.page.views', :tags => [tags]) %>
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;* Log-in : We can update the code on the ***views>devise>session>new.html.erb*** section of the app 

```erb
<%= render "devise/shared/links" %>

<% tags = "page:log_in" %>
<% $statsd.increment('blog.page.views', :tags => [tags]) %>
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;* New post:

```ruby
def new
		@post = Post.new
	#Every-time the authorized user wants to create a new post, statsd increments the count and sends it to Datadog
	#Here the metrics refers to a new post view, tag refers to the initial creation of a post
			tags = "page:creation"
			$statsd.increment('blog.page.views', :tags => [tags, 'support'])
```

Here is a graph of the various page views with a different color per page view

## Visualize the latency by page on a graph (using stacked areas, with one color per page)

Let’s add some code to visualize latency : latency is defined as the difference of time between the rendering and the beginning of the action 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;* Index page view latency 

```ruby
def index
	#Start the count before the action of rendering the index page
		start_time = Time.now
		@posts = Post.all.order('created_at DESC')
	#After the action, calculate the timeslot with the duration variable
		duration = Time.now - start_time
		tags = "page:index"
	#Add the histogram of the new metrics 'blob.latency'. We keep the same tag to well identify the page view
		$statsd.histogram('blog.latency', duration, :tags => [tags, 'support'])
		$statsd.increment('blog.page.views', :tags => [tags, 'support'])
	end
```

Following the same rules :

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;* Post View

```ruby
def show
		start_time = Time.now
		@post = Post.find(params[:id])
		duration = Time.now - start_time
		tags = "page:#{@post.title}"
		$statsd.histogram('blog.latency', duration, :tags => [tags, 'support'])
		$statsd.increment('blog.page.views', :tags => [tags, 'support'])
	end
```

I update the code for all the blog page views. In order to correctly classify them I also updated the sign up and log_in tags into ***page:sign_up*** and ***post:log_in***

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;* Sign up

```erb
 <% start_time=Time.now %>

<%= render "devise/shared/links" %>

  <% duration = Time.now - start_time %>
  <% tags = "page:sign_up" %>
  <% $statsd.increment('blog.page.views', :tags => [tags]) %>
  <% $statsd.histogram('blog.latency', duration, :tags => [tags]) %>
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;* Log in

```erb
<% start_time=Time.now %>

<%= render "devise/shared/links" %>

<% duration = Time.now - start_time %>
<% tags = "page:log_in" %>
<% $statsd.increment('blog.page.views', :tags => [tags]) %>
<% $statsd.histogram('blog.latency', duration, :tags => [tags]) %>
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;* Visualization 

Using the ***Metrics>Explorer*** section of the Datadog Website, I filtered the data to be vizualized first by host, then selected the sum by tag ***page*** rendering the data from all the pages described previously :

![latency-per-page](/images-challenge/latency-per-page.png) 


# Level 4 

## Count the overall number of page views using dogstatsd counters.

Overall count independently from which page is a sum of every page counts settled on the host, explained in level 2 and level 3 
For this part, I also use my Vagrant environment as there are more pages to view, so the analysis seems more interesting
We can visualize this through the ***Metrics>Explorer*** section :

![sum-page-views](/images-challenge/sum-page-views-set-up.png) 

![sum-page-views](/images-challenge/sum-page-views.png) 

![sum-page-views](/images-challenge/sum-page-views-graph.png) 


## Count the number of page views, split by page (hint: use tags)

Thank to level 2 and 3, I have already gathered data on the page views
I visualize the results using the Top List feature, decreasing order , over the past 4 hours

![split-page-views](/images-challenge/split-page-views.png) 


## Bonus question: do you know why the graphs are very spiky?

To me the graphs are spiky because they count isolated events, the data is not continually displayed as could be a CPU usage for example. This is well represented through a histogram. We can indeed visualize that there are time slots in which there are no events / page view. 
The load on the system is sudden, not continuous 

![histo-replace-spike](/images-challenge/aggregated-pages.png) 

# Level 5 

## Write an agent check that samples a random value. Call this new metric: test.support.random

In order to set up an Agent Check, both ***/etc/dd-agent/checks.d*** and ***/etc/dd-agent/conf.d***  need to be updated

Once in my ***/etc/dd-agent/conf.d*** folder I initiated the *random_check.yaml* config file as follows : 

```yaml
init_config:

instances:
    [{}]
```

I then configured the *random_check.py* that I created in my ***/etc/dd-agent/checks.d*** to run the check

```python
from checks import AgentCheck
import random

class random_check(AgentCheck):
    def check(self,instance):
 		self.gauge('test.support.random' , random.random() )
```

I restarted the Agent thanks to the ***sudo /etc/init.d/datadog-agent restart*** command to take these changes into account.

## Visualize this new metric on Datadog, send us the link.

After some time running, the visualization of the check is as follows: we can see that all values belong to the intervall[0;1], which is relevant to the definition of the random function 

![Agent-random-check](/images-challenge/Agent-random-check.png) 

A real-time view of this Agent Check can be viewed [here](https://p.datadoghq.com/sb/15d4408a4-1390d6e3fd)










