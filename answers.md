## Level 1

#### Sign up for Datadog, get the agent reporting metrics from your local machine.

After signing up and generating an API Key, I installed the Agent via the terminal using:

    <DD_API_KEY> bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/dd-agent/master/packaging/datadog-agent/source/setup_agent.sh)"

#### Bonus question: what is the agent?

The Datadog Agent is piece of software that runs on your hosts. Its job is to faithfully collect events and metrics and bring them to Datadog on your behalf so that you can do something useful with your monitoring and performance data.

The Agent has three main parts: the collector, dogstatsd, and the forwarder.

* The collector runs checks on the current machine for whatever integrations you have and it will capture system metrics like memory and CPU.
* Dogstatsd is a statsd backend server you can send custom metrics to from an application.
* The forwader is pushed data from both dogstatsd and the collector and queues it up to be sent to Datadog.

#### Submit an event via the API.

in file `datadog_event.rb` I write:

    # Load the dogstats module.
    require 'statsd'
    
    # Create a stats instance.
    statsd = Statsd.new('localhost', 8125)
    
    # Submit an event via the API, @mention desired e-mail (be sure e-mail subscription is enabled)
    statsd.event('Good work!', 'You submitted and event via the API. @Jeremy.Salig@gmail.com')

To send an event I run:

    ruby datadog_event.rb

The event will post to my stream and the @mention will forward the event to my e-mail.

#### Get an event to appear in your email inbox (the email address you signed up for the account with)

![event_image](https://s3-us-west-2.amazonaws.com/documentationimages/datadog_L1_01.png)
![email_image](https://s3-us-west-2.amazonaws.com/documentationimages/datadog_L1_02.png)

***

## Level 2

####Take a simple web app ([in any of our supported languages](http://docs.datadoghq.com/libraries/)) that you've already built and instrument your code with dogstatsd. This will create **metrics**.

Added statsd, created a new instance, sent incriment to a new metric for my simple Ruby web app running on Sinatra:

    require 'statsd'
    
    statsd = Statsd.new('localhost', 8125)
    get "/" do
      # get page elements
      statsd.increment('pixtr.pages.views')
      erb :index
    end


####While running a load test (see References) for a few minutes, visualize page views per second. Send us the link to this graph!

I used apache bench to run a simple load test.

Results while running a load test look like this:

![load_test_image](https://s3-us-west-2.amazonaws.com/documentationimages/datadog_L2_load_test.png)

Link to live shared version of this graph:

[Home Page Views per Second](https://app.datadoghq.com/graph/embed?from_ts=1418686848738&to_ts=1418773248738&token=e5c0ebebe575ee8cabc94d4d6a43f0bb85ccb99ebc535b2d574dd3bc186f6e70&height=300&width=600&tile_size=m&live=true)

####Create a histogram to see the latency; also give us the link to the graph

First I sampled the response time using `statsd.histogram` passing in time duration as an argument:

    get "/" do
      start_time = Time.now 
      duration = Time.now - start_time
      
      # page loading logic
    
      statsd.histogram('pixtr.pages.response.time', duration, tags: ['support', "page:home"])
    end

I graphed median response time, 95th percentile and average response time.

Results while running a load test look like this:

![load_test_response_image](https://s3-us-west-2.amazonaws.com/documentationimages/datadog_L2_load_test_response.png)

Link to live shared version of this graph:

[Home Page Latency](https://app.datadoghq.com/graph/embed?from_ts=1418761579120&to_ts=1418761884018&token=b288d1b539d52b3d3aa23bd81a7a12c3ee5aa936086077e7998528130f4fbe73&height=300&width=600&tile_size=m&live=true)

####Bonus points for putting together more creative dashboards.

![dashboard](https://s3-us-west-2.amazonaws.com/documentationimages/datadog_L2_dashboard.png)

***

## Level 3

####tag your metrics with `support` (one tag for all metrics)

To add tags I add `tags: ['support']` to the arguments list:

    statsd.increment('pixtr.pages.views', tags: ['support', "page:home"])

####tag your metrics per page (e.g. metrics generated on `/` can be tagged with `page:home`, `/page1` with  `page:page1`)

To add tags for individual pages, galleries in my example app, of which there are many, I use string interpolation to auto populate tag names:

    get "/galleries/:id" do
      @gallery = Gallery.find(params[:id])
      @images = @gallery.images
    
      statsd.increment("pixtr.pages.views", tags: ['support', "page:gallery#{@gallery.name}"])
    end

####visualize the latency by page on a graph (using stacked areas, with one color per `page`)

Created a new metric logging average response time displayed as stacked areas broken down by page utilizing differentiating `page` tags.

Screenshot:

![response_by_page_image](https://s3-us-west-2.amazonaws.com/documentationimages/datadog_L3_response_by_page.png)

Link to live shared version of this graph:

[Response by Page](https://app.datadoghq.com/graph/embed?from_ts=1418692782050&to_ts=1418779182050&token=88fc33d9f257c48e240adf77fa066878732aae01ad31dddce6305a84b764a32d&height=300&width=600&tile_size=m&live=true)

***

## Level 4

####count the overall number of page views using dogstatsd counters.

I used `increment` to send `+1` to the `pixtr.pages.views` metric for each view of any page utilizing the support tag which all pages share:

    statsd.increment("pixtr.pages.views", tags: ['support'])

####count the number of page views, split by page (hint: use tags)

Adding custom tags using string interpolation automaticaly generates custom `page:name` tags we can then split by in our stacked graph:

    statsd.increment("pixtr.pages.views", tags: ['support', **"page:gallery#{@gallery.name}"**])

####visualize the results on a graph

Screenshot of graph:

Screenshot:

![views_by_page_image](https://s3-us-west-2.amazonaws.com/documentationimages/datadog_L4_views_by_page.png)

Link to live shared version of this graph:

[Views by Page](https://app.datadoghq.com/graph/embed?from_ts=1418694482157&to_ts=1418780882157&token=efff34b56b19fe78152d0309d76f1cb61c1d2f551714a54bbb4db26d70bc03ea&height=300&width=600&tile_size=m&live=true)

####Bonus question: do you know why the graphs are very spiky?

My thought as to why stacked area graphs tend to be spikier is that the overall form takes the sum of all combined elements, pages in this case, and changes in one element shifts the others along with it on the y-axis.

***

## Level 5

####Write an agent check that samples a random value. Call this new metric: `test.support.random`

To write this agent check we will add two files to the directory structure of The Datadog Agent. Using the terminal we can run the following from our `agent` directory within `~/.datadog-agent`:

    touch checks.d/randomval.py

    touch conf.d/randomval.yaml

Worth noting is that the names must match.

Within `randomval.yaml` will be:

    init_config:
    
    instances:
        [{}]

Within `randomval.py` will be:

```python
import random
from checks import AgentCheck

class RandomvalCheck(AgentCheck):
    def check(self, instance):
        val = random.random()
        self.gauge('test.support.random', val)
```

####Visualize this new metric on Datadog, send us the link.

We can now sample this metric in Datadog.

Screenshot:

![test_support_random](https://s3-us-west-2.amazonaws.com/documentationimages/datadog_L5_test_support_random.png)

Link to live shared version of this graph:

[Random Value Agent Check](https://app.datadoghq.com/graph/embed?from_ts=1418768345249&to_ts=1418782745249&token=9aa28df81bb1473e1ada410b5a127513a45de52cba5df9c589a6c34e1a544fda&height=300&width=600&tile_size=m&live=true)

