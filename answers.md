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

in file 'datadog_event.rb' I write:

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

[Page Views per Second](https://app.datadoghq.com/graph/embed?from_ts=1418686848738&to_ts=1418773248738&token=e5c0ebebe575ee8cabc94d4d6a43f0bb85ccb99ebc535b2d574dd3bc186f6e70&height=300&width=600&tile_size=m&live=true)

####Create a histogram to see the latency; also give us the link to the graph

I graphed median response time, 95th percentile and average response time.

Results while running a load test look like this:

![load_test_response_image](https://s3-us-west-2.amazonaws.com/documentationimages/datadog_L2_load_test_response.png)

Link to live shared version of this graph:

[Latency](https://app.datadoghq.com/graph/embed?from_ts=1418761579120&to_ts=1418761884018&token=b288d1b539d52b3d3aa23bd81a7a12c3ee5aa936086077e7998528130f4fbe73&height=300&width=600&tile_size=m&live=true)

####Bonus points for putting together more creative dashboards.

![dashboard](https://s3-us-west-2.amazonaws.com/documentationimages/datadog_L2_dashboard.png)
